"""
The metadata (`index`, `count`, ...) for a field (`Base`, `SelectionBase`)
is stored as a definition object. For ease of use, all definitions
of one type (`input`, `holding`, ...) are provided as a sorted list of objects.
This usually contains only predefined definitions (generated out of
`HOLDINGS_DEFINITIONS_LIST` or `INPUTS_DEFINITIONS_LIST`),
but can be expanded by the user.
"""

from luxtronik.datatypes import Unknown
from luxtronik.shi.constants import (
    LUXTRONIK_DEFAULT_DEFINITION_OFFSET,
    LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE
)
from luxtronik.shi.common import (
    LOGGER,
    parse_version
)


###############################################################################
# LuxtronikDefinition
###############################################################################

class LuxtronikDefinition:
    """
    Metadata container for a Luxtronik data field.

    Also provides a method to create a related field object.
    """

    DEFAULT_DATA = {
        "index": -1,
        "count": 1,
        "type": Unknown,
        "writeable": False,
        "names": [],
        "since": "",
        "until": "",
        "description": "",
    }

    def __init__(self, data_dict, type_name, offset=LUXTRONIK_DEFAULT_DEFINITION_OFFSET):
        """
        Initialize a definition from a data-dictionary.

        Args:
            data_dict (dict): Definition values. Missing keys are filled with defaults.
            type_name (str): The type name e.g. 'holding', 'input', ... .
            offset (str): Offset of the address from the specified index.
                (Default: LUXTRONIK_DEFAULT_DEFINITION_OFFSET)

        Notes:
            - Only 'index' is strictly required within the `data_dict`.
            - The class may only be created with dictionaries
              that have been checked for correctness using pytest.
              This eliminates the need for type tests here.
        """
        try:
            data_dict = self.DEFAULT_DATA | data_dict
            index = int(data_dict["index"])
            self._valid = index >= 0
            self._index = index if self._valid else 0
            self._count = int(data_dict["count"])
            self._data_type = data_dict["type"]
            self._writeable = bool(data_dict["writeable"])
            names = data_dict["names"]
            if not isinstance(names, list):
                names = [str(names)]
            names = [str(name).strip() for name in names if str(name).strip()]
            if not names:
                names = ["_invalid_"]
            self._names = names
            self._aliases = []
            since = str(data_dict["since"])
            self._since = parse_version(since)
            until = str(data_dict["until"])
            self._until = parse_version(until)
            self._description = str(data_dict["description"])
            self._type_name = type_name.lower()
            self._valid &= len(self._type_name) > 0
            self._offset = int(offset)
            self._addr = self._offset + self._index
        except Exception as e:
            self._valid = False
            self._index = 0
            LOGGER.error(f"Failed to create LuxtronikDefinition: '{e}' with {data_dict}")

    @classmethod
    def unknown(cls, index, type_name, offset=LUXTRONIK_DEFAULT_DEFINITION_OFFSET):
        """
        Create an "unknown" definition.

        Args:
            index (int): The register index of the "unknown" definition.
            type_name (str): The type name e.g. 'holding', 'input', ... .
            offset (str): Offset of the address from the specified index.
                (Default: LUXTRONIK_DEFAULT_DEFINITION_OFFSET)

        Returns:
            LuxtronikDefinition: A definition marked as unknown.
        """
        return cls({
            "index": index,
            "names": [f"unknown_{type_name.lower()}_{index}"]
        }, type_name, offset)

    def __bool__(self):
        """Return True if the definition is valid."""
        return self._valid

    def __repr__(self):
        return f"(name={self.name}, data_type={self.data_type}," \
            + f" index={self.index}, count={self.count})"

    @property
    def valid(self):
        return self._valid

    @property
    def type_name(self):
        "Returns the type name (e.g. 'holding', 'input', ...)."
        return self._type_name

    @property
    def index(self):
        return self._index

    @property
    def offset(self):
        return self._offset

    @property
    def addr(self):
        return self._addr

    @property
    def count(self):
        "Returns the assigned number of used bytes/words."
        return self._count

    @property
    def data_type(self):
        return self._data_type

    @property
    def writeable(self):
        return self._writeable

    @property
    def names(self):
        return self._names

    @property
    def aliases(self):
        return self._aliases

    @property
    def name(self):
        "Returns the preferred name."
        return self._names[0]

    @property
    def since(self):
        return self._since

    @property
    def until(self):
        return self._until

    def create_field(self):
        """
        Create a data field instance from this definition.

        Returns:
            Base | None: Field instance or None if invalid.
        """
        return self.data_type(self.name, self.writeable) if self.valid else None


###############################################################################
# LuxtronikDefinitionsDictionary
###############################################################################

class LuxtronikDefinitionsDictionary:
    """
    Dictionary of definitions that can be searched by index, name, or aliases.

    To use aliases, they must first be registered here (locally =
    only valid for this dictionary) or directly in the `LuxtronikDefinitionsList`
    (globally = valid for all newly created dictionaries).

    This class is intended to speed up the lookup of definitions.
    Dictionaries are used instead of searching through a list of definitions
    one by one to find the one you are looking for.
    """

    def __init__(self):
        self._index_dict = {}
        self._name_dict = {}
        self._alias_dict = {}

    def __getitem__(self, name_or_idx):
        return self.get(name_or_idx)

    def __contains__(self, def_name_or_idx):
        if isinstance(def_name_or_idx, LuxtronikDefinition):
            return any(def_name_or_idx is d for d in self._index_dict.values())
        return self._get(def_name_or_idx) is not None

    def _add_alias(self, definition, alias):
        """
        Register a single alias that references the given definition.

        Args:
            definition (LuxtronikDefinition): Definition that the alias should map to.
            alias (Hashable): Alias to register (str will be normalized).
        """
        alias = alias.lower() if isinstance(alias, str) else alias
        self._alias_dict[alias] = definition

    def register_alias(self, def_name_or_idx, alias):
        """
        Register an alias (locally) that references a definition specified by
        name, index, or the definition object.

        Args:
            def_name_or_idx (str | int | LuxtronikDefinition):
                Name, index, or definition to alias.
            alias (Hashable): Alias key to register (str will be normalized).

        Returns:
            LuxtronikDefinition | None: The resolved definition
                when registration succeeded, otherwise None.
        """
        if alias is None:
            return None
        # look-up definition
        if isinstance(def_name_or_idx, LuxtronikDefinition):
            definition = self.get(def_name_or_idx.name)
        else:
            definition = self.get(def_name_or_idx)
        if definition is None:
            return None
        self._add_alias(definition, alias)
        return definition

    def add(self, definition, alias=None):
        """
        Add a definition to internal lookup tables and register its aliases.
        Existing entries will be overwritten.

        Args:
            definition (LuxtronikDefinition): Definition to add.
            alias (Hashable): Optional additional alias to register for this definition.
        """
        # Add to indices-dictionary
        self._index_dict[definition.index] = definition

        # Add to name-dictionary
        # Unique names has already been ensured by the pytest
        for name in definition.names:
            self._name_dict[name.lower()] = definition

        # Add to alias-dictionary
        for a in definition.aliases:
            self._add_alias(definition, a)
        if alias is not None:
            self._add_alias(definition, alias)

    def get(self, name_or_idx, default=None):
        """
        Retrieve a definition by name or index.

        Args:
            name_or_idx (str | int): Definition name or register index.
            default (LuxtronikDefinition): Definition to return if the searched one is not found.

        Returns:
            LuxtronikDefinition | None: The matching definition, or None if not found.

        Note:
            If multiple definitions added for the same index/name, the last added takes precedence.
        """
        d = self._get(name_or_idx)
        if d is None:
            LOGGER.warning(f"Definition for '{name_or_idx}' not found", )
        return d if d is not None else default

    def _get(self, name_or_idx):
        """
        Retrieve a definition by name or index.

        Args:
            name_or_idx (str | int): Definition name or register index.

        Returns:
            LuxtronikDefinition | None: The matching definition, or None if not found.

        Note:
            If multiple definitions added for the same index/name, the last added takes precedence.
        """
        d = self._get_definition_by_alias(name_or_idx)
        if d is None:
            if isinstance(name_or_idx, int):
                d = self._get_definition_by_idx(name_or_idx)
                if d is None:
                    # search in alias-dict again with the index converted to a string
                    d = self._get_definition_by_alias(str(name_or_idx))
            if isinstance(name_or_idx, str):
                try:
                    # Numbers are not allowed as names, so it could be an index as string
                    idx_from_str = int(name_or_idx)
                    d = self._get_definition_by_idx(idx_from_str)
                    if d is None:
                        # search in alias-dict again with the string converted to an index
                        d = self._get_definition_by_alias(str(name_or_idx))
                except ValueError:
                    d = self._get_definition_by_name(name_or_idx)
        return d

    def _get_definition_by_idx(self, idx):
        """
        Retrieve a definition by its index.

        Args:
            idx (int): Register index.

        Returns:
            LuxtronikDefinition | None: The matching definition, or None if not found.

        Note:
            If multiple definitions added for the same index, the last added takes precedence.
        """
        return self._index_dict.get(idx, None)

    def _get_definition_by_name(self, name):
        """
        Retrieve a definition by its name (case-insensitive).

        Args:
            name (str): Definition name.

        Returns:
            LuxtronikDefinition | None: The matching definition, or None if not found.

        Note:
            If multiple definitions added for the same name, the last added takes precedence.
        """
        definition = self._name_dict.get(name.lower(), None)
        if definition is not None and definition.valid and name.lower() != definition.name.lower():
            LOGGER.warning(f"'{name}' is outdated! Use '{definition.name}' instead.")
        return definition

    def _get_definition_by_alias(self, alias):
        """
        Retrieve a definition by its alias (case-insensitive when using strings).

        Args:
            alias (Hashable): Alias for a definition.

        Returns:
            LuxtronikDefinition | None: The matching definition, or None if not found.

        Note:
            If multiple definitions added for the same alias, the last added takes precedence.
        """
        alias = alias.lower() if isinstance(alias, str) else alias
        return self._alias_dict.get(alias, None)


###############################################################################
# LuxtronikDefinitionsList
###############################################################################

class LuxtronikDefinitionsList:
    """
    Container for Luxtronik definitions.

    Provides lookup by index, name or alias.

    To use aliases, they must first be registered here (globally = valid for
    all newly created dictionaries) or within the `LuxtronikDefinitionsDictionary`
    (locally = only valid for that dictionary).
    """

    def __init__(self, definitions_list, name, offset=LUXTRONIK_DEFAULT_DEFINITION_OFFSET):
        """
        Initialize the (by index sorted) definitions list.

        Args:
            definitions_list (list[dict]): Raw definition entries as list of data-dictionaries.
            name (str): Name related to this type of definitions (e.g. "holding")
            offset (int): Offset applied to register indices.
                (Default: LUXTRONIK_DEFAULT_DEFINITION_OFFSET)

        Notes on the definitions_list:
            - Must be sorted by ascending index
            - Each version may contain only one entry per register
            - If there exists more than one definition per index,
              only the last one can be found using indices/names
            - The value of count must always be greater than or equal to 1
            - All names should be unique
        """
        self._name = name
        self._offset = offset
        # sorted list of all definitions
        self._definitions = []
        self._lookup = LuxtronikDefinitionsDictionary()

        # Add definition objects only for valid items.
        # The correct sorting has already been ensured by the pytest
        for item in definitions_list:
            d = LuxtronikDefinition(item, name, offset)
            if d.valid:
                self._add(d)

    def __getitem__(self, name_or_idx):
        return self.get(name_or_idx)

    def __contains__(self, def_name_or_idx):
        return def_name_or_idx in self._lookup

    def __len__(self):
        return len(self._definitions)

    def __iter__(self):
        return iter(self._definitions)

    def __repr__(self):
        defs = [repr(d) for d in self._definitions]
        return f"({self.name}, {self.offset}, {' ,'.join(defs)})"

    def create_unknown_definition(self, index):
        """
        Create an "unknown" definition.

        Args:
            index (int): The register index of the "unknown" definition.

        Returns:
            LuxtronikDefinition: A definition marked as unknown.
        """
        return LuxtronikDefinition.unknown(index, self._name, self._offset)

    def register_alias(self, def_name_or_idx, alias):
        """
        Register an alias (globally) that references a definition specified by
        name, index, or the definition object.

        Args:
            def_name_or_idx (str | int | LuxtronikDefinition):
                Name, index, or definition to alias.
            alias (any): (Hashable) Alias key to register (str will be normalized).

        Returns:
            LuxtronikDefinition | None: The resolved definition
                when registration succeeded, otherwise None.
        """
        # "local" registration to be able to find the definition again
        definition = self._lookup.register_alias(def_name_or_idx, alias)
        # "global" registration that is used in newly created definition-dictionaries
        if definition is not None:
            definition.aliases.append(alias)
        return definition

    @property
    def name(self):
        return self._name

    @property
    def offset(self):
        return self._offset

    def get(self, name_or_idx, default=None):
        """
        Retrieve a definition by name or index.

        Args:
            name_or_idx (str | int): Definition name or register index.

        Returns:
            LuxtronikDefinition | None: The matching definition, or None if not found.

        Note:
            If multiple definitions added for the same index/name, the last added takes precedence.
        """
        return self._lookup.get(name_or_idx, default)

    def _add(self, definition):
        """
        Add a valid definition to the internal dictionaries

        Args:
            definition (LuxtronikDefinition): Definition to add
        """
        self._definitions.append(definition)
        self._lookup.add(definition)

    def add(self, data_dict):
        """
        Add a custom (valid) definition. Existing definitions will not be overwritten.

        Args:
            data_dict (dict): Data for the definition to add

        Returns:
            LuxtronikDefinition | None: The created definition or None if not valid

        Note:
            If multiple definitions added for the same index/name, the last added takes precedence.
        """
        definition = LuxtronikDefinition(data_dict, self._name, self._offset)
        if not definition.valid:
            return None
        self._add(definition)
        self._definitions.sort(key=lambda item: item.index)
        return definition


###############################################################################
# Definition-Field-Pair methods
###############################################################################

def get_data_arr(definition, field):
    """
    Normalize the field's data to a list of the correct size.

    Args:
        definition (LuxtronikDefinition): Meta-data of the field.
        field (Base): Field object that contains data to get.

    Returns:
        list[int] | None: List of length `definition.count`, or None if insufficient.
    """
    data = field.raw
    if not isinstance(data, list):
        data = [data]
    data = data[:definition.count]
    return data if len(data) == definition.count else None

def check_data(definition, field):
    """
    Validate that the field contains sufficient raw data.

    Args:
        definition (LuxtronikDefinition): Meta-data of the field.
        field (Base): Field object that contains the data to check.

    Returns:
        bool: True if valid, False otherwise.
    """
    return get_data_arr(definition, field) is not None

def integrate_data(definition, field, raw_data, data_offset=-1):
    """
    Integrate raw values from a data array into the field.

    Args:
        definition (LuxtronikDefinition): Meta-data of the field.
        field (Base): Field object where to integrate the data.
        raw_data (list): Source array of bytes/words.
        data_offset (int): Optional offset. Defaults to `definition.index`.
    """
    data_offset = data_offset if data_offset >= 0 else definition.index
    # Use the information of the definition to extract the raw-value
    if (data_offset + definition.count - 1) >= len(raw_data):
        raw = None
    elif definition.count == 1:
        raw = raw_data[data_offset]
        raw = raw if raw != LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE else None
    else:
        raw = raw_data[data_offset : data_offset + definition.count]
        raw = raw if len(raw) == definition.count and \
            not any(data == LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE for data in raw) else None
    field.raw = raw
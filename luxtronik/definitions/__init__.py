"""
The metadata (`index`, `count`, ...) for a field (`Base`, `SelectionBase`)
is stored as a definition object. For ease of use, all definitions
of one type (`input`, `holding`, ...) are provided as a sorted list of objects.
This usually contains only predefined definitions (generated out of
`HOLDINGS_DEFINITIONS_LIST`, `INPUTS_DEFINITIONS_LIST`, ...),
but can be expanded by the user.
"""

import logging

from luxtronik.constants import LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE
from luxtronik.common import (
    parse_version,
    version_in_range
)
from luxtronik.datatypes import Unknown


LOGGER = logging.getLogger(__name__)

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
        "datatype": "",
        "description": "",
    }

    # It is permissible not to specify a data type.
    # In this case, all functions based on it will be disabled.
    VALID_DATA_TYPES = ("", "UINT16", "UINT32", "UINT64", "INT16", "INT32", "INT64")


    def __init__(self, data_dict, type_name, offset):
        """
        Initialize a definition from a data-dictionary.

        Args:
            data_dict (dict): Definition values. Missing keys are filled with defaults.
            type_name (str): The type name e.g. 'parameter', 'holding', 'input', ... .
            offset (str): Offset of the address from the specified index.

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
            self._field_type = data_dict["type"]
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
            self._data_type = data_dict["datatype"]
            data_type_valid = self._data_type in self.VALID_DATA_TYPES
            self._valid &= data_type_valid
            data_type_valid &= self._data_type != ""
            self._num_bits = int(self._data_type.replace('U', '').replace('INT', '')) \
                if data_type_valid else 0
        except Exception as e:
            self._valid = False
            self._index = 0
            LOGGER.error(f"Failed to create LuxtronikDefinition: '{e}' with {data_dict}")

    @classmethod
    def unknown(cls, index, type_name, offset, data_type=""):
        """
        Create an "unknown" definition.

        Args:
            index (int): The register index of the "unknown" definition.
            type_name (str): The type name e.g. 'holding', 'input', ... .
            offset (str): Offset of the address from the specified index.
            data_type (str): Data type of the field (see VALID_DATA_TYPES).

        Returns:
            LuxtronikDefinition: A definition marked as unknown.
        """
        return cls({
            "index": index,
            "names": [f"unknown_{type_name.lower()}_{index}"],
            "datatype": data_type,
        }, type_name, offset)

    def __bool__(self):
        """Return True if the definition is valid."""
        return self._valid

    def __repr__(self):
        return f"(name={self.name}, field_type={self.field_type}," \
            + f" index={self.index}, count={self.count})"

    @property
    def valid(self):
        return self._valid

    @property
    def type_name(self):
        "Returns the type name (e.g. 'parameter', 'holding', 'input', ...)."
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
        "Returns the assigned number of used registers."
        return self._count

    @property
    def field_type(self):
        return self._field_type

    @property
    def writeable(self):
        return self._writeable

    @property
    def data_type(self):
        return self._data_type

    @property
    def num_bits(self):
        return self._num_bits

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
        return self.field_type(self.names, self.writeable) if self.valid else None

    def check_raw_not_none(self, raw):
        """
        Check if the related raw value to this definition represents not 'not available'.

        Args:
            raw (int): Raw-value to check.
        """
        # TODO: Check if there are other magic values
        if isinstance(raw, int) and self._data_type in ['INT16']:
            return raw != LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE
        return True


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
            LOGGER.debug(f"Definition for '{name_or_idx}' not found", )
        return d if d is not None else default

    def _is_hashable(self, x):
        try:
            hash(x)
            return True
        except TypeError:
            return False

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
        d = None
        if self._is_hashable(name_or_idx):
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

    def _init_instance(self, name, offset, default_data_type, version):
        """Re-usable method to initialize all instance variables."""
        self._name = name
        self._offset = offset
        self._default_data_type = default_data_type
        self._version = version
        # sorted list of all definitions
        self._definitions = []
        self._lookup = LuxtronikDefinitionsDictionary()

    def __init__(self, definitions_list, name, offset, default_data_type):
        """
        Initialize the (by index sorted) definitions list.

        Args:
            definitions_list (list[dict]): Raw definition entries as list of data-dictionaries.
            name (str): Name related to this type of definitions (e.g. "calculation", "holding", etc.)
            offset (int): Offset applied to register indices.

        Notes on the definitions_list:
            - Must be sorted by ascending index
            - Each version may contain only one entry per register
            - If there exists more than one definition per index,
              only the last one can be found using indices/names
            - The value of count must always be greater than or equal to 1
            - All names should be unique
        """
        self._init_instance(name, offset, default_data_type, None)

        # Add definition objects only for valid items.
        # The correct sorting has already been ensured by the pytest
        for item in definitions_list:
            d = LuxtronikDefinition(item, name, offset)
            if d.valid:
                self._add(d)

    @classmethod
    def filtered(cls, definitions, version):
        """
        Filter an existing definitions list by the given version
        and return the new (by index sorted) definitions list.

        Args:
            definitions (LuxtronikDefinitionsList): List of definitions to filter.
            version (tuple[int] | None):
                Only definitions that match this version are added to the list.
                If None is passed, all available fields are added.
        """
        obj = cls.__new__(cls) # this don't call __init__()
        obj._init_instance(definitions.name, definitions.offset, definitions._default_data_type, version)

        for d in definitions:
            if d.valid and version_in_range(obj._version, d.since, d.until):
                obj._add(d)

        return obj

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
        return LuxtronikDefinition.unknown(index, self._name, self._offset, self._default_data_type)

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
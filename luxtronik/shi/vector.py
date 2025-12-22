from luxtronik.data_vector import DataVector
from luxtronik.datatypes import Base, Unknown

from luxtronik.shi.constants import LUXTRONIK_LATEST_SHI_VERSION
from luxtronik.shi.common import version_in_range
from luxtronik.shi.definitions import (
    integrate_data,
    LuxtronikDefinition,
    LuxtronikDefinitionsDictionary,
)
from luxtronik.shi.contiguous import ContiguousDataBlockList

###############################################################################
# Smart home interface data-vector
###############################################################################

class DataVectorSmartHome(DataVector):
    """
    Specialized DataVector for Luxtronik Smart Home fields.

    Provides access to fields by name, index or alias.
    To use aliases, they must first be registered here (locally = only valid
    for this vector) or directly in the `LuxtronikDefinitionsList`
    (globally = valid for all newly created vector).
    """

    # DataVector specific list of definitions as `LuxtronikDefinitionsList`
    definitions = None # override this

# Field construction methods ##################################################

    @classmethod
    def create_unknown_field(cls, idx):
        """
        Create an unknown field object.
        Be careful! The used controller firmware
        may not support this field.

        Args:
            idx (int): Register index.

        Returns:
            Unknown: A field instance of type 'Unknown'.
        """
        return Unknown(f"unknown_{cls.name}_{idx}", False)

    @classmethod
    def create_any_field(cls, name_or_idx):
        """
        Create a field object from an available definition
        (= included in class variable `cls.definitions`).
        Be careful! The used controller firmware
        may not support this field.

        Args:
            name_or_idx (str | int): Field name or register index.

        Returns:
            Base | None: The created field, or None if not found or not valid.
        """
        # The definitions object hold all available definitions
        definition = cls.definitions.get(name_or_idx)
        if definition is not None and definition.valid:
            return definition.create_field()
        return None

    def create_field(self, name_or_idx):
        """
        Create a field object from a version-dependent definition (= included in
        class variable `cls.definitions` and is valid for `self.version`).

        Args:
            name_or_idx (str | int): Field name or register index.

        Returns:
            Base | None: The created field, or None if not found or not valid.
        """
        definition, _ = self._get_definition(name_or_idx, False)
        if definition is not None and definition.valid:
            return definition.create_field()
        return None


# Constructors and magic methods ##############################################

    def _init_instance(self, version, safe):
        """Re-usable method to initialize all instance variables."""
        self.safe = safe
        self._version = version

        # There may be several names or alias that points to one definition.
        # So in order to spare memory we split the name/index-to-field-lookup
        # into a name/index-to-definition-lookup and a definition-to-field-lookup
        self._def_lookup = LuxtronikDefinitionsDictionary()
        self._field_lookup = {}
        # Furthermore stores the definition-to-field-lookup separate from the
        # field-definition pairs to keep the index-sorted order when adding new entries
        self._items = [] # list of tuples, 0: definition, 1: field

        # Instead of re-create the block-list on every read, we just update it
        # on first time used or on next time used if some fields are added.
        self._read_blocks_up_to_date = False
        self._read_blocks = ContiguousDataBlockList(self.name, True)

    def __init__(self, version=LUXTRONIK_LATEST_SHI_VERSION, safe=True):
        """
        Initialize the data-vector instance.

        Creates field objects for all version-dependent definitions (= included
        in class variable `cls.definitions` and is valid for `self.version`)
        and stores them in the data vector.

        Args:
            version (tuple[int] | None):
                Version to be used for creating the field objects.
                This ensures that the data vector only contain valid fields.
                If None is passed, all available fields are added.
                (default: LUXTRONIK_LATEST_SHI_VERSION)
            safe (bool): If true, prevent fields marked as
                not secure from being written to.
        """
        self._init_instance(version, safe)

        # Create fields depending on the given version
        for d in self.definitions:
            if version_in_range(version, d.since, d.until):
                # The definitions are already sorted correctly.
                # So we can just add them one after the other.
                self._add(d, d.create_field())

    @classmethod
    def empty(cls, version=LUXTRONIK_LATEST_SHI_VERSION, safe=True):
        """
        Initialize the data-vector instance without any fields.

        Args:
            version (tuple[int] | None):
                Version to be used for creating the field objects afterwards.
                This ensures that the data vector only contain valid fields.
                If None is passed, all available fields can be added.
                (default: LUXTRONIK_LATEST_SHI_VERSION)
            safe (bool): If true, prevent fields marked as
                not secure from being written to.
        """
        obj = cls.__new__(cls) # this don't call __init__()
        obj._init_instance(version, safe)
        return obj

    def __getitem__(self, def_name_or_idx):
        return self.get(def_name_or_idx)

    def __setitem__(self, def_name_or_idx, value):
        return self.set(def_name_or_idx, value)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        # _items is a list of tuples, 0: definition, 1: field
        return iter([item[0] for item in self._items])

    def __contains__(self, def_field_name_or_idx):
        """
        Check whether the data vector contains a name, index,
        or definition matching an added field, or the field itself.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Definition object, field object, field name or register index.

        Returns:
            True if the searched element was found, otherwise False.
        """
        if isinstance(def_field_name_or_idx, Base):
            return any(def_field_name_or_idx is field for field in self._field_lookup.values())
        elif isinstance(def_field_name_or_idx, LuxtronikDefinition):
            # speed-up the look-up by search only the name-dict
            return def_field_name_or_idx.name in self._def_lookup._name_dict
        else:
            return def_field_name_or_idx in self._def_lookup


# properties and access methods ###############################################

    @property
    def version(self):
        return self._version

    def values(self):
        # _items is a list of tuples, 0: definition, 1: field
        return iter([item[1] for item in self._items])

    def items(self):
        """
        Iterator for all definition-field-pairs (list of tuples with
        0: definition, 1: field) contained herein."""
        return iter(self._items)


# Find, add and alias methods #################################################

    def _get_definition(self, def_field_name_or_idx, all_not_version_dependent):
        """
        Look-up a definition by name, index, a field instance or by the definition itself.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Definition object, field object, field name or register index.
            all_not_version_dependent (bool): If true, look up the definition
                within the `cls.definitions` otherwise within `self._def_lookup` (which
                contain all definitions related to all added fields)

        Returns:
            tuple[LuxtronikDefinition | None, Base | None]:
                A definition-field-pair tuple:
                Index 0: Return the found or given definitions, otherwise None
                Index 1: Return the given field, otherwise None
        """
        definition = def_field_name_or_idx
        field = None
        if isinstance(def_field_name_or_idx, Base):
            definition = def_field_name_or_idx.name
            field = def_field_name_or_idx
        if not isinstance(def_field_name_or_idx, LuxtronikDefinition):
            if all_not_version_dependent:
                definition = self.definitions.get(definition)
            else:
                # def_lookup contains only valid and addable definitions
                definition = self._def_lookup.get(definition)
        return definition, field

    def _add(self, definition, field, alias=None):
        """
        Add a definition-field-pair to the internal dictionaries.

        Args:
            definition (LuxtronikDefinition): Definition related to the field.
            field (Base): Field to add.
            alias (Hashable | None): Alias, which can be used to access the field again.
        """
        self._def_lookup.add(definition, alias)
        self._field_lookup[definition] = field
        self._items.append((definition, field))

    def add(self, def_field_name_or_idx, alias=None):
        """
        Adds an additional version-dependent field (= included in class variable
        `cls.definitions` and is valid for `self.version`) to this data vector.
        Mainly used for data vectors created via `empty()`
        to read/write individual fields. Existing fields will not be overwritten.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Field to add. Either by definition, name or index, or the field itself.
            alias (Hashable | None): Alias, which can be used to access the field again.

        Returns:
            Base | None: The added field object if this could be added or
                the existing field, otherwise None. In case a field

        Note:
            It is not possible to add fields which are not defined.
            To add custom fields, add them to the used `LuxtronikDefinitionsList`
            (`cls.definitions`) first.
            If multiple fields added for the same index/name, the last added takes precedence.
        """
        # Look-up the related definition
        definition, field = self._get_definition(def_field_name_or_idx, True)
        if definition is None:
            return None

        # Check if the field already exists
        existing_field = self._field_lookup.get(definition, None)
        if existing_field is not None:
            return existing_field

        # Add a (new) field
        if version_in_range(self._version, definition.since, definition.until):
            if field is None:
                field = definition.create_field()
            self._read_blocks_up_to_date = False
            self._add(definition, field, alias)
            # sort _items by definition.index
            # _items is a list of tuples, 0: definition, 1: field
            self._items.sort(key=lambda item: item[0].index)
            return field
        return None

    def register_alias(self, def_field_name_or_idx, alias):
        """
        Add an alternative name (or anything hashable else)
        that can be used to access a specific field.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Field to which the alias is to be added.
                Either by definition, name, register index, or the field itself.
            alias (Hashable): Alias, which can be used to access the field again.

        Returns:
            Base | None: The field to which the alias was added,
                or None if not possible
        """
        # Resolve a field input
        def_name_or_idx = def_field_name_or_idx
        if isinstance(def_name_or_idx, Base):
            def_name_or_idx = def_name_or_idx.name
        # register alias
        definition = self._def_lookup.register_alias(def_name_or_idx, alias)
        if definition is None:
            return None
        return self._field_lookup.get(definition, None)


# Data-blocks methods #########################################################

    def update_read_blocks(self):
        """
        (Re-)Create the data block list (`ContiguousDataBlockList`) for read-operations.

        Since the data blocks do not change as long as no new fields are added,
        it is sufficient to regenerate them only when a change occurs.
        """
        if not self._read_blocks_up_to_date:
            self._read_blocks.clear()
            for definition, field in self._items:
                self._read_blocks.collect(definition, field)
        self._read_blocks_up_to_date = True


# Data and access methods #####################################################

    def parse(self, raw_data):
        """
        Parse raw data into the corresponding fields.

        Args:
            raw_data (list[int]): List of raw register values.
                The raw data must start at register index 0.
        """
        raw_len = len(raw_data)
        for definition, field in self._items:
            if definition.index + definition.count >= raw_len:
                continue
            integrate_data(definition, field, raw_data)

    def get(self, def_name_or_idx, default=None):
        """
        Retrieve a field by definition, name or register index.

        Args:
            def_name_or_idx (LuxtronikDefinition | str | int):
                Definition, name, or register index to be used to search for the field.

        Returns:
            Base | None: The field found or the provided default if not found.

        Note:
            If multiple fields added for the same index/name,
            the last added takes precedence.
        """
        if isinstance(def_name_or_idx, LuxtronikDefinition):
            definition = def_name_or_idx
        else:
            definition = self._def_lookup.get(def_name_or_idx)
        if definition is not None:
            return self._field_lookup.get(definition, default)
        return default

    def set(self, def_field_name_or_idx, value):
        """
        Set field to new value.

        The value is set, even if the field marked as non-writeable.
        No data validation is performed either.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | int | str):
                Definition, name, or register index to be used to search for the field.
                It is also possible to pass the field itself.
            value (int | List[int]): Value to set
        """
        field = def_field_name_or_idx
        if not isinstance(field, Base):
            field = self.get(def_field_name_or_idx)
        if field is not None:
            field.value = value
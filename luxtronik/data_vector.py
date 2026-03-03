"""Provides a base class for parameters, calculations, visibilities."""

import logging

from luxtronik.collections import LuxtronikFieldsDictionary
from luxtronik.datatypes import Base, Unknown
from luxtronik.definitions import LuxtronikDefinition


LOGGER = logging.getLogger(__name__)


###############################################################################
# Base class for all luxtronik data vectors
###############################################################################

class DataVector:
    """
    Class that holds a vector of data fields.

    Provides access to fields by name, index or alias.
    To use aliases, they must first be registered here (locally = only valid
    for this vector) or directly in the `LuxtronikDefinitionsList`
    (globally = valid for all newly created vector).
    """

    name = "DataVector"

    # DataVector specific list of definitions as `LuxtronikDefinitionsList`
    definitions = None # override this

    _obsolete = {}


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
            Unknown: A field instance of type `Unknown`.
        """
        return Unknown(f"unknown_{cls.name}_{idx}", False)

    @classmethod
    def create_any_field(cls, def_name_or_idx):
        """
        Create a field object from an available definition
        (= included in class variable `cls.definitions`).
        Be careful! The used controller firmware
        may not support this field.

        If `def_name_or_idx`
        - is a definition -> create the field from the provided definition
        - is a name -> lookup the definition by name and create the field
        - is a idx -> lookup definition by index and create the field

        Args:
            def_name_or_idx (LuxtronikDefinition | str | int): Definitions object,
                field name or register index.

        Returns:
            Base | None: The created field, or None if not found or not valid.
        """
        if isinstance(def_name_or_idx, LuxtronikDefinition):
            definition = def_name_or_idx
        else:
            # The definitions object hold all available definitions
            definition = cls.definitions.get(def_name_or_idx)
        if definition is not None and definition.valid:
            return definition.create_field()
        return None

    def create_field(self, def_name_or_idx):
        """
        Create a field object from a version-dependent definition (= included in
        class variable `cls.definitions` and is valid for `self.version`).

        If `def_name_or_idx`
        - is a definition -> create the field from the provided definition
        - is a name -> lookup the definition by name and create the field
        - is a idx -> lookup definition by index and create the field

        Args:
            def_name_or_idx (str | int): Definitions object,
                field name or register index.

        Returns:
            Base | None: The created field, or None if not found or not valid.
        """
        definition, _ = self._get_definition(def_name_or_idx, False)
        if definition is not None and definition.valid:
            return definition.create_field()
        return None


# constructor, magic methods and iterators ####################################

    def _init_instance(self, safe):
        """Re-usable method to initialize all instance variables."""
        self.safe = safe

        # Dictionary that holds all fields
        self._data = LuxtronikFieldsDictionary()

    def __init__(self):
        """Initialize DataVector class."""
        self._init_instance(True)

    @property
    def data(self):
        """
        Return the internal `LuxtronikFieldsDictionary`.
        Please check its documentation.
        """
        return self._data

    def __getitem__(self, def_name_or_idx):
        """
        Array-style access to method `get`.
        Please check its documentation.
        """
        return self.get(def_name_or_idx)

    def __setitem__(self, def_name_or_idx, value):
        """
        Array-style access to method `set`.
        Please check its documentation.
        """
        return self.set(def_name_or_idx, value)

    def __len__(self):
        """
        Forward the `LuxtronikFieldsDictionary.__len__` method.
        Please check its documentation.
        """
        return len(self._data)

    def __iter__(self):
        """
        Forward the `LuxtronikFieldsDictionary.__iter__` method.
        Please check its documentation.
        """
        return iter(self._data)

    def __contains__(self, def_field_name_or_idx):
        """
        Forward the `LuxtronikFieldsDictionary.__contains__` method.
        Please check its documentation.
        """
        return def_field_name_or_idx in self._data

    def values(self):
        """
        Forward the `LuxtronikFieldsDictionary.values` method.
        Please check its documentation.
        """
        return self._data.values()

    def items(self):
        """
        Forward the `LuxtronikFieldsDictionary.items` method.
        Please check its documentation.
        """
        return iter(self._data.items())


# Alias methods ###############################################################

    def register_alias(self, def_field_name_or_idx, alias):
        """
        Forward the `LuxtronikFieldsDictionary.register_alias` method.
        Please check its documentation.
        """
        return self._data.register_alias(def_field_name_or_idx, alias)


# Get and set methods #########################################################

    def _get_definition(self, def_field_name_or_idx, all_not_version_dependent):
        """
        Look-up a definition by name, index, a field instance or by the definition itself.

        If `def_field_name_or_idx`
        - is a definition -> lookup the definition by the definition's name
        - is a field -> lookup the definition by the field's name
        - is a name -> lookup the field by the name
        - is a idx -> lookup the field by the index

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Definition object, field object, field name or register index.
            all_not_version_dependent (bool): If true, look up the definition
                within the `cls.definitions` otherwise within `self._data` (which
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
            # In case we got a field, search for the description by the field name
            definition = def_field_name_or_idx.name
            field = def_field_name_or_idx
        if not isinstance(def_field_name_or_idx, LuxtronikDefinition):
            if all_not_version_dependent:
                # definitions contains all available definitions
                definition = self.definitions.get(definition)
            else:
                # _data.def_dict contains only valid and previously added definitions
                definition = self._data.def_dict.get(definition)
        return definition, field

    def get(self, def_field_name_or_idx, default=None):
        """
        Retrieve an added field by definition, field, name or register index.
        Triggers a key error when we try to query obsolete fields.

        If `def_field_name_or_idx`
        - is a definition -> lookup the field by the definition
        - is a field -> lookup the field by the field's name
        - is a name -> lookup the field by the name
        - is a idx -> lookup the field by the index

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Definition, name, or register index to be used to search for the field.

        Returns:
            Base | None: The field found or the provided default if not found.

        Note:
            If multiple fields added for the same index/name,
            the last added takes precedence.
        """
        # check for obsolete
        obsolete_entry = self._obsolete.get(def_field_name_or_idx, None)
        if obsolete_entry:
            raise KeyError(f"The name '{def_field_name_or_idx}' is obsolete! Use '{obsolete_entry}' instead.")
        # look-up the field
        field = self._data.get(def_field_name_or_idx, default)
        if field is None:
            LOGGER.warning(f"entry '{def_field_name_or_idx}' not found")
        return field

    def set(self, def_field_name_or_idx, value):
        """
        Set the data of a field to the given value.

        The value is set, even if the field marked as non-writeable.
        No data validation is performed either.

        If `def_field_name_or_idx`
        - is a definition -> lookup the field by the definition and set the value
        - is a field -> set the value of this field
        - is a name -> lookup the field by the name and set the value
        - is a idx -> lookup the field by the index and set the value

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
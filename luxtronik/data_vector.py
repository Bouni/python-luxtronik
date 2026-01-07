"""Provides a base class for parameters, calculations, visibilities."""

import logging

from luxtronik.constants import (
    LUXTRONIK_NAME_CHECK_PREFERRED,
    LUXTRONIK_NAME_CHECK_OBSOLETE,
)

from luxtronik.datatypes import Base
from luxtronik.definitions import LuxtronikDefinition, LuxtronikDefinitionsDictionary


LOGGER = logging.getLogger(__name__)


###############################################################################
# Field dictionary for data vectors
###############################################################################

class LuxtronikFieldsDictionary:
    """
    Dictionary that behaves like the earlier data vector dictionaries (index-field-dictionary),
    with the addition that obsolete fields are also supported and can be addressed by name.
    Aliases are also supported.
    """

    def __init__(self):
        # There may be several names or alias that points to one definition.
        # So in order to spare memory we split the name/index-to-field-lookup
        # into a name/index-to-definition-lookup and a definition-to-field-lookup
        self._def_lookup = LuxtronikDefinitionsDictionary()
        self._field_lookup = {}
        # Furthermore stores the definition-to-field-lookup separate from the
        # field-definition pairs to keep the index-sorted order when adding new entries
        self._items = [] # list of tuples, 0: definition, 1: field

    def __getitem__(self, def_field_name_or_idx):
        return self.get(def_field_name_or_idx)

    def __setitem__(self, def_name_or_idx, value):
        assert False, "__setitem__ not implemented."

    def __len__(self):
        return len(self._def_lookup._index_dict)

    def __iter__(self):
        """
        Iterate over all non-obsolete indices. If an index is assigned multiple times,
        only the index of the preferred definition will be output.
        """
        # _items is a list of tuples, 0: definition, 1: field
        all_related_defs = self._def_lookup._index_dict.values()
        return iter([d.index for d in self._items if d in all_related_defs])

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

    def values(self):
        """
        Iterator for all added non-obsolete fields. If an index is assigned multiple times,
        only the field of the preferred definition will be output.
        """
        # _items is a list of tuples, 0: definition, 1: field
        all_related_defs = self._def_lookup._index_dict.values()
        return iter([f for d, f in self._items if d in all_related_defs])

    def items(self):
        """
        Iterator for all non-obsolete index-field-pairs (list of tuples with
        0: index, 1: field) contained herein. If an index is assigned multiple times,
        only the index-field-pair of the preferred definition will be output.
        """
        # _items is a list of tuples, 0: definition, 1: field
        all_related_defs = self._def_lookup._index_dict.values()
        return iter([(d.index, f) for d, f in self._items if d in all_related_defs])

    @property
    def def_items(self):
        """
        Iterator for all definition-field-pairs (list of tuples with
        0: definition, 1: field) contained herein.
        """
        return self._items

    @property
    def def_dict(self):
        """Return the internal definition dictionary"""
        return self._def_lookup

    def add(self, definition, field, alias=None):
        """
        Add a definition-field-pair to the internal dictionaries.

        Args:
            definition (LuxtronikDefinition): Definition related to the field.
            field (Base): Field to add.
            alias (Hashable | None): Alias, which can be used to access the field again.
        """
        if definition.valid:
            self._def_lookup.add(definition, alias)
            self._field_lookup[definition] = field
            self._items.append((definition, field))

    def add_sorted(self, definition, field, alias=None):
        if definition.valid:
            self.add(definition, field, alias)
            # sort _items by definition.index
            # _items is a list of tuples, 0: definition, 1: field
            self._items.sort(key=lambda item: item[0].index)

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

    def get(self, def_field_name_or_idx, default=None):
        """
        Retrieve a field by definition, name or register index.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | str | int):
                Definition, name, or register index to be used to search for the field.

        Returns:
            Base | None: The field found or the provided default if not found.

        Note:
            If multiple fields added for the same index/name,
            the last added takes precedence.
        """
        def_name_or_idx = def_field_name_or_idx
        if isinstance(def_name_or_idx, Base):
            def_name_or_idx = def_name_or_idx.name
        if isinstance(def_name_or_idx, LuxtronikDefinition):
            definition = def_name_or_idx
        else:
            definition = self._def_lookup.get(def_name_or_idx)
        if definition is not None:
            return self._field_lookup.get(definition, default)
        return default

###############################################################################
# Base class for all luxtronik data vectors
###############################################################################

class DataVector:
    """Class that holds a vector of data entries."""

    logger = LOGGER
    name = "DataVector"

    _obsolete = {}

    def __init__(self):
        """Initialize DataVector class."""
        self._data = LuxtronikFieldsDictionary()

    def __iter__(self):
        """Iterator for the data entries."""
        return iter(self._data.items())

    @property
    def data(self):
        return self._data

    def parse(self, raw_data):
        """Parse raw data."""
        for index, data in enumerate(raw_data):
            entry = self._data.get(index, None)
            if entry is not None:
                entry.raw = data
            else:
                # self.logger.warning(f"Entry '%d' not in list of {self.name}", index)
                definition = LuxtronikDefinition.unknown(index, self.name, 0)
                field = definition.create_field()
                field.raw = data
                self._data.add_sorted(definition, field)

    def _name_lookup(self, name):
        """
        Try to find the index using the given field name.

        Args:
            name (string): Field name.

        Returns:
            tuple[int | None, str | None]:
                0: Index found or None
                1: New preferred name, if available, otherwise None
        """
        obsolete_entry = self._obsolete.get(name, None)
        if obsolete_entry:
            return None, obsolete_entry
        for index, entry in self._data.items():
            check_result = entry.check_name(name)
            if check_result == LUXTRONIK_NAME_CHECK_PREFERRED:
                return index, None
            elif check_result == LUXTRONIK_NAME_CHECK_OBSOLETE:
                return index, entry.name
        return None, None

    def _lookup(self, target, with_index=False):
        """
        Lookup an entry

        "target" could either be its id or its name.

        In case "with_index" is set, also the index is returned.
        """
        if isinstance(target, str):
            try:
                # Try to get entry by id
                target_index = int(target)
            except ValueError:
                # Get entry by name
                target_index, new_name = self._name_lookup(target)
                if new_name is not None:
                    raise KeyError(f"The name '{target}' is obsolete! Use '{new_name}' instead.")
        elif isinstance(target, int):
            # Get entry by id
            target_index = target
        else:
            target_index = None

        target_entry = self._data.get(target_index, None)
        if target_entry is None:
            self.logger.warning("entry '%s' not found", target)
        if with_index:
            return target_index, target_entry
        return target_entry

    def get(self, target):
        """Get entry by id or name."""
        entry = self._lookup(target)
        return entry

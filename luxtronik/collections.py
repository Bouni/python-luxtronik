"""Common used collection objects."""

import logging

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
        self._pairs = [] # list of tuples, 0: definition, 1: field

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
        # _pairs is a list of tuples, 0: definition, 1: field
        all_related_defs = self._def_lookup._index_dict.values()
        return iter([d.index for d in self._pairs if d in all_related_defs])

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
        # _pairs is a list of tuples, 0: definition, 1: field
        all_related_defs = self._def_lookup._index_dict.values()
        return iter([f for d, f in self._pairs if d in all_related_defs])

    def items(self):
        """
        Iterator for all non-obsolete index-field-pairs (list of tuples with
        0: index, 1: field) contained herein. If an index is assigned multiple times,
        only the index-field-pair of the preferred definition will be output.
        """
        # _pairs is a list of tuples, 0: definition, 1: field
        all_related_defs = self._def_lookup._index_dict.values()
        return iter([(d.index, f) for d, f in self._pairs if d in all_related_defs])

    def pairs(self):
        """
        Return all definition-field-pairs (list of tuples with
        0: definition, 1: field) contained herein.
        """
        return self._pairs

    @property
    def def_dict(self):
        """Return the internal definition dictionary, containing all added definitions"""
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
            self._pairs.append((definition, field))

    def add_sorted(self, definition, field, alias=None):
        """
        Behaves like the normal `add` but then sorts the pairs.

        Args:
            definition (LuxtronikDefinition): Definition related to the field.
            field (Base): Field to add.
            alias (Hashable | None): Alias, which can be used to access the field again.
        """
        if definition.valid:
            self.add(definition, field, alias)
            # sort _pairs by definition.index
            # _pairs is a list of tuples, 0: definition, 1: field
            self._pairs.sort(key=lambda pair: pair[0].index)

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
        Retrieve a field by definition, name or register index, or the field itself.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Definition, field, name, or register index to be used to search for the field.

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
"""Provides a base class for parameters, calculations, visibilities."""

import logging

from luxtronik.constants import (
    LUXTRONIK_NAME_CHECK_PREFERRED,
    LUXTRONIK_NAME_CHECK_OBSOLETE,
)

from luxtronik.collections import LuxtronikFieldsDictionary


LOGGER = logging.getLogger(__name__)


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


    def __contains__(self, def_field_name_or_idx):
        """
        Forward the `LuxtronikFieldsDictionary.__contains__` method.
        Please check its documentation.
        """
        return def_field_name_or_idx in self._data

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

    def set(self, target, value):
        "TODO: Placeholder for future changes"
        pass


import logging

from luxtronik.data_vector import DataVector


LOGGER = logging.getLogger(__name__)

###############################################################################
# Configuration interface data-vector
###############################################################################

class DataVectorConfig(DataVector):
    """Specialized DataVector for Luxtronik configuration fields."""

    def _init_instance(self, safe):
        """Re-usable method to initialize all instance variables."""
        super()._init_instance(safe)

    def __init__(self, safe=True):
        """
        Initialize the data-vector instance.
        Creates field objects for definitions and stores them in the data vector.

        Args:
            safe (bool): If true, prevent fields marked as
                not secure from being written to.
        """
        self._init_instance(safe)

        # Add all available fields
        for d in self.definitions:
            self._data.add(d, d.create_field())

    @classmethod
    def empty(cls, safe=True):
        """
        Initialize the data-vector instance without any fields.

        Args:
            safe (bool): If true, prevent fields marked as
                not secure from being written to.
        """
        obj = cls.__new__(cls) # this don't call __init__()
        obj._init_instance(safe)
        return obj

    def add(self, def_field_name_or_idx, alias=None):
        """
        Adds an additional field to this data vector.
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
        existing_field = self._data.get(definition, None)
        if existing_field is not None:
            return existing_field

        # Add a (new) field
        if field is None:
            field = definition.create_field()
        self._data.add_sorted(definition, field, alias)
        return field
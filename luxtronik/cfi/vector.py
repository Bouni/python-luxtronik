
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


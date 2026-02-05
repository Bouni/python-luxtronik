"""Main components of the Luxtronik smart home interface."""

import logging

from luxtronik.collections import get_data_arr
from luxtronik.common import classproperty, version_in_range
from luxtronik.datatypes import Base
from luxtronik.definitions import (
    LuxtronikDefinition,
    LuxtronikDefinitionsList,
)
from luxtronik.shi.constants import (
    LUXTRONIK_LATEST_SHI_VERSION,
    LUXTRONIK_SHI_REGISTER_BIT_SIZE
)
from luxtronik.shi.common import (
    LuxtronikSmartHomeReadHoldingsTelegram,
    LuxtronikSmartHomeReadInputsTelegram,
    LuxtronikSmartHomeWriteHoldingsTelegram,
)
from luxtronik.shi.vector import DataVectorSmartHome
from luxtronik.shi.holdings import Holdings, HOLDINGS_DEFINITIONS
from luxtronik.shi.inputs import Inputs, INPUTS_DEFINITIONS
from luxtronik.shi.contiguous import ContiguousDataBlockList


LOGGER = logging.getLogger(__name__)

READ = True
WRITE = False
SAFE = True

###############################################################################
# Smart home interface data
###############################################################################

class LuxtronikSmartHomeData:
    """
    Data-vector collection for all smart home interface data vectors.

    Holds both the `holdings` and `inputs` data structures that represent
    the smart home data exposed by the Luxtronik controller.
    """

    def __init__(
        self,
        holdings=None,
        inputs=None,
        version=LUXTRONIK_LATEST_SHI_VERSION,
        safe=SAFE
    ):
        """
        Initialize a LuxtronikSmartHomeData instance.

        Args:
            holdings (Holdings): Optional holdings data vector. If not provided,
                a new `Holdings` instance is created.
            inputs (Inputs): Optional inputs data vector. If not provided,
                a new `Inputs` instance is created.
            version (tuple[int] | None): Version to be used for creating the data vectors.
                This ensures that the data vectors only contain valid fields.
                If None is passed, all available fields are added.
                (default: LUXTRONIK_LATEST_SHI_VERSION)
            safe (bool): If true, prevent holding fields marked as
                not secure from being written to.
        """
        self.holdings = holdings if holdings is not None else Holdings(version, safe)
        self.inputs = inputs if inputs is not None else Inputs(version)

    @classmethod
    def empty(
        cls,
        version=LUXTRONIK_LATEST_SHI_VERSION,
        safe=SAFE
    ):
        """
        Initialize an empty LuxtronikSmartHomeData instance
        (= no fields are added to the data-vectors).

        Args:
            version (tuple[int] | None): The version is added to the data vectors
                so some checks can be performed later.
                (default: LUXTRONIK_LATEST_SHI_VERSION)
            safe (bool): If true, prevent holding fields marked as
                not secure from being written to.
        """
        obj = cls.__new__(cls)
        obj.holdings = Holdings.empty(version, safe)
        obj.inputs = Inputs.empty(version)
        return obj

###############################################################################
# Smart home interface
###############################################################################

class LuxtronikSmartHomeInterface:
    """
    Read/write interface for Luxtronik smart home fields.

    This class builds on the simple addr/count/data interface and
    provides indexing and name resolution for easier access.

    This interface contains an internal list of operations to be executed.
    Operations can be added to the list using the "collect" methods.
    "Send" will process the entire list and then clear it. "Read" or "write" methods
    (except "raw") also adds an operation and then processes the entire list,
    which is cleared afterwards.
    """

    def __init__(self, interface, version=LUXTRONIK_LATEST_SHI_VERSION):
        """
        Initialize the smart home interface.

        Args:
            interface: The underlying read/write interface.
            version (tuple[int] | None): Version to be used for creating fields or data vectors.
                This ensures that the data vectors only contain valid fields.
                If None is passed, all available fields are added.
                Additionally, the version is used to performed some consistency checks.
                (default: LUXTRONIK_LATEST_SHI_VERSION)
        """
        self._interface = interface
        self._version = version
        self._blocks_list = []
        self._filtered_holdings = LuxtronikDefinitionsList.filtered(HOLDINGS_DEFINITIONS, version)
        self._filtered_inputs = LuxtronikDefinitionsList.filtered(INPUTS_DEFINITIONS, version)

    @property
    def version(self):
        return self._version

# Helper methods ##############################################################

    def _get_definition(self, def_name_or_idx, definitions):
        """
        Retrieve a definition by name or index that is supported by the controller.

        Args:
            def_name_or_idx (LuxtronikDefinition | str | int):
                Name, register index or the definition of the field.

        Returns:
            LuxtronikDefinition | None: The matching definition, or None if not found.
        """
        if isinstance(def_name_or_idx, LuxtronikDefinition):
            definition = def_name_or_idx
        else:
            definition = definitions.get(def_name_or_idx)
        if definition is None:
            return None
        if not version_in_range(self._version, definition.since, definition.until):
            LOGGER.debug(f"Field {definition.name} not valid for {self._version}")
            return None
        return definition

    def _get_def_field_pair(self, def_field_name_or_idx, definitions):
        """
        Retrieve a definition by name or index that is supported by the controller.
        On success, additionally returns either the passed field or a newly created field.

        Args:
            def_name_or_idx (LuxtronikDefinition | Base| str | int):
                Name, register index or the definition of the field, or the field itself.

        Returns:
            tuple[LuxtronikDefinition, Base]: The matching definition-field pair.
        """
        if isinstance(def_field_name_or_idx, Base):
            definition = self._get_definition(def_field_name_or_idx.name, definitions)
            field = def_field_name_or_idx if definition is not None else None
        else:
            definition = self._get_definition(def_field_name_or_idx, definitions)
            field = definition.create_field() if definition is not None else None
        return definition, field

    def _get_index_from_name(self, name):
        """
        Extract the index from an 'unknown' identifier (e.g. 'Unknown_Input_105').

        Args:
            name (str): The identifier string.

        Returns:
            int | None: The extracted index, or None if it cannot be determined.
        """
        parts = name.split("_")
        if len(parts) == 3 and parts[2].isdigit():
            return int(parts[2])
        return None

    def _try_create_definition(self, def_name_or_idx, definitions):
        """
        Retrieve the definition for the given name or index. If no definition
        is found out of all available, attempt to generate a temporary one.
        If this also fails, return None.

        Args:
            def_name_or_idx (LuxtronikDefinition | str | int):
                The field name, register index or a definition object.
            definitions (LuxtronikDefinitionsList):
                Field definition list to look-up the desired definition

        Returns:
            LuxtronikDefinition | None: A valid definition, or None if not found.
        """
        if isinstance(def_name_or_idx, LuxtronikDefinition):
            definition = def_name_or_idx
        else:
            definition = definitions.get(def_name_or_idx)
        if definition is not None:
            return definition

        LOGGER.debug(
            f"Definition for {def_name_or_idx} not found. Attempting to create a temporary one."
        )

        # Handle unknown names like 'Unknown_Input_105'
        if isinstance(def_name_or_idx, str) and def_name_or_idx.lower().startswith("unknown_"):
            index = self._get_index_from_name(def_name_or_idx)
            if index is None:
                LOGGER.debug(
                    "Cannot determine index from name '{def_name_or_idx}'. " \
                    + "Use format 'Unknown_Input_INDEX'."
                )
                return None
            return definitions.create_unknown_definition(index)

        if isinstance(def_name_or_idx, str) and def_name_or_idx.isdigit():
            index = int(def_name_or_idx)
            return definitions.create_unknown_definition(index)

        # Handle integer indices
        if isinstance(def_name_or_idx, int):
            return definitions.create_unknown_definition(def_name_or_idx)

        LOGGER.debug(f"Could not find or generate a definition for {def_name_or_idx}.")
        return None


# Telegram methods ############################################################

    def _create_read_telegram(self, block, telegram_type):
        """
        Create a read-telegram of type `telegram_type` out of this `ContiguousDataBlock`.

        Args:
            telegram_type (class of LuxtronikSmartHomeReadTelegram):
                Type of the telegram to create.

        Returns:
            LuxtronikSmartHomeReadTelegram:
                The created telegram.
        """
        return telegram_type(block.first_addr, block.overall_count)

    def _create_write_telegram(self, block, telegram_type):
        """
        Create a write-telegram of type `telegram_type` out of this `ContiguousDataBlock`.

        Args:
            telegram_type (class of LuxtronikSmartHomeWriteTelegram):
                Type of the telegram to create.

        Returns:
            LuxtronikSmartHomeWriteTelegram | None:
                The created telegram or None in case of an error.
        """
        data_arr = block.get_data_arr()
        if data_arr is None:
            LOGGER.error(f"Failed to create a {telegram_type} telegram! " \
                + "The provided data is not valid.")
            return None
        return telegram_type(block.first_addr, data_arr)

    def _create_telegram(self, block, type_name, read_not_write):
        """
        Create a read or write-telegram out of this `ContiguousDataBlock`.

        Returns:
            LuxtronikSmartHomeReadTelegram | LuxtronikSmartHomeWriteTelegram | None:
                The created telegram or None in case of an error.
        """
        if type_name == self.holdings.name and (read_not_write == READ):
            return self._create_read_telegram(block, LuxtronikSmartHomeReadHoldingsTelegram)
        if type_name == self.inputs.name and (read_not_write == READ):
            return self._create_read_telegram(block, LuxtronikSmartHomeReadInputsTelegram)
        if type_name == self.holdings.name and (read_not_write == WRITE):
            return self._create_write_telegram(block, LuxtronikSmartHomeWriteHoldingsTelegram)
        LOGGER.error(f"Could not create a telegram for {block}. Skip this operation.")
        return None

    def _create_telegrams(self, blocks_list):
        """
        Create read and/or write-telegrams out of the blocks list.

        Args:
            blocks_list (list[ContiguousDataBlockList]):
                List of contiguous block lists.

        Returns:
            list[tuple(ContiguousDataBlock, LuxtronikSmartHomeReadTelegram
                | LuxtronikSmartHomeWriteTelegram, bool)]:
                Data-tuple for `_send_and_integrate` method.
        """
        telegrams_data = []
        for blocks in blocks_list:
            for block in blocks:
                telegram = self._create_telegram(block, blocks.type_name, blocks.read_not_write)
                if telegram is not None:
                    telegrams_data.append((block, telegram, blocks.read_not_write))
        return telegrams_data

    def _integrate_data(self, telegrams_data):
        """
        Integrate the read data from telegrams back into the corresponding blocks.
        '_create_telegrams' must be called up beforehand.

        Returns:
            bool: True if all data could be integrated.
        """
        success = True
        for block, telegram, read_not_write in telegrams_data:
            if (read_not_write == READ):
                # integrate_data() also resets the write_pending flag,
                # intentionally only for read fields
                valid = block.integrate_data(telegram.data)
                if not valid:
                    LOGGER.debug(f"Failed to integrate read data into {block}")
                success &= valid
            else:
                # Reset write_pending flag
                for part in block:
                    part.field.write_pending = False
        return success


# Main methods ################################################################

    def _prepare_read_field(self, definition, field):
        """
        Check whether the field to be read is supported by the controller.

        Args:
            definition (LuxtronikDefinition):
                Definition object related to the field to be read.
            field (Base):
                Field to be read.

        Returns:
            bool: True if all checks have been passed, False otherwise.
        """
        # Skip non-supported fields
        if not version_in_range(self._version, definition.since, definition.until):
            field.raw = None
            return False

        return True

    def _prepare_write_field(self, definition, field, safe, data):
        """
        Check whether the field to be written
        - is supported by the controller
        - got data (either within the field or via `data`)
        - is writeable (if `safe` is True)
        and additionally integrates transferred data

        Args:
            definition (LuxtronikDefinition):
                Definition object related to the field to be read.
            field (Base):
                Field to be read.

        Returns:
            bool: True if all checks have been passed, False otherwise.
        """
        # Skip non-supported fields
        if not version_in_range(self._version, definition.since, definition.until):
            return False

        # Skip fields that do not carry user-data and not data is provided
        if not field.write_pending and data is None:
            return False

        # Override the field's data with the provided data
        if data is not None:
            field.value = data

        # Abort if field is not writeable or the value is invalid
        if not field.check_for_write(safe):
            return False

        # Abort if insufficient data is provided
        if not get_data_arr(definition, field, LUXTRONIK_SHI_REGISTER_BIT_SIZE):
            LOGGER.warning("Data error / insufficient data provided: " \
                + f"name={definition.name}, data={field.raw}")
            return False

        return True

    def _collect_field(self, blocks_list, def_field_name_or_idx, definitions, \
        read_not_write, safe, data):
        """
        Add a single field to the blocks list.

        The field may correspond to multiple registers and can be specified by
        name (str), register index (int), or directly as a field or definition object.
        Only if the controller supports the field will it be collected.

        Args:
            blocks_list (list[ContiguousDataBlockList]):
                List of contiguous block lists.
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Field name, register index, field object or definition object.
            definitions (LuxtronikDefinitionsList):
                List of definitions that contains the desired field definition.
            read_not_write (bool): If True, the field is collected for read, otherwise for write.
            safe (bool): If True, do not collect the field for write when it is marked as non-writeable.
            data (list[int] | None): Optional raw data to override the field's data.

        Returns:
            Base | None: The field object with integrated data, or None in case of an error.
        """
        if def_field_name_or_idx is None:
            return None

        definition, field = self._get_def_field_pair(def_field_name_or_idx, definitions)

        # create temporary definition for trial-and-error-mode
        if self._version is None and definition is None and isinstance(def_field_name_or_idx, (int, str)):
            definition = self._try_create_definition(def_field_name_or_idx, definitions)
            if definition is None:
                return None
            field = definition.create_field()

        if definition is None:
            # We have to clear non-supported fields here, see comment below
            if (read_not_write == READ) and isinstance(def_field_name_or_idx, Base):
                def_field_name_or_idx.raw = None
            return None

        # _get_def_field_pair ensures that the field is supported, no need to call _prepare_read_field
        #if (read_not_write == READ) and not self._prepare_read_field(definition, field):
        #    return None
        if (read_not_write == WRITE) and not self._prepare_write_field(definition, field, safe, data):
            return None

        blocks = ContiguousDataBlockList(definitions.name, read_not_write)
        blocks.append_single(definition, field)
        blocks_list.append(blocks)
        return field

    def _collect_fields(self, blocks_list, data_vector, definitions, read_not_write):
        """
        Add all fields to the blocks list.
        Only by the controller supported fields will be collected.

        Args:
            blocks_list (list[ContiguousDataBlockList]):
                List of contiguous block lists.
            data_vector (DataVectorSmartHome): The data vector class providing fields.
            definitions (LuxtronikDefinitionsList):
                List of definitions that contains the desired field definitions.
            read_not_write (bool): If True, the fields are collected for read, otherwise for write.
        """
        if not isinstance(data_vector, DataVectorSmartHome):
            return

        if self._version is None:
            # Trial-and-error mode: Add a block for every field
            blocks = ContiguousDataBlockList(definitions.name, read_not_write)
            if (read_not_write == READ):
                for definition, field in data_vector.data.pairs():
                    # _prepare_read_field will never fail, no need to call it
                    #if self._prepare_read_field(definition, field):
                    blocks.append_single(definition, field)
            else:
                for definition, field in data_vector.data.pairs():
                    if self._prepare_write_field(definition, field, data_vector.safe, None):
                        blocks.append_single(definition, field)
            if len(blocks) > 0:
                blocks_list.append(blocks)
        else:
            if (read_not_write == READ):
                # We can directly use the prepared read-blocks
                data_vector.update_read_blocks()
                if len(data_vector._read_blocks) > 0:
                    blocks_list.append(data_vector._read_blocks)
            else:
                blocks = ContiguousDataBlockList(definitions.name, read_not_write)
                # Organize data into contiguous blocks
                for definition, field in data_vector.data.pairs():
                    if self._prepare_write_field(definition, field, data_vector.safe, None):
                        blocks.collect(definition, field)
                if len(blocks) > 0:
                    blocks_list.append(blocks)

    def _send_and_integrate(self, blocks_list):
        """
        Generate all necessary telegrams and then send them.
        Subsequently, the retrieved data is integrated into the provided fields.

        Args:
            blocks_list (list[ContiguousDataBlockList]):
                List of contiguous block lists.

        Returns:
            bool: True if no errors occurred, otherwise False.
        """
        # Convert the list of contiguous blocks to telegrams
        telegrams_data = self._create_telegrams(blocks_list)
        # Send all telegrams. The retrieved data is returned within the telegrams
        telegrams = [data[1] for data in telegrams_data]
        success = self._interface.send(telegrams)
        # Transfer the data from the telegrams into the fields
        success &= self._integrate_data(telegrams_data)
        return success


# Collect and send methods ####################################################

    def collect_holding_for_read(self, def_field_name_or_idx):
        """
        Collect a single field to read.
        Only if the controller supports the field will it be collected.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Field name, register index, field object or definition object.

        Returns:
            Base | None: The field object with integrated data, or None in case of an error.
        """
        return self._collect_field(self._blocks_list, def_field_name_or_idx, \
            self.holdings, READ, SAFE, None)

    def collect_holding_for_write(self, def_field_name_or_idx, data=None, safe=True):
        """
        Collect a single field to write.
        Only if the controller supports the field will it be collected.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Field name, register index, field object or definition object.
            data (list[int] | None): Optional raw data to override the field's data.
            safe (bool): If True, do not collect the field when it is marked as non-writeable.

        Returns:
            Base | None: The field object with integrated data, or None in case of an error.
        """
        return self._collect_field(self._blocks_list, def_field_name_or_idx, \
            self.holdings, WRITE, safe, data)

    def collect_holding(self, def_field_name_or_idx, data=None, safe=True):
        """
        First, collect a single field for writing and, in addition, for reading.
        Only if the controller supports the field will it be collected.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Field name, register index, field object or definition object.
            data (list[int] | None): Optional raw data to override the field's data to write.
            safe (bool): If True, do not collect the field for write when it is marked as non-writeable.

        Returns:
            Base | None: The field object with integrated data, or None in case of an error.
        """
        field = self._collect_field(self._blocks_list, def_field_name_or_idx, \
            self.holdings, WRITE, safe, data)
        if field is None:
            return None
        self._collect_field(self._blocks_list, field, \
            self.holdings, READ, SAFE, None)
        return field

    def collect_holdings_for_read(self, holdings):
        """
        Collect all fields of a holding data vector for reading
        that are supported by the controller. All others are filled with None.

        Args:
            holdings (Holdings): The holdings object containing field data.
                If None is provided, nothing is collected.
        """
        self._collect_fields(self._blocks_list, holdings, self.holdings, READ)

    def collect_holdings_for_write(self, holdings):
        """
        Collect all fields of a holding data vector for writing
        that are supported by the controller.

        Args:
            holdings (Holdings): The holdings object containing field data.
                If None is provided, nothing is collected.
        """
        self._collect_fields(self._blocks_list, holdings, self.holdings, WRITE)

    def collect_holdings(self, holdings):
        """
        First, collect all fields of a holding data vector for writing and,
        in addition, all fields for reading that are supported by the controller.
        All others are filled with None when reading.

        Args:
            holdings (Holdings): The holdings object containing field data.
                If None is provided, nothing is collected.
        """
        self.collect_holdings_for_write(holdings)
        self.collect_holdings_for_read(holdings)

    def collect_input(self, def_field_name_or_idx):
        """
        Collect a single field to read.
        Only if the controller supports the field will it be collected.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Field name, register index, field object or definition object.

        Returns:
            Base | None: The field object with integrated data, or None in case of an error.
        """
        return self._collect_field(self._blocks_list, def_field_name_or_idx, \
            self.inputs, READ, SAFE, None)

    def collect_inputs(self, inputs):
        """
        Collect all fields of a inputs data vector for reading
        that are supported by the controller. All others are filled with None.

        Args:
            inputs (Inputs): The inputs object containing field data.
                If None is provided, nothing is collected.
        """
        self._collect_fields(self._blocks_list, inputs, self.inputs, READ)

    def collect_data_for_read(self, data):
        """
        Collect all fields of all data vectors within the collection for reading
        that are supported by the controller. All others are filled with None.

        Args:
            data (LuxtronikSmartHomeData): The data vector collection containing field data.
                If None is provided, nothing is collected.
        """
        if not isinstance(data, LuxtronikSmartHomeData):
            return
        self.collect_holdings_for_read(data.holdings)
        self.collect_inputs(data.inputs)

    def collect_data_for_write(self, data):
        """
        Collect all fields of all data vectors within the collection for writing
        that are supported by the controller.

        Args:
            data (LuxtronikSmartHomeData): The data vector collection containing field data.
                If None is provided, nothing is collected.
        """
        if not isinstance(data, LuxtronikSmartHomeData):
            return
        self.collect_holdings_for_write(data.holdings)

    def collect_data(self, data):
        """
        First, collect all fields of all data vectors within the collection for writing and,
        in addition, all fields for reading that are supported by the controller.
        All others are filled with None when reading.

        Args:
            data (LuxtronikSmartHomeData): The data vector collection containing field data.
                If None is provided, nothing is collected.
        """
        if not isinstance(data, LuxtronikSmartHomeData):
            return
        self.collect_data_for_write(data)
        self.collect_data_for_read(data)

    def send(self):
        """
        Send all collected operations via the "collect" methods.
        Afterwards clears the internal list of operations.

        Returns:
            bool: True if no errors occurred, otherwise False.
        """
        success = self._send_and_integrate(self._blocks_list)
        self._blocks_list = []
        return success


# Holding methods #############################################################

    @classproperty
    def holdings(cls):
        """Returns the holdings dictionary containing all available holding definitions."""
        return HOLDINGS_DEFINITIONS

    def get_holdings(self, full_not_filtered=False):
        """
        Returns either the holdings dictionary containing all available holding definitions
        or a version-dependent variant of it, depending on the parameter `full_not_filtered`.

        Args:
            full_not_filtered (LuxtronikDefinition | str | int):
                Parameter for selecting the returned definitions list.

        Returns:
            LuxtronikDefinitionsList: List of definitions.
        """
        if full_not_filtered:
            return self.holdings
        else:
            return self._filtered_holdings

    def create_holding(self, def_name_or_idx):
        """
        Create a holding field if the related definition matches the stored version.

        Args:
            def_name_or_idx (LuxtronikDefinition | str | int):
                Name, register index or definition of the holding.

        Returns:
            Base | None: On success the created field, otherwise None.

        """
        _, field = self._get_def_field_pair(def_name_or_idx, HOLDINGS_DEFINITIONS)
        return field

    def create_holdings(self, safe=SAFE):
        """
        Create a holdings data-vector only with fields that match the stored version.

        Args:
            safe (bool): If true, prevent holding fields marked as
                not secure from being written to.

        Returns:
            DataVectorSmartHome: The created data-vector.
        """
        return Holdings(self._version, safe)

    def create_empty_holdings(self, safe=SAFE):
        """
        Create an empty holdings data-vector for the stored version.

        Args:
            safe (bool): If true, prevent holding fields marked as
                not secure from being written to.

        Returns:
            DataVectorSmartHome: The created data-vector.
        """
        return Holdings.empty(self._version, safe)

    def read_holding(self, def_field_name_or_idx):
        """
        Read the data of a single field.

        The field may correspond to multiple registers and can be specified by
        name (str), register index (int), or directly as a field or definition object.
        Only if the controller supports the field will it be read.
        The required offset is added automatically.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Field name, register index, field object or definition object.

        Returns:
            Base | None: The field object containing the read data,
                or None if the read failed.
        """
        field = self.collect_holding_for_read(def_field_name_or_idx)
        success = self.send()
        return field if success else None

    def read_holdings(self, holdings=None):
        """
        Read the data of all fields within the holdings data vector
        that are supported by the controller. All others are filled with None.

        Args:
            holdings (Holdings | None): Optional existing holdings object.
                If None is provided, a new instance is created.

        Returns:
            Holdings: The passed / created holdings data vector.
        """
        if not isinstance(holdings, Holdings):
            holdings = self.create_holdings(SAFE)

        self.collect_holdings_for_read(holdings)
        self.send()
        return holdings

    def write_holding(self, def_field_name_or_idx, data=None, safe=True):
        """
        Write all provided data or the field's own data to a field.

        The field may correspond to multiple registers and can be specified by
        name (str), register index (int), or directly as a field or definition object.
        Only if the controller supports the field will it be written.
        The required offset is added automatically.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Field name, register index, field object or definition object.
            data (list[int] | None): Optional raw data to override the field's data.
            safe (bool): If True, aborts when the field is marked as non-writeable.

        Returns:
            Base | None: The written field object, or None if the write failed.
        """
        field = self.collect_holding_for_write(def_field_name_or_idx, data, safe)
        success = self.send()
        return field if success else None

    def write_holdings(self, holdings):
        """
        Write the data of all fields within the holdings data vector
        that are supported by the controller.

        Args:
            holdings (Holdings): The holdings object containing field data.
                If None is provided, the write is aborted.

        Returns:
            bool: True if no errors occurred, otherwise False.
        """
        if not isinstance(holdings, Holdings):
            LOGGER.warning("Abort write! No data to write provided.")
            return False

        self.collect_holdings_for_write(holdings)
        return self.send()

    def write_and_read_holdings(self, holdings):
        """
        Write and then read the data of all fields within the holdings data vector
        that are supported by the controller. All others are filled with None.

        Args:
            holdings (Holdings): The holdings object containing field data.
                If None is provided, the write and read is aborted.

        Returns:
            bool: True if no errors occurred, otherwise False.
        """
        if not isinstance(holdings, Holdings):
            LOGGER.warning("Abort write and read! No data to write provided.")
            return False

        self.collect_holdings(holdings)
        return self.send()


# Input methods ###############################################################

    @classproperty
    def inputs(cls):
        """Returns the inputs dictionary containing all available input definitions."""
        return INPUTS_DEFINITIONS

    def get_inputs(self, full_not_filtered=False):
        """
        Returns either the inputs dictionary containing all available input definitions
        or a version-dependent variant of it, depending on the parameter `full_not_filtered`.

        Args:
            full_not_filtered (LuxtronikDefinition | str | int):
                Parameter for selecting the returned definitions list.

        Returns:
            LuxtronikDefinitionsList: List of definitions.
        """
        if full_not_filtered:
            return self.inputs
        else:
            return self._filtered_inputs

    def create_input(self, def_name_or_idx):
        """
        Create an input field if the related definition matches the stored version.

        Args:
            def_name_or_idx (LuxtronikDefinition | str | int):
                Name, register index or definition of the holding.

        Returns:
            Base | None: On success the created field, otherwise None.

        """
        _, field = self._get_def_field_pair(def_name_or_idx, INPUTS_DEFINITIONS)
        return field

    def create_inputs(self):
        """
        Create an inputs data-vector only with fields that match the stored version.

        Returns:
            DataVectorSmartHome: The created data-vector.
        """
        return Inputs(self._version, SAFE)

    def create_empty_inputs(self):
        """
        Create an empty inputs data-vector for the stored version.

        Returns:
            DataVectorSmartHome: The created data-vector.
        """
        return Inputs.empty(self._version, SAFE)

    def read_input(self, def_field_name_or_idx):
        """
        Read the data of a single field.

        The field may correspond to multiple registers and can be specified by
        name (str), register index (int), or directly as a field or definition object.
        Only if the controller supports the field will it be read.
        The required offset is added automatically.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Field name, register index, field object or definition object.

        Returns:
            Base | None: The field object containing the read data,
                or None if the read failed.
        """
        field = self.collect_input(def_field_name_or_idx)
        success = self.send()
        return field if success else None

    def read_inputs(self, inputs=None):
        """
        Read the data of all fields within the inputs data vector
        that are supported by the controller. All others are filled with None.

        Args:
            inputs (Inputs | None): Optional existing inputs object.
                If None is provided, a new instance is created.

        Returns:
            Inputs: The passed / created inputs data vector.
        """
        if not isinstance(inputs, Inputs):
            inputs = self.create_inputs()

        self.collect_inputs(inputs)
        self.send()
        return inputs


# Data methods ################################################################

    def create_data(self, safe=SAFE):
        """
        Create a data vector collection only with fields that match the stored version.

        Args:
            safe (bool): If true, prevent holding fields marked as
                not secure from being written to.

        Returns:
            LuxtronikSmartHomeData: The created data-collection.
        """
        return LuxtronikSmartHomeData(None, None, self._version, safe)

    def create_empty_data(self, safe=SAFE):
        """
        Create an empty data-collection for the stored version.

        Args:
            safe (bool): If true, prevent holding fields marked as
                not secure from being written to.

        Returns:
            LuxtronikSmartHomeData: The created data-collection.
        """
        return LuxtronikSmartHomeData.empty(self._version, safe)

    def read_data(self, data=None):
        """
        Read the data of all fields within the data vector collection
        that are supported by the controller. All others are filled with None.

        Args:
            data (LuxtronikSmartHomeData | None): Optional existing data vector collection.
                If None is provided, a new instance is created.

        Returns:
            LuxtronikSmartHomeData: The passed / created data vector collection.
        """
        if not isinstance(data, LuxtronikSmartHomeData):
            data = self.create_data(SAFE)

        self.collect_data_for_read(data)
        self.send()
        return data

    def write_data(self, data):
        """
        Write the data of all fields within the data vector collection
        that are supported by the controller.

        Args:
            data (LuxtronikSmartHomeData): The data vector collection containing field data.
                If None is provided, the write is aborted.

        Returns:
            bool: True if no errors occurred, otherwise False.
        """
        if not isinstance(data, LuxtronikSmartHomeData):
            LOGGER.warning("Abort write! No data to write provided.")
            return False

        self.collect_data_for_write(data)
        return self.send()

    def write_and_read_data(self, data):
        """
        Write and then read the data of all fields within the data vector collection
        that are supported by the controller. All others are filled with None.

        Args:
            data (LuxtronikSmartHomeData): The data vector collection containing field data.
                If None is provided, the write and read is aborted.

        Returns:
            bool: True if no errors occurred, otherwise False.
        """
        if not isinstance(data, LuxtronikSmartHomeData):
            LOGGER.warning("Abort write and read! No data to write provided.")
            return False

        self.collect_data(data)
        return self.send()


# Debug methods ###############################################################

    def read_holding_raw(self, index, count=1):
        """
        Read a specified number of registers starting at the given index,
        without performing version consistency checks.
        Mainly for debugging purposes.

        The required offset is added automatically.

        Args:
            index (int): The starting register index.
            count (int): Number of registers to read (Defaults to 1).

        Returns:
            list[int] | None: On success the list of read register values,
                otherwise None.
        """
        telegram = LuxtronikSmartHomeReadHoldingsTelegram(index + HOLDINGS_DEFINITIONS.offset, count)
        success = self._interface.send(telegram)
        return telegram.data if success else None

    def write_holding_raw(self, index, data_arr):
        """
        Write all provided data to registers at the specified index,
        without performing version consistency checks.
        Mainly for debugging purposes.

        The required offset is added automatically.

        Args:
            index (int): Starting register index.
            data_arr (list[int]): Values to be written to the registers.

        Returns:
            bool: True if no errors occurred, otherwise False.
        """
        telegram = LuxtronikSmartHomeWriteHoldingsTelegram(index + HOLDINGS_DEFINITIONS.offset, data_arr)
        return self._interface.send(telegram)

    def read_input_raw(self, index, count=1):
        """
        Read a specified number of registers starting at the given index,
        without performing version consistency checks.
        Mainly for debugging purposes.

        The required offset is added automatically.

        Args:
            index (int): The starting register index.
            count (int): Number of registers to read (Defaults to 1).

        Returns:
            list[int] | None: On success the list of read register values,
                otherwise None.
        """
        telegram = LuxtronikSmartHomeReadInputsTelegram(index + self.inputs.offset, count)
        success = self._interface.send(telegram)
        return telegram.data if success else None


# Standard methods ############################################################
# Be careful with method names!
# Identical named methods could be overridden in a derived class.

    def read(self, data=None):
        """
        Calls `read_data()`. Please check its documentation.
        Exists mainly to standardize the various interfaces.
        """
        return self.read_data(data)

    def write(self, data):
        """
        Calls `write_data()`. Please check its documentation.
        Exists mainly to standardize the various interfaces.
        """
        return self.write_data(data)

    def write_and_read(self, data):
        """
        Calls `write_and_read_data()`. Please check its documentation.
        Exists mainly to standardize the various interfaces.
        """
        return self.write_and_read_data(data)
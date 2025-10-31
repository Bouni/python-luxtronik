"""
Methods and classes to group contiguous fields of same type into single blocks to minimize
the number of read/write operations. They are necessary, because an invalid address
or a non-existent register within a read/write operation will result in a transmission error.
"""

from luxtronik.shi.common import LOGGER
from luxtronik.shi.definitions import get_data_arr, integrate_data

###############################################################################
# ContiguousDataPart
###############################################################################

class ContiguousDataPart:
    """
    Represents a single element of a contiguous data block.
    Each part references a `field` and its associated `definition`.
    """

    def __init__(self, definition, field):
        """
        Initialize a contiguous data part.

        Args:
            field (Base): The field object to read or write.
            definition (LuxtronikDefinition): The definition for this field.
        """
        self.field = field
        self.definition = definition

    def __repr__(self):
        return f"({self.index}, {self.count})"

    @property
    def index(self):
        return self.definition.index

    @property
    def addr(self):
        return self.definition.addr

    @property
    def count(self):
        return self.definition.count

    def get_data_arr(self):
        """
        Normalize the field's data to a list of the correct size.

        Returns:
            list[int] | None: List of length `definition.count`, or None if insufficient.
        """
        return get_data_arr(self.definition, self.field)

    def integrate_data(self, raw_data, data_offset=-1):
        """
        Integrate the related parts of the `raw_data` into the field

        Args:
            raw_data (list): Source array of bytes/words.
            data_offset (int): Optional offset. Defaults to `definition.index`.
        """
        integrate_data(self.definition, self.field, raw_data, data_offset)


###############################################################################
# ContiguousDataBlock
###############################################################################

class ContiguousDataBlock:
    """
    Represents a contiguous block of fields for efficient read/write access.
    Contiguous fields of same type are grouped into a single block to minimize
    the number of read/write operations.

    Note:
        - An invalid address or a non-existent register within a block
          will result in a transmission error.
        - Parts must be added in non-decreasing index order.
    """

    def __init__(self):
        self._parts = []
        self._last_idx = -1

    @classmethod
    def create_and_add(cls, definition, field):
        """
        Create a new block and add a single part.

        Args:
            definition (LuxtronikDefinition): Definition to add.
            field (Base): Associated field object.

        Returns:
            ContiguousDataBlock: New block with the part added.
        """
        obj = cls()
        obj.add(definition, field)
        return obj

    def clear(self):
        """Remove all parts from the block."""
        self._parts = []
        self._last_idx = -1

    def __iter__(self):
        return iter(self._parts)

    def __getitem__(self, index):
        return self._parts[index]

    def __len__(self):
        return len(self._parts)

    def __repr__(self):
        parts_str = ", ".join(repr(part) for part in self._parts)
        return f"(index={self.first_index}, count={self.overall_count}, " \
            + f"parts=[{parts_str}])"

    def can_add(self, definition):
        """
        Check whether a part with the given definition
        can be appended without creating gaps.
        We assume that the (valid) parts are added in order.
        Therefore, some special cases can be disregarded.

        Args:
            definition (LuxtronikDefinition): Definition to add.

        Returns:
            bool: True if the part can be added to this block, otherwise False.
        """
        if self._last_idx == -1:
            return True
        start_idx = definition.index
        return start_idx >= self.first_index and start_idx <= self._last_idx + 1

    def add(self, definition, field):
        """
        Add a subsequent part to this contiguous data block.
        We assume that the (valid) parts are added in order.
        Therefore, some special cases can be disregarded.
        Call `can_add` before `add` to ensure validity.

        Args:
            definition (LuxtronikDefinition): Definition to add.
            field (Base): Associated field object.
        """
        self._parts.append(ContiguousDataPart(definition, field))
        self._last_idx = max(self._last_idx, definition.index + definition.count - 1)

    @property
    def first_index(self):
        """
        Return the first index of the block, or 0 if empty.
        This should be sufficient since the (valid) parts are added in index-sorted order.

        Returns:
            int: index of the first part or 0 if empty.
        """
        return self._parts[0].index if self._parts else 0

    @property
    def first_addr(self):
        """
        Return the first addr of the block, or 0 if empty.
        This should be sufficient since the (valid) parts are added in index-sorted order.

        Returns:
            int: addr of the first part or 0 if empty.
        """
        return self._parts[0].addr if self._parts else 0

    @property
    def overall_count(self):
        """
        Total contiguous register count covered by this block.

        Returns:
            int: number of registers or 0 if block is empty.
        """
        return self._last_idx - self.first_index + 1 if self._parts else 0

    def integrate_data(self, data_arr):
        """
        Integrate an array of registers (e.g. the read data)
        into the raw values of the corresponding fields.

        Args:
            data_arr (list[int] | None): A list of register values.

        Returns:
            bool: True if data length matches `overall_count`
                and integration succeeded, False otherwise.
        """
        valid = data_arr is not None and isinstance(data_arr, list)
        data_len = len(data_arr) if valid else 0
        valid &= data_len == self.overall_count

        if not valid:
            LOGGER.error(
                f"Data to integrate not valid! Expected length {self.overall_count} " \
                + f"but got {data_len}: data = {data_arr}, block = {self}"
            )
            return False

        first = self.first_index
        for part in self._parts:
            data_offset = part.index - first
            part.integrate_data(data_arr, data_offset)

        return True

    def get_data_arr(self):
        """
        Build a data array to write from parts' fields.

        Returns:
            list[int] | None: List of register values when valid, otherwise None.
                Returns None if overlapping writes occur or if some elements are missing.
        """
        if not self._parts:
            return None

        total = self.overall_count
        data_arr = [None] * total
        first = self.first_index
        valid = True
        for part in self._parts:
            data_offset = part.index - first
            data = part.get_data_arr()

            if data is None:
                valid = False
                LOGGER.error(f"No data provided for part {part}")
                continue

            end = data_offset + part.count
            if end > total:
                valid = False
                LOGGER.error(f"Part {part} would overflow block (end={end}, total={total})")
                continue

            # Integrate data only if not already done (first data wins)
            for i, value in enumerate(data):
                slot = data_offset + i
                if data_arr[slot] is None:
                    data_arr[slot] = value
                else:
                    valid = False
                    LOGGER.error(
                        f"Overlapping write detected for slot {slot}: " \
                        + f"existing={data_arr[slot]}, new={value}, part={part}"
                    )

        if not valid:
            return None

        if any(value is None for value in data_arr):
            LOGGER.error(f"Missing data after assembly: {data_arr}, block = {self}")
            return None

        return data_arr


###############################################################################
# ContiguousDataBlockList
###############################################################################

class ContiguousDataBlockList:
    """
    Maintain ordered contiguous data blocks for a single register type.

    Notes:
        - Parts (definitions) are expected to be presented in non-decreasing index order.
        - This container groups parts into contiguous blocks to minimize read/write operations.
    """

    def __init__(self, type_name, read_not_write):
        """
        Initialize a new container.

        Args:
            type_name (str): descriptive name for this block list (e.g., "holding", "input").
            read_not_write (bool): True when these blocks are for reads, False for writes.
        """
        self._blocks = []
        self._type_name = type_name
        self._read_not_write = read_not_write
        self._can_add = True

    def clear(self):
        """Remove all blocks."""
        self._blocks = []

    def __iter__(self):
        return iter(self._blocks)

    def __getitem__(self, index):
        return self._blocks[index]

    def __len__(self):
        return len(self._blocks)

    def __repr__(self):
        blocks_str = ", ".join(repr(block) for block in self._blocks)
        return f"(type_name={self._type_name}, read_not_write={self._read_not_write}, " \
            + f"blocks=[{blocks_str}])"

    @property
    def type_name(self):
        return self._type_name

    @property
    def read_not_write(self):
        return self._read_not_write

    def collect(self, definition, field):
        """
        Add a part into the appropriate contiguous block.
        Assumes parts arrive in sorted order by index. (see LuxtronikDefinitionsList).

        Args:
            definition (LuxtronikDefinition): Definition to add.
            field (Base): Associated field object.
        """
        # Start a new block if none exists or the last block cannot accept this definition
        if not self._blocks or not self._can_add or not self._blocks[-1].can_add(definition):
            self._blocks.append(ContiguousDataBlock())
        self._can_add = True

        # Append the (new) part to the last block
        self._blocks[-1].add(definition, field)

    def append(self, block):
        """
        Append an existing ContiguousDataBlock to the list.

        Args:
            block (ContiguousDataBlock): Block to append.
        """
        self._blocks.append(block)

    def append_single(self, definition, field):
        """
        Create a new block with a single part and append it.

        Args:
            definition (LuxtronikDefinition): Definition to add.
            field (Base): Associated field object.
        """
        self._blocks.append(ContiguousDataBlock.create_and_add(definition, field))
        self._can_add = False
"""
The metadata (`index`, `count`, ...) for a field (`Base`, `SelectionBase`)
is stored as a definition object. For ease of use, all definitions
of one type (`input`, `holding`, ...) are provided as a sorted list of objects.
This usually contains only predefined definitions (generated out of
`HOLDINGS_DEFINITIONS_LIST` or `INPUTS_DEFINITIONS_LIST`),
but can be expanded by the user.
"""

import logging

from luxtronik.shi.constants import (
    LUXTRONIK_SHI_REGISTER_BIT_SIZE,
    LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE
)


LOGGER = logging.getLogger(__name__)

###############################################################################
# Definition-Field-Pair methods
###############################################################################

VALUE_MASK = (1 << LUXTRONIK_SHI_REGISTER_BIT_SIZE) - 1

def pack_values(values, reverse=True):
    """
    Packs a list of data chunks into one integer.

    Args:
        values (list[int]): raw data; distributed across multiple registers.
        reverse (bool): Use big-endian/MSB-first if true,
            otherwise use little-endian/LSB-first order.

    Returns:
        int: Packed raw data as a single integer value.

    Note:
        The smart home interface uses a chunk size of 16 bits.
    """
    count = len(values)

    result = 0
    for idx, value in enumerate(values):
        # normal: idx = 0..n-1
        # reversed index: highest chunk first
        bit_index = (count - 1 - idx) if reverse else idx

        result |= (value & VALUE_MASK) << (LUXTRONIK_SHI_REGISTER_BIT_SIZE * bit_index)

    return result

def unpack_values(packed, count, reverse=True):
    """
    Unpacks 'count' values from a packed integer.

    Args:
        packed (int): Packed raw data as a single integer value.
        count (int): Number of chunks to unpack.
        reverse (bool): Use big-endian/MSB-first if true,
            otherwise use little-endian/LSB-first order.

    Returns:
        list[int]: List of unpacked raw data values.

    Note:
        The smart home interface uses a chunk size of 16 bits.
    """
    values = []

    for idx in range(count):
        # normal: idx = 0..n-1
        # reversed: highest chunk first
        bit_index = (count - 1 - idx) if reverse else idx

        chunk = (packed >> (LUXTRONIK_SHI_REGISTER_BIT_SIZE * bit_index)) & VALUE_MASK
        values.append(chunk)

    return values


def get_data_arr(definition, field):
    """
    Normalize the field's data to a list of the correct size.

    Args:
        definition (LuxtronikDefinition): Meta-data of the field.
        field (Base): Field object that contains data to get.

    Returns:
        list[int] | None: List of length `definition.count`,
            or None if the data size does not match.
    """
    data = field.raw
    if data is None:
        return None
    if not isinstance(data, list) and definition.count > 1 \
            and field.concatenate_multiple_data_chunks:
        # Usually big-endian (reverse=True) is used
        data = unpack_values(data, definition.count)
    if not isinstance(data, list):
        data = [data]
    return data if len(data) == definition.count else None

def check_data(definition, field):
    """
    Validate that the field contains sufficient raw data.

    Args:
        definition (LuxtronikDefinition): Meta-data of the field.
        field (Base): Field object that contains the data to check.

    Returns:
        bool: True if valid, False otherwise.
    """
    return get_data_arr(definition, field) is not None

def integrate_data(definition, field, raw_data, data_offset=-1):
    """
    Integrate raw values from a data array into the field.

    Args:
        definition (LuxtronikDefinition): Meta-data of the field.
        field (Base): Field object where to integrate the data.
        raw_data (list): Source array of bytes/words.
        data_offset (int): Optional offset. Defaults to `definition.index`.
    """
    data_offset = data_offset if data_offset >= 0 else definition.index
    # Use the information of the definition to extract the raw-value
    if (data_offset + definition.count - 1) >= len(raw_data):
        raw = None
    elif definition.count == 1:
        raw = raw_data[data_offset]
        raw = raw if raw != LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE else None
    else:
        raw = raw_data[data_offset : data_offset + definition.count]
        raw = raw if len(raw) == definition.count and \
            not any(data == LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE for data in raw) else None
        if field.concatenate_multiple_data_chunks and raw is not None:
            # Usually big-endian (reverse=True) is used
            raw = pack_values(raw)
    field.raw = raw
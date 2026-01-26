"""Common used collection objects."""

import logging

from luxtronik.datatypes import Base
from luxtronik.definitions import LuxtronikDefinition, LuxtronikDefinitionsDictionary

# TODO: Remove SHI dependency
LUXTRONIK_SHI_REGISTER_BIT_SIZE = 16
LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE = 0x7FFF

LOGGER = logging.getLogger(__name__)


###############################################################################
# Common methods
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
    Unpacks 'count' chunks from a packed integer.

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
    should_unpack = field.concatenate_multiple_data_chunks \
        and definition.count > 1
    if should_unpack and not isinstance(data, list):
        # Usually big-endian (reverse=True) is used
        data = unpack_values(data, definition.count)
    if not isinstance(data, list):
        data = [data]
    return data if len(data) == definition.count else None

def integrate_data(definition, field, raw_data, data_offset=-1):
    """
    Integrate the related parts of the `raw_data` into the field.

    Args:
        definition (LuxtronikDefinition): Meta-data of the field.
        field (Base): Field object where to integrate the data.
        raw_data (list): Source array of register values.
        data_offset (int): Optional offset. Defaults to `definition.index`.
    """
    # Use data_offset if provided, otherwise the index
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
        should_pack = field.concatenate_multiple_data_chunks
        if should_pack and raw is not None :
            # Usually big-endian (reverse=True) is used
            raw = pack_values(raw)
    field.raw = raw

###############################################################################
# Definition / field pair
###############################################################################

class LuxtronikDefFieldPair:
    """
    Combines a definition and a field into a single iterable object.
    """

    def __init__(self, definition, field):
        """
        Initialize a definition-field-pair.

        Args:
            field (Base): The field object.
            definition (LuxtronikDefinition): The definition for this field.
        """
        self.field = field
        self.definition = definition

    def __iter__(self):
        """
        Yield the definition and the field to unpack the object like `d, f = pair`.
        """
        yield self.definition
        yield self.field

    @property
    def index(self):
        """
        Forward the `LuxtronikDefinition.index` property.
        Please check its documentation.
        """
        return self.definition.index

    @property
    def addr(self):
        """
        Forward the `LuxtronikDefinition.addr` property.
        Please check its documentation.
        """
        return self.definition.addr

    @property
    def count(self):
        """
        Forward the `LuxtronikDefinition.count` property.
        Please check its documentation.
        """
        return self.definition.count

    def get_data_arr(self):
        """
        Forward the `get_data_arr` method with the stored objects.
        Please check its documentation.
        """
        return get_data_arr(self.definition, self.field)

    def integrate_data(self, raw_data, data_offset=-1):
        """
        Forward the `integrate_data` method with the stored objects.
        Please check its documentation.
        """
        integrate_data(self.definition, self.field, raw_data, data_offset)

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
        # There may be several names or alias that points to one definition and field.
        # So in order to spare memory we split the name/index-to-field-lookup
        # into a name/index-to-definition-lookup and a definition-to-field-lookup
        self._def_lookup = LuxtronikDefinitionsDictionary()
        self._field_lookup = {}
        # Furthermore stores the definition-to-field-lookup separate from the
        # field-definition pairs to keep the index-sorted order when adding new entries
        self._pairs = [] # list of LuxtronikDefFieldPair

    def __getitem__(self, def_field_name_or_idx):
        """
        Array-style access to method `get`.
        Please check its documentation.
        """
        return self.get(def_field_name_or_idx)

    def __len__(self):
        return len(self._def_lookup._index_dict)

    def __iter__(self):
        """
        Iterate over all non-obsolete indices. If an index is assigned multiple times,
        only the index of the preferred definition will be output.
        """
        all_related_defs = self._def_lookup._index_dict.values()
        return iter([d.index for d in self._pairs if d in all_related_defs])

    def __contains__(self, def_field_name_or_idx):
        """
        Check whether the data vector contains a name, index,
        or definition matching an added field, or the field itself.

        If `def_field_name_or_idx`
        - is a definition -> check whether a field with this definition has been added
        - is a field -> check whether this field has been added
        - is a name -> check whether a field with this name has been added
        - is a idx -> check whether a field with this index has been added

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
        all_related_defs = self._def_lookup._index_dict.values()
        return iter([f for d, f in self._pairs if d in all_related_defs])

    def items(self):
        """
        Iterator for all non-obsolete index-field-pairs (list of tuples with
        0: index, 1: field) contained herein. If an index is assigned multiple times,
        only the index-field-pair of the preferred definition will be output.
        """
        all_related_defs = self._def_lookup._index_dict.values()
        return iter([(d.index, f) for d, f in self._pairs if d in all_related_defs])

    def pairs(self):
        """
        Return all definition-field-pairs contained herein.
        """
        return self._pairs

    @property
    def def_dict(self):
        """
        Return the internal definition dictionary,
        containing all definitions related to the added fields.
        """
        return self._def_lookup

    @property
    def field_dict(self):
        """
        Return the internal field dictionary,
        containing all added fields.
        """
        return self._field_lookup

    def add(self, definition, field, alias=None):
        """
        Add a definition-field-pair to the internal dictionaries.

        Args:
            definition (LuxtronikDefinition): Definition related to the field.
            field (Base): Field to add.
            alias (Hashable | None): Alias, which can be used to access the field again.

        Note: Only use this method if the definitions order is already correct.
        """
        if definition.valid:
            self._def_lookup.add(definition, alias)
            self._field_lookup[definition] = field
            self._pairs.append(LuxtronikDefFieldPair(definition, field))

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
            self._pairs.sort(key=lambda pair: pair.definition.index)

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
        def_name_or_idx = def_field_name_or_idx
        # Resolve a field argument
        if isinstance(def_name_or_idx, Base):
            def_name_or_idx = def_name_or_idx.name
        # register alias
        definition = self._def_lookup.register_alias(def_name_or_idx, alias)
        if definition is None:
            return None
        return self._field_lookup.get(definition, None)

    def get(self, def_field_name_or_idx, default=None):
        """
        Retrieve an added field by definition, name or register index, or the field itself.

        If `def_field_name_or_idx`
        - is a definition -> lookup the field by the definition
        - is a field -> lookup the field by the field's name
        - is a name -> lookup the field by the name
        - is a idx -> lookup the field by the index

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
"""Constants used throughout the Luxtronik Smart Home Interface (SHI) module."""

from typing import Final

# Default TCP port for connecting to the Luxtronik controller
LUXTRONIK_DEFAULT_MODBUS_PORT: Final = 502

# Default timeout (in seconds) for Modbus operations
LUXTRONIK_DEFAULT_MODBUS_TIMEOUT: Final = 30

# Default offset for the input or holding indices
LUXTRONIK_DEFAULT_DEFINITION_OFFSET: Final = 10000

# Waiting time (in seconds) after writing the holdings
# to give the controller time to recalculate values, etc.
LUXTRONIK_WAIT_TIME_AFTER_HOLDING_WRITE: Final = 1

# Since version 3.92.0, all unavailable data fields
# have been returning this value (0x7FFF)
LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE: Final = 32767

# First Luxtronik firmware version that supports the Smart Home Interface (SHI)
LUXTRONIK_FIRST_VERSION_WITH_SHI: Final = (3, 90, 1, 0)

"""Constants used throughout the Luxtronik smart home interface (SHI) module."""

from typing import Final

# Default TCP port for connecting to the Luxtronik controller
LUXTRONIK_DEFAULT_MODBUS_PORT: Final = 502

# Default timeout (in seconds) for Modbus operations
LUXTRONIK_DEFAULT_MODBUS_TIMEOUT: Final = 30

# Identifier of holding data-vectors and partial name for unknown holding fields
HOLDINGS_FIELD_NAME: Final = "holding"

# Identifier of input data-vectors and partial name for unknown input fields
INPUTS_FIELD_NAME: Final = "input"

# Waiting time (in seconds) after writing the holdings
# to give the controller time to recalculate values, etc.
LUXTRONIK_WAIT_TIME_AFTER_HOLDING_WRITE: Final = 1

# The data from the smart home interface are transmitted in 16-bit chunks.
LUXTRONIK_SHI_REGISTER_BIT_SIZE: Final = 16

# First Luxtronik firmware version that supports the smart home interface (SHI)
LUXTRONIK_FIRST_VERSION_WITH_SHI: Final = (3, 90, 1, 0)

# Latest supported Luxtronik firmware version
# Note:
# No checks are performed against this version.
# This is merely the default value if no version is specified.
LUXTRONIK_LATEST_SHI_VERSION: Final = (3, 92, 1, 0)

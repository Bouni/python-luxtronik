"""Constants used throughout the Luxtronik config interface (CFI) module."""

from typing import Final

# Default port to be used to connect to Luxtronik controller.
LUXTRONIK_DEFAULT_PORT: Final = 8889

LUXTRONIK_PARAMETERS_WRITE: Final = 3002
LUXTRONIK_PARAMETERS_READ: Final = 3003
LUXTRONIK_CALCULATIONS_READ: Final = 3004
LUXTRONIK_VISIBILITIES_READ: Final = 3005

LUXTRONIK_SOCKET_READ_SIZE_PEEK: Final = 16

LUXTRONIK_SOCKET_READ_SIZE_INTEGER: Final = 4
LUXTRONIK_SOCKET_READ_SIZE_CHAR: Final = 1

# Identifier of calculation data-vectors and partial name for unknown calculation fields
CALCULATIONS_FIELD_NAME: Final = "calculation"

# Identifier of parameter data-vectors and partial name for unknown parameter fields
PARAMETERS_FIELD_NAME: Final = "parameter"

# Identifier of visibilities data-vectors and partial name for unknown visibility fields
VISIBILITIES_FIELD_NAME: Final = "visibility"

# Wait time (in seconds) after writing parameters to give controller
# some time to re-calculate values, etc.
WAIT_TIME_AFTER_PARAMETER_WRITE = 1

# The data from the config interface are transmitted in 32-bit chunks.
LUXTRONIK_CFI_REGISTER_BIT_SIZE: Final = 32
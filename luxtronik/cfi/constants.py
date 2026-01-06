"""Constants used throughout the Luxtronik config interface (CFI) module."""

# Default port to be used to connect to Luxtronik controller.
LUXTRONIK_DEFAULT_PORT = 8889

LUXTRONIK_PARAMETERS_WRITE = 3002
LUXTRONIK_PARAMETERS_READ = 3003
LUXTRONIK_CALCULATIONS_READ = 3004
LUXTRONIK_VISIBILITIES_READ = 3005

LUXTRONIK_SOCKET_READ_SIZE_PEEK = 16

LUXTRONIK_SOCKET_READ_SIZE_INTEGER = 4
LUXTRONIK_SOCKET_READ_SIZE_CHAR = 1

# Identifier of calculation data-vectors and partial name for unknown calculation fields
CALCULATIONS_FIELD_NAME = "calculation"

# Identifier of parameter data-vectors and partial name for unknown parameter fields
PARAMETERS_FIELD_NAME = "parameter"

# Identifier of visibilities data-vectors and partial name for unknown visibility fields
VISIBILITIES_FIELD_NAME = "visibility"
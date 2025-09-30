"""Constants used throughout the Luxtronik Smart Home Interface (SHI) module."""

# Default TCP port for connecting to the Luxtronik controller
LUXTRONIK_DEFAULT_MODBUS_PORT = 502

# Default timeout (in seconds) for Modbus operations
LUXTRONIK_DEFAULT_MODBUS_TIMEOUT = 30

# Waiting time (in seconds) after writing the holdings
# to give the controller time to recalculate values, etc.
LUXTRONIK_WAIT_TIME_AFTER_HOLDING_WRITE = 1

# First Luxtronik firmware version that supports the Smart Home Interface (SHI)
LUXTRONIK_FIRST_VERSION_WITH_SHI = "3.90.1"

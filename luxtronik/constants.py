"""Constants used throughout the luxtronik module"""

# Default port to be used to connect to Luxtronik controller.
LUXTRONIK_DEFAULT_PORT = 8889

LUXTRONIK_PARAMETERS_WRITE = 3002
LUXTRONIK_PARAMETERS_READ = 3003
LUXTRONIK_CALCULATIONS_READ = 3004
LUXTRONIK_VISIBILITIES_READ = 3005

LUXTRONIK_SOCKET_READ_SIZE_PEEK = 16

LUXTRONIK_SOCKET_READ_SIZE_INTEGER = 4
LUXTRONIK_SOCKET_READ_SIZE_CHAR = 1

# List of ports that are known to respond to discovery packets
LUXTRONIK_DISCOVERY_PORTS = [4444, 47808]

# Time (in seconds) to wait for response after sending discovery broadcast
LUXTRONIK_DISCOVERY_TIMEOUT = 2

# Content of packet that will be sent for discovering heat pumps
LUXTRONIK_DISCOVERY_MAGIC_PACKET = "2000;111;1;\x00"

# Content of response that is contained in responses to discovery broadcast
LUXTRONIK_DISCOVERY_RESPONSE_PREFIX = "2500;111;"

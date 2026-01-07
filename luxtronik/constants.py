"""Constants used throughout the luxtronik module"""

from typing import Final

# List of ports that are known to respond to discovery packets
LUXTRONIK_DISCOVERY_PORTS: Final = [4444, 47808]

# Time (in seconds) to wait for response after sending discovery broadcast
LUXTRONIK_DISCOVERY_TIMEOUT: Final = 2

# Content of packet that will be sent for discovering heat pumps
LUXTRONIK_DISCOVERY_MAGIC_PACKET: Final = "2000;111;1;\x00"

# Content of response that is contained in responses to discovery broadcast
LUXTRONIK_DISCOVERY_RESPONSE_PREFIX: Final = "2500;111;"

LUXTRONIK_NAME_CHECK_NONE: Final = "none"
LUXTRONIK_NAME_CHECK_PREFERRED: Final = "preferred"
LUXTRONIK_NAME_CHECK_OBSOLETE: Final = "obsolete"

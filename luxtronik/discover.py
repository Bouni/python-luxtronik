"""Discovery function for Luxtronik heat pump controllers"""
import logging
import socket

LUXTRONIK_DISCOVERY_PORTS = [4444, 47808]
LUXTRONIK_DISCOVERY_TIMEOUT = 2
LUXTRONIK_DISCOVERY_MAGIC_PACKET = "2000;111;1;\x00"
LUXTRONIK_DISCOVERY_RESPONSE_PREFIX = "2500;111;"

LOGGER = logging.getLogger("Luxtronik.Discover")


def discover() -> list[(str, int)]:
    """Broadcast discovery for Luxtronik heat pumps"""

    results: list[(str, int)] = []

    for port in LUXTRONIK_DISCOVERY_PORTS:
        LOGGER.debug("Send discovery packets to port %s", port)
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server.bind(("", port))
        server.settimeout(LUXTRONIK_DISCOVERY_TIMEOUT)

        # send AIT magic broadcast packet
        server.sendto(LUXTRONIK_DISCOVERY_MAGIC_PACKET.encode(), ("<broadcast>", port))
        LOGGER.debug("Sending broadcast request %s", LUXTRONIK_DISCOVERY_MAGIC_PACKET.encode())

        while True:
            try:
                res, con = server.recvfrom(1024)
                res = res.decode("ascii", errors="ignore")
                # if we receive what we just sent, continue
                if res == LUXTRONIK_DISCOVERY_MAGIC_PACKET:
                    continue
                ip_address = con[0]
                # if the response starts with the magic nonsense
                if res.startswith(LUXTRONIK_DISCOVERY_RESPONSE_PREFIX):
                    res = res.split(";")
                    LOGGER.debug("Received answer from %s %s", ip_address, str(res))
                    try:
                        port = int(res[2])
                        if port < 1 or port > 65535:
                            port = None
                    except ValueError:
                        port = None
                    if port is None:
                        LOGGER.debug(
                            "Response did not contain a valid port number,"
                            "an old Luxtronic software version might be the reason."
                        )
                    results.append((ip_address, port))
                LOGGER.debug(
                    "Received answer from %s, but with wrong content, skipping",
                    ip_address,
                )
                continue
            # if the timeout triggers, go on an use the other broadcast port
            except socket.timeout:
                break

    return results

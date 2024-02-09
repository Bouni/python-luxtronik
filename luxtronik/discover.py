"""Discovery function for Luxtronik heat pump controllers."""

from __future__ import annotations

import logging
import socket

from luxtronik.constants import (
    LUXTRONIK_DISCOVERY_PORTS,
    LUXTRONIK_DISCOVERY_TIMEOUT,
    LUXTRONIK_DISCOVERY_MAGIC_PACKET,
    LUXTRONIK_DISCOVERY_RESPONSE_PREFIX,
)

LOGGER = logging.getLogger("Luxtronik.Discover")


def discover() -> list[tuple[str, int | None]]:
    """Broadcast discovery for Luxtronik heat pumps."""

    results: list[tuple[str, int | None]] = []

    # pylint: disable=too-many-nested-blocks
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
                recv_bytes, con = server.recvfrom(1024)
                res = recv_bytes.decode("ascii", errors="ignore")
                # if we receive what we just sent, continue
                if res == LUXTRONIK_DISCOVERY_MAGIC_PACKET:
                    continue
                ip_address = con[0]
                # if the response starts with the magic nonsense
                if res.startswith(LUXTRONIK_DISCOVERY_RESPONSE_PREFIX):
                    res_list = res.split(";")
                    LOGGER.debug("Received response from %s %s", ip_address, str(res_list))
                    try:
                        res_port: int | None = int(res_list[2])
                        if res_port is None or res_port < 1 or res_port > 65535:
                            LOGGER.debug("Response contained an invalid port, ignoring")
                            res_port = None
                    except ValueError:
                        res_port = None
                    if res_port is None:
                        LOGGER.debug(
                            "Response did not contain a valid port number,"
                            "an old Luxtronic software version might be the reason"
                        )
                    results.append((ip_address, res_port))
                LOGGER.debug(
                    "Received response from %s, but with wrong content, skipping",
                    ip_address,
                )
                continue
            # if the timeout triggers, go on an use the other broadcast port
            except socket.timeout:
                break

    return results

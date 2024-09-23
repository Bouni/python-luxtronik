"""Discovery function for Luxtronik heat pump controllers."""

from __future__ import annotations

import logging
import socket

from luxtronik.constants import (
    LUXTRONIK_DISCOVERY_MAGIC_PACKET,
    LUXTRONIK_DISCOVERY_PORTS,
    LUXTRONIK_DISCOVERY_RESPONSE_PREFIX,
    LUXTRONIK_DISCOVERY_TIMEOUT,
)

LOGGER = logging.getLogger("Luxtronik.Discover")

"""Discovery function for Luxtronik heat pump controllers."""


def discover() -> list[tuple[str, int | None]]:
    """Broadcast discovery for Luxtronik heat pumps."""
    results: list[tuple[str, int | None]] = []

    for port in LUXTRONIK_DISCOVERY_PORTS:
        server = setup_broadcast_socket(port)
        send_discovery_packet(server, port)
        results.extend(collect_responses(server))

    return results


def setup_broadcast_socket(port: int) -> socket.socket:
    """Set up a broadcast socket for the given port."""
    LOGGER.debug("Setting up broadcast socket on port %s", port)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.bind(("", port))
    server.settimeout(LUXTRONIK_DISCOVERY_TIMEOUT)
    return server


def send_discovery_packet(server: socket.socket, port: int) -> None:
    """Send discovery broadcast packet to the specified port."""
    LOGGER.debug("Send discovery packets to port %s", port)
    server.sendto(LUXTRONIK_DISCOVERY_MAGIC_PACKET.encode(), ("<broadcast>", port))
    LOGGER.debug("Sending broadcast request %s", LUXTRONIK_DISCOVERY_MAGIC_PACKET.encode())


def collect_responses(server: socket.socket) -> list[tuple[str, int | None]]:
    """Collect responses from the server socket and return valid results."""
    results = []

    while True:
        try:
            recv_bytes, con = server.recvfrom(1024)
            ip_address, res = handle_response(recv_bytes, con)
            if res and res.startswith(LUXTRONIK_DISCOVERY_RESPONSE_PREFIX):
                parsed_response = parse_response(res, ip_address)
                if parsed_response:
                    results.append(parsed_response)
                else:
                    LOGGER.debug("Received response from %s, but with wrong content, skipping", ip_address)
        except socket.timeout:
            break

    return results


def handle_response(recv_bytes: bytes, con: tuple[str, int]) -> tuple[str, str]:
    """Handle received bytes and return the IP address and decoded response."""
    ip_address = con[0]
    res = recv_bytes.decode("ascii", errors="ignore")
    if res == LUXTRONIK_DISCOVERY_MAGIC_PACKET:
        LOGGER.debug("Received self-sent magic packet, ignoring")
        return ip_address, ""
    return ip_address, res


def parse_response(res: str, ip_address: str) -> tuple[str, int | None]:
    """Parse the discovery response and return the IP address and port, if valid."""
    res_list = res.split(";")
    LOGGER.debug("Received response from %s %s", ip_address, str(res_list))

    try:
        res_port: int | None = int(res_list[2])
        if res_port < 1 or res_port > 65535:
            LOGGER.debug("Response contained an invalid port, ignoring")
            res_port = None
    except (ValueError, IndexError):
        res_port = None

    if res_port is None:
        LOGGER.debug(
            "Response did not contain a valid port number, an old Luxtronic software version might be the reason"
        )

    return ip_address, res_port

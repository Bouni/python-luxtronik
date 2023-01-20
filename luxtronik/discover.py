"""Discovery function for Luxtronik heat pump controllers"""
import logging
import socket

LOGGER = logging.getLogger("Luxtronik.Discover")


def discover() -> list[(str, int)]:
    """Broadcast discovery for Luxtronik2 heat pumps"""

    results: list[(str, int)] = []

    for magic_port in (4444, 47808):
        LOGGER.debug("Send discovery packets to port %s", magic_port)
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server.bind(("", magic_port))
        server.settimeout(2)

        # send AIT magic broadcast packet
        data = "2000;111;1;\x00"
        server.sendto(data.encode(), ("<broadcast>", magic_port))
        LOGGER.debug("Sending broadcast request %s", data.encode())

        while True:
            try:
                res, con = server.recvfrom(1024)
                res = res.decode("ascii", errors="ignore")
                # if we receive what we just sent, continue
                if res == data:
                    continue
                ip_address = con[0]
                # if the response starts with the magic nonsense
                if res.startswith("2500;111;"):
                    res = res.split(";")
                    LOGGER.debug("Received answer from %s %s", ip_address, str(res))
                    try:
                        port = int(res[2])
                    except ValueError:
                        LOGGER.debug(
                            "Response did not contain a valid port number,"
                            "an old Luxtronic software version might be the reason."
                        )
                        port = None
                    results.append((ip_address, port))
                LOGGER.debug(
                    "Received answer, but with wrong magic bytes,"
                    "from %s skip this one",
                    ip_address,
                )
                continue
            # if the timeout triggers, go on an use the other broadcast port
            except socket.timeout:
                break

    return results

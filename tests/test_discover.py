"""Test suite for Luxtronik Discover"""

import pytest
from unittest import mock
import socket

from luxtronik.discover import (
    discover,
    setup_broadcast_socket,
    send_discovery_packet,
    collect_responses,
    handle_response,
    parse_response,
)

from luxtronik.constants import (
    LUXTRONIK_DISCOVERY_MAGIC_PACKET,
    LUXTRONIK_DISCOVERY_RESPONSE_PREFIX,
    LUXTRONIK_DISCOVERY_TIMEOUT,
)

# Mock constants
LUXTRONIK_DISCOVERY_PORTS = [1234]


@pytest.fixture
def mock_socket():
    """Fixture to mock socket behavior."""
    with mock.patch("socket.socket") as mock_socket:
        yield mock_socket


def test_setup_broadcast_socket(mock_socket):
    """Test the setup_broadcast_socket function."""
    mock_server = mock.Mock()
    mock_socket.return_value = mock_server

    server = setup_broadcast_socket(1234)

    # Check that socket is initialized correctly
    mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    mock_server.setsockopt.assert_called_once_with(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    mock_server.bind.assert_called_once_with(("", 1234))
    mock_server.settimeout.assert_called_once_with(LUXTRONIK_DISCOVERY_TIMEOUT)

    assert server == mock_server


def test_send_discovery_packet(mock_socket):
    """Test the send_discovery_packet function."""
    mock_server = mock_socket.return_value

    send_discovery_packet(mock_server, 1234)
    # Verify that sendto was called with the correct arguments
    expected_packet = LUXTRONIK_DISCOVERY_MAGIC_PACKET.encode()
    expected_address = ("<broadcast>", 1234)

    mock_server.sendto.assert_called_once_with(expected_packet, expected_address)


def test_handle_response():
    """Test the handle_response function."""
    recv_bytes = b"RESPONSE_PREFIX;data;1234"
    con = ("192.168.1.100", 5678)

    ip_address, res = handle_response(recv_bytes, con)

    assert ip_address == "192.168.1.100"
    assert res == "RESPONSE_PREFIX;data;1234"


def test_handle_response_ignore_magic_packet():
    """Test that handle_response ignores the magic packet response."""
    recv_bytes = LUXTRONIK_DISCOVERY_MAGIC_PACKET.encode()
    con = ("192.168.1.100", 5678)

    ip_address, res = handle_response(recv_bytes, con)

    assert ip_address == "192.168.1.100"
    assert res == ""  # Magic packet should be ignored


def test_parse_response():
    """Test the parse_response function."""
    res = "RESPONSE_PREFIX;data;1234"
    ip_address = "192.168.1.100"

    result = parse_response(res, ip_address)

    assert result == ("192.168.1.100", 1234)


def test_parse_response_invalid_port():
    """Test parse_response when the port is invalid."""
    res = "RESPONSE_PREFIX;data;99999"  # Invalid port > 65535
    ip_address = "192.168.1.100"

    result = parse_response(res, ip_address)

    assert result == ("192.168.1.100", None)


def test_parse_response_missing_port():
    """Test parse_response when the response doesn't have a port."""
    res = "RESPONSE_PREFIX;data"
    ip_address = "192.168.1.100"

    result = parse_response(res, ip_address)

    assert result == ("192.168.1.100", None)


def test_collect_responses_timeout(mock_socket):
    """Test collect_responses handling a socket timeout."""
    mock_server = mock_socket.return_value

    mock_server.recvfrom.side_effect = socket.timeout

    results = collect_responses(mock_server)

    assert results == []  # Timeout should return an empty result


def test_collect_responses_with_valid_data(mock_socket):
    """Test collect_responses with valid data."""
    mock_server = mock_socket.return_value
    mock_server.recvfrom.side_effect = [
        (f"{LUXTRONIK_DISCOVERY_RESPONSE_PREFIX}1234".encode(), ("192.168.1.100", 5678)),
        socket.timeout,
    ]

    results = collect_responses(mock_server)

    assert results == [("192.168.1.100", 1234)]


def test_discover(mock_socket):
    """Test the discover function."""
    mock_server = mock_socket.return_value

    # Mock sendto for sending the discovery packet
    mock_server.sendto = mock.Mock()

    # Mock recvfrom for receiving the response
    mock_server.recvfrom.side_effect = [
        (f"{LUXTRONIK_DISCOVERY_RESPONSE_PREFIX}1234".encode(), ("192.168.1.100", 5678)),
        socket.timeout,
        socket.timeout,  # dummy to prevent stopIteration error
    ]

    results = discover()

    assert results == [("192.168.1.100", 1234)]

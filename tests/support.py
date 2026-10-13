"""Small deterministic fixtures and process-wide offline test boundaries."""

from __future__ import annotations

import ipaddress
import os
import socket
import sqlite3
import tempfile
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


class OutboundNetworkDenied(RuntimeError):
    """Raised when a test attempts to resolve or connect outside loopback."""


class FrozenClock:
    """A small aware clock that advances only when explicitly requested."""

    def __init__(self, now: datetime) -> None:
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("FrozenClock requires a timezone-aware datetime")
        self._now = now

    def now(self) -> datetime:
        return self._now

    def advance(self, delta: timedelta) -> None:
        self._now += delta


class SequenceIds:
    """Return caller-supplied IDs and fail loudly when the sequence is spent."""

    def __init__(self, values: Iterable[str]) -> None:
        self._values = iter(values)

    def next_id(self) -> str:
        try:
            return next(self._values)
        except StopIteration:
            raise AssertionError("synthetic ID sequence exhausted") from None


class RecordedEffect:
    """Capture a synthetic effect invocation and return its configured result."""

    def __init__(self, result: Any = None) -> None:
        self.result = result
        self.calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.calls.append((args, kwargs))
        return self.result


@contextmanager
def private_temporary_directory() -> Iterator[Path]:
    """Yield a temporary directory with owner-only permissions."""
    with tempfile.TemporaryDirectory(prefix="career-helper-test-") as directory:
        path = Path(directory)
        path.chmod(0o700)
        yield path


@contextmanager
def independent_sqlite_connections(
    database_path: Path,
) -> Iterator[tuple[sqlite3.Connection, sqlite3.Connection]]:
    """Yield two independent connections to the same private, file-backed DB."""
    database_path = database_path.resolve()
    database_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    database_path.parent.chmod(0o700)
    first = sqlite3.connect(database_path)
    try:
        second = sqlite3.connect(database_path)
        try:
            yield first, second
        finally:
            second.close()
    finally:
        first.close()


def _normalized_host(host: str | bytes) -> str:
    if isinstance(host, bytes):
        try:
            host = host.decode("ascii")
        except UnicodeDecodeError:
            raise OutboundNetworkDenied("non-ASCII hostname denied in tests") from None
    if not isinstance(host, str):
        raise OutboundNetworkDenied("non-literal network target denied in tests")
    normalized = host.rstrip(".").lower()
    if normalized == "localhost":
        return normalized
    address = normalized.split("%", maxsplit=1)[0]
    try:
        parsed = ipaddress.ip_address(address)
    except ValueError:
        raise OutboundNetworkDenied(f"external hostname denied in tests: {host}") from None
    if not parsed.is_loopback:
        raise OutboundNetworkDenied(f"external address denied in tests: {host}")
    return normalized


def require_loopback_host(host: str | bytes) -> None:
    """Reject hostnames and addresses that are not literal loopback targets."""
    _normalized_host(host)


def install_network_denial() -> None:
    """Block DNS resolution and socket writes outside loopback for this process."""
    global _NETWORK_DENIAL_INSTALLED
    if _NETWORK_DENIAL_INSTALLED:
        return

    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        os.environ.pop(name, None)
    os.environ["NO_PROXY"] = "*"
    os.environ["no_proxy"] = "*"

    original_getaddrinfo = socket.getaddrinfo
    original_gethostbyname = socket.gethostbyname
    original_gethostbyname_ex = socket.gethostbyname_ex
    original_getnameinfo = socket.getnameinfo
    original_connect = socket.socket.connect
    original_connect_ex = socket.socket.connect_ex
    original_sendto = socket.socket.sendto
    original_sendmsg = getattr(socket.socket, "sendmsg", None)

    def guarded_getaddrinfo(
        host: str | bytes | None,
        *args: Any,
        **kwargs: Any,
    ) -> list[tuple[Any, ...]]:
        if host is None:
            raise OutboundNetworkDenied("unspecified host resolution denied in tests")
        normalized = _normalized_host(host)
        # Resolve localhost without consulting configured external DNS servers.
        lookup_host = "127.0.0.1" if normalized == "localhost" else normalized
        return original_getaddrinfo(lookup_host, *args, **kwargs)

    def guarded_gethostbyname(host: str | bytes) -> str:
        normalized = _normalized_host(host)
        if normalized == "localhost":
            return "127.0.0.1"
        return original_gethostbyname(normalized)

    def guarded_gethostbyname_ex(host: str | bytes) -> tuple[str, list[str], list[str]]:
        normalized = _normalized_host(host)
        if normalized == "localhost":
            return "localhost", ["localhost"], ["127.0.0.1"]
        return original_gethostbyname_ex(normalized)

    def guarded_gethostbyaddr(address: str) -> tuple[str, list[str], list[str]]:
        normalized = _normalized_host(address)
        if normalized in {"localhost", "127.0.0.1", "::1"}:
            return "localhost", ["localhost"], ["127.0.0.1", "::1"]
        raise OutboundNetworkDenied(f"reverse DNS denied in tests: {address}")

    def guarded_getnameinfo(
        sockaddr: tuple[Any, ...],
        flags: int,
    ) -> tuple[str, str]:
        if not sockaddr:
            raise OutboundNetworkDenied("empty socket address denied in tests")
        require_loopback_host(sockaddr[0])
        return original_getnameinfo(sockaddr, flags | socket.NI_NUMERICHOST)

    def validate_socket_target(sock: socket.socket, address: Any) -> None:
        if sock.family == socket.AF_UNIX:
            return
        if not isinstance(address, tuple) or not address:
            raise OutboundNetworkDenied("invalid socket target denied in tests")
        require_loopback_host(address[0])

    def guarded_connect(sock: socket.socket, address: Any) -> None:
        validate_socket_target(sock, address)
        original_connect(sock, address)

    def guarded_connect_ex(sock: socket.socket, address: Any) -> int:
        validate_socket_target(sock, address)
        return original_connect_ex(sock, address)

    def guarded_sendto(sock: socket.socket, *args: Any) -> int:
        if not args:
            raise OutboundNetworkDenied("missing datagram target denied in tests")
        validate_socket_target(sock, args[-1])
        return original_sendto(sock, *args)

    def guarded_sendmsg(sock: socket.socket, buffers: Any, *args: Any, **kwargs: Any) -> int:
        address = kwargs.get("address")
        if address is None and len(args) >= 3:
            address = args[2]
        if address is None:
            if sock.family != socket.AF_UNIX:
                try:
                    address = sock.getpeername()
                except (AttributeError, OSError):
                    raise OutboundNetworkDenied(
                        "sendmsg requires a connected loopback socket in tests"
                    ) from None
        validate_socket_target(sock, address)
        if original_sendmsg is None:
            raise OutboundNetworkDenied("sendmsg is unavailable in this runtime")
        return original_sendmsg(sock, buffers, *args, **kwargs)

    socket.getaddrinfo = guarded_getaddrinfo
    socket.gethostbyname = guarded_gethostbyname
    socket.gethostbyname_ex = guarded_gethostbyname_ex
    socket.gethostbyaddr = guarded_gethostbyaddr
    socket.getnameinfo = guarded_getnameinfo
    socket.socket.connect = guarded_connect
    socket.socket.connect_ex = guarded_connect_ex
    socket.socket.sendto = guarded_sendto
    if original_sendmsg is not None:
        socket.socket.sendmsg = guarded_sendmsg
    _NETWORK_DENIAL_INSTALLED = True


_NETWORK_DENIAL_INSTALLED = False

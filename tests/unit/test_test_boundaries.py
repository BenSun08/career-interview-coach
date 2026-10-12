import socket
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from stat import S_IMODE

from tests.support import (
    FrozenClock,
    OutboundNetworkDenied,
    RecordedEffect,
    SequenceIds,
    independent_sqlite_connections,
    install_network_denial,
    private_temporary_directory,
    require_loopback_host,
)

install_network_denial()


class TestTestBoundaries(unittest.TestCase):
    def test_clock_is_controllable(self) -> None:
        initial_time = datetime(2026, 10, 12, 9, 30, tzinfo=timezone.utc)
        clock = FrozenClock(initial_time)

        self.assertEqual(clock.now(), initial_time)
        clock.advance(timedelta(minutes=5))
        self.assertEqual(clock.now(), datetime(2026, 10, 12, 9, 35, tzinfo=timezone.utc))

    def test_ids_are_returned_in_order_and_exhaustion_is_explicit(self) -> None:
        ids = SequenceIds(["synthetic-id-1", "synthetic-id-2"])

        self.assertEqual(ids.next_id(), "synthetic-id-1")
        self.assertEqual(ids.next_id(), "synthetic-id-2")
        with self.assertRaises(AssertionError):
            ids.next_id()

    def test_effect_fixture_records_arguments_and_returns_configured_result(self) -> None:
        result = {"status": "synthetic-success"}
        effect = RecordedEffect(result)

        returned = effect("synthetic-dispatch", job_id="job-1")

        self.assertIs(returned, result)
        self.assertEqual(
            effect.calls,
            [(('synthetic-dispatch',), {"job_id": "job-1"})],
        )

    def test_temporary_data_directory_is_private_and_outside_the_repository(self) -> None:
        temporary_root = Path(tempfile.gettempdir()).resolve()
        repository_root = Path.cwd().resolve()

        with private_temporary_directory() as data_root:
            resolved_root = data_root.resolve()

            self.assertTrue(data_root.is_dir())
            self.assertTrue(resolved_root.is_relative_to(temporary_root))
            self.assertFalse(resolved_root.is_relative_to(repository_root))
            self.assertEqual(S_IMODE(data_root.stat().st_mode), 0o700)

    def test_sqlite_helper_uses_two_connections_to_the_same_file(self) -> None:
        with private_temporary_directory() as data_root:
            database_path = data_root / "synthetic.sqlite3"

            with independent_sqlite_connections(database_path) as (first, second):
                self.assertIsNot(first, second)
                first.execute("CREATE TABLE sample (value TEXT NOT NULL)")
                first.execute("INSERT INTO sample VALUES (?)", ("synthetic",))
                first.commit()

                row = second.execute("SELECT value FROM sample").fetchone()

            self.assertEqual(row, ("synthetic",))
            self.assertTrue(database_path.is_file())

    def test_network_policy_allows_loopback_and_rejects_external_hosts(self) -> None:
        require_loopback_host("127.0.0.1")
        require_loopback_host("::1")

        with self.assertRaises(OutboundNetworkDenied):
            require_loopback_host("provider.invalid")

    def test_socket_apis_reject_external_targets_without_network_io(self) -> None:
        external_address = ("203.0.113.8", 443)
        socket_sentinel = type("SocketSentinel", (), {"family": socket.AF_INET})()

        with self.assertRaises(OutboundNetworkDenied):
            socket.socket.connect(socket_sentinel, external_address)
        with self.assertRaises(OutboundNetworkDenied):
            socket.socket.connect_ex(socket_sentinel, external_address)
        with self.assertRaises(OutboundNetworkDenied):
            socket.socket.sendto(
                socket_sentinel, b"synthetic", ("203.0.113.8", 53)
            )
        if hasattr(socket.socket, "sendmsg"):
            with self.assertRaises(OutboundNetworkDenied):
                socket.socket.sendmsg(
                    socket_sentinel,
                    [b"synthetic"],
                    [],
                    0,
                    ("203.0.113.8", 53),
                )
            with self.assertRaises(OutboundNetworkDenied):
                socket.socket.sendmsg(socket_sentinel, [b"synthetic"])

    def test_dns_lookup_rejects_external_hosts_before_resolution(self) -> None:
        with self.assertRaises(OutboundNetworkDenied):
            socket.getaddrinfo("provider.invalid", 443)


if __name__ == "__main__":
    unittest.main()

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from singleton import DatabaseConnection


@pytest.fixture(autouse=True)
def reset_singleton():
    DatabaseConnection._instance = None
    yield
    DatabaseConnection._instance = None


class TestSingletonInstance:
    def test_same_instance_returned(self) -> None:
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        assert db1 is db2

    def test_only_one_instance_exists(self) -> None:
        instances = [DatabaseConnection() for _ in range(5)]
        assert all(i is instances[0] for i in instances)

    def test_default_host(self) -> None:
        db = DatabaseConnection()
        assert db.host == "localhost"

    def test_default_port(self) -> None:
        db = DatabaseConnection()
        assert db.port == 5432

    def test_not_connected_by_default(self) -> None:
        db = DatabaseConnection()
        assert db.connected is False


class TestDatabaseConnection:
    def test_connect_returns_message(self) -> None:
        db = DatabaseConnection()
        assert db.connect() == "Connected to localhost:5432"

    def test_connect_sets_connected(self) -> None:
        db = DatabaseConnection()
        db.connect()
        assert db.connected is True

    def test_query_requires_connection(self) -> None:
        db = DatabaseConnection()
        assert db.query("SELECT 1") == "Error: Not connected"

    def test_query_after_connect(self) -> None:
        db = DatabaseConnection()
        db.connect()
        assert db.query("SELECT * FROM users") == "Result of: SELECT * FROM users"

    def test_state_shared_across_instances(self) -> None:
        db1 = DatabaseConnection()
        db1.connect()

        db2 = DatabaseConnection()
        assert db2.connected is True

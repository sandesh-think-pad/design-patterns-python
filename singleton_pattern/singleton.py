import threading

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.host = "localhost"
                    cls._instance.port = 5432
                    cls._instance.connected = False
        return cls._instance

    def connect(self) -> str:
        self.connected = True
        return f"Connected to {self.host}:{self.port}"

    def query(self, sql: str) -> str:
        if not self.connected:
            raise RuntimeError("Error: Not connected")
        return f"Result of: {sql}"

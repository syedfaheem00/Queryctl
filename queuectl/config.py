import json
import threading

_CONFIG_FILE = "config.json"
_DEFAULTS = {"max_retries": 3, "backoff_base": 2, "worker_count": 1}

class Config:
    def __init__(self, path=_CONFIG_FILE):
        self.path = path
        self.lock = threading.Lock()
        self.data = _DEFAULTS.copy()
        self.load()

    def load(self):
        with self.lock:
            try:
                with open(self.path, "r") as f:
                    self.data.update(json.load(f))
            except Exception:
                pass
        return self.data

    def save(self):
        with self.lock, open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def set(self, key, value):
        self.data[key] = int(value) if value.isdigit() else value
        self.save()

    def get(self, key, default=None):
        return self.data.get(key, default)

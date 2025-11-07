import json

class Config:
    def __init__(self, filepath='config.json'):
        self.filepath = filepath
        self._config = {"max_retries": 3, "backoff_base": 2}

    def load(self):
        try:
            with open(self.filepath, 'r') as f:
                self._config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return self._config

    def save(self):
        with open(self.filepath, 'w') as f:
            json.dump(self._config, f, indent=2)

    def set(self, key, value):
        self._config[key] = int(value) if value.isdigit() else value
        self.save()
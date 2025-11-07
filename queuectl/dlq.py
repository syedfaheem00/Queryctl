import json

class DLQ:
    def __init__(self, filepath='dlq.json'):
        self.filepath = filepath

    def load(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self, jobs):
        with open(self.filepath, 'w') as f:
            json.dump(jobs, f, indent=2)
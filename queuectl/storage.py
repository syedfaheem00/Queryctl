import json
from threading import Lock

class JobStorage:
    def __init__(self, filepath='jobs.json'):
        self.filepath = filepath
        self.lock = Lock()

    def load_jobs(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_jobs(self, jobs):
        with self.lock, open(self.filepath, 'w') as f:
            json.dump(jobs, f, indent=2)
import json
import os
import threading

_JOB_FILE = "jobs.json"
_DLQ_FILE = "dlq.json"

class JobStorage:
    def __init__(self, jobs_path=_JOB_FILE, dlq_path=_DLQ_FILE):
        self.jobs_path = jobs_path
        self.dlq_path = dlq_path
        self.jobs_lock = threading.Lock()
        self.dlq_lock = threading.Lock()

    def load_jobs(self):
        with self.jobs_lock:
            if not os.path.exists(self.jobs_path):
                return []
            try:
                with open(self.jobs_path, "r") as f:
                    return json.load(f)
            except Exception:
                return []

    def save_jobs(self, jobs):
        with self.jobs_lock, open(self.jobs_path, "w") as f:
            json.dump(jobs, f, indent=2)

    def load_dlq(self):
        with self.dlq_lock:
            if not os.path.exists(self.dlq_path):
                return []
            try:
                with open(self.dlq_path, "r") as f:
                    return json.load(f)
            except Exception:
                return []

    def save_dlq(self, jobs):
        with self.dlq_lock, open(self.dlq_path, "w") as f:
            json.dump(jobs, f, indent=2)

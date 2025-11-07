import uuid
from datetime import datetime

class Job:
    def __init__(self, command, max_retries=3):
        self.id = str(uuid.uuid4())
        self.command = command
        self.state = "pending"
        self.attempts = 0
        self.max_retries = max_retries
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = self.created_at

    def to_dict(self):
        return {
            "id": self.id,
            "command": self.command,
            "state": self.state,
            "attempts": self.attempts,
            "max_retries": self.max_retries,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
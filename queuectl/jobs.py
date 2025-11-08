import uuid
from datetime import datetime

class Job:
    def __init__(self, id=None, command="", state="pending", attempts=0, max_retries=3,
                 created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        self.command = command
        self.state = state
        self.attempts = attempts
        self.max_retries = max_retries
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or self.created_at

    @staticmethod
    def from_dict(data):
        return Job(
            id=data.get("id"),
            command=data.get("command", ""),
            state=data.get("state", "pending"),
            attempts=int(data.get("attempts", 0)),
            max_retries=int(data.get("max_retries", 3)),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "command": self.command,
            "state": self.state,
            "attempts": self.attempts,
            "max_retries": self.max_retries,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def update_state(self, new_state):
        self.state = new_state
        self.updated_at = datetime.utcnow().isoformat()

    def can_retry(self):
        return self.attempts < self.max_retries

    def is_finished(self):
        return self.state in ("completed", "dead")

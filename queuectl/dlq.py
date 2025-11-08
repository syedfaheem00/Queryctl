from queuectl.storage import JobStorage

class DLQManager:
    def __init__(self, storage: JobStorage):
        self.storage = storage

    def add_job(self, job_dict):
        dlq = self.storage.load_dlq()
        dlq.append(job_dict)
        self.storage.save_dlq(dlq)

    def retry_job(self, job_id):
        dlq = self.storage.load_dlq()
        jobs = self.storage.load_jobs()
        for job in dlq:
            if job["id"] == job_id:
                job["state"] = "pending"
                job["attempts"] = 0
                jobs.append(job)
                dlq.remove(job)
                self.storage.save_jobs(jobs)
                self.storage.save_dlq(dlq)
                return True
        return False

    def list_dlq(self):
        return self.storage.load_dlq()

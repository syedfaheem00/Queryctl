import os
import signal
import subprocess
import threading
from multiprocessing import Process, current_process
from queuectl.jobs import Job
from queuectl.storage import JobStorage
from queuectl.dlq import DLQManager
from queuectl.utils import sleep_backoff

class WorkerPool:
    def __init__(self, count, config: dict, storage: JobStorage):
        self.count = count
        self.config = config
        self.storage = storage
        self.dlq = DLQManager(storage)
        self.stop_event = threading.Event()
        self.workers = []

    def start(self):
        self.stop_event.clear()
        print(f"Starting {self.count} worker(s)...")
        self.workers = []
        for i in range(self.count):
            p = Process(target=self.worker_loop, args=(i,))
            p.start()
            self.workers.append(p)
        print(f"Workers started: {[p.pid for p in self.workers]}")

    def stop(self):
        print("Stopping workers gracefully...")
        self.stop_event.set()
        for p in self.workers:
            p.join()
        print("All workers stopped.")

    def worker_loop(self, index):
        while not self.stop_event.is_set():
            jobs_data = self.storage.load_jobs()
            found = False
            for job_dict in jobs_data:
                job = Job.from_dict(job_dict)
                if job.state == "pending":
                    found = True
                    job.update_state("processing")
                    job_dict["state"] = "processing"
                    self.storage.save_jobs(jobs_data)
                    self.process_job(job)
                    break
            if not found:
                # No pending jobs: sleep briefly before checking again
                import time
                time.sleep(1)

    def process_job(self, job: Job):
        config = self.config
        print(f"[Worker {current_process().pid}] Executing: {job.command} (attempt {job.attempts+1}/{job.max_retries})")
        try:
            result = subprocess.run(job.command, shell=True)
            success = (result.returncode == 0)
        except Exception as e:
            print(f"[Worker {current_process().pid}] Error executing: {e}")
            success = False
        job.attempts += 1

        jobs_data = self.storage.load_jobs()
        # Find and update the job in the list
        for jd in jobs_data:
            if jd["id"] == job.id:
                if success:
                    job.update_state("completed")
                else:
                    if job.attempts < job.max_retries:
                        job.update_state("failed")
                        sleep_backoff(config.get("backoff_base", 2), job.attempts)
                        job.update_state("pending")
                    else:
                        job.update_state("dead")
                        self.storage.save_jobs([j for j in jobs_data if j["id"] != job.id])
                        self.dlq.add_job(job.to_dict())
                        print(f"[Worker {current_process().pid}] Job moved to DLQ: {job.id}")
                        return
                jd.update(job.to_dict())
                break
        self.storage.save_jobs(jobs_data)

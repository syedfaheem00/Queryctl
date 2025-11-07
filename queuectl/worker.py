import subprocess
from datetime import datetime

def worker_process(job, config):
    job.state = "processing"
    job.updated_at = datetime.utcnow().isoformat()
    try:
        result = subprocess.run(job.command, shell=True)
        if result.returncode == 0:
            job.state = "completed"
        else:
            job.attempts += 1
            job.state = "failed"
    except Exception:
        job.attempts += 1
        job.state = "failed"
    job.updated_at = datetime.utcnow().isoformat()
    return job
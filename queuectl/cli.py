import argparse
import sys
import json
from queuectl.jobs import Job
from queuectl.storage import JobStorage
from queuectl.worker import WorkerPool
from queuectl.config import Config
from queuectl.dlq import DLQManager

def main():
    parser = argparse.ArgumentParser(description="QueueCTL - Job Queue CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    enqueue_parser = subparsers.add_parser("enqueue", help="Add a new job to the queue")
    enqueue_parser.add_argument("job_json", help="JSON string of the job")

    worker_parser = subparsers.add_parser("worker", help="Worker management")
    worker_parser.add_argument("action", choices=["start", "stop"], help="start or stop workers")
    worker_parser.add_argument("--count", type=int, default=None, help="Number of workers to start")

    subparsers.add_parser("status", help="Show status summary")

    list_parser = subparsers.add_parser("list", help="List jobs by state")
    list_parser.add_argument("--state", choices=["pending", "processing", "completed", "failed", "dead"], help="Job state")

    dlq_parser = subparsers.add_parser("dlq", help="Dead Letter Queue")
    dlq_parser.add_argument("action", choices=["list", "retry"], help="List or retry DLQ jobs")
    dlq_parser.add_argument("job_id", nargs="?", help="Retry a specific DLQ job")

    config_parser = subparsers.add_parser("config", help="Configure system settings")
    config_parser.add_argument("action", choices=["set"], help="Set configuration value")
    config_parser.add_argument("key", help="Configuration key, e.g., max-retries")
    config_parser.add_argument("value", help="Value to set")

    args = parser.parse_args()
    storage = JobStorage()
    config = Config()
    dlq_mgr = DLQManager(storage)

    # For demonstration: basic worker lifecycle management
    global_pool = {"workers": None}

    if args.command == "enqueue":
        job_data = json.loads(args.job_json)
        job = Job.from_dict(job_data)
        jobs = storage.load_jobs()
        jobs.append(job.to_dict())
        storage.save_jobs(jobs)
        print(f"Job enqueued with ID: {job.id}")

    elif args.command == "worker":
        worker_count = args.count or config.get("worker_count", 1)
        pool = WorkerPool(worker_count, config.data, storage)
        if args.action == "start":
            pool.start()
            print(f"{worker_count} worker(s) running in background.")
        elif args.action == "stop":
            pool.stop()
            print("Workers stopped.")

    elif args.command == "status":
        jobs = storage.load_jobs()
        summary = {}
        for j in jobs:
            summary[j["state"]] = summary.get(j["state"], 0) + 1
        workers_active = "N/A"
        print(f"Job states: {summary}")
        print(f"Active workers: {workers_active}")

    elif args.command == "list":
        jobs = storage.load_jobs()
        if args.state:
            jobs = [j for j in jobs if j["state"] == args.state]
        for job in jobs:
            print(json.dumps(job, indent=2))

    elif args.command == "dlq":
        if args.action == "list":
            for job in dlq_mgr.list_dlq():
                print(json.dumps(job, indent=2))
        elif args.action == "retry" and args.job_id:
            success = dlq_mgr.retry_job(args.job_id)
            print("DLQ job requeued." if success else "DLQ job not found.")

    elif args.command == "config":
        if args.action == "set" and args.key and args.value:
            config.set(args.key, args.value)
            print(f"Config set: {args.key} = {args.value}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

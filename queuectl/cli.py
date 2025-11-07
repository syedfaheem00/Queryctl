import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="QueueCTL - Job Queue CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    enqueue_parser = subparsers.add_parser("enqueue", help="Add a new job to the queue")
    enqueue_parser.add_argument("job_json", help="JSON string of the job")

    worker_parser = subparsers.add_parser("worker", help="Worker management")
    worker_parser.add_argument("action", choices=["start", "stop"], help="start or stop workers")
    worker_parser.add_argument("--count", type=int, default=1, help="Number of workers to start")

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
    # TODO: Connect to functionality in other modules

if __name__ == "__main__":
    main()
import subprocess
import json

def run(cmd):
    print(f">>> {cmd}")
    result = subprocess.run(cmd, shell=True)
    print(result)

def main():
    # Enqueue some jobs: one that succeeds, one that fails
    job_good = json.dumps({"command": "echo Hello", "max_retries": 2})
    job_bad = json.dumps({"command": "some_invalid_command", "max_retries": 2})

    run(f"python queuectl/cli.py enqueue '{job_good}'")
    run(f"python queuectl/cli.py enqueue '{job_bad}'")

    # List pending jobs
    run("python queuectl/cli.py list --state pending")

    # Start workers (default one)
    run("python queuectl/cli.py worker start")

    # Sleep to let jobs process
    import time; time.sleep(8)

    # Status
    run("python queuectl/cli.py status")

    # DLQ List
    run("python queuectl/cli.py dlq list")

    # Retry DLQ job (demonstration: requires you to provide actual ID from DLQ list)
    # run("python queuectl/cli.py dlq retry <job-id>")

if __name__ == "__main__":
    main()

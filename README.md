# QueueCTL

## Overview

QueueCTL is a CLI-based background job queue system designed for backend job handling. It includes worker pools, retry/backoff logic, and a dead letter queue (DLQ).

## Features

- CLI: enqueue jobs, worker management, status, DLQ, config
- Persistent job storage (JSON files)
- Retry with exponential backoff
- Multiple worker support

## Setup Instructions

1. Clone Repo  
    ```
    git clone https://github.com/syedfaheem00/Queryctl.git
    cd Queryctl
    ```

2. Install Requirements  
    ```
    pip install -r requirements.txt
    ```

3. Run CLI Help  
    ```
    python queuectl/cli.py --help
    ```

## Usage Examples

- Enqueue job:  
  `python queuectl/cli.py enqueue '{"command": "echo Hello"}'`
- Start workers:  
  `python queuectl/cli.py worker start --count 3`
- Stop workers:  
  `python queuectl/cli.py worker stop`
- Show status:  
  `python queuectl/cli.py status`
- List jobs by state:  
  `python queuectl/cli.py list --state pending`
- DLQ jobs:  
  `python queuectl/cli.py dlq list`  
  `python queuectl/cli.py dlq retry <job-id>`
- Configure:  
  `python queuectl/cli.py config set max-retries 3`

## Architecture Overview

- Job model: managed as JSON objects
- Worker pool logic: parallel job processing
- Persistent storage: jobs and DLQ jobs stored in JSON files
- Status and config managed via CLI

## Assumptions & Trade-offs

- JSON file storage used for simplicity
- Locks and concurrency are handled in-memory
- CLI-only interface

## Testing

Run example flows as in Usage above.
Or add custom test scripts in `tests/`.

## Demo

[Upload demo and provide link here]

## License

MIT

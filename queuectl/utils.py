import time

def compute_exponential_backoff(base, attempts):
    return base ** attempts

def sleep_backoff(base, attempts):
    delay = compute_exponential_backoff(base, attempts)
    print(f"[Backoff] Sleeping for {delay} seconds before retry...")
    time.sleep(delay)

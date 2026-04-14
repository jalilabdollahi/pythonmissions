# Mission 114 - Metrics Push Gateway
# Fix the 2 bugs in this script.

def sanitize_job_name(name):
    return name.replace("-", "_")  # BUG 1: should also replace spaces with _

def push_metrics(session, gateway_url, job_name, metrics_text):
    """Push metrics to Prometheus Pushgateway."""
    job = sanitize_job_name(job_name)
    url = f"{gateway_url}/metrics/{job}"  # BUG 2: should be /metrics/job/{job}
    resp = session.post(url, data=metrics_text,
                        headers={"Content-Type": "text/plain"})
    resp.raise_for_status()
    return resp.status_code

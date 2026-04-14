# Mission 114 - Metrics Push Gateway
# Fixed solution

def sanitize_job_name(name):
    return name.replace("-", "_").replace(" ", "_")

def push_metrics(session, gateway_url, job_name, metrics_text):
    job = sanitize_job_name(job_name)
    url = f"{gateway_url}/metrics/job/{job}"
    resp = session.post(url, data=metrics_text,
                        headers={"Content-Type": "text/plain"})
    resp.raise_for_status()
    return resp.status_code

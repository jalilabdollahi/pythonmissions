# Mission 032 - CSV Report Writer
# Fix the 2 bugs in this script.
import csv
import io

def write_report(metrics):
    """Write metrics list of dicts to CSV string."""
    output = io.StringIO()
    fieldnames = ["service", "requests", "errors", "latency_ms"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writerows(metrics)  # BUG 1: writeheader() must be called first
    return output.getvalue()

def format_metric(service, req, err, lat):
    return {
        "service": service,
        "requests": req,
        "errors": err,
        "latency_ms": f"{lat:.1f}",
    }

# Mission 017 - Log Filter Comprehension
# Fixed solution

def filter_errors(lines):
    return [line for line in lines if "ERROR" in line]

def extract_ips(lines):
    return [line.split()[0] for line in lines if line.strip()]

def summarize(lines):
    errors = filter_errors(lines)
    ips = extract_ips(errors)
    return {"error_count": len(errors), "unique_ips": list(set(ips))}

# Mission 086 - Ansible Inventory Parser
# Fixed solution

def parse_inventory(content):
    groups = {}
    current_group = "ungrouped"
    groups[current_group] = []

    for line in content.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_group = line[1:-1]
            if current_group not in groups:
                groups[current_group] = []
        else:
            parts = line.split()
            hostname = parts[0]
            vars_ = {}
            for part in parts[1:]:
                if "=" in part:
                    k, v = part.split("=", 1)
                    vars_[k] = v
            groups[current_group].append({"host": hostname, "vars": vars_})

    return groups

def get_hosts_in_group(inventory, group):
    return [h["host"] for h in inventory.get(group, [])]

def get_host_var(inventory, group, host, var):
    for h in inventory.get(group, []):
        if h["host"] == host:
            return h["vars"].get(var)
    return None

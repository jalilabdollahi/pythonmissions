# Mission 059 - Missing Resources Section
# Reads optional resource settings from parsed Kubernetes-style manifests.


def memory_limit(doc):
    return doc["spec"]["resources"]["limits"]["memory"]


def cpu_request(doc):
    resources = doc.get("spec", {}).get("resources", {})
    return resources.get("requests", {}).get("cpu")


def unlimited(docs):
    names = []
    for doc in docs:
        if memory_limit(doc) is None:
            names.append(doc["name"])
    return names


def summarize(doc):
    mem = memory_limit(doc) or "unlimited"
    cpu = cpu_request(doc) or "unset"
    return "%s mem=%s cpu=%s" % (doc["name"], mem, cpu)


if __name__ == "__main__":
    sample = {"name": "web", "spec": {"resources": {"limits": {"memory": "512Mi"}}}}
    print(summarize(sample))

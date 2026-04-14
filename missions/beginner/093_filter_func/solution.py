# Mission 093 - Solution
def running_containers(containers):
    return list(filter(lambda c: c["status"] != "stopped", containers))

if __name__ == "__main__":
    containers = [
        {"id":"c1","status":"running"},
        {"id":"c2","status":"stopped"},
        {"id":"c3","status":"running"},
    ]
    result = running_containers(containers)
    print(type(result))

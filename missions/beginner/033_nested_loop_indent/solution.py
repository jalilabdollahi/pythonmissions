# Mission 033 - Port Scan Matrix Mixup (solution)
# Probe every port on every host and collect the open ones per host.


def scan_matrix(hosts, ports, is_open):
    results = {}
    for host in hosts:
        open_ports = []
        for port in ports:
            if is_open(host, port):
                open_ports.append(port)
        results[host] = open_ports
    return results


def count_exposed(matrix):
    return sum(len(open_ports) for open_ports in matrix.values())

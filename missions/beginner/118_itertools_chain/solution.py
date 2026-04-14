# Mission 118 - Solution
from itertools import chain

def chain_logs(sources):
    return list(chain(*sources))

if __name__ == "__main__":
    app_logs = ["INFO: started", "ERROR: crash"]
    sys_logs = ["WARN: disk 90%", "INFO: ok"]
    nginx_logs = ["GET /api 200", "POST /login 401"]
    print(chain_logs([app_logs, sys_logs, nginx_logs]))

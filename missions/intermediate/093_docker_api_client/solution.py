# Mission 093 - Docker API Client
# Fixed solution

class DockerClient:
    def __init__(self, session, base_url="http://localhost:2375"):
        self.session = session
        self.base_url = base_url.rstrip("/")

    def list_containers(self, all=False):
        params = {"all": "1" if all else "0"}
        resp = self.session.get(f"{self.base_url}/containers/json", params=params)
        resp.raise_for_status()
        return resp.json()

    def short_id(self, container_id):
        return container_id[:12]

    def stop_container(self, container_id, timeout=10):
        short = self.short_id(container_id)
        resp = self.session.post(f"{self.base_url}/containers/{container_id}/stop",
                                 params={"t": timeout})
        resp.raise_for_status()
        return short

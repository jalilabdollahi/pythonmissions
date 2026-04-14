# Mission 097 - gRPC Stub Mock
# Fix the 2 bugs in this script.

class DeployResponse:
    def __init__(self, deployment_id, status):
        self.deployment_id = deployment_id
        self.status = status

class DeployServiceClient:
    def __init__(self, stub):
        self.stub = stub

    def deploy(self, service, version):
        try:
            request = {"service": service, "version": version}  # BUG 1: should be proper request object not dict
            response = self.stub.Deploy(request)
            return response.deployment_id
        except Exception as e:
            raise RuntimeError(f"Deploy failed: {e}")

    def get_status(self, deployment_id):
        response = self.stub.GetStatus(deployment_id)  # BUG 2: should pass a request object
        return response.status

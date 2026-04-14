# Mission 097 - gRPC Stub Mock
# Fixed solution

class DeployRequest:
    def __init__(self, service, version):
        self.service = service
        self.version = version

class StatusRequest:
    def __init__(self, deployment_id):
        self.deployment_id = deployment_id

class DeployResponse:
    def __init__(self, deployment_id, status):
        self.deployment_id = deployment_id
        self.status = status

class DeployServiceClient:
    def __init__(self, stub):
        self.stub = stub

    def deploy(self, service, version):
        try:
            request = DeployRequest(service=service, version=version)
            response = self.stub.Deploy(request)
            return response.deployment_id
        except Exception as e:
            raise RuntimeError(f"Deploy failed: {e}")

    def get_status(self, deployment_id):
        request = StatusRequest(deployment_id=deployment_id)
        response = self.stub.GetStatus(request)
        return response.status

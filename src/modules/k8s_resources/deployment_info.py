from ocp_resources.deployment import Deployment
from core.config import Config

class DeploymentInfo:
    def __init__(self, client):
        self.client = client
        self.namespace = Config.get_k8s_namespace()
        self.deploy_name = Config.get_k8s_deploy_name()

    def get_info(self) -> dict:
        deployment = Deployment(name=self.deploy_name, namespace=self.namespace, client=self.client)
        if deployment.exists:
            info = {
                "deployment": self.deploy_name,
                "namespace": self.namespace,
                "replicas": None,
                "containers": []
            }
            instance = deployment.instance
            containers = instance.spec.template.spec.containers
            info["replicas"] = instance.spec.replicas
            for container in containers:
                info["containers"].append({
                    "name": container.name,
                    "resources": {
                        "requests": {
                            "cpu": container.resources.requests.get("cpu", "N/A") if container.resources and container.resources.requests else "N/A",
                            "memory": container.resources.requests.get("memory", "N/A") if container.resources and container.resources.requests else "N/A",
                        },
                        "limits": {
                            "cpu": container.resources.limits.get("cpu", "N/A") if container.resources and container.resources.limits else "N/A",
                            "memory": container.resources.limits.get("memory", "N/A") if container.resources and container.resources.limits else "N/A",
                        }
                    }
                })
        else:
            info = {
                "deployment": self.deploy_name,
                "namespace": self.namespace,
                "error": "Deployment not found"
            }
        return info
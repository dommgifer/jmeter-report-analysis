from kubernetes.client import ApiException
from core.config import Config

class HPAInfo:
    def __init__(self, dyn_client):
        self.dyn_client = dyn_client
        self.namespace = Config.get_k8s_namespace()
        self.hpa_name = Config.get_k8s_deploy_name()

    def get_info(self) -> dict:
        hpa_resource = self.dyn_client.resources.get(
            api_version="autoscaling/v2",
            kind="HorizontalPodAutoscaler"
        )
        try:
            hpa = hpa_resource.get(name=self.hpa_name, namespace=self.namespace)
            return {
                "enabled": True,
                "minReplicas": hpa.spec.minReplicas,
                "maxReplicas": hpa.spec.maxReplicas,
                "metrics": [m.to_dict() for m in hpa.spec.metrics or []]
            }
        except ApiException as e:
            if e.status == 404:
                return {"enabled": False}
            else:
                return {
                    "enabled": False,
                    "error": f"API error: {e.status} {e.reason}"
                }
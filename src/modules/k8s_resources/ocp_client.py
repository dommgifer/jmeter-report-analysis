from kubernetes import client
from kubernetes.dynamic import DynamicClient
from core.config import Config

class OcpClient:
    def __init__(self):
        self.config = client.Configuration()
        self.config.host = Config.get_k8s_api_url()
        self.config.verify_ssl = False  # 忽略 SSL 驗證
        self.config.api_key = {"authorization": f"Bearer {Config.get_k8s_token()}"}
        self.api_client = client.ApiClient(self.config)
        self.dyn_client = DynamicClient(self.api_client)

    def get_dynamic_client(self) -> DynamicClient:
        return self.dyn_client

    def get_api_client(self) -> client.ApiClient:
        return self.api_client

    def get_config(self) -> client.Configuration:
        return self.config
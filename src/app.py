import os
import json
from datetime import datetime

# from dotenv import load_dotenv

from modules.k8s_resources.ocp_client import OcpClient
from modules.k8s_resources.deployment_info import DeploymentInfo
from modules.k8s_resources.hpa_info import HPAInfo
from modules.grafana_screenshot.panel_screenshot import PanelScreenshot
from modules.grafana_screenshot.dashboard_screenshot import DashboardScreenshot
from modules.reports_download.downloader import StatisticsDownloader


def main():
    # 讀取 .env
    # load_dotenv()

    ocp_client = OcpClient()
    dyn_client = ocp_client.get_dynamic_client()
    deployment_info = DeploymentInfo(dyn_client).get_info()
    hpa_info = HPAInfo(dyn_client).get_info()
    # k8s_config = init_config(api_url, token)
    # dyn_client = init_dynamic_client(k8s_config)
 
    # # 查詢 Deployment 與 HPA
    # deployment_info = get_deployment_info(dyn_client, namespace, deploy_name)
    # hpa_info = get_hpa_info(dyn_client, namespace, deploy_name)


    # # 整合結果
    application_info = {
        **deployment_info,
        "hpa": hpa_info
    }

    # 輸出為 JSON
    # print(json.dumps(application_info, indent=2, ensure_ascii=False))

    ps = PanelScreenshot()
    panel_screenshot_info = ps.run()
    ds = DashboardScreenshot()
    dashboard_screenshot_info = ds.run()
    sd = StatisticsDownloader()
    statistics_info = sd.download()
if __name__ == "__main__":
    main()

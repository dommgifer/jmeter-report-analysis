import os
import requests
from core.config import Config

class GrafanaScreenshotBase:
    def __init__(self):
        self.grafana_url = Config.get_grafana_url()
        self.api_key = Config.get_grafana_api_key()
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.dashboard_uid = Config.get_grafana_dashboard_id()
        self.time_from = Config.get_grafana_time_from()
        self.time_to = Config.get_grafana_time_to()
        self.download_dir = Config.get_grafana_download_dir()
        self.width = Config.get_grafana_screenshot_width()
        self.height = Config.get_grafana_screenshot_height()
        self.theme = Config.get_grafana_theme()
        self.tz = Config.get_grafana_tz()
        self.kiosk = Config.get_grafana_kiosk()
        self.timeout = Config.get_grafana_timeout()

    def get_dashboard_json(self):
        resp = requests.get(
            f"{self.grafana_url}/api/dashboards/uid/{self.dashboard_uid}",
            headers=self.headers,
            timeout=int(self.timeout)
        )
        resp.raise_for_status()
        return resp.json()

    def get_slug(self, dashboard_json):
        return dashboard_json["meta"]["slug"]
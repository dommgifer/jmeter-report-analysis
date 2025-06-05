import os
from datetime import datetime
from .base import GrafanaScreenshotBase
from core.config import Config
import requests

class PanelScreenshot(GrafanaScreenshotBase):
    def __init__(self):
        super().__init__()
        self.panel_titles = Config.get_grafana_panel_titles()
        # dashboard 預設尺寸可覆寫
        self.width = "1920"
        self.height ="1000"
        
    def find_panel_ids(self, dashboard_json):
        panel_ids = {}
        for panel in dashboard_json["dashboard"].get("panels", []):
            if panel["title"] in self.panel_titles:
                panel_ids[panel["title"]] = panel["id"]
        return panel_ids

    def fetch_panel_screenshot(self, slug, panel_id, params, save_path):
        resp = requests.get(
            f"{self.grafana_url}/render/d-solo/{self.dashboard_uid}/{slug}",
            headers=self.headers,
            params={**params, "panelId": panel_id},
            timeout=int(self.timeout),
            stream=True
        )
        if resp.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)
            return True, None
        else:
            return False, f"HTTP {resp.status_code}: {resp.text}"

    def run(self):
        os.makedirs(os.path.join(self.download_dir, "panels"), exist_ok=True)
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        dashboard_json = self.get_dashboard_json()
        slug = self.get_slug(dashboard_json)

        panel_ids = self.find_panel_ids(dashboard_json)
        screenshots = {}
        errors = []

        for title in self.panel_titles:
            panel_id = panel_ids.get(title)
            if not panel_id:
                screenshots[title] = None
                errors.append(f"Panel with title '{title}' not found in dashboard")
                continue

            params = {
                "from": self.time_from,
                "to": self.time_to,
                "theme": self.theme,
                "width": self.width,
                "height": self.height
            }
            if self.tz:
                params["tz"] = self.tz
            if self.kiosk:
                params["kiosk"] = self.kiosk

            save_path = os.path.join(self.download_dir, "panels", f"{now_str}_{title}.png")
            ok, err = self.fetch_panel_screenshot(slug, panel_id, params, save_path)
            if ok:
                screenshots[title] = save_path
            else:
                screenshots[title] = None
                errors.append(f"Panel '{title}' screenshot failed: {err}")

        result = {
            "dashboard_uid": self.dashboard_uid,
            "time_range": {"from": self.time_from, "to": self.time_to},
            "type": "panel",
            "screenshots": screenshots,
            "success": all(v is not None for v in screenshots.values()),
            "errors": errors
        }
        return result
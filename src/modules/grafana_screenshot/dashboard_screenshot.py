import os
import requests
from datetime import datetime
from .base import GrafanaScreenshotBase

class DashboardScreenshot(GrafanaScreenshotBase):
    def __init__(self):
        super().__init__()


    def fetch_dashboard_screenshot(self, slug, params, save_path):
        resp = requests.get(
            f"{self.grafana_url}/render/d/{self.dashboard_uid}/{slug}",
            headers=self.headers,
            params=params,
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
        os.makedirs(os.path.join(self.download_dir, "dashboard"), exist_ok=True)
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        dashboard_json = self.get_dashboard_json()
        slug = self.get_slug(dashboard_json)

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

        save_path = os.path.join(self.download_dir, "dashboard", f"{now_str}_dashboard_full.png")
        ok, err = self.fetch_dashboard_screenshot(slug, params, save_path)

        result = {
            "dashboard_uid": self.dashboard_uid,
            "time_range": {"from": self.time_from, "to": self.time_to},
            "type": "dashboard",
            "screenshot_path": save_path if ok else None,
            "success": ok,
            "errors": [] if ok else [f"Dashboard screenshot failed: {err}"]
        }
        return result
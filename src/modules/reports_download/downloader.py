import os
import time
import json
import requests
from pathlib import Path
from datetime import datetime
from core.config import Config

class StatisticsDownloader:
    def __init__(self, retries: int = 3, backoff: int = 2, timeout: int = 10):
        self.download_url = Config.get_jmeter_stat_url()
        self.download_dir = Config.get_jmeter_download_dir()
        self.retries = retries
        self.backoff = backoff
        self.timeout = timeout

    def download(self) -> dict:
        if not self.download_url:
            return {
                "download_success": False,
                "file_path": None,
                "file_size_bytes": 0,
                "error": "JMETER_STAT_URL is not set"
            }

        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}_statistics.json"
        file_path = os.path.join(self.download_dir, file_name)

        last_error = None

        for attempt in range(1, self.retries + 1):
            try:
                response = requests.get(self.download_url, timeout=self.timeout)
                if response.status_code != 200:
                    last_error = f"HTTP {response.status_code}"
                    break

                try:
                    json_content = response.json()  # Validate JSON
                except json.JSONDecodeError:
                    last_error = "Downloaded file is not valid JSON"
                    break

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(json_content, f, ensure_ascii=False, indent=2)

                file_size = os.path.getsize(file_path)
                return {
                    "download_success": True,
                    "file_path": file_path,
                    "file_size_bytes": file_size,
                    "error": None
                }

            except requests.exceptions.RequestException as e:
                last_error = str(e)
                if attempt < self.retries:
                    time.sleep(self.backoff * attempt)
                else:
                    break

        if os.path.exists(file_path):
            os.remove(file_path)

        return {
            "download_success": False,
            "file_path": None,
            "file_size_bytes": 0,
            "error": f"Download failed after {self.retries} attempts: {last_error}"
        }
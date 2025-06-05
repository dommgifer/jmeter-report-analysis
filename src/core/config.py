import os
import json
import time
from pathlib import Path
from typing import Optional


class ConfigError(Exception):
    """自訂例外：環境變數未設定時拋出"""
    pass


class Config:
    """
    統一讀取並驗證各種環境變數的工具類別。
    - 如果 required=True 且沒有取得值，會 raise ConfigError。
    - 如果有預設值就帶 default；若沒有 default 且 required=False，回傳 None。
    """

    @staticmethod
    def _get_env(name: str,
                 default: Optional[str] = None,
                 required: bool = False) -> Optional[str]:
        value = os.getenv(name, default)
        if required and (value is None or value.strip() == ""):
            raise ConfigError(f"Environment variable `{name}` is required but not set.")
        return value

    # ────────────────────────────────────────────────────────────────────────────
    # JMeter 相關
    # ────────────────────────────────────────────────────────────────────────────

    @staticmethod
    def get_jmeter_stat_url() -> str:
        """取得 JMETER_STAT_URL，若不存在則拋錯"""
        return Config._get_env("JMETER_STAT_URL", required=True)

    @staticmethod
    def get_jmeter_download_dir() -> Path:
        """
        取得 JMETER_DOWNLOAD_DIR（若沒設定則用 ./reports/jmeter），
        並確保該目錄已存在
        """
        raw = Config._get_env("JMETER_DOWNLOAD_DIR", default="./reports/jmeter")
        path = Path(raw)
        path.mkdir(parents=True, exist_ok=True)
        return path

    # ────────────────────────────────────────────────────────────────────────────
    # K8s 相關
    # ────────────────────────────────────────────────────────────────────────────

    @staticmethod
    def get_k8s_api_url() -> str:
        """取得 K8S_API_URL，若不存在則拋錯"""
        return Config._get_env("K8S_API_URL", required=True)

    @staticmethod
    def get_k8s_token() -> str:
        """取得 K8S_TOKEN，若不存在則拋錯"""
        return Config._get_env("K8S_TOKEN", required=True)

    @staticmethod
    def get_k8s_namespace() -> str:
        """取得 K8S_NAMESPACE，若不存在則拋錯"""
        return Config._get_env("K8S_NAMESPACE", required=True)

    @staticmethod
    def get_k8s_deploy_name() -> str:
        """取得 K8S_DEPLOY_NAME，若不存在則拋錯"""
        return Config._get_env("K8S_DEPLOY_NAME", required=True)

    # ────────────────────────────────────────────────────────────────────────────
    # Grafana 相關
    # ────────────────────────────────────────────────────────────────────────────

    @staticmethod
    def get_grafana_url() -> str:
        return Config._get_env("GRAFANA_URL", required=True)

    @staticmethod
    def get_grafana_api_key() -> str:
        return Config._get_env("GRAFANA_API_KEY", required=True)

    @staticmethod
    def get_grafana_dashboard_id() -> str:
        return Config._get_env("GRAFANA_DASHBOARD_ID", required=True)

    @staticmethod
    def get_grafana_panel_titles() -> list:
        val = Config._get_env("GRAFANA_PANEL_TITLES", default="")
        if not val.strip():
            return []
        # 以逗號切割並去除每個項目前後空白
        return [v.strip() for v in val.split(",") if v.strip()]

    @staticmethod
    def get_grafana_time_from() -> str:
        return Config._get_env("GRAFANA_TIME_FROM", default="now-30m")

    @staticmethod
    def get_grafana_time_to() -> str:
        return Config._get_env("GRAFANA_TIME_TO", default="now")

    @staticmethod
    def get_grafana_download_dir() -> str:
        return Config._get_env("GRAFANA_DOWNLOAD_DIR", default="./screenshots")

    @staticmethod
    def get_grafana_screenshot_width() -> int:
        return int(Config._get_env("GRAFANA_SCREENSHOT_WIDTH", default="1600"))

    @staticmethod
    def get_grafana_screenshot_height() -> int:
        return int(Config._get_env("GRAFANA_SCREENSHOT_HEIGHT", default="1200"))

    @staticmethod
    def get_grafana_theme() -> str:
        return Config._get_env("GRAFANA_THEME", default="dark")

    @staticmethod
    def get_grafana_tz() -> str:
        return Config._get_env("GRAFANA_TZ", default="Asia/Taipei")

    @staticmethod
    def get_grafana_timeout() -> int:
        return int(Config._get_env("GRAFANA_TIMEOUT", default="60"))

    @staticmethod
    def get_grafana_kiosk() -> str:
        return Config._get_env("GRAFANA_KIOSK", default="true")
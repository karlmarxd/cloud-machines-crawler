import json
import os
from datetime import datetime
from pprint import pprint

import requests
from requests import Response

from machinescrawlers.linode import LinodeMachinesCrawler
from machinescrawlers.vultr import VultrMachinesCrawler

from .settings import FILES_DIR


class MachinesCrawler:
    _platforms: dict = {
        "vultr": VultrMachinesCrawler,
        "linode": LinodeMachinesCrawler,
    }
    machines: list[dict[str, str]] = []
    page_body: str = ""

    def __init__(self, platform: str):
        try:
            self.page_url = self._platforms[platform].page_url
        except KeyError:
            raise KeyError(f"Unavailable platform `{platform}`!")
        self.platform = platform
        self.extract_content()

    def extract_page_body(self) -> str:
        _request: Response = requests.get(
            self.page_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64; rv:98.0) "
                    "Gecko/20100101 Firefox/98.0"
                ),
            },
        )
        return _request.text

    def print(self) -> None:
        pprint(self.machines)

    def save_csv(self) -> None:
        _csv_filename = (
            self.platform + "_machines.csv"
            if self.platform is not None
            else "machines.csv"
        )
        _csv_body = (
            "CPU / VCPU;"
            "MEMORY;"
            "STORAGE / SSD DISK;"
            "BANDWIDTH / TRANSFER;"
            "PRICE [ $/mo ]"
            "\n"
        )

        for machine in self.machines:
            _csv_body += (
                f"{machine['CPU / VCPU']};"
                f"{machine['MEMORY']};"
                f"{machine['STORAGE / SSD DISK']};"
                f"{machine['BANDWIDTH / TRANSFER']};"
                f"{machine['PRICE [ $/mo ]']}"
                "\n"
            )
        self._save_file(_csv_filename, _csv_body)
        print(f"file {_csv_filename} saved!")

    def save_json(self) -> None:
        _body = {
            "utc_updated_at": self.updated_at,
            "machines": self.machines,
        }
        _json_filename = (
            self.platform + "_machines.json"
            if self.platform is not None
            else "machines.csv"
        )
        self._save_file(_json_filename, json.dumps(_body, indent=4))
        print(f"file {_json_filename} saved!")

    def _save_file(self, filename: str, data: str) -> None:
        file = open(os.path.join(FILES_DIR, filename), "w")
        file.write(data)

    def extract_content(self) -> None:
        self.page_body = self.extract_page_body()
        self.updated_at = datetime.utcnow().isoformat()
        self.machines = self._platforms[self.platform]().get_machines(self.page_body)

import re
import requests
import chompjs

from parsel import Selector


class DigitalOceanMachinesCrawler:
    platform = "digitalocean"
    page_url = "https://www.digitalocean.com/pricing"
    _base_url = "https://www.digitalocean.com"

    def get_machines(self, page: str) -> list[dict[str, str]]:
        machines: list[dict[str, str]] = []
        html_selector = Selector(page)
        pricing_script_path = html_selector.xpath(
            "//head//script[contains(@src, 'pricing')]/@src"
        ).get()
        pricing_script_req = requests.get(f"{self._base_url}/{pricing_script_path}")
        prices_pattern = re.compile(r"var\s+Wt=(\s*{.*?\})\S*}")
        prices_script = prices_pattern.search(pricing_script_req.text).group()
        pricing_obj = chompjs.parse_js_object(prices_script)

        products_prices = pricing_obj["priceData"]["product_prices"]
        prices = {}
        for price in products_prices:
            if price.get("droplet"):
                prices[
                    int(price["droplet"]["size_id"].strip())
                ] = f'${price["droplet"]["item_price"]["usd_rate_per_month"]}'
        regular_machines_pattern = re.compile(r"regular:\s*(\[.*?\])\s*\s*")
        regular_machines_code = (
            regular_machines_pattern.search(pricing_script_req.text)
            .group()
            .replace("regular:[", "var regular=[")
        )
        remove_vt_pattern = re.compile(r".concat\(Vt\(\s*.*?\)\)\s*\s*")
        for match in remove_vt_pattern.findall(regular_machines_code):
            size_id = int(match.split(",")[1].replace('"', "").strip())
            usd_rate_type = match.split(",")[2].replace('"', "")
            if usd_rate_type == "usd_rate_per_month":
                regular_machines_code = regular_machines_code.replace(
                    f'""{match}', f'"{prices[size_id]}"'
                )
            else:
                regular_machines_code = regular_machines_code.replace(match, "")
        regular_machines_list = chompjs.parse_js_object(regular_machines_code)
        for regular_machine in regular_machines_list:
            machine = {
                "CPU / VCPU": regular_machine["cpuType"],
                "MEMORY": regular_machine["cpuAmount"],
                "STORAGE / SSD DISK": regular_machine["ssdAmount"],
                "BANDWIDTH / TRANSFER": regular_machine["transferAmount"],
                "PRICE [ $/mo ]": regular_machine["priceMo"],
            }
            if machine not in machines:
                machines.append(machine)
        return machines

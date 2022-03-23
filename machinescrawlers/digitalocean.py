# from parsel import Selector


class DigitalOceanMachinesCrawler:
    platform = "digitalocean"
    page_url = "https://www.digitalocean.com/pricing"

    def get_machines(self) -> list[dict[str, str]]:
        machines: list[dict[str, str]] = []
        cloud_compute_machine_rows = []
        for machine in cloud_compute_machine_rows:
            machine = {
                "CPU / VCPU": "",
                "MEMORY": "",
                "STORAGE / SSD DISK": "",
                "BANDWIDTH / TRANSFER": "",
                "PRICE [ $/mo ]": "",
            }
            if machine not in machines:
                machines.append(machine)
        return machines

from parsel import Selector


class LinodeMachinesCatcher:
    platform = "linode"
    page_url = "https://www.linode.com/pricing/"

    def get_machines(self, page: str) -> list[dict[str, str]]:
        machines: list[dict[str, str]] = []
        html_selector = Selector(page)
        dedicated_cpu_plans = html_selector.css("div#compute-dedicated table tbody tr")
        shared_cpu_plans = html_selector.css("div#compute table tbody tr")
        for machine in dedicated_cpu_plans + shared_cpu_plans:
            machine = {
                "CPU / VCPU": machine.css(".col--cpus::text").get(),
                "MEMORY": machine.css(".col--ram::text").get(),
                "STORAGE / SSD DISK": machine.css(".col--ssd-storage::text").get(),
                "BANDWIDTH / TRANSFER": machine.css(".col--transfer::text").get(),
                "PRICE [ $/mo ]": machine.css(".col--monthly::text")
                .get()
                .replace(",", ""),
            }
            if machine not in machines:
                machines.append(machine)
        return machines

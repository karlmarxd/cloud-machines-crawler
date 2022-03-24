from parsel import Selector


class VultrMachinesCatcher:
    platform = "vultr"
    page_url = "https://www.vultr.com/pricing/#cloud-compute"

    def get_machines(self, page: str) -> list[dict[str, str]]:
        machines: list[dict[str, str]] = []
        html_selector = Selector(page)
        machine_row_csspath = (
            "#cloud-compute.section "
            "div.pricing__subsection "
            "div.pt.pt--md-boxes.is-animated "
            "div.pt__body.js-body "
            "div.pt__row "
            "div.pt__row-content"
        )
        cloud_compute_machine_rows = html_selector.css(machine_row_csspath)
        for machine in cloud_compute_machine_rows:
            machine_cells = machine.css(".pt__cell")
            machine = {
                "CPU / VCPU": self._format_machine_cell(machine_cells[0]),
                "MEMORY": self._format_machine_cell(machine_cells[1]),
                "STORAGE / SSD DISK": self._format_machine_cell(machine_cells[3]),
                "BANDWIDTH / TRANSFER": self._format_machine_cell(machine_cells[2]),
                "PRICE [ $/mo ]": self._format_machine_cell(machine_cells[4]),
            }
            if machine not in machines:
                machines.append(machine)
        return machines

    def _format_machine_cell(self, cell) -> str:
        return (
            f"{cell.css('strong::text').get()} {cell.css('div::text').get()}".replace(
                "\u00a0", ""
            )
        )

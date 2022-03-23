from machinescrawlers import MachinesCrawler

vultr_machines = MachinesCrawler("vultr")
linode_machines = MachinesCrawler("linode")


def step_one():
    vultr_machines.print()


def step_two():
    step_one()
    vultr_machines.save_json()


def step_three():
    step_two()
    vultr_machines.save_csv()


def step_four():
    linode_machines.print()
    linode_machines.save_csv()
    linode_machines.save_json()


def main():
    step_three()
    step_four()


if __name__ == "__main__":
    main()

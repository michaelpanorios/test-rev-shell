from nautobot.apps.jobs import Job, register_jobs
from nautobot.dcim.models import ConsolePort, Device, PowerPort
from nautobot.extras.models import Status


class DeviceConnectionsReport(Job):
    description = "Validate the minimum physical connections for each device"

    def test_console_connection(self):
        STATUS_ACTIVE = Status.objects.get(name='Active')

        # Check that every console port for every active device has a connection defined.
        for console_port in ConsolePort.objects.select_related('device').filter(device__status=STATUS_ACTIVE):
            if console_port.connected_endpoint is None:
                self.logger.error(
                    "No console connection defined for %s",
                    console_port.name,
                    extra={"object": console_port.device},
                )
            else:
                self.logger.info(
                    "Console port %s has a connection defined",
                    console_port.name,
                    extra={"object": console_port.device},
                )

    def test_power_connections(self):
        STATUS_ACTIVE = Status.objects.get(name='Active')

        # Check that every active device has at least two connected power supplies.
        for device in Device.objects.filter(status=STATUS_ACTIVE):
            connected_ports = 0
            for power_port in PowerPort.objects.filter(device=device):
                if power_port.connected_endpoint is not None:
                    connected_ports += 1
            if connected_ports < 2:
                self.logger.error(
                    "%s connected power supplies found (2 needed)",
                    connected_ports,
                    extra={"object": device},
                )
            else:
                self.logger.info("At least two connected power supplies found", extra={"object": device})

    def run(self):
        self.test_console_connection()
        self.test_power_connections()


register_jobs(DeviceConnectionsReport)

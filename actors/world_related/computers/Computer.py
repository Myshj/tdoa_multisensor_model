from actor_system.broadcasters import Broadcaster
from actor_system.broadcasters.messages import Broadcast
from actor_system.messages import Message
from actors.world_related import AbstractWorldRelatedActor
from actors.worlds import Base as World
from auxillary import Position
from .messages.actions.hardware_actions import *
from .messages.actions.software_actions import *
from .messages.events.hardware_events import *
from .messages.events.software_events import *
from .software import AbstractSoftware


class Computer(AbstractWorldRelatedActor):
    def __init__(
            self,
            position: Position,
            world: World,
    ):
        super().__init__(position, world)
        self.connected_hardware = set()
        self.installed_software = set()
        self.hardware_events_broadcaster = Broadcaster()
        self.software_events_broadcaster = Broadcaster()

    def on_message(self, message: Message):
        if isinstance(message, AbstractHardwareAction):
            self.on_hardware_action(message)
        elif isinstance(message, AbstractSoftwareAction):
            self.on_software_action(message)

    def on_hardware_action(self, message: AbstractHardwareAction):
        if isinstance(message, ConnectHardware):
            self.on_connect_hardware(message.hardware)
        elif isinstance(message, DisconnectHardware):
            self.on_disconnect_hardware(message.hardware)

    def on_connect_hardware(self, hardware):
        self._connect_hardware(hardware)
        self._notify_that_hardware_connected(hardware)

    def on_disconnect_hardware(self, hardware):
        self._disconnect_hardware(hardware)
        self._notify_that_hardware_disconnected(hardware)

    def on_software_action(self, message: AbstractSoftwareAction):
        if isinstance(message, InstallSoftware):
            self.on_install_software(message.software)

    def on_install_software(self, software: AbstractSoftware):
        self._install_software(software)
        self._notify_that_software_installed(software)

    def on_uninstall_software(self, software: AbstractSoftware):
        self._uninstall_software(software)
        self._notify_that_software_uninstalled(software)

    def _install_software(self, software: AbstractSoftware):
        self.installed_software.add(software)

    def _uninstall_software(self, software: AbstractSoftware):
        self.installed_software.remove(software)

    def _notify_that_software_installed(self, software: AbstractSoftware):
        self.software_events_broadcaster.tell(
            Broadcast(
                sender=self,
                message=SoftwareInstalled(
                    sender=self,
                    software=software
                )
            )
        )

    def _notify_that_software_uninstalled(self, software: AbstractSoftware):
        self.software_events_broadcaster.tell(
            Broadcast(
                sender=self,
                message=SoftwareUninstalled(
                    sender=self,
                    software=software
                )
            )
        )

    def _connect_hardware(self, hardware):
        self.connected_hardware.add(hardware)

    def _disconnect_hardware(self, hardware):
        self.connected_hardware.remove(hardware)

    def _notify_that_hardware_connected(self, hardware):
        self.hardware_events_broadcaster.tell(
            Broadcast(
                sender=self,
                message=HardwareConnected(
                    sender=self,
                    hardware=hardware
                )
            )
        )

    def _notify_that_hardware_disconnected(self, hardware):
        self.hardware_events_broadcaster.tell(
            Broadcast(
                sender=self,
                message=HardwareDisconnected(
                    sender=self,
                    hardware=hardware
                )
            )
        )

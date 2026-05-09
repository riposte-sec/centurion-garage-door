from __future__ import annotations

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import CenturionCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: CenturionCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        CenturionLampSwitch(coordinator),
        CenturionVacationSwitch(coordinator),
    ])


class _CenturionSwitchBase(CoordinatorEntity[CenturionCoordinator], SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: CenturionCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.host)},
            name="Centurion Garage Door",
            manufacturer="Centurion",
            model="Garage Door",
        )


class CenturionLampSwitch(_CenturionSwitchBase):
    _attr_name = "Lamp"
    _attr_device_class = SwitchDeviceClass.OUTLET

    def __init__(self, coordinator: CenturionCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.host}_lamp"

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.get("lamp") == "on"

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_send_command("lamp", "on")

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_send_command("lamp", "off")


class CenturionVacationSwitch(_CenturionSwitchBase):
    _attr_name = "Vacation Mode"

    def __init__(self, coordinator: CenturionCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.host}_vacation"

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.get("vacation") == "on"

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_send_command("vacation", "on")

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_send_command("vacation", "off")

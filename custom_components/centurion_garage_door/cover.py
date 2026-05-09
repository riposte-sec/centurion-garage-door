from __future__ import annotations

from homeassistant.components.cover import CoverDeviceClass, CoverEntity, CoverEntityFeature
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
    async_add_entities([CenturionDoorCover(coordinator)])


class CenturionDoorCover(CoordinatorEntity[CenturionCoordinator], CoverEntity):
    _attr_device_class = CoverDeviceClass.GARAGE
    _attr_supported_features = (
        CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP
    )
    _attr_name = "Garage Door"
    _attr_has_entity_name = True

    def __init__(self, coordinator: CenturionCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.host}_door"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.host)},
            name="Centurion Garage Door",
            manufacturer="Centurion",
            model="Garage Door",
        )

    @property
    def _door_str(self) -> str:
        return (self.coordinator.data.get("door") or "").lower()

    @property
    def is_closed(self) -> bool | None:
        door = self._door_str
        if "closing" in door or "opening" in door:
            return None
        return door.startswith("closed")

    @property
    def is_closing(self) -> bool:
        return "closing" in self._door_str

    @property
    def is_opening(self) -> bool:
        return "opening" in self._door_str

    @property
    def extra_state_attributes(self) -> dict:
        data = self.coordinator.data
        return {
            "door_status": data.get("door"),
            "cycles": data.get("cycles"),
            "wifi_signal_dbm": data.get("wdBm"),
            "error": data.get("error"),
            "last_event": data.get("dt"),
        }

    async def async_open_cover(self, **kwargs) -> None:
        await self.coordinator.async_send_command("door", "open")

    async def async_close_cover(self, **kwargs) -> None:
        await self.coordinator.async_send_command("door", "close")

    async def async_stop_cover(self, **kwargs) -> None:
        await self.coordinator.async_send_command("door", "stop")

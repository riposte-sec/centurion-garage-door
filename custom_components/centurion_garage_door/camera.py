from __future__ import annotations

import asyncio

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_HOST, DOMAIN

_FRAME_TIMEOUT = 5
_FRAME_MAX_BYTES = 1024 * 1024  # 1 MB guard


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    host = entry.data[CONF_HOST]
    async_add_entities([CenturionCamera(hass, host)])


class CenturionCamera(Camera):
    _attr_has_entity_name = True
    _attr_name = "Camera"
    _attr_is_streaming = True

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        super().__init__()
        self.hass = hass
        self._stream_url = f"http://{host}:88/"
        self._attr_unique_id = f"{host}_camera"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, host)},
            name="Centurion Garage Door",
            manufacturer="Centurion",
            model="Garage Door",
        )

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a single JPEG frame extracted from the MJPEG stream."""
        session = async_get_clientsession(self.hass)
        try:
            async with asyncio.timeout(_FRAME_TIMEOUT):
                async with session.get(self._stream_url) as resp:
                    buf = b""
                    async for chunk in resp.content.iter_chunked(4096):
                        buf += chunk
                        start = buf.find(b"\xff\xd8")
                        if start != -1:
                            end = buf.find(b"\xff\xd9", start + 2)
                            if end != -1:
                                return buf[start : end + 2]
                        if len(buf) > _FRAME_MAX_BYTES:
                            break
        except Exception:
            pass
        return None

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class CenturionCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, host: str, api_key: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.host = host
        self.api_key = api_key
        self._session = async_get_clientsession(hass)

    def _api_url(self, **params: str) -> str:
        qs = "&".join(f"{k}={v}" for k, v in {"key": self.api_key, **params}.items())
        return f"http://{self.host}/api?{qs}"

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            async with self._session.get(
                self._api_url(status="json"), timeout=10
            ) as resp:
                if resp.status == 401:
                    raise UpdateFailed("Invalid API key (401)")
                if resp.status != 200:
                    raise UpdateFailed(f"Unexpected HTTP {resp.status}")
                data = await resp.json(content_type=None)
                if "door" not in data:
                    raise UpdateFailed("Unexpected response format")
                return data
        except UpdateFailed:
            raise
        except Exception as err:
            raise UpdateFailed(f"Cannot connect to device: {err}") from err

    async def async_send_command(self, param: str, value: str) -> None:
        try:
            async with self._session.get(
                self._api_url(**{param: value}), timeout=10
            ) as resp:
                if resp.status != 200:
                    _LOGGER.warning("Command %s=%s returned HTTP %s", param, value, resp.status)
        except Exception as err:
            _LOGGER.error("Error sending command %s=%s: %s", param, value, err)
        await self.async_request_refresh()

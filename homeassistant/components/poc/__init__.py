"""The poc integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
import homeassistant.helpers.device_registry as dr

from .const import DOMAIN

_PLATFORMS: list[Platform] = [Platform.LIGHT]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Create a bare Device so it shows up in UI (0 entities for now)."""
    reg = dr.async_get(hass)

    host = entry.data["host"]
    port = entry.data["port"]
    unique = f"{host}:{port}"

    reg.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, unique)},
        manufacturer="POC",
        model="POC Device",
        name=f"POC {unique}",
        sw_version="0.0",
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)

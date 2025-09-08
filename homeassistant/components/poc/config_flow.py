"""Config flow for the poc integration."""

from __future__ import annotations

import ipaddress
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


SCHEMA = vol.Schema(
    {
        vol.Required("host"): vol.All(str),
        vol.Required("port", default=1234): vol.All(int, vol.Range(min=1, max=65535)),
        vol.Required("code"): vol.All(str, vol.Length(min=1, max=128)),
    }
)


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for poc."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=SCHEMA)

        host = user_input["host"]
        port = user_input["port"]
        unique = f"{host}:{port}"

        await self.async_set_unique_id(unique)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"POC {unique}",
            data={
                "host": host,
                "port": port,
                "code": user_input["code"],
            },
        )

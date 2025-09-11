from __future__ import annotations

from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    AlarmControlPanelEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import CONF_NAME

from .const import (
    DOMAIN,
    DATA_COORDINATOR,
    DATA_DEVICE_ID,
    DATA_CLIENT,
    CONF_PARTITIONS,
    CONF_ID,
)

STATE_MAP = {
    "disarmed": "disarmed",
    "armed_home": "armed_home",
    "armed_away": "armed_away",
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, add: AddEntitiesCallback
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data[DATA_COORDINATOR]
    device_id = data[DATA_DEVICE_ID]
    client = data[DATA_CLIENT]
    parts = entry.data.get(CONF_PARTITIONS, [])
    if not parts:
        return

    entities = [
        IntegraPartitionPanel(
            coordinator=coordinator,
            client=client,
            entry_id=entry.entry_id,
            device_identifier=(DOMAIN, device_id),
            part_id=int(p[CONF_ID]),
            name=str(p[CONF_NAME]),
        )
        for p in parts
    ]
    add(entities)


class IntegraPartitionPanel(CoordinatorEntity, AlarmControlPanelEntity):
    _attr_should_poll = False
    _attr_supported_features = (
        AlarmControlPanelEntityFeature.ARM_HOME
        | AlarmControlPanelEntityFeature.ARM_AWAY
    )

    def __init__(
        self,
        coordinator,
        client,
        entry_id: str,
        device_identifier,
        part_id: int,
        name: str,
    ) -> None:
        super().__init__(coordinator)
        self._client = client
        self._entry_id = entry_id
        self._device_identifier = device_identifier
        self._part_id = part_id
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}-partition-{part_id}"

    @property
    def state(self) -> str | None:
        d = self.coordinator.data or {}
        raw = (d.get("partitions") or {}).get(self._part_id)
        return STATE_MAP.get(raw, "unknown")

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(identifiers={self._device_identifier})

    async def async_alarm_disarm(self, code: str | None = None) -> None:
        await self._client.async_disarm(self._part_id)
        await self.coordinator.async_request_refresh()

    async def async_alarm_arm_home(self, code: str | None = None) -> None:
        await self._client.async_arm(self._part_id, "home")
        await self.coordinator.async_request_refresh()

    async def async_alarm_arm_away(self, code: str | None = None) -> None:
        await self._client.async_arm(self._part_id, "away")
        await self.coordinator.async_request_refresh()

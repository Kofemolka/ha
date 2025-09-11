from __future__ import annotations
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
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
    CONF_ZONES,
    CONF_ID,
    CONF_TYPE,
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, add: AddEntitiesCallback
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data[DATA_COORDINATOR]
    device_id = data[DATA_DEVICE_ID]
    zones = entry.data.get(CONF_ZONES, [])
    if not zones:
        return

    ents = []
    for z in zones:
        zid = int(z[CONF_ID])
        name = str(z[CONF_NAME])
        ztype = str(z.get(CONF_TYPE, "opening")).lower()
        device_class = (
            BinarySensorDeviceClass.MOTION
            if ztype == "motion"
            else BinarySensorDeviceClass.OPENING
        )
        ents.append(
            IntegraZoneBinarySensor(
                coordinator=coordinator,
                entry_id=entry.entry_id,
                device_identifier=(DOMAIN, device_id),
                zone_id=zid,
                name=name,
                device_class=device_class,
                zone_type=ztype,
            )
        )
    add(ents)


class IntegraZoneBinarySensor(CoordinatorEntity, BinarySensorEntity):
    _attr_should_poll = False

    def __init__(
        self,
        coordinator,
        entry_id: str,
        device_identifier,
        zone_id: int,
        name: str,
        device_class: BinarySensorDeviceClass,
        zone_type: str,
    ) -> None:
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._device_identifier = device_identifier
        self._zone_id = zone_id
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}-zone-{zone_id}"
        self._attr_device_class = device_class
        self._zone_type = zone_type

    @property
    def is_on(self) -> bool:
        d = self.coordinator.data or {}
        return bool((d.get("zones") or {}).get(self._zone_id, False))

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(identifiers={self._device_identifier})

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"zone_id": self._zone_id, "zone_type": self._zone_type}

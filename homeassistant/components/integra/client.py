from __future__ import annotations

from typing import Any


class IntegraClient:
    def __init__(self, host: str, port: int, code: str) -> None:
        self._host, self._port, self._code = host, port, code
        self._connected = False

    async def async_connect(self) -> None:
        self._connected = True

    async def async_close(self) -> None:
        self._connected = False

    async def async_get_states(
        self, zones: list[int], partitions: list[int]
    ) -> dict[str, Any]:
        # TODO: replace with real TCP protocol.
        return {
            "zones": {z: False for z in zones},  # False=closed / not triggered
            "partitions": {
                p: "disarmed" for p in partitions
            },  # "disarmed"|"armed_home"|"armed_away"
        }

    async def async_arm(self, partition_id: int, mode: str) -> None:
        # TODO: send arm command
        return

    async def async_disarm(self, partition_id: int) -> None:
        # TODO: send disarm command
        return

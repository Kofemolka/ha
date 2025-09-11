from homeassistant.const import Platform

DOMAIN = "integra"
PLATFORMS: list[Platform] = [Platform.ALARM_CONTROL_PANEL, Platform.BINARY_SENSOR]

CONF_CODE = "code"
CONF_ZONES = "zones"
CONF_PARTITIONS = "partitions"
CONF_ID = "id"
CONF_TYPE = "type"

DATA_CLIENT = "client"
DATA_COORDINATOR = "coordinator"
DATA_DEVICE_ID = "device_id"

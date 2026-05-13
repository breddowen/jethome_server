# ./backend/app/modules/settings/enums.py
from enum import Enum


class ServiceStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    UNKNOWN = "unknown"


class ServiceType(str, Enum):
    VPN = "vpn"
    ADBLOCK = "adblock"
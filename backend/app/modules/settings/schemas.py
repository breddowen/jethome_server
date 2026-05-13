# ./backend/app/modules/settings/schemas.py
from pydantic import BaseModel
from datetime import datetime
from .enums import ServiceStatus, ServiceType


class SettingsBase(BaseModel):
    vpn_enabled: bool
    adblock_enabled: bool


class SettingsResponse(BaseModel):
    uid: str
    vpn_enabled: bool
    vpn_status: ServiceStatus
    adblock_enabled: bool
    adblock_status: ServiceStatus
    wifi_ssid: str | None
    wifi_clients_count: int
    total_traffic_mb: float
    vpn_traffic_mb: float
    updated_at: datetime


class ServiceToggleRequest(BaseModel):
    enabled: bool


class ServiceStatusResponse(BaseModel):
    service: ServiceType
    enabled: bool
    status: ServiceStatus
    message: str | None = None


class ServiceLogResponse(BaseModel):
    uid: str
    service_type: ServiceType
    action: str
    message: str | None
    created_at: datetime


class WiFiInfo(BaseModel):
    ssid: str
    password: str | None
    clients_count: int
    ip_address: str
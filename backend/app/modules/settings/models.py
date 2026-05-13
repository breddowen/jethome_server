# ./backend/app/modules/settings/models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

from .enums import ServiceStatus, ServiceType


class SystemSettings(SQLModel, table=True):
    __tablename__ = "system_settings"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()), unique=True, index=True)
    
    # VPN настройки
    vpn_enabled: bool = Field(default=True)
    vpn_status: ServiceStatus = Field(default=ServiceStatus.ENABLED)
    
    # AdBlock настройки
    adblock_enabled: bool = Field(default=False)
    adblock_status: ServiceStatus = Field(default=ServiceStatus.DISABLED)
    
    # WiFi настройки (для отображения)
    wifi_ssid: Optional[str] = Field(default="MyHotspot")
    wifi_password: Optional[str] = None
    wifi_clients_count: int = Field(default=0)
    
    # Статистика
    total_traffic_mb: float = Field(default=0.0)
    vpn_traffic_mb: float = Field(default=0.0)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ServiceLog(SQLModel, table=True):
    __tablename__ = "service_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()), unique=True, index=True)
    
    service_type: ServiceType
    action: str  # "enabled", "disabled", "error"
    message: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
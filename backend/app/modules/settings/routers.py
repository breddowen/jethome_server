# ./backend/app/modules/settings/routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from ...core.db import get_session
from .models import SystemSettings, ServiceLog
from .schemas import (
    SettingsResponse,
    ServiceToggleRequest,
    ServiceStatusResponse,
    ServiceLogResponse,
    WiFiInfo
)
from .enums import ServiceType, ServiceStatus
from .utils import (
    toggle_vpn,
    toggle_adblock,
    get_service_status,
    get_wifi_info,
    get_traffic_stats
)

router = APIRouter(prefix="/api/v1/settings", tags=["Settings"])


def get_or_create_settings(session: Session) -> SystemSettings:
    """Получить или создать запись настроек"""
    statement = select(SystemSettings)
    settings = session.exec(statement).first()
    
    if not settings:
        settings = SystemSettings()
        session.add(settings)
        session.commit()
        session.refresh(settings)
    
    return settings


def create_log(
    session: Session,
    service_type: ServiceType,
    action: str,
    message: str = None
):
    """Создать запись в логе"""
    log = ServiceLog(
        service_type=service_type,
        action=action,
        message=message
    )
    session.add(log)
    session.commit()


@router.get("/", response_model=SettingsResponse)
def get_settings(session: Session = Depends(get_session)):
    """Получить текущие настройки"""
    settings = get_or_create_settings(session)
    
    # Обновить статусы сервисов
    settings.vpn_status = get_service_status("xray")
    settings.adblock_status = ServiceStatus.DISABLED  # TODO: реальный статус
    
    # Обновить информацию о WiFi
    wifi_info = get_wifi_info()
    settings.wifi_clients_count = wifi_info["clients_count"]
    
    # Обновить статистику трафика
    traffic = get_traffic_stats()
    settings.total_traffic_mb = traffic["total_traffic_mb"]
    settings.vpn_traffic_mb = traffic["vpn_traffic_mb"]
    
    session.add(settings)
    session.commit()
    session.refresh(settings)
    
    return settings


@router.post("/vpn/toggle", response_model=ServiceStatusResponse)
def toggle_vpn_service(
    request: ServiceToggleRequest,
    session: Session = Depends(get_session)
):
    """Включить/выключить VPN"""
    settings = get_or_create_settings(session)
    
    # Выполнить переключение
    success, message = toggle_vpn(request.enabled)
    
    if not success:
        create_log(session, ServiceType.VPN, "error", message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )
    
    # Обновить настройки
    settings.vpn_enabled = request.enabled
    settings.vpn_status = ServiceStatus.ENABLED if request.enabled else ServiceStatus.DISABLED
    session.add(settings)
    session.commit()
    
    # Записать в лог
    action = "enabled" if request.enabled else "disabled"
    create_log(session, ServiceType.VPN, action, message)
    
    return ServiceStatusResponse(
        service=ServiceType.VPN,
        enabled=request.enabled,
        status=settings.vpn_status,
        message=message
    )


@router.post("/adblock/toggle", response_model=ServiceStatusResponse)
def toggle_adblock_service(
    request: ServiceToggleRequest,
    session: Session = Depends(get_session)
):
    """Включить/выключить блокировщик рекламы"""
    settings = get_or_create_settings(session)
    
    # Выполнить переключение
    success, message = toggle_adblock(request.enabled)
    
    if not success:
        create_log(session, ServiceType.ADBLOCK, "error", message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )
    
    # Обновить настройки
    settings.adblock_enabled = request.enabled
    settings.adblock_status = ServiceStatus.ENABLED if request.enabled else ServiceStatus.DISABLED
    session.add(settings)
    session.commit()
    
    # Записать в лог
    action = "enabled" if request.enabled else "disabled"
    create_log(session, ServiceType.ADBLOCK, action, message)
    
    return ServiceStatusResponse(
        service=ServiceType.ADBLOCK,
        enabled=request.enabled,
        status=settings.adblock_status,
        message=message
    )


@router.get("/wifi", response_model=WiFiInfo)
def get_wifi_information():
    """Получить информацию о WiFi"""
    return get_wifi_info()


@router.get("/logs", response_model=List[ServiceLogResponse])
def get_service_logs(
    limit: int = 50,
    session: Session = Depends(get_session)
):
    """Получить логи сервисов"""
    statement = select(ServiceLog).order_by(ServiceLog.created_at.desc()).limit(limit)
    logs = session.exec(statement).all()
    return logs
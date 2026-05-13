# ./backend/app/modules/settings/utils.py
import subprocess
import re
from .enums import ServiceStatus, ServiceType


def run_command(command: str) -> tuple[bool, str]:
    """Выполнить shell команду и вернуть результат"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def get_service_status(service_name: str) -> ServiceStatus:
    """Получить статус systemd сервиса"""
    success, output = run_command(f"systemctl is-active {service_name}")
    if success and "active" in output:
        return ServiceStatus.ENABLED
    return ServiceStatus.DISABLED


def toggle_vpn(enable: bool) -> tuple[bool, str]:
    """Включить/выключить VPN"""
    if enable:
        # Запустить Xray и применить TPROXY правила
        success1, msg1 = run_command("systemctl start xray")
        if not success1:
            return False, f"Failed to start xray: {msg1}"
        
        success2, msg2 = run_command("/usr/local/bin/xray-tproxy.sh")
        if not success2:
            return False, f"Failed to apply TPROXY rules: {msg2}"
        
        return True, "VPN enabled successfully"
    else:
        # Остановить Xray и очистить TPROXY правила
        run_command("systemctl stop xray")
        run_command("iptables -t mangle -F XRAY")
        run_command("iptables -t mangle -X XRAY")
        return True, "VPN disabled successfully"


def toggle_adblock(enable: bool) -> tuple[bool, str]:
    """Включить/выключить блокировщик рекламы"""
    if enable:
        # TODO: Реализовать блокировку рекламы через DNS
        # Например, через dnsmasq или AdGuard Home
        # Пока заглушка
        return True, "AdBlock enabled (stub)"
    else:
        return True, "AdBlock disabled (stub)"


def get_wifi_info() -> dict:
    """Получить информацию о WiFi hotspot"""
    try:
        # SSID
        success, output = run_command("nmcli -t -f 802-11-wireless.ssid connection show MyHotspot")
        ssid = output.strip().split(":")[-1] if success else "Unknown"
        
        # Password
        success, output = run_command("nmcli -t -f 802-11-wireless-security.psk connection show MyHotspot")
        password = output.strip().split(":")[-1] if success else None
        
        # Clients count
        success, output = run_command("ip neigh show dev wlan0 | grep -c REACHABLE")
        clients = int(output.strip()) if success and output.strip().isdigit() else 0
        
        # IP address
        success, output = run_command("ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'")
        ip_address = output.strip() if success else "10.42.0.1"
        
        return {
            "ssid": ssid,
            "password": password,
            "clients_count": clients,
            "ip_address": ip_address
        }
    except Exception as e:
        return {
            "ssid": "Unknown",
            "password": None,
            "clients_count": 0,
            "ip_address": "Unknown"
        }


def get_traffic_stats() -> dict:
    """Получить статистику трафика"""
    try:
        # Получить статистику из iptables
        success, output = run_command("iptables -t mangle -L XRAY -v -n | grep -E 'pkts|bytes'")
        
        # Парсинг вывода (упрощенный вариант)
        # TODO: Реализовать правильный парсинг статистики
        
        return {
            "total_traffic_mb": 0.0,
            "vpn_traffic_mb": 0.0
        }
    except Exception:
        return {
            "total_traffic_mb": 0.0,
            "vpn_traffic_mb": 0.0
        }
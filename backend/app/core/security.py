# ./backend/app/core/security.py
from fastapi import HTTPException, status


def verify_local_network():
    """
    Заглушка для проверки доступа только из локальной сети
    В production можно проверять IP клиента
    """
    # TODO: Добавить проверку IP адреса клиента
    pass
# Деплой на JetHub

## 1. Подготовка JetHub

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo apt install docker-compose -y

# Создание директории проекта
sudo mkdir -p /opt/jethome_server
sudo chown $USER:$USER /opt/jethome_server
```

## 2. Клонирование репозитория

```bash
cd /opt
git clone https://github.com/breddowen/jethome_server.git
cd jethome_server
```

## 3. Запуск

```bash
cd deploy
docker-compose up -d
```

## 4. Проверка

```bash
# Проверка статуса контейнеров
docker-compose ps

# Логи
docker-compose logs -f

# Проверка API
curl http://localhost:8000/health

# Проверка фронтенда
curl http://localhost:3000
```

## 5. GitHub Secrets

Добавьте в Settings → Secrets and variables → Actions:

- `SSH_PRIVATE_KEY` - приватный SSH ключ для доступа к JetHub
- `JETHUB_HOST` - IP адрес JetHub (например, 10.42.0.1)
- `JETHUB_USER` - пользователь SSH (например, root)

## 6. Доступ к панели

После запуска панель доступна по адресу:
- Через WiFi: http://10.42.0.1
- Локально на JetHub: http://localhost

```

---

## 📝 Дополнительные файлы

### .gitignore

```
# ./.gitignore
# Backend
backend/test_database.db
backend/app/.env
backend/__pycache__/
backend/**/__pycache__/
backend/.pytest_cache/
backend/**/*.pyc

# Frontend
frontend/node_modules/
frontend/.nuxt/
frontend/.output/
frontend/dist/
frontend/.env

# Docker
deploy/data/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### README.md основной

```markdown
# ./README.md
# 🚀 JetHub VPN Router Manager

Веб-панель управления JetHub в качестве VPN WiFi роутера с Xray (VLESS + Reality)

## 📋 Возможности

- ✅ Включение/отключение VPN (Xray)
- ✅ Включение/отключение блокировщика рекламы
- ✅ Мониторинг подключенных устройств
- ✅ Просмотр логов событий
- ✅ Информация о WiFi сети
- ✅ Статистика трафика

## 🛠️ Технологии

**Backend:**
- FastAPI
- SQLModel
- SQLite

**Frontend:**
- Nuxt 4
- Pinia
- Tailwind CSS
- Nuxt Icon

**Deployment:**
- Docker
- Docker Compose
- GitHub Actions

## 📦 Установка

См. [DEPLOYMENT.md](./DEPLOYMENT.md)

## 🎨 Скриншоты

TODO: Добавить скриншоты

## 📝 Лицензия

MIT
```

---

## 🎯 Итоговые команды для запуска

### Локальная разработка

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd app
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Production на JetHub

```bash
cd /opt/jethome_server/deploy
docker-compose up -d
```

### GitHub Actions

Просто сделайте:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

GitHub Actions автоматически задеплоит на JetHub!

---

## ✅ Что осталось доработать

1. **Блокировщик рекламы** - реализовать через:
   - AdGuard Home (рекомендуется)
   - Pi-hole
   - Или простой DNS фильтр через dnsmasq

2. **Аутентификация** - добавить логин/пароль для доступа к панели

3. **Реальная статистика трафика** - парсить iptables или использовать vnstat

4. **WebSocket** - для real-time обновления статуса

5. **Мобильная версия** - оптимизировать интерфейс для телефонов

---

Все готово! Хотите, чтобы я добавил что-то еще или доработал какую-то часть?
# 🧪 Тестирование прямо на JetHub (без GitHub Actions)

Да, можно! Запустим всё локально на самом JetHub.

---

## 🚀 Быстрый старт на JetHub

### 1️⃣ Подключитесь к JetHub

```bash
# С вашего рабочего компьютера
ssh root@192.168.137.119
```

---

### 2️⃣ Клонируйте репозиторий на JetHub

```bash
# Установите git если нет
apt update && apt install -y git

# Клонируйте репозиторий
cd /opt
git clone https://github.com/breddowen/jethome_server.git

# Или если уже есть - обновите
cd /opt/jethome_server
git pull origin main
```

---

### 3️⃣ Соберите образы локально на JetHub

```bash
cd /opt/jethome_server

# Сборка Backend
echo "🔨 Building Backend..."
cd backend
docker build -t ghcr.io/breddowen/jethome-backend:latest .

# Сборка Frontend
echo "🔨 Building Frontend..."
cd ../frontend
docker build -t ghcr.io/breddowen/jethome-frontend:latest .

cd ..
```

**Это займет 5-10 минут**

---

### 4️⃣ Запустите контейнеры

```bash
cd /opt/jethome_server/deploy

# Запуск
docker-compose up -d

# Проверка
docker-compose ps
docker-compose logs -f
```

---

### 5️⃣ Проверка работы

```bash
# Health check
curl http://localhost:8000/health
curl http://localhost:3000
curl http://localhost

# В браузере на рабочем компьютере
# Откройте: http://192.168.137.119
```

---

## 📝 Полный скрипт для быстрого деплоя

Создайте файл на JetHub:

```bash
# ./deploy/local-build-deploy.sh
#!/bin/bash

set -e

echo "🚀 Local Build & Deploy on JetHub"
echo "=================================="

# Проверка директории
if [ ! -d "/opt/jethome_server" ]; then
    echo "📥 Cloning repository..."
    cd /opt
    git clone https://github.com/breddowen/jethome_server.git
fi

cd /opt/jethome_server

# Обновление кода
echo ""
echo "📥 Pulling latest code..."
git pull origin main

# Остановка старых контейнеров
echo ""
echo "⏹️  Stopping old containers..."
cd deploy
docker-compose down || true
cd ..

# Сборка Backend
echo ""
echo "🔨 Building Backend..."
cd backend
docker build -t ghcr.io/breddowen/jethome-backend:latest .

# Сборка Frontend
echo ""
echo "🔨 Building Frontend..."
cd ../frontend
docker build -t ghcr.io/breddowen/jethome-frontend:latest .

# Запуск контейнеров
echo ""
echo "▶️  Starting containers..."
cd ../deploy
docker-compose up -d

# Ожидание
echo ""
echo "⏳ Waiting for services to start..."
sleep 15

# Проверка статуса
echo ""
echo "📊 Container status:"
docker-compose ps

# Health check
echo ""
echo "🔍 Health check:"
curl -f http://localhost:8000/health && echo "✅ Backend OK" || echo "❌ Backend failed"
curl -f http://localhost:3000 && echo "✅ Frontend OK" || echo "❌ Frontend failed"
curl -f http://localhost && echo "✅ Nginx OK" || echo "❌ Nginx failed"

# Логи
echo ""
echo "📋 Recent logs:"
docker-compose logs --tail=20

echo ""
echo "================================"
echo "✅ Deployment completed!"
echo ""
echo "Access the app at:"
echo "  http://$(hostname -I | awk '{print $1}')"
echo "  http://localhost (from JetHub)"
echo ""
echo "View logs: docker-compose logs -f"
echo "Stop: docker-compose down"
```

**Запустите:**

```bash
# На JetHub
cd /opt/jethome_server/deploy

# Если файла нет - создайте
nano local-build-deploy.sh
# Вставьте содержимое выше (Ctrl+O, Enter, Ctrl+X)

# Сделайте исполняемым
chmod +x local-build-deploy.sh

# Запустите
./local-build-deploy.sh
```

---

## 🔧 Если возникнут ошибки

### Ошибка: недостаточно места

```bash
# Очистка Docker
docker system prune -a -f
docker volume prune -f

# Проверка места
df -h
```

### Ошибка: не хватает памяти при сборке

```bash
# Остановите ненужные сервисы
systemctl stop xray

# Соберите по очереди
docker build -t ghcr.io/breddowen/jethome-backend:latest ./backend
sleep 10
docker build -t ghcr.io/breddowen/jethome-frontend:latest ./frontend

# Запустите обратно
systemctl start xray
```

### Проверка логов отдельных сервисов

```bash
cd /opt/jethome_server/deploy

# Backend
docker-compose logs backend

# Frontend  
docker-compose logs frontend

# Nginx
docker-compose logs nginx

# Все вместе
docker-compose logs -f
```

---

## 📊 Мониторинг процесса сборки

```bash
# В одном терминале - сборка
./local-build-deploy.sh

# В другом терминале SSH - мониторинг ресурсов
watch -n 1 'docker stats --no-stream'

# Или
htop
```

---

## ✅ Быстрый тест (без git)

Если хотите просто протестировать без клонирования репозитория:

```bash
# На JetHub создайте минимальную структуру
mkdir -p /opt/test-deploy
cd /opt/test-deploy

# Создайте docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  backend:
    image: python:3.11-slim
    container_name: test-backend
    command: python -m http.server 8000
    ports:
      - "8000:8000"

  frontend:
    image: node:20-alpine
    container_name: test-frontend
    command: sh -c "echo 'Hello from Frontend' && npx http-server -p 3000"
    ports:
      - "3000:3000"

  nginx:
    image: nginx:alpine
    container_name: test-nginx
    ports:
      - "80:80"
EOF

# Запуск
docker-compose up -d

# Проверка
curl http://localhost:8000
curl http://localhost:3000
curl http://localhost

# Остановка
docker-compose down
```

---

## 🎯 Рекомендуемый план действий

### Сейчас (на работе):

1. **SSH на JetHub**
   ```bash
   ssh root@192.168.137.119
   ```

2. **Быстрый тест**
   ```bash
   cd /opt/jethome_server/deploy
   ./local-build-deploy.sh
   ```

3. **Проверьте в браузере**
   ```
   http://192.168.137.119
   ```

### Дома:

1. **Настроите GitHub Secrets** с правильным домашним IP

2. **GitHub Actions будет работать** (если JetHub доступен из интернета)

3. **Или используете автоматический update.sh** (если в локальной сети)

---

## 📋 Структура для коммита

Добавьте локальный деплой скрипт в репозиторий:

```bash
# Создайте файл на вашем компьютере
# ./deploy/local-build-deploy.sh
# (содержимое выше)

# Коммит
git add deploy/local-build-deploy.sh
git commit -m "Add local build and deploy script for JetHub"
git push origin main
```

---

## 🔄 Workflow на JetHub

```bash
# При каждом обновлении кода:

# 1. Обновить репозиторий
cd /opt/jethome_server
git pull origin main

# 2. Пересобрать и запустить
cd deploy
./local-build-deploy.sh
```

---

Попробуйте сейчас запустить `local-build-deploy.sh` и дайте знать что получилось! 🚀
# ./deploy/update.sh
#!/bin/bash

set -e

echo "🚀 JetHub Update Script"
echo "======================="

# Переход в директорию
cd /opt/jethome_server/deploy || {
    echo "❌ Directory /opt/jethome_server/deploy not found"
    exit 1
}

# Проверка файлов
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found"
    exit 1
fi

# Логин в GHCR (если нужно)
echo ""
echo "🔐 Checking GitHub Container Registry login..."
docker login ghcr.io -u breddowen --password-stdin < /root/.ghcr-token 2>/dev/null || {
    echo "⚠️  Not logged in to GHCR. Trying to pull public images..."
}

# Остановка контейнеров
echo ""
echo "⏹️  Stopping containers..."
docker-compose down

# Удаление старых образов
echo ""
echo "🗑️  Removing old images..."
docker rmi ghcr.io/breddowen/jethome-backend:latest 2>/dev/null || true
docker rmi ghcr.io/breddowen/jethome-frontend:latest 2>/dev/null || true

# Загрузка новых образов
echo ""
echo "📥 Pulling new images..."
docker-compose pull

# Запуск контейнеров
echo ""
echo "▶️  Starting containers..."
docker-compose up -d

# Ожидание запуска
echo ""
echo "⏳ Waiting for services to start..."
sleep 15

# Проверка статуса
echo ""
echo "📊 Container status:"
docker-compose ps

# Проверка здоровья
echo ""
echo "🔍 Health check:"

# Backend
if curl -f http://localhost:8000/health 2>/dev/null; then
    echo "✅ Backend is healthy"
else
    echo "⚠️  Backend health check failed"
fi

# Frontend
if curl -f http://localhost:3000 2>/dev/null; then
    echo "✅ Frontend is healthy"
else
    echo "⚠️  Frontend health check failed"
fi

# Nginx
if curl -f http://localhost 2>/dev/null; then
    echo "✅ Nginx is working"
else
    echo "⚠️  Nginx check failed"
fi

# Логи
echo ""
echo "📋 Recent logs:"
docker-compose logs --tail=10

# Очистка
echo ""
echo "🧹 Cleaning up old images..."
docker image prune -f

echo ""
echo "================================"
echo "✅ Update completed!"
echo "Access the app at: http://$(hostname -I | awk '{print $1}')"
echo ""
echo "To view logs: docker-compose logs -f"
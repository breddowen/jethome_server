# ./deploy/manual-deploy.sh
#!/bin/bash

set -e

echo "🚀 Manual Deployment Script"
echo "============================"

# Переход в директорию деплоя
cd /opt/jethome_server/deploy || {
    echo "❌ Directory /opt/jethome_server/deploy not found"
    exit 1
}

# Проверка docker-compose.yml
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found"
    exit 1
fi

# Логин в GitHub Container Registry (если нужно)
echo ""
echo "🔐 Logging in to GitHub Container Registry..."
read -p "Enter your GitHub username [breddowen]: " GITHUB_USER
GITHUB_USER=${GITHUB_USER:-breddowen}

read -sp "Enter your GitHub PAT: " GITHUB_TOKEN
echo ""

echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_USER" --password-stdin

# Остановка контейнеров
echo ""
echo "⏹️  Stopping containers..."
docker-compose down || true

# Удаление старых образов
echo ""
echo "🗑️  Removing old images..."
docker rmi ghcr.io/breddowen/jethome-backend:latest || true
docker rmi ghcr.io/breddowen/jethome-frontend:latest || true

# Загрузка новых образов
echo ""
echo "📥 Pulling new images..."
docker-compose pull

# Запуск контейнеров
echo ""
echo "▶️  Starting containers..."
docker-compose up -d

# Ожидание
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Проверка статуса
echo ""
echo "📊 Container status:"
docker-compose ps

# Проверка логов
echo ""
echo "📋 Recent logs:"
docker-compose logs --tail=20

# Health check
echo ""
echo "🔍 Health check:"
if curl -f http://localhost:8000/health; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
fi

if curl -f http://localhost:3000; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend is not accessible"
fi

echo ""
echo "================================"
echo "✅ Deployment completed!"
echo "Access the app at: http://$(hostname -I | awk '{print $1}')"
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
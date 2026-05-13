# ./deploy/setup-jethub.sh
#!/bin/bash

set -e

echo "🚀 JetHub Initial Setup Script"
echo "================================"

# Проверка что запущено на JetHub
if [ ! -f "/etc/armbian-release" ] && [ ! -f "/etc/os-release" ]; then
    echo "⚠️  Warning: This script is designed for JetHub (Armbian/Linux)"
fi

# Установка Docker
echo ""
echo "📦 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    echo "✅ Docker installed"
else
    echo "✅ Docker already installed"
fi

# Установка Docker Compose
echo ""
echo "📦 Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    apt-get update
    apt-get install -y docker-compose
    echo "✅ Docker Compose installed"
else
    echo "✅ Docker Compose already installed"
fi

# Добавление текущего пользователя в группу docker
echo ""
echo "👤 Adding user to docker group..."
usermod -aG docker $USER || true

# Создание директорий
echo ""
echo "📁 Creating directories..."
mkdir -p /opt/jethome_server/deploy
mkdir -p /opt/jethome_server/deploy/data/database
chmod -R 755 /opt/jethome_server

# Проверка сетевого подключения
echo ""
echo "🌐 Checking network connectivity..."
if ping -c 1 google.com &> /dev/null; then
    echo "✅ Network is OK"
else
    echo "❌ No network connectivity"
    exit 1
fi

# Проверка доступа к GitHub Container Registry
echo ""
echo "🔐 Checking GitHub Container Registry access..."
echo "You need to login to GitHub Container Registry"
echo ""
read -p "Enter your GitHub username [breddowen]: " GITHUB_USER
GITHUB_USER=${GITHUB_USER:-breddowen}

read -sp "Enter your GitHub Personal Access Token (PAT): " GITHUB_TOKEN
echo ""

if echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_USER" --password-stdin; then
    echo "✅ Successfully logged in to ghcr.io"
    
    # Сохранение креденшелов
    echo "💾 Credentials saved to ~/.docker/config.json"
else
    echo "❌ Failed to login to ghcr.io"
    echo "Please check your token and try again"
    exit 1
fi

# Финальная проверка
echo ""
echo "================================"
echo "✅ Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Make sure GitHub Actions secrets are configured"
echo "2. Push to main branch to trigger deployment"
echo "3. Or manually pull and run: cd /opt/jethome_server/deploy && docker-compose up -d"
echo ""
echo "Access the app at: http://$(hostname -I | awk '{print $1}')"
# jethome_server# 🚀 Обновленная структура с GitHub Container Registry

## 📝 Содержание
1. [Настройка ключей и токенов](#1-настройка-ключей-и-токенов)
2. [Обновленные файлы](#2-обновленные-файлы)
3. [Инструкция по деплою](#3-инструкция-по-деплою)

---

## 1. Настройка ключей и токенов

### 📌 1.1 Создание SSH ключа для доступа к JetHub

**На вашем компьютере (Windows):**

```bash
# Откройте PowerShell или Git Bash

# Создайте SSH ключ (без пароля для автоматизации)
ssh-keygen -t ed25519 -C "github-actions-jethub" -f ~/.ssh/jethub_deploy -N ""

# Это создаст два файла:
# ~/.ssh/jethub_deploy (приватный ключ)
# ~/.ssh/jethub_deploy.pub (публичный ключ)

# Посмотреть приватный ключ (для GitHub Secrets)
cat ~/.ssh/jethub_deploy

# Посмотреть публичный ключ (для JetHub)
cat ~/.ssh/jethub_deploy.pub
```

**На JetHub (через SSH):**

```bash
# Подключитесь к JetHub
ssh root@10.42.0.1  # или ваш IP

# Создайте директорию для SSH ключей (если нет)
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Добавьте публичный ключ в authorized_keys
nano ~/.ssh/authorized_keys

# Вставьте содержимое файла jethub_deploy.pub (из вашего компьютера)
# Должно выглядеть примерно так:
# ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJx... github-actions-jethub

# Сохраните (Ctrl+O, Enter, Ctrl+X)

# Установите права
chmod 600 ~/.ssh/authorized_keys

# Проверьте подключение с вашего компьютера
exit
ssh -i ~/.ssh/jethub_deploy root@10.42.0.1
```

**Если подключение успешно - ключ настроен правильно! ✅**

---

### 📌 1.2 Создание GitHub Personal Access Token (PAT)

**Шаг 1: Создание токена**

1. Откройте GitHub: https://github.com
2. Нажмите на аватар → **Settings**
3. Слева внизу → **Developer settings**
4. **Personal access tokens** → **Tokens (classic)**
5. **Generate new token** → **Generate new token (classic)**

**Шаг 2: Настройка токена**

- **Note:** `JetHub Deployment`
- **Expiration:** `No expiration` (или на ваш выбор)
- **Scopes:** отметьте галочки:
  - ✅ `repo` (Full control of private repositories)
  - ✅ `write:packages` (Upload packages to GitHub Package Registry)
  - ✅ `read:packages` (Download packages from GitHub Package Registry)
  - ✅ `delete:packages` (Delete packages from GitHub Package Registry)

**Шаг 3: Сохранение токена**

1. Нажмите **Generate token**
2. **ВАЖНО:** Скопируйте токен прямо сейчас! Он показывается только один раз!
3. Сохраните его в надежном месте (например, password manager)

Токен будет выглядеть примерно так: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

### 📌 1.3 Добавление Secrets в GitHub репозиторий

1. Откройте ваш репозиторий: https://github.com/breddowen/jethome_server
2. **Settings** → **Secrets and variables** → **Actions**
3. Нажмите **New repository secret**

**Добавьте следующие секреты:**

#### 1. `SSH_PRIVATE_KEY`
```
Содержимое файла ~/.ssh/jethub_deploy (приватный ключ)

Должно начинаться с:
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

#### 2. `JETHUB_HOST`
```
IP адрес вашего JetHub, например:
10.42.0.1
```

#### 3. `JETHUB_USER`
```
Пользователь SSH, обычно:
root
```

#### 4. `GHCR_TOKEN`
```
Personal Access Token, созданный в шаге 1.2
Начинается с ghp_...
```

**Итого должно быть 4 секрета:**
- ✅ SSH_PRIVATE_KEY
- ✅ JETHUB_HOST
- ✅ JETHUB_USER
- ✅ GHCR_TOKEN

---

### 📌 1.4 Настройка GitHub Container Registry

**Включение GHCR для репозитория:**

1. Откройте репозиторий: https://github.com/breddowen/jethome_server
2. **Settings** → **Actions** → **General**
3. Прокрутите до **Workflow permissions**
4. Выберите: **Read and write permissions**
5. Поставьте галочку: **Allow GitHub Actions to create and approve pull requests**
6. **Save**

---

## 2. Обновленные файлы

### 🐳 2.1 Docker Compose (использует registry)

```yaml
# ./deploy/docker-compose.yml
version: '3.8'

services:
  backend:
    image: ghcr.io/breddowen/jethome-backend:latest
    container_name: jethub-backend
    restart: unless-stopped
    volumes:
      - ./data/database:/app/data
      - /var/run/dbus:/var/run/dbus:ro
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    network_mode: host
    privileged: true
    environment:
      - DATABASE_URL=sqlite:////app/data/test_database.db
      - CORS_ORIGINS=["http://localhost:3000","http://10.42.0.1:3000","http://10.42.0.1"]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    image: ghcr.io/breddowen/jethome-frontend:latest
    container_name: jethub-frontend
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NUXT_PUBLIC_API_BASE=http://localhost:8000
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    container_name: jethub-nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:80"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

### 🚀 2.2 GitHub Actions (Build & Deploy)

```yaml
# ./.github/workflows/deploy.yml
name: Build and Deploy to JetHub

on:
  push:
    branches:
      - main
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  BACKEND_IMAGE: ghcr.io/breddowen/jethome-backend
  FRONTEND_IMAGE: ghcr.io/breddowen/jethome-frontend

jobs:
  build-and-push:
    name: Build and Push Docker Images
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata for Backend
        id: meta-backend
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.BACKEND_IMAGE }}
          tags: |
            type=raw,value=latest
            type=sha,prefix={{branch}}-

      - name: Build and push Backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./backend/Dockerfile
          push: true
          tags: ${{ steps.meta-backend.outputs.tags }}
          labels: ${{ steps.meta-backend.outputs.labels }}
          cache-from: type=registry,ref=${{ env.BACKEND_IMAGE }}:buildcache
          cache-to: type=registry,ref=${{ env.BACKEND_IMAGE }}:buildcache,mode=max

      - name: Extract metadata for Frontend
        id: meta-frontend
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.FRONTEND_IMAGE }}
          tags: |
            type=raw,value=latest
            type=sha,prefix={{branch}}-

      - name: Build and push Frontend
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          file: ./frontend/Dockerfile
          push: true
          tags: ${{ steps.meta-frontend.outputs.tags }}
          labels: ${{ steps.meta-frontend.outputs.labels }}
          cache-from: type=registry,ref=${{ env.FRONTEND_IMAGE }}:buildcache
          cache-to: type=registry,ref=${{ env.FRONTEND_IMAGE }}:buildcache,mode=max

  deploy:
    name: Deploy to JetHub
    needs: build-and-push
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup SSH
        uses: webfactory/ssh-agent@v0.9.0
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

      - name: Add JetHub to known hosts
        run: |
          mkdir -p ~/.ssh
          ssh-keyscan -H ${{ secrets.JETHUB_HOST }} >> ~/.ssh/known_hosts

      - name: Copy deployment files to JetHub
        env:
          JETHUB_HOST: ${{ secrets.JETHUB_HOST }}
          JETHUB_USER: ${{ secrets.JETHUB_USER }}
        run: |
          # Создаем директорию если нет
          ssh $JETHUB_USER@$JETHUB_HOST "mkdir -p /opt/jethome_server/deploy"
          
          # Копируем docker-compose и nginx.conf
          scp deploy/docker-compose.yml $JETHUB_USER@$JETHUB_HOST:/opt/jethome_server/deploy/
          scp deploy/nginx.conf $JETHUB_USER@$JETHUB_HOST:/opt/jethome_server/deploy/

      - name: Deploy to JetHub
        env:
          JETHUB_HOST: ${{ secrets.JETHUB_HOST }}
          JETHUB_USER: ${{ secrets.JETHUB_USER }}
          GHCR_TOKEN: ${{ secrets.GHCR_TOKEN }}
        run: |
          ssh $JETHUB_USER@$JETHUB_HOST << 'ENDSSH'
            set -e
            
            echo "🚀 Starting deployment..."
            
            cd /opt/jethome_server/deploy || exit 1
            
            # Логин в GitHub Container Registry
            echo "${{ secrets.GHCR_TOKEN }}" | docker login ghcr.io -u breddowen --password-stdin
            
            # Остановка старых контейнеров
            echo "⏹️  Stopping old containers..."
            docker-compose down || true
            
            # Удаление старых образов
            echo "🗑️  Removing old images..."
            docker rmi ghcr.io/breddowen/jethome-backend:latest || true
            docker rmi ghcr.io/breddowen/jethome-frontend:latest || true
            
            # Загрузка новых образов
            echo "📥 Pulling new images..."
            docker-compose pull
            
            # Запуск новых контейнеров
            echo "▶️  Starting new containers..."
            docker-compose up -d
            
            # Проверка статуса
            echo "✅ Checking status..."
            sleep 10
            docker-compose ps
            
            # Очистка неиспользуемых образов
            echo "🧹 Cleaning up..."
            docker image prune -f
            
            echo "🎉 Deployment completed!"
          ENDSSH

      - name: Verify deployment
        env:
          JETHUB_HOST: ${{ secrets.JETHUB_HOST }}
        run: |
          echo "🔍 Verifying deployment..."
          sleep 5
          
          # Проверка backend
          if curl -f http://$JETHUB_HOST:8000/health; then
            echo "✅ Backend is healthy"
          else
            echo "❌ Backend health check failed"
            exit 1
          fi
          
          # Проверка frontend через nginx
          if curl -f http://$JETHUB_HOST; then
            echo "✅ Frontend is accessible"
          else
            echo "❌ Frontend is not accessible"
            exit 1
          fi
          
          echo "🎉 All health checks passed!"

      - name: Notify on success
        if: success()
        run: |
          echo "✅ Deployment successful!"
          echo "Access your app at: http://${{ secrets.JETHUB_HOST }}"

      - name: Notify on failure
        if: failure()
        run: |
          echo "❌ Deployment failed!"
          echo "Check the logs above for details"
```

---

### 📄 2.3 Скрипт для первоначальной настройки JetHub

```bash
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
```

**Сделайте скрипт исполняемым:**

```bash
chmod +x ./deploy/setup-jethub.sh
```

---

### 📄 2.4 Скрипт для ручного деплоя (если GitHub Actions не используется)

```bash
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
```

**Сделайте скрипт исполняемым:**

```bash
chmod +x ./deploy/manual-deploy.sh
```

---

## 3. Инструкция по деплою

### 📋 3.1 Первоначальная настройка (один раз)

**Шаг 1: Настройка ключей и токенов**

Следуйте инструкциям из раздела [1. Настройка ключей и токенов](#1-настройка-ключей-и-токенов)

**Шаг 2: Настройка JetHub**

```bash
# На JetHub (через SSH)
ssh root@10.42.0.1

# Загрузите скрипт настройки
curl -o setup-jethub.sh https://raw.githubusercontent.com/breddowen/jethome_server/main/deploy/setup-jethub.sh

# Или создайте вручную и скопируйте содержимое из секции 2.3

# Запустите скрипт
chmod +x setup-jethub.sh
./setup-jethub.sh
```

Скрипт запросит:
- GitHub username (по умолчанию: breddowen)
- GitHub Personal Access Token (созданный в шаге 1.2)

**Шаг 3: Проверка**

```bash
# Проверка Docker
docker --version
docker-compose --version

# Проверка логина в GHCR
docker login ghcr.io
# Должно показать: Login Succeeded

# Проверка директорий
ls -la /opt/jethome_server/deploy
```

---

### 🚀 3.2 Автоматический деплой через GitHub Actions

**После настройки ключей и JetHub:**

```bash
# На вашем компьютере
cd /path/to/jethome_server

# Добавьте все файлы
git add .

# Коммит
git commit -m "Initial setup with GHCR"

# Пуш в main ветку (триггерит деплой)
git push origin main
```

**Что произойдет:**

1. ✅ GitHub Actions начнет работу
2. ✅ Соберет Docker образы для backend и frontend
3. ✅ Загрузит образы в GitHub Container Registry (ghcr.io)
4. ✅ Подключится к JetHub по SSH
5. ✅ Скопирует docker-compose.yml и nginx.conf
6. ✅ Загрузит образы из GHCR на JetHub
7. ✅ Запустит контейнеры
8. ✅ Проверит health статус

**Мониторинг деплоя:**

1. Откройте GitHub: https://github.com/breddowen/jethome_server
2. Перейдите в **Actions**
3. Нажмите на запущенный workflow
4. Смотрите логи в реальном времени

---

### 🔧 3.3 Ручной деплой (без GitHub Actions)

```bash
# На JetHub
ssh root@10.42.0.1

cd /opt/jethome_server/deploy

# Запустите скрипт ручного деплоя
./manual-deploy.sh
```

Или вручную:

```bash
# Логин в GHCR
echo "YOUR_PAT" | docker login ghcr.io -u breddowen --password-stdin

# Остановка
docker-compose down

# Обновление образов
docker-compose pull

# Запуск
docker-compose up -d

# Проверка
docker-compose ps
docker-compose logs -f
```

---

### 🔍 3.4 Проверка работы

**На JetHub:**

```bash
# Статус контейнеров
docker-compose ps

# Логи всех сервисов
docker-compose logs

# Логи конкретного сервиса
docker-compose logs backend
docker-compose logs frontend
docker-compose logs nginx

# Живые логи
docker-compose logs -f

# Health check
curl http://localhost:8000/health
curl http://localhost:3000
curl http://localhost
```

**В браузере:**

- Откройте: `http://10.42.0.1` (или IP вашего JetHub)
- Должна открыться панель управления

---

### 🛠️ 3.5 Управление контейнерами

```bash
# Остановка
docker-compose down

# Остановка с удалением volumes
docker-compose down -v

# Запуск
docker-compose up -d

# Перезапуск
docker-compose restart

# Перезапуск конкретного сервиса
docker-compose restart backend

# Обновление образов и перезапуск
docker-compose pull && docker-compose up -d

# Просмотр использования ресурсов
docker stats
```

---

### 📊 3.6 Мониторинг образов в GHCR

**Просмотр образов:**

1. Откройте GitHub: https://github.com/breddowen
2. Перейдите в **Packages**
3. Вы увидите:
   - `jethome-backend`
   - `jethome-frontend`

**Или через командную строку:**

```bash
# Просмотр образов на JetHub
docker images | grep ghcr.io/breddowen

# Удаление старых образов
docker image prune -a
```

---

### 🔐 3.7 Troubleshooting

**Проблема: GitHub Actions не может подключиться к JetHub**

```bash
# Проверьте SSH ключ на JetHub
cat ~/.ssh/authorized_keys

# Проверьте права
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# Проверьте подключение вручную
ssh -i ~/.ssh/jethub_deploy root@10.42.0.1
```

**Проблема: Не может загрузить образы из GHCR**

```bash
# На JetHub проверьте логин
docker login ghcr.io

# Если не залогинены
echo "YOUR_PAT" | docker login ghcr.io -u breddowen --password-stdin

# Проверьте доступ к образам
docker pull ghcr.io/breddowen/jethome-backend:latest
docker pull ghcr.io/breddowen/jethome-frontend:latest
```

**Проблема: Образы приватные и требуют аутентификации**

Нужно сделать образы публичными:

1. Откройте: https://github.com/breddowen?tab=packages
2. Нажмите на `jethome-backend`
3. **Package settings** → **Change visibility** → **Public**
4. Повторите для `jethome-frontend`

**Проблема: Контейнеры не запускаются**

```bash
# Проверьте логи
docker-compose logs

# Проверьте статус
docker-compose ps

# Проверьте наличие образов
docker images

# Попробуйте пересоздать
docker-compose down
docker-compose up -d --force-recreate
```

---

## 📝 Итоговый чеклист

### ✅ На вашем компьютере:

- [ ] Создан SSH ключ (`~/.ssh/jethub_deploy`)
- [ ] Создан GitHub PAT с правами на packages
- [ ] SSH ключ проверен (можно подключиться к JetHub)

### ✅ В GitHub репозитории:

- [ ] Добавлены Secrets:
  - [ ] `SSH_PRIVATE_KEY`
  - [ ] `JETHUB_HOST`
  - [ ] `JETHUB_USER`
  - [ ] `GHCR_TOKEN`
- [ ] Workflow permissions: Read and write
- [ ] Packages (образы) сделаны публичными (опционально)

### ✅ На JetHub:

- [ ] Установлен Docker
- [ ] Установлен Docker Compose
- [ ] Создана директория `/opt/jethome_server/deploy`
- [ ] Добавлен SSH публичный ключ в `~/.ssh/authorized_keys`
- [ ] Выполнен логин в GHCR (`docker login ghcr.io`)

### ✅ Первый деплой:

- [ ] Сделан `git push origin main`
- [ ] GitHub Actions успешно завершился
- [ ] Контейнеры запущены на JetHub
- [ ] Панель доступна по `http://10.42.0.1`

---

## 🎉 Готово!

Теперь при каждом push в main ветку:

1. Образы автоматически собираются
2. Загружаются в GitHub Container Registry
3. Деплоятся на JetHub
4. Запускаются автоматически

**Доступ к панели:** `http://10.42.0.1` (или IP вашего JetHub)

Хотите что-то добавить или изменить?
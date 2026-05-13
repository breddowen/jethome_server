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

КАК ЗАЛИТЬ НА GITHUB

Чтобы загрузить ваш проект на GitHub, выполните следующие шаги в терминале на вашем ПК.
## Шаг 1: Инициализация и подготовка

   1. Откройте терминал и перейдите в корневую директорию проекта:
   
   cd jethome_server
   
   2. Создайте файл .gitignore в корневой директории (jethome_server/), чтобы не загружать в репозиторий лишние файлы (базу данных, секреты, логи и зависимости):
   
   touch .gitignore
   
   3. Откройте .gitignore в текстовом редакторе и добавьте туда следующие строки:
   
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   .venv/
   venv/
   
   # Databases
   backend/test_database.db
   
   # Node / Nuxt
   node_modules/
   .nuxt/
   dist/
   .output/
   
   # Environment variables
   .env
   backend/.env
   frontend/.env
   
   
## Шаг 2: Привязка и отправка кода

   1. Инициализируйте локальный Git-репозиторий:
   
   git init
   
   2. Добавьте все файлы проекта в индекс (кроме тех, что указаны в .gitignore):
   
   git add .
   
   3. Сделайте первый коммит:
   
   git commit -m "Initial commit: backend, frontend, deploy and workflow"
   
   4. Установите имя главной ветки main:
   
   git branch -M main
   
   5. Привяжите ваш удаленный репозиторий GitHub к локальному:
   
   git remote add origin https://github.com/breddowen/jethome_server.git
   
   6. Отправьте код на GitHub (если у вас настроен GitHub CLI или SSH, команда выполнится сразу; если нет — потребуется ввести логин и Personal Access Token вместо пароля):
   
   git push -u origin main
   
   
Если вы хотите автоматизировать деплой через созданный файл deploy.yml, сообщите:

* Какую платформу/сервер (VPS, AWS, Heroku) вы планируете использовать для деплоя?
* Настроены ли уже секреты репозитория (Repository Secrets) в настройках вашего GitHub?

Я помогу правильно донастроить GitHub Actions для вашей структуры.


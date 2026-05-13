# ./frontend/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Копирование package.json
COPY package*.json ./

# Установка зависимостей
RUN npm ci

# Копирование кода
COPY . .

# Сборка приложения
RUN npm run build

# Production образ
FROM node:20-alpine

WORKDIR /app

# Копирование собранного приложения
COPY --from=builder /app/.output ./.output

# Установка переменных окружения
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

# Запуск
CMD ["node", ".output/server/index.mjs"]
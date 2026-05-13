# ./frontend/Dockerfile
FROM node:24-alpine AS builder

WORKDIR /app

# Копирование package.json
COPY package*.json ./

# Установка зависимостей (вместо npm ci используем npm install)
RUN npm install --legacy-peer-deps

# Копирование кода
COPY . .

# Сборка приложения
RUN npm run build

# Production образ
FROM node:24-alpine

WORKDIR /app

# Копирование собранного приложения
COPY --from=builder /app/.output ./.output
COPY --from=builder /app/package*.json ./

# Установка только production зависимостей
RUN npm install --production --legacy-peer-deps

# Установка переменных окружения
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000
ENV NODE_ENV=production

EXPOSE 3000

# Запуск
CMD ["node", ".output/server/index.mjs"]
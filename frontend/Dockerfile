# 建置階段
FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 服務階段 - 用 nginx 提供靜態檔案
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
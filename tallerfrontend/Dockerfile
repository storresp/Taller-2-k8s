# Etapa build
FROM node:22-alpine AS build

WORKDIR /tallerfrontend

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Etapa producción
FROM nginx:alpine

COPY dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
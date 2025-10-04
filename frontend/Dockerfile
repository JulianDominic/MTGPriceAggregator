FROM node:current-alpine AS build-stage
WORKDIR /frontend
COPY /frontend/ ./
RUN npm ci 
RUN npm run build 

FROM nginx:stable-alpine AS production-stage
VOLUME /var/log/nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /frontend/dist /usr/share/nginx/html
EXPOSE 80

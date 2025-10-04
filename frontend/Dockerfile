FROM node:current-alpine AS build-stage

# https://stackoverflow.com/a/77490465
# Define build arguments for environment variables
ARG VITE_HOST_IP
# Set environment variables during the build process
ENV VITE_HOST_IP=$VITE_HOST_IP

WORKDIR /frontend
COPY /frontend/ ./
RUN npm ci 
RUN npm run build 

FROM nginx:stable-alpine AS production-stage
VOLUME /var/log/nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /frontend/dist /usr/share/nginx/html
EXPOSE 80

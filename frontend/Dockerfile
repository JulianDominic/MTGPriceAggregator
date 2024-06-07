FROM node:22-alpine3.19

WORKDIR /frontend

ENV PATH /frontend/node_modules/.bin:$PATH

COPY /frontend/package.json ./
COPY /frontend/package-lock.json ./
RUN npm ci

COPY /frontend ./

CMD ["npm", "run", "dev"]

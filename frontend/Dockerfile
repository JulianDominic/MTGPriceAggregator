FROM node:22-alpine3.19

WORKDIR /frontend

ENV PATH /frontend/node_modules/.bin:$PATH

COPY package.json ./
COPY package-lock.json ./
RUN npm ci

COPY . ./

CMD ["npm", "run", "dev"]

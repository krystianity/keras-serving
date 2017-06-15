FROM node:8
MAINTAINER Christian Fröhlingsdorf <chris@5cf.de>

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV NODE_ENV "production"
COPY package.json /usr/src/app/
RUN npm install && npm cache clean --force
COPY . /usr/src/app

CMD [ "npm", "start" ]
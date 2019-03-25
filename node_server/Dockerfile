FROM node:10
MAINTAINER Christian Fröhlingsdorf <chris@5cf.de>

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV NODE_ENV "production"
COPY package.json /usr/src/app/
COPY yarn.lock /usr/src/app/
RUN yarn && npm cache clean --force
COPY . /usr/src/app

CMD [ "yarn", "start" ]
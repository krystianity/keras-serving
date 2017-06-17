#!/usr/bin/env bash
docker-compose -f docker-compose.dual.yml rm -f -v --all && \
docker-compose -f docker-compose.dual.yml build --no-cache && \
docker-compose -f docker-compose.dual.yml up --force-recreate
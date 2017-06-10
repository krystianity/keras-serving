#!/usr/bin/env bash
docker-compose rm -f -v && docker-compose build && docker-compose up
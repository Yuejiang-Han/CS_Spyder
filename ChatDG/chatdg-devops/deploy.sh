#!/usr/bin/env bash

set -e

docker-compose -p chatdg --env-file .env -f docker-compose-infra.yml -f docker-compose-milvus.yml \
     -f docker-compose-biz.yml \
    up -d --pull aways --remove-orphans $@
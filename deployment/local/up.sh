#!/bin/bash

docker compose --project-name omnisect-local \
               --file project/docker-compose.yml \
               up -d
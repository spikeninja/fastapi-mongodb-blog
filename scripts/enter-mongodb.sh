#!/bin/bash

source .env

docker compose exec -it mongodb mongosh -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD

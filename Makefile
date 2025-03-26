ifneq (,$(wildcard ./.env))
    include .env
    export
endif

execute-init: ./scripts/init.sql
	docker exec "${CONTAINER_NAME}" psql --dbname="${DATABASE_NAME}" --username "${DATABASE_USERNAME}" --password "${DATABASE_PASSWORD}" --file /scripts/init.sql

execute-export-xml: ./scripts/export-xml.sql
	docker exec "${CONTAINER_NAME}" psql --dbname="${DATABASE_NAME}" --username "${DATABASE_USERNAME}" --password "${DATABASE_PASSWORD}" --file /scripts/export-xml.sql

up:
	docker compose up --detach

stop:
	docker stop "${CONTAINER_NAME}"

connect:
	docker exec -it "${CONTAINER_NAME}" /bin/bash

connect-to-bd:
	docker exec -it "${CONTAINER_NAME}" psql --dbname="${DATABASE_NAME}" --username "${DATABASE_USERNAME}" --password "${DATABASE_PASSWORD}"

# Testing docker image.
build-image:
	docker build . -t ${IMAGE_NAME}

# - Adhoc tasks.
run:
	docker run --name "${CONTAINER_NAME}" --detach --rm "${IMAGE_NAME}"

rm-all-containers:
	docker rm $(docker ps --quiet --all)

# # Apache hadoop specific.
prepare-hadoop:
	git submodule update --init --recursive -- ./Apache__hadoop

pull-hadoop: prepare-hadoop
	docker compose -f ./Apache__hadoop/docker-compose-non-dev.yml pull

up-hadoop:
	docker compose -f ./Apache__hadoop/docker-compose-non-dev.yml up

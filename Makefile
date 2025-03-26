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
	git submodule update --init --recursive -- ./Apache__Hadoop

# TODO: Reuse `build-image` target.
build-hadoop:
	docker build -t "${IMAGE_NAME}" ./Apache__Hadoop

# TODO: Reuse `run` target.
run-hadoop:
	docker run -it --name "${CONTAINER_NAME}" -p 9864:9864 -p "${ADMIN_PANEL_PORT}":9870 -p 8088:8088 --hostname "${ADMIN_PANEL_HOST}" "${IMAGE_NAME}"

open-hadoop-admin-panel:
	open http://"${ADMIN_PANEL_HOST}":"${ADMIN_PANEL_PORT}"

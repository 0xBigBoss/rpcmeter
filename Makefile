.SILENT:

.PHONY: help
## This help screen
help:
	printf "Available targets\n\n"
	awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "%-30s %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

.PHONY: start
## Start a local dockerized django app with `make start`
start:
	docker-compose up --force-recreate -d
	echo "Go to http://localhost:8000/"

.PHONY: connect
## Connect (i.e. open a shell) Start to the local dockerzied django app with `make connect)
connect:
	docker exec -it thundermeter /bin/bash

.PHONY: freeze
## Snapshot current python dependencies into a requirements.txt file with `make freeze` (run from inside container)
freeze:
# docker exec -it thundermeter pip freeze > requirements.txt
	pip freeze > requirements.txt

.PHONY: format
## General code formatting: `black . && isort .`
format:
	black . && isort .

.PHONY: migrate
## Run django migrations
migrate:
	python manage.py makemigrations
	python manage.py migrate

.PHONY: populate_providers
## Populate the providers table in the database
populate_providers:
	sqlite3 db "insert into provider (id,name,url,symbol,chain_id) values \
		(1,'POKT','https://poly-mainnet.gateway.pokt.network/v1/lb/6248e19a3bd808003a80fc61','POKT',1), \
		(2,'Official','https://polygon-rpc.com/','POLY-RPC',1), \
		(3,'Infura','https://polygon-mainnet.infura.io/v3/8c2432519ae84c7fac909007f759e172','INF',1), \
		(4,'Quicknode','https://still-dawn-cloud.matic.quiknode.pro/a72402cf6dd3cb6e8a314032ba437445e8977c31/','QUICK',1), \
		(5,'POKT','https://eth-mainnet.gateway.pokt.network/v1/lb/6248e19a3bd808003a80fc61','POKT',2), \
		(6,'Infura','https://mainnet.infura.io/v3/8c2432519ae84c7fac909007f759e172','INF',2);"
	sqlite3 db "insert into chain (id,name,chain_id) values \
		(1, 'polygon', '137'), \
		(2, 'ethereum', '1');"
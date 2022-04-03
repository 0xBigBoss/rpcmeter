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
	docker-compose up -d

.PHONY: connect
## Connect (i.e. open a shell) Start to the local dockerzied django app with `make connect)
connect:
	docker exec -it thundermeter /bin/bash

.PHONY: freeze
## Snapshot current python dependencies into a requirements.txt file with `make freeze` (run from inside container)
freeze:
# docker exec -it thundermeter pip freeze > requirements.txt
	pip freeze > requirements.txt
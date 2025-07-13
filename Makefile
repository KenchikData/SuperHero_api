.PHONY: up down build test shell logs db-shell

up:
	@docker compose up -d --build

down:
	@docker compose down --volumes

build:
	@docker compose build

test:
	@docker compose exec api pytest -q

shell:
	@docker compose exec api bash

logs:
	@docker compose logs -f

db-shell:
	@docker compose exec db psql -U heroes_user -d heroes

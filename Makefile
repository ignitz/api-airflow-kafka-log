.PHONY: help
help: ## Show help menu
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

local: ## Run in development mode
	docker compose -f docker-compose.dev.yaml up -d
	fastapi dev app/main.py

down: ## Stop the local development server
	docker compose -f docker-compose.dev.yaml down --volumes

run: ## Run in production mode
	gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

build: ## Build the docker image
	docker build -t api-airlfow-event-listener .

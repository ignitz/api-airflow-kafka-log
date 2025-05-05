.PHONY: help
help: ## Show help menu
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

local: ## Run in development mode
	docker compose -f docker-compose.dev.yaml up -d
	fastapi dev app/main.py

down: ## Stop the local development server
	docker compose -f docker-compose.dev.yaml down --volumes

run: ## Run in production mode
	fastapi run

build: ## Build the docker image
	docker build -t "192.168.3.2:50000/ignitz/api-airflow-kafka-log:$(shell git rev-parse HEAD)" .
	docker push "192.168.3.2:50000/ignitz/api-airflow-kafka-log:$(shell git rev-parse HEAD)"
	docker buildx build --progress=plain -f Dockerfile . --platform linux/amd64,linux/arm64 -t "ignitz/api-airflow-kafka-log:$(shell git rev-parse HEAD)" --push

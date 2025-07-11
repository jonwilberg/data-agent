.PHONY: help install_deps drop_db bootstrap_db run_backend run_frontend run_frontend_mock

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install_deps: ## Install dependencies for both backend and frontend
	@echo "Installing backend dependencies..."
	cd backend && poetry install
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "All dependencies installed successfully!"

drop_db: ## Stop and remove the database container with volumes
	docker compose down -v

bootstrap_db: ## Start database, run init script, and populate with census data
	docker compose up -d postgres
	@echo "Waiting for database to be ready..."
	@sleep 10
	@echo "Running census data bootstrap..."
	cd backend && poetry run python database/bootstrap_census_db.py
	@echo "Database bootstrap complete"

run_backend: ## Start the FastAPI backend server
	cd backend && poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

run_frontend: ## Start the React frontend development server
	cd frontend && npm run dev

run_frontend_mock: ## Start the React frontend with mock API responses (no backend needed)
	cd frontend && npm run dev:mock
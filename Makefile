.PHONY: help install dev-up dev-down test test-unit test-integration test-e2e lint format clean

help:
	@echo "FinanceAI Development Commands"
	@echo "==============================="
	@echo "install          - Install dependencies"
	@echo "dev-up           - Start development environment"
	@echo "dev-down         - Stop development environment"
	@echo "test             - Run all tests"
	@echo "test-unit        - Run unit tests"
	@echo "test-integration - Run integration tests"
	@echo "test-e2e         - Run end-to-end tests"
	@echo "lint             - Run linters"
	@echo "format           - Format code"
	@echo "clean            - Clean generated files"

install:
	pip install -r requirements.txt
	pre-commit install

dev-up:
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 10
	uvicorn finance_ai.frameworks.api.entry_point:app --reload

dev-down:
	docker-compose down

test:
	python -m unittest discover -s tests -p "test_*.py"

test-unit:
	python -m unittest discover -s tests/unit_tests -p "test_*.py"

test-integration:
	docker-compose up -d
	@sleep 5
	python -m unittest discover -s tests/integration -p "test_*.py"
	docker-compose down

test-e2e:
	docker-compose up -d
	@sleep 10
	python -m unittest discover -s tests/e2e -p "test_*.py"
	docker-compose down

lint:
	ruff check finance_ai/
	mypy finance_ai/

format:
	ruff format finance_ai/
	ruff check --fix finance_ai/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -rf .coverage coverage.xml

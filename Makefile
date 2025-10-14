.PHONY: help install dev-install build clean test lint format run

help:
	@echo "Media Crawler - Available commands:"
	@echo ""
	@echo "  make install        - Install package in production mode"
	@echo "  make dev-install    - Install package in development mode with dev dependencies"
	@echo "  make build          - Build distribution packages"
	@echo "  make clean          - Remove build artifacts and cache files"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run code linters"
	@echo "  make format         - Format code with black"
	@echo "  make run            - Run example crawler"
	@echo ""

install:
	pip install -e .

dev-install:
	pip install -e ".[dev,auto-chromedriver]"

build: clean
	python -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf media_crawler/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*~' -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache

test:
	pytest

lint:
	flake8 media_crawler
	mypy media_crawler

format:
	black media_crawler cli.py

run:
	python cli.py youtube -k "test" -d 1

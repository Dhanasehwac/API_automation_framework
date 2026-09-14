# API Automation Framework

Python + Pytest + Requests API automation framework.

## APIs
- Swagger Petstore
- Open-Meteo Weather API

## Run
pytest -v
pytest -v tests/test_pet.py
pytest -v tests/test_weather.py
pytest --cov=. --cov-report=html
ruff check .
ruff check . --fix

## Architecture
tests -> API classes -> reusable APIClient -> external API

Generated caches, virtual environments, logs and reports are excluded through .gitignore.

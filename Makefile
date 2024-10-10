.PHONY: start
start:
	poetry run uvicorn --app-dir=backend main:app --reload --port 8080
	uvicorn main:app --reload --port 8080

	conda create -n chatbot-4t python=3.11
	conda activate chatbot-4t
	pip freeze > requirements.txt
	pip install -r requirements.txt

.PHONY: format
format:
	poetry run ruff format .
	poetry run ruff --select I --fix .

.PHONY: lint
lint:
	poetry run ruff .
	poetry run ruff format . --diff
	poetry run ruff --select I .


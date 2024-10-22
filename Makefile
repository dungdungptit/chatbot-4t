.PHONY: start
start:
	poetry run uvicorn --app-dir=backend main:app --reload --port 8080
	uvicorn main:app --reload --port 8080

	conda create -n chatbot-4t python=3.11
	conda activate chatbot-4t
	pip freeze > requirements.txt
	pip install -r requirements.txt

	
	Pydantic upgrade

	Upgrade pydantic to the latest version

		pip install pydantic --force-reinstall

	Upgrade FastAPI to the latest version or version above 0.100.2 to fix the issue with pydantic that is related to fastapi

		pip install fastapi --force-reinstall

	Install bump-pydantic and run it via bump.sh script to convert all pydantic models to the latest version

		pip install bump-pydantic
		./bump.sh

.PHONY: format
format:
	poetry run ruff format .
	poetry run ruff --select I --fix .

.PHONY: lint
lint:
	poetry run ruff .
	poetry run ruff format . --diff
	poetry run ruff --select I .


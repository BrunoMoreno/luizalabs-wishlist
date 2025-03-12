format:
	black .

test:
	pytest

run:
	fastapi dev --reload app/main.py


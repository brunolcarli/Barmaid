install:
	pip3 install -r barmaid/requirements/${ENV_REF}.txt

run:
	python3 main.py

migrate:
	python3 -c 'from core.database import init_db; init_db()'

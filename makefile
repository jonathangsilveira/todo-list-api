# Environment
setup_venv:
	(python3 -m venv .venv && \
		source ./.venv/bin/activate)

# Requirements
setup_requirements:
	pip install -r requirements/requirements.txt

# Dot env
setup_dotenv:
	cp example.env .env

tear_down_mongo:
	docker stop todo-list-mongo
	docker network rm todo-list-mongo-network
	docker rm todo-list-mongo

setup_mongo:
	docker network create todo-list-mongo-network
	(docker run -d \
		--name todo-list-mongo \
		--network todo-list-mongo-network \
		-p 27017:27017 \
		-e MONGO_INITDB_ROOT_USERNAME=local \
		-e MONGO_INITDB_ROOT_PASSWORD=local \
		mongo:8.0.10)

run:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
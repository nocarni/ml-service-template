build:
	docker build -t app .

run: build
	docker run -p 8000:8000 app

stop:
	docker stop $(shell docker ps --filter "ancestor=app" --format "{{.ID}}")

shell:
	docker run -it app /bin/bash

hit:
	curl -X POST -d @data.json -H "Content-Type: application/json" http://localhost:8000/user/

clean: stop-all
	docker rmi $(shell docker images -f dangling=true -q)

stop-all:
	docker rm -f $(shell docker ps --filter "status=exited" -q)
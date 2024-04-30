.PHONY: start stop restart

start:
	docker-compose up --build -d

stop:
	docker-compose down --rmi local

restart:
	docker-compose restart


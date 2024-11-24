
build-producer:
	@echo "Building Docker image: cart_service:latest"
	docker build -t cart_service:latest -f ./producer/Dockerfile ./producer

build-consumer:
	@echo "Building Docker image: order_service:latest"
	docker build -t order_service:latest -f ./consumer/Dockerfile ./consumer

run-build-app:
	@echo Running Application
	docker-compose up --build

run-app:
	@echo Running Application
	docker-compose up

stop-app:
	@echo Stopping Application
	docker-compose down

logs:
	docker-compose logs
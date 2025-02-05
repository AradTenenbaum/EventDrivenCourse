
build-producer:
	@echo "Building Docker image: kafka_cart_service:latest"
	docker build -t kafka_cart_service:latest -f ./producer/Dockerfile ./producer

build-consumer:
	@echo "Building Docker image: kafka_order_service:latest"
	docker build -t kafka_order_service:latest -f ./consumer/Dockerfile ./consumer

run-build-app:
	@echo Running Application
	docker-compose up --build -d

run-app:
	@echo Running Application
	docker-compose up

stop-app:
	@echo Stopping Application
	docker-compose down

logs:
	docker-compose logs


remove-none-images:
	docker images --filter "dangling=true" -q | ForEach-Object { docker rmi $_ }


publish:
	@echo Tag images
	docker tag kafka_order_service 19871654/kafka_order_service:latest
	docker tag kafka_cart_service 19871654/kafka_cart_service:latest
	@echo Push to docker hub
	docker push 19871654/kafka_order_service:latest
	docker push 19871654/kafka_cart_service:latest
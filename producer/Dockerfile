FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY *.py .

RUN pip install -r requirements.txt

CMD ["python", "cart_service.py"]

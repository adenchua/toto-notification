FROM python:3.13.3-alpine

WORKDIR /app/toto-service

COPY ../requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ../toto_service ./toto_service
COPY ../shared ./shared

ENV PYTHONUNBUFFERED=1

CMD [ "python", "-m", "toto_service.main"]
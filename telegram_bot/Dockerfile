FROM python:3.13.3-alpine

WORKDIR /app/telegram-bot-app

COPY ../requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ../telegram_bot ./telegram_bot
COPY ../shared ./shared

ENV PYTHONUNBUFFERED=1

CMD [ "python", "-m", "telegram_bot.main"]
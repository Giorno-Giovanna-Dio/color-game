FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 建立資料庫遷移檔
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD gunicorn server.wsgi:application --bind 0.0.0.0:$PORT
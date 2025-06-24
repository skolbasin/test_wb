FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV DB_HOST=db
ENV DB_PORT=5432
ENV DB_NAME=wb_analytics
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
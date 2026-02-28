FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY task_platform task_platform/
COPY run_demo.py .

EXPOSE 8000

CMD ["uvicorn", "task_platform.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim

WORKDIR /app

# Оновлюємо pip і wheel
RUN pip install --upgrade pip wheel

# Встановлення залежностей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код у контейнер
COPY ./app /app

# Запускаємо uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

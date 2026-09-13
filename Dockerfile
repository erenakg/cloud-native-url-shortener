FROM python:3.11-slim

WORKDIR /app

# Katman önbelleklemesi (Layer Caching) için önce sadece gereksinimleri kopyalıyoruz
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyalıyoruz
COPY app/ ./app

EXPOSE 8000

# Cloud konteynerleri için sunucuyu 0.0.0.0 üzerinden dinletmek şarttır
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
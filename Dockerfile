# Hafif Python ortamı
FROM python:3.10-slim

# Çalışma klasörü
WORKDIR /app

# Önce bağımlılıkları kur (cache için)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Kodları kopyala
COPY . .

# Uygulamayı başlat
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]

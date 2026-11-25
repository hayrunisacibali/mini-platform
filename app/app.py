import os
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(message="Merhaba! Mini Platform calisiyor.")

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/load")
def load():
    # CPU'yu yorar: ileride HPA'yi tetiklemek icin kullanacagiz
    start = time.time()
    while time.time() - start < 0.5:
        sum(i * i for i in range(10000))
    return jsonify(message="CPU yuklendi")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


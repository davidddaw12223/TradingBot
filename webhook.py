from flask import Flask, request
from datetime import datetime
import csv
import os

app = Flask(__name__)

ARCHIVO_CSV = "senales.csv"

@app.route('/webhook', methods=['POST'])
def webhook():

    datos = request.json

    print("Señal recibida:")
    print(datos)

    archivo_existe = os.path.isfile(ARCHIVO_CSV)

    with open(ARCHIVO_CSV, "a", newline="") as f:

        writer = csv.writer(f)

        if not archivo_existe:
            writer.writerow([
                "fecha",
                "symbol",
                "action",
                "price"
            ])

        writer.writerow([
            datetime.now(),
            datos.get("symbol"),
            datos.get("action"),
            datos.get("price")
        ])

    return {"status": "ok"}

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
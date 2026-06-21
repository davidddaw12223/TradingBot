from flask import Flask, request
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
client = gspread.authorize(creds)

SHEET_NAME = "Señales Trading"
sheet = client.open(SHEET_NAME).sheet1

@app.route('/webhook', methods=['POST'])
def webhook():
    datos = request.json
    print("Señal recibida:", datos)
    sheet.append_row([
        str(datetime.now()),
        datos.get("ticker"),
        datos.get("action"),
        datos.get("price")
    ])
    return {"status": "ok"}

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
from flask import Flask, request
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timezone, timedelta
import os
import json

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds_json = json.loads(os.environ.get('GOOGLE_CREDENTIALS'))
creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
client = gspread.authorize(creds)

SHEET_ID = "1ml2Va7PBgkjiDGvZvD-5pwC4WHEKmOblwGbJk04fV-c"
sheet = client.open_by_key(SHEET_ID).sheet1

@app.route('/webhook', methods=['POST'])
def webhook():
    datos = request.json
    hora_espana = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%d/%m/%Y %H:%M:%S")
    sheet.append_row([
        hora_espana,
        datos.get("ticker"),
        datos.get("action"),
        datos.get("price"),
        datos.get("volume"),
        datos.get("stop_loss"),
        datos.get("take_profit"),
        datos.get("timeframe"),
        datos.get("indicator")
    ])
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
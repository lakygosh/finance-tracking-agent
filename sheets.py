import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Dinamička putanja do JSON fajla
base_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(base_dir, "creds", "agent-key.json")

creds = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
client = gspread.authorize(creds)

# Otvori postojeći sheet po imenu
sheet = client.open("MojeFinansije").sheet1

def upisi_transakciju(data: dict):
    row = [data.get("datum"), data.get("vreme"), data.get("iznos"), data.get("prodavac"), data.get("kategorija")]
    sheet.append_row(row)

from fastapi import FastAPI
from pydantic import BaseModel
from sheets import upisi_transakciju
from sms import parsiraj_sms  # Importuj funkciju iz sms.py

app = FastAPI()

class SMSInput(BaseModel):
    message: str

@app.post("/sms")
def primi_sms(input: SMSInput):
    try:
        # Pozivamo parsiranje poruke iz sms.py
        transakcija = parsiraj_sms(input.message)
        upisi_transakciju(transakcija)
        return {"status": "upisano", "data": transakcija}
    except Exception as e:
        return {"status": "greska", "poruka": str(e)}

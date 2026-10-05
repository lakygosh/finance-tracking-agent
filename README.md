# Finance Tracking Agent

A small FastAPI service that turns bank card SMS notifications into rows in a Google Sheet, for hands-off expense tracking.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=flat-square&logo=googlesheets&logoColor=white)

```mermaid
flowchart LR
    A[Bank SMS text] -->|POST /sms| B[FastAPI]
    B --> C[sms.py<br/>regex parser]
    C --> D[sheets.py<br/>gspread client]
    D --> E[(Google Sheet<br/>MojeFinansije)]
```

## Overview

My bank sends an SMS for every card payment. This project captures that text and logs the transaction without manual entry. Any client that can make an HTTP POST, such as a phone automation app, can send the raw SMS body to the `/sms` endpoint. The service extracts the amount, currency, date, and merchant, assigns a basic category, and appends a row to a Google Sheet through a service account. The project is an early-stage personal tool. Empty modules (`ocr.py`, `qr.py`, `manual.py`) mark planned input channels beyond SMS.

## Key features

- **`POST /sms` webhook** with a Pydantic-validated request body (`{"message": "..."}`).
- **SMS parsing** for Serbian bank card notifications (`POTROSNJA po kartici ... Iznos ... Datum ... Trgovac ...`). It extracts the amount, currency (RSD/EUR), date, and merchant.
- **Normalisation**: decimal commas are converted to floats and dates go from `dd.mm.yyyy` to ISO `yyyy-mm-dd`.
- **Rule-based categorisation**: EUR transactions are tagged as online purchases and RSD transactions default to a general category.
- **Google Sheets sink**: each transaction is appended as `date | time | amount | merchant | category`.
- **Structured responses**: the endpoint returns `{"status": "upisano", "data": ...}` on success and `{"status": "greska", "poruka": ...}` with the error message on failure.

## Tech stack

- **Python 3**, **FastAPI**, **Pydantic v2**, **Uvicorn**
- **gspread** and **oauth2client** (Google service-account auth)
- Google Sheets and Google Drive APIs

## Technical highlights

- **Separated layers.** HTTP handling (`main.py`), parsing (`sms.py`), and persistence (`sheets.py`) are independent modules. The parser is a pure function, `str -> dict`, so it is easy to unit-test and to swap out for new message formats.
- **Fail-loud parsing.** A message the parser does not recognise raises `ValueError` rather than writing a partial row. The endpoint turns that error into a structured JSON response.
- **Path-independent credentials.** The service-account key path is resolved relative to the module, so the app runs from any working directory.

## Getting started

### Prerequisites

- Python 3.10 or newer
- A Google Cloud service account with the Sheets and Drive APIs enabled
- A Google Sheet named `MojeFinansije`, shared with the service account's email

### Install

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install gspread oauth2client
```

### Configure

Put the service-account JSON key at `creds/agent-key.json`. The `creds/` folder is git-ignored.

### Run

```bash
uvicorn main:app --reload
```

Example request:

```bash
curl -X POST http://127.0.0.1:8000/sms \
  -H "Content-Type: application/json" \
  -d '{"message": "POTROSNJA po kartici 123456**7890 Iznos 1250,00 RSD Datum 05.10.2025 Trgovac MAXI BEOGRAD"}'
```

Interactive API docs are available at `http://127.0.0.1:8000/docs`.

## Project structure

```
finance-tracking-agent/
├── main.py          # FastAPI app, POST /sms endpoint
├── sms.py           # Bank SMS regex parser + categorisation
├── sheets.py        # Google Sheets client (gspread, service account)
├── ocr.py           # placeholder: receipt OCR (planned)
├── qr.py            # placeholder: QR receipt input (planned)
├── manual.py        # placeholder: manual entry (planned)
└── requirements.txt
```

## Author

Lazar Gošić — GitHub [@lakygosh](https://github.com/lakygosh)

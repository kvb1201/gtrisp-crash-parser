# G-TRISP Crash Report Parser

Hybrid PDF + OCR based crash report extraction pipeline.

## Features

- PDF text extraction
- OCR fallback extraction
- Hybrid text fusion
- Structured field parsing
- Excel export
- Batch PDF processing


# G-TRISP Crash Report Parser

## Overview

G-TRISP Crash Report Parser is a hybrid document-processing pipeline designed to extract structured road accident data from crash-report PDFs.

The system combines:
- PDF text extraction
- OCR-based scanned document recovery
- Regex-based deterministic parsing
- NLP-assisted fuzzy matching
- Structured Excel export

The final output is a clean analytics-ready dataset along with a human-readable formatted crash report.

---

# Problem Statement

Road accident reports are often stored as:
- unstructured PDFs
- scanned documents
- inconsistent report layouts

Manual extraction of accident information into structured datasets is:
- slow
- error-prone
- difficult to scale

This project automates the extraction and structuring of crash-report information into machine-readable formats.

---

# Features

## Dual Extraction Pipeline
- `pdfplumber` extraction for digital PDFs
- OCR extraction using `Tesseract` for scanned PDFs

## Hybrid Parsing Engine
- Regex-based field extraction
- RapidFuzz NLP-assisted fallback recovery
- Robust against OCR inconsistencies

## Structured Outputs
- Analytics-ready dataset export
- Human-readable formatted report export

## Professional Excel Export
- Multi-sheet Excel workbook
- Auto-sized columns
- Styled headers
- Freeze panes
- Clean formatting

---

# System Architecture

```text
                ┌─────────────────┐
                │   Input PDF     │
                └────────┬────────┘
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
 ┌────────────────┐           ┌────────────────┐
 │ pdfplumber     │           │ OCR Extraction │
 │ Text Extraction│           │ (Tesseract)    │
 └────────┬───────┘           └────────┬───────┘
          │                             │
          └──────────────┬──────────────┘
                         ▼
              ┌──────────────────┐
              │ Combined Text     │
              └────────┬─────────┘
                       ▼
             ┌────────────────────┐
             │ Regex Parsing      │
             └────────┬──────────┘
                      ▼
           ┌────────────────────────┐
           │ NLP Fuzzy Recovery     │
           │ (RapidFuzz Fallback)   │
           └────────┬──────────────┘
                    ▼
          ┌─────────────────────────┐
          │ Structured Dictionary    │
          └────────┬────────────────┘
                   ▼
         ┌──────────────────────────┐
         │ Excel Export Pipeline     │
         └──────────────────────────┘
```

---

# Folder Structure

```text
gtrisp-crash-parser/
│
├── input_pdfs/
│   └── sample.pdf
│
├── outputs/
│   └── crash_reports.xlsx
│
├── src/
│   ├── extract_text.py
│   ├── ocr_extract.py
│   ├── pdf_processor.py
│   ├── parse_fields.py
│   ├── fusion_engine.py
│   └── excel_export.py
│
├── run.py
├── requirements.txt
└── README.md
```

---

# Tech Stack

| Component | Technology |
|---|---|
| PDF Extraction | pdfplumber |
| OCR | Tesseract OCR |
| PDF to Image | pdf2image |
| NLP Fallback | RapidFuzz |
| Data Processing | pandas |
| Excel Formatting | openpyxl |
| Language | Python |

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd gtrisp-crash-parser
```

---

## Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Install System Dependencies

## macOS

### Install Tesseract

```bash
brew install tesseract
```

### Install Poppler

```bash
brew install poppler
```

---

# Running the Project

Place PDFs inside:

```text
input_pdfs/
```

Then run:

```bash
python run.py
```

---

# Output Files

## Excel Output

Generated at:

```text
outputs/crash_reports.xlsx
```

Contains:
- `structured_dataset`
- `formatted_report`

---

# Sample Structured Output

```python
{
    'accident_id': '2032112233445566',
    'district_name': 'Surat',
    'severity': 'Fatal',
    'road_classification': 'National Highway',
    'collision_type': 'Vehicle to Pedestrian',
    'traffic_violation': 'High Speed',
    'weather_condition': 'Sunny / Clear',
    'vehicle_type': 'Car/Jeep/Van/Taxi',
    'driver_gender': 'Male',
    'driver_age': '24'
}
```

---

# Excel Sheets

## structured_dataset

Machine-readable analytics dataset.

| accident_id | severity | district_name |
|---|---|---|
| 2032112233445566 | Fatal | Surat |

---

## formatted_report

Human-readable vertical report format.

| Field | Value |
|---|---|
| accident_id | 2032112233445566 |
| severity | Fatal |
| weather_condition | Sunny / Clear |

---

# Parsing Strategy

The system uses a layered extraction strategy:

## 1. Deterministic Regex Parsing
Primary field extraction using controlled regex patterns.

## 2. NLP-Assisted Recovery
RapidFuzz-based fuzzy matching helps recover:
- OCR typos
- formatting inconsistencies
- partially corrupted labels

This hybrid approach improves robustness while maintaining deterministic extraction quality.

---

# Future Improvements

Potential future upgrades:
- batch folder ingestion
- CSV export
- SQLite database integration
- FastAPI backend
- dashboard visualization
- confidence scoring
- advanced NLP entity extraction
- multi-format crash report support

---

# Conclusion

This project demonstrates a modular hybrid document-intelligence pipeline capable of converting unstructured crash-report PDFs into structured analytics-ready datasets.

The system combines:
- OCR
- deterministic parsing
- NLP-assisted recovery
- professional reporting exports

to create a scalable and production-style crash-report processing workflow.
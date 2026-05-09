from src.extract_text import (
    extract_text_from_pdf
)

from src.ocr_extract import (
    extract_text_with_ocr
)


def process_pdf(pdf_path):

    print("\n[INFO] Running pdfplumber extraction...")

    pdf_text = extract_text_from_pdf(pdf_path)

    print(
        f"[INFO] pdfplumber extracted "
        f"{len(pdf_text)} characters"
    )

    print("\n[INFO] Running OCR extraction...")

    ocr_text = extract_text_with_ocr(pdf_path)

    print(
        f"[INFO] OCR extracted "
        f"{len(ocr_text)} characters"
    )

    combined_text = (
        pdf_text
        + "\n"
        + ocr_text
    )

    return combined_text
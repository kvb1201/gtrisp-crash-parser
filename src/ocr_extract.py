import pytesseract

from pdf2image import convert_from_path


def extract_text_with_ocr(pdf_path):

    full_text = []

    try:

        pages = convert_from_path(pdf_path)

        for page in pages:

            text = pytesseract.image_to_string(page)

            if text:
                full_text.append(text)

    except Exception as e:

        print(f"[OCR ERROR] {e}")

    return "\n".join(full_text)
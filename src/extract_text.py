import pdfplumber


def extract_text_from_pdf(pdf_path):

    full_text = []

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if text:
                    full_text.append(text)

    except Exception as e:

        print(f"[ERROR] PDF extraction failed: {e}")

    return "\n".join(full_text)
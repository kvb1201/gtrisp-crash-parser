from pprint import pprint

from src.pdf_processor import (
    process_pdf
)

from src.parse_fields import (
    parse_crash_fields
)


PDF_PATH = "input_pdfs/sample.pdf"


text = process_pdf(PDF_PATH)


print("\n===== COMBINED EXTRACTED TEXT =====\n")

print(text[:3000])


parsed_data = parse_crash_fields(text)


print("\n===== PARSED STRUCTURED DATA =====\n")

pprint(parsed_data)
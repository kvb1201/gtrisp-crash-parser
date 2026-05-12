from pathlib import Path

import pandas as pd

from src.extract_text import extract_text_from_pdf
from src.parse_fields import parse_crash_fields


INPUT_FOLDER = "sample_reports"
OUTPUT_EXCEL = "outputs/crash_reports.xlsx"
OUTPUT_CSV = "outputs/crash_reports.csv"



def process_single_report(pdf_path):

    print(f"\n[INFO] Processing: {pdf_path.name}")

    extracted_text = extract_text_from_pdf(
        str(pdf_path)
    )

    parsed_data = parse_crash_fields(
        extracted_text
    )

    parsed_data["source_file"] = pdf_path.name

    return parsed_data



def process_report_folder(folder_path):

    folder = Path(folder_path)

    pdf_files = sorted(
        folder.glob("*.pdf")
    )

    if len(pdf_files) == 0:
        print("[ERROR] No PDF files found")
        return []

    all_reports = []

    for pdf_file in pdf_files:

        try:

            report_data = process_single_report(
                pdf_file
            )

            all_reports.append(report_data)

            print(
                f"[SUCCESS] Parsed: {pdf_file.name}"
            )

        except Exception as e:

            print(
                f"[ERROR] Failed: {pdf_file.name}"
            )

            print(str(e))

    return all_reports



def export_dataset(all_reports):

    if len(all_reports) == 0:
        print("[ERROR] No reports to export")
        return

    df = pd.DataFrame(all_reports)

    df = df.sort_index(axis=1)

    Path("outputs").mkdir(exist_ok=True)

    df.to_excel(
        OUTPUT_EXCEL,
        index=False
    )

    df.to_csv(
        OUTPUT_CSV,
        index=False
    )

    print(
        f"\n[SUCCESS] Excel exported -> {OUTPUT_EXCEL}"
    )

    print(
        f"[SUCCESS] CSV exported -> {OUTPUT_CSV}"
    )

    print(
        f"[INFO] Total Reports Processed: {len(df)}"
    )

    print(
        f"[INFO] Total Extracted Fields: {len(df.columns)}"
    )



def main():

    all_reports = process_report_folder(
        INPUT_FOLDER
    )

    export_dataset(all_reports)


if __name__ == "__main__":
    main()
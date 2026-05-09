import pandas as pd


def export_to_excel(
    records,
    output_path="outputs/crash_reports.xlsx"
):

    try:

        df = pd.DataFrame(records)

        df.to_excel(
            output_path,
            index=False
        )

        print(
            f"\n[INFO] Excel exported to: "
            f"{output_path}"
        )

    except Exception as e:

        print(
            f"\n[ERROR] Excel export failed: {e}"
        )
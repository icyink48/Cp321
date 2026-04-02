
from __future__ import annotations

from pathlib import Path
import io
from contextlib import redirect_stdout
from data_utils import RAW_CSV, CLEANED_CSV, load_and_clean


def main() -> None:
    report_path = Path(__file__).resolve().parent / "analysis_report.md"

    import pandas as pd
    raw_df = pd.read_csv(RAW_CSV)

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print("# Assignment 4 - Data Cleaning Report\n")
        print("## head()")
        print(raw_df.head().to_markdown(index=False))
        print("\n## info()")
        raw_df.info()

    cleaned_df = load_and_clean(RAW_CSV, CLEANED_CSV)

    missing_before = int(raw_df["new_vaccinations"].isna().sum())
    missing_after = int(cleaned_df["new_vaccinations"].isna().sum())

    report_text = (
        buffer.getvalue()
        + f"\n\n## Cleaning choices\n"
        + f"- Parsed the `date` column as datetime values.\n"
        + f"- Interpolated {missing_before} missing `new_vaccinations` values within each country timeline; {missing_after} missing values remain after cleaning.\n"
        + f"- Clipped mild spikes in `new_cases` and `new_vaccinations` at each country's 1st and 99th percentiles to reduce distortion from unrealistic jumps while preserving the overall trend.\n"
        + f"- Computed 3-month rolling averages for both metrics to support smoother interpretation in the app.\n"
        + f"- Saved the cleaned file to `data/COVID_Country_Sample_Cleaned.csv`.\n"
    )

    report_path.write_text(report_text, encoding="utf-8")
    print(f"Saved cleaned CSV to: {CLEANED_CSV}")
    print(f"Saved report to: {report_path}")


if __name__ == "__main__":
    main()

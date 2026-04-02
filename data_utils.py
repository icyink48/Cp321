
from __future__ import annotations

from pathlib import Path
import pandas as pd

RAW_CSV = Path(__file__).resolve().parent / "data" / "COVID_Country_Sample.csv"
CLEANED_CSV = Path(__file__).resolve().parent / "data" / "COVID_Country_Sample_Cleaned.csv"

METRIC_CONFIG = {
    "new_cases": {
        "cleaned": "new_cases_cleaned",
        "rolling": "new_cases_rolling_3",
        "label": "New COVID-19 cases",
        "short_label": "Cases",
    },
    "new_vaccinations": {
        "cleaned": "new_vaccinations_cleaned",
        "rolling": "new_vaccinations_rolling_3",
        "label": "New vaccinations",
        "short_label": "Vaccinations",
    },
}


def _clip_series_countrywise(series: pd.Series) -> pd.Series:
    """Winsorize mild spikes using the 1st and 99th percentiles."""
    lower = max(0.0, float(series.quantile(0.01)))
    upper = float(series.quantile(0.99))
    return series.clip(lower=lower, upper=upper)


def load_and_clean(raw_path: Path | str = RAW_CSV, save_path: Path | str = CLEANED_CSV) -> pd.DataFrame:
    """Load the raw CSV, clean it, and save a cleaned version for the Flask app."""
    raw_path = Path(raw_path)
    save_path = Path(save_path)

    df = pd.read_csv(raw_path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.sort_values(["country", "date"]).reset_index(drop=True)

    # Interpolate sparse missing vaccination values within each country timeline.
    df["new_vaccinations"] = (
        df.groupby("country")["new_vaccinations"]
          .transform(lambda s: s.interpolate(method="linear", limit_direction="both"))
          .fillna(0)
          .clip(lower=0)
    )

    # Clip mild spikes while preserving the general trend.
    for metric in ["new_cases", "new_vaccinations"]:
        cleaned_col = METRIC_CONFIG[metric]["cleaned"]
        rolling_col = METRIC_CONFIG[metric]["rolling"]

        df[cleaned_col] = (
            df.groupby("country")[metric]
              .transform(_clip_series_countrywise)
              .round(2)
        )

        df[rolling_col] = (
            df.groupby("country")[cleaned_col]
              .transform(lambda s: s.rolling(window=3, min_periods=1).mean())
              .round(2)
        )

    save_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(save_path, index=False)
    return df


def load_cleaned_data(cleaned_path: Path | str = CLEANED_CSV) -> pd.DataFrame:
    cleaned_path = Path(cleaned_path)
    if not cleaned_path.exists():
        return load_and_clean()

    df = pd.read_csv(cleaned_path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def build_summary(df: pd.DataFrame) -> dict:
    countries = sorted(df["country"].dropna().unique().tolist())
    return {
        "countries": countries,
        "date_min": df["date"].min().strftime("%Y-%m-%d"),
        "date_max": df["date"].max().strftime("%Y-%m-%d"),
        "default_country": countries[0] if countries else "",
        "default_metric": "new_cases",
        "metrics": list(METRIC_CONFIG.keys()),
    }

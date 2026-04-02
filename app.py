
from __future__ import annotations

from flask import Flask, jsonify, render_template, request
import plotly.graph_objects as go
from data_utils import METRIC_CONFIG, build_summary, load_cleaned_data, load_and_clean, CLEANED_CSV

app = Flask(__name__)

if not CLEANED_CSV.exists():
    load_and_clean()

df = load_cleaned_data()
summary = build_summary(df)


def get_country_metric_frame(country: str, metric: str):
    if country not in summary["countries"]:
        country = summary["default_country"]
    if metric not in METRIC_CONFIG:
        metric = summary["default_metric"]

    config = METRIC_CONFIG[metric]
    filtered = (
        df.loc[df["country"] == country, ["date", config["cleaned"], config["rolling"]]]
          .rename(columns={config["cleaned"]: "value", config["rolling"]: "rolling_mean"})
          .copy()
    )
    filtered["date"] = filtered["date"].dt.strftime("%Y-%m-%d")
    return filtered, country, metric, config


def make_figure(country: str, metric: str) -> go.Figure:
    filtered, country, metric, config = get_country_metric_frame(country, metric)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=filtered["date"],
            y=filtered["value"],
            mode="lines+markers",
            name=config["label"],
            hovertemplate="%{x}<br>%{y:,.0f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=filtered["date"],
            y=filtered["rolling_mean"],
            mode="lines",
            name="3-month rolling average",
            line=dict(dash="dash"),
            hovertemplate="%{x}<br>%{y:,.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"{config['label']} in {country}",
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title=config["label"],
        legend_title_text="",
        hovermode="x unified",
        margin=dict(l=50, r=20, t=70, b=50),
    )
    return fig


@app.route("/")
def index():
    country = request.args.get("country", summary["default_country"])
    metric = request.args.get("metric", summary["default_metric"])
    fig = make_figure(country, metric)

    insights = [
        "The chart uses cleaned monthly data from January 2020 to December 2024 for five countries.",
        "Missing vaccination values were interpolated within each country timeline instead of dropping rows, which preserves continuity.",
        "A light outlier treatment clips only the most extreme spikes so one unusual month does not dominate the scale.",
        "The dashed line shows a 3-month rolling average to make longer trends easier to read.",
        "These trends are descriptive only: a rise in cases, deaths, or vaccinations does not prove direct causation.",
    ]

    design_choices = [
        "Plotly was used for hover labels and smooth client-side updates.",
        "The y-axis label changes with the selected metric for clarity.",
        "Markers were kept on the main line so monthly points remain visible.",
        "The layout is responsive and stacks the controls on smaller screens.",
    ]

    return render_template(
        "index.html",
        summary=summary,
        plot_json=fig.to_json(),
        initial_country=country,
        initial_metric=metric,
        insights=insights,
        design_choices=design_choices,
    )


@app.route("/data")
def data():
    country = request.args.get("country", summary["default_country"])
    metric = request.args.get("metric", summary["default_metric"])
    filtered, country, metric, config = get_country_metric_frame(country, metric)

    return jsonify(
        {
            "country": country,
            "metric": metric,
            "label": config["label"],
            "records": filtered.to_dict(orient="records"),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)

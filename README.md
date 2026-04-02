
# Assignment 4 - Interactive Web Visualization with Flask & Plotly

This project is a small Flask web app that visualizes cleaned COVID-19 country data with Plotly.  
It supports country switching, metric switching, and client-side chart updates without reloading the page.

## Project structure

```text
assignment4_flask_plotly_covid/
├── app.py
├── clean_data.py
├── data_utils.py
├── analysis_report.md
├── README.md
├── screenshots.pdf
├── data/
│   ├── COVID_Country_Sample.csv
│   └── COVID_Country_Sample_Cleaned.csv
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## What was done

- Loaded the CSV with pandas and parsed the `date` column as datetime.
- Inspected the file using `head()` and `info()` (saved in `analysis_report.md`).
- Interpolated sparse missing values in `new_vaccinations`.
- Applied mild outlier clipping (1st/99th percentile within each country) to reduce unrealistic spikes.
- Computed 3-month rolling averages for `new_cases` and `new_vaccinations`.
- Built a Flask app with:
  - `/` for the dashboard
  - `/data?country=Canada&metric=new_cases` for JSON updates
- Used JavaScript `fetch()` + `Plotly.react()` to update the chart without a page reload.
- Added an Insights section and design notes under the chart.
- Included basic responsive CSS for laptop and mobile width.

## Run steps

1. Open a terminal in the project folder.
2. Install the required packages:

```bash
pip install flask plotly pandas
```

3. Generate the cleaned CSV and report (optional if the cleaned file already exists):

```bash
python clean_data.py
```

4. Start the Flask app:

```bash
flask --app app run
```

5. Open the local URL shown in the terminal, usually:

```text
http://127.0.0.1:5000/
```

## Notes for the assignment write-up

- The chart uses cleaned monthly values as the solid line.
- The dashed line is a 3-month rolling average to support easier interpretation.
- Missing vaccination values were interpolated instead of dropping rows.
- Mild spikes were clipped rather than deleted so the trend stays realistic.
- The dashboard is descriptive only: visual correlation does not imply causation.

## Deliverables included

- Flask app source files
- HTML/CSS template files
- Cleaned CSV
- Screenshot PDF
- README
- Short analysis/cleaning report

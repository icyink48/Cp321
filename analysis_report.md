# Assignment 4 - Data Cleaning Report

## head()
| date       | country   |   new_cases |   new_deaths |   new_vaccinations |   population |   cases_per_million |   vaccinations_per_hundred |
|:-----------|:----------|------------:|-------------:|-------------------:|-------------:|--------------------:|---------------------------:|
| 2020-01-01 | Canada    |         383 |            1 |                  0 |     38000000 |               10.09 |                          0 |
| 2020-02-01 | Canada    |         582 |            2 |                  0 |     38000000 |               15.32 |                          0 |
| 2020-03-01 | Canada    |         738 |           10 |                  0 |     38000000 |               19.43 |                          0 |
| 2020-04-01 | Canada    |         692 |            8 |                  0 |     38000000 |               18.24 |                          0 |
| 2020-05-01 | Canada    |         392 |            3 |                  0 |     38000000 |               10.32 |                          0 |

## info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 300 entries, 0 to 299
Data columns (total 8 columns):
 #   Column                    Non-Null Count  Dtype  
---  ------                    --------------  -----  
 0   date                      300 non-null    object 
 1   country                   300 non-null    object 
 2   new_cases                 300 non-null    int64  
 3   new_deaths                300 non-null    int64  
 4   new_vaccinations          294 non-null    float64
 5   population                300 non-null    int64  
 6   cases_per_million         300 non-null    float64
 7   vaccinations_per_hundred  300 non-null    float64
dtypes: float64(3), int64(3), object(2)
memory usage: 18.9+ KB


## Cleaning choices
- Parsed the `date` column as datetime values.
- Interpolated 6 missing `new_vaccinations` values within each country timeline; 0 missing values remain after cleaning.
- Clipped mild spikes in `new_cases` and `new_vaccinations` at each country's 1st and 99th percentiles to reduce distortion from unrealistic jumps while preserving the overall trend.
- Computed 3-month rolling averages for both metrics to support smoother interpretation in the app.
- Saved the cleaned file to `data/COVID_Country_Sample_Cleaned.csv`.

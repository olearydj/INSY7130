# Data for 11a

These unchanged local extracts are copied from the 10b lecture package so this notebook runs independently.

| File | Measurement | Source |
| --- | --- | --- |
| `aus-beer.csv` | Australian quarterly beer production, megalitres; 1956 Q1–2010 Q2 | ABS production data via [FPP Pythonic](https://otexts.com/fpppy/data/aus_production.csv), retaining `ds` and `Beer` |
| `us-nuclear-generation.csv` | Monthly US nuclear generation, GWh; January 2001–June 2024 | [Downey’s EIA snapshot](https://raw.githubusercontent.com/AllenDowney/ThinkStats/v3/data/Net_generation_for_all_sectors.csv), retaining the nuclear series |

Neither extract fills gaps or removes seasonality. The beer source is the Australian Bureau of Statistics, catalogue 8301.0.55.001 table 1. The nuclear extract selects `United States : nuclear` from Downey’s EIA snapshot, omits metadata columns, and transposes the monthly values into `month` and `generation_gwh`. Its source units, thousand megawatthours, are numerically equivalent to GWh. The snapshot carries a September 15, 2024 export timestamp. Both extracts were retrieved for the course on October 22, 2026 and copied here without changing their values.

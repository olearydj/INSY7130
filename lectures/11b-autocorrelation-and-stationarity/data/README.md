# Data for 11b

The notebook uses these local CSVs for offline execution. Source data are distributed with [FPPpy](https://otexts.com/fpppy/data/). No missing values are imputed and no observations are interpolated. Extract and upstream-download hashes are recorded in `sha256.json`.

| File | Source and Measurement | Preparation |
| --- | --- | --- |
| `aus-beer.csv` | [Australian production](https://otexts.com/fpppy/data/aus_production.csv), ABS catalogue 8301.0.55.001 table 1; quarterly beer production in megalitres | Unchanged copy of the 11a package's extract, originally retrieved October 22, 2026. Contains 218 observations from 1956 Q1 to 2010 Q2. The notebook selects the 42 observations from 2000 onward, matching FPPpy §2.7. |
| `google-2015.csv` | [GAFA stock data](https://otexts.com/fpppy/data/gafa_stock.csv); Google closing price in USD | Retrieved October 29, 2026. Select `unique_id == "GOOG_Close"` and dates in 2015; retain `ds` and rename `y` to `Close`. Contains 252 trading observations. Preserve actual trading dates; do not insert weekends or holidays. |
| `a10-monthly.csv` | [Australian Pharmaceutical Benefits Scheme data](https://otexts.com/fpppy/data/PBS_unparsed.csv); cost of antidiabetic prescriptions | Retrieved October 29, 2026. Select `ATC2 == "A10"`, sum `Cost` over all concession/payment categories within each `Month`, divide by one million, and rename `Month` to `ds`. Contains 204 monthly totals, July 1991–June 2008, in millions of Australian dollars. These are prescription costs, not prescription counts. |

The notebook's fallback performs the same selections and aggregation from the public source URLs. Since those URLs can change, the local extracts and recorded hashes define this draft's data snapshot.

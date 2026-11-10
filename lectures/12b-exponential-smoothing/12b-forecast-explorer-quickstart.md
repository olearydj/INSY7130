# Exponential Smoothing Forecast Explorer

Choose a class dataset and forecasting model, change its parameters, and step through the predictions. The controls and chart share a wide classroom view.

## Run a Downloaded Copy

Download [12b-forecast-explorer.py](12b-forecast-explorer.py). With [uv](https://docs.astral.sh/uv/) installed, run:

```sh
uvx --from 'marimo==0.25.1' marimo run --sandbox 12b-forecast-explorer.py
```

The script includes pinned dependencies. Launch once before class to allow installation. Keep the terminal open; Ctrl+C stops the app. Replace `run` with `edit` to inspect or modify the cells. This is a marimo Python app, not a Colab notebook.

For offline use, put the three [data CSVs](data/README.md) in a `data/` folder beside the script. Without local data, the app retrieves the frozen public course copies over the internet. The illustrative monthly series is built in.

## Run in the Course Workspace

From the production repository root:

```sh
uv run --locked --offline marimo run content/lectures/12b-exponential-smoothing/12b-forecast-explorer.py
```

## Choose the Experiment

- **Dataset and model:** SES, Holt, damped Holt, and additive/multiplicative Holt–Winters with optional damping. For seasonal models, select **Australian Holiday Trips**, with four quarters per cycle.
- **Starting history:** observations used to estimate initial parameters and components. Later observations update the components using fixed weights.
- **Parameter mode:** retain weights estimated on the starting history, or choose alpha (level), beta-star (slope), gamma (seasonality), and phi (damping). Manual weights apply after the starting history; the initial component estimates remain fixed. Controls for absent components are disabled.
- **Forecast horizon:** maximum number of periods projected ahead, from one to forty.

## Step Through Predictions

**Update** mode uses three frames per observation: forecast before seeing it, reveal the observation and error, then update the components. Use arrow keys on the Frame slider for individual steps. The table shows before/after components; expand Update Calculations for the arithmetic. The error ledger compares successive one-step forecasts with a naive or seasonal-naive baseline.

**Forecast** mode fixes an origin, defaulting to the end of the observed record. Move Periods Ahead (h) to reveal each successive prediction. The components stay fixed while growth accumulates and matching seasonal effects or factors repeat. The sidebar shows how those parts produce the selected prediction. Observations beyond the origin remain hidden.

## Try These Comparisons

1. Use the illustrative series with SES and twelve starting observations. Compare alpha 0.1 and 0.8 as the series rises in month 13.
2. Use population with Holt and damped Holt. In Forecast mode, extend the horizon to thirty and explain how damping changes accumulated growth.
3. Use holiday trips with additive and multiplicative Holt–Winters. Follow the seasonal positions through two forecast years. Compare effects in the original units with factors that scale the projected level.

Keep dataset, starting history, and revealed observations the same when comparing errors. These experiments support model exploration; reserve an untouched later period for a final performance claim. [Data sources and units](data/README.md) accompany the frozen historical class datasets.

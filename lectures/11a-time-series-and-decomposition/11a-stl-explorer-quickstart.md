# STL Explorer

Change STL settings for the lecture's monthly nuclear-generation data and inspect the resulting decomposition, seasonally adjusted series, and robust weights. Plots update automatically as controls change.

## Run in the Course Workspace

From the repository root:

```sh
uv run --locked --offline marimo run content/lectures/11a-time-series-and-decomposition/11a-stl-explorer.py
```

Keep the terminal open. Ctrl+C stops the app. Replace `run` with `edit` to inspect or modify its code.

## Run a Downloaded Copy

With [uv](https://docs.astral.sh/uv/) installed:

```sh
uvx --from 'marimo==0.25.1' marimo run --sandbox 11a-stl-explorer.py
```

The script includes pinned dependencies. Launch once before class to allow installation. Place [us-nuclear-generation.csv](data/us-nuclear-generation.csv) in a `data/` folder beside the script for offline use. Without that local file, the app reads the published course copy over the internet. This is a Python marimo app; open it with marimo rather than as a Colab notebook.

## Controls and Views

- **Period:** observations per cycle. Use 12 for annual seasonality in monthly data; 6 and 24 demonstrate different assumed cycles.
- **Seasonal window:** smoothing across repeated cycle positions. At period 12, these are successive occurrences of the same calendar month. Larger windows favor slower seasonal change.
- **Trend window:** smoothing over consecutive months. Uncheck automatic selection to adjust it.
- **Low-pass window:** an advanced smoothing control that helps separate slower movement from seasonality. Leave automatic selection on initially.
- **Robust fitting:** reduces unusual observations' influence on the smoothers. Compare its effects while holding the windows fixed.
- **Lecture fit:** overlays a fixed reference using period 12, seasonal 13, automatic trend and low-pass windows, and robust fitting. It stays unchanged as you experiment.
- **Years displayed:** zooms the charts. Fits always use all 282 observations, including when only one year is shown. The 2024 record ends in June.

Use the **View** dropdown beside the chart to choose the compact 2×2 decomposition overview, one enlarged component (trend-cycle, seasonal, or remainder), seasonal adjustment, or robust weights. Changing fit settings retains the selected view. The decomposition panels use different vertical scales; both fits share a scale within each panel.

On wide screens, the controls and current chart share one row. The control column stays beside the chart and scrolls independently if browser zoom or a short display makes the controls too tall. For classroom projection, choose a single component when the overview labels become too small. Narrow portrait screens stack the controls and chart instead.

Period and low-pass controls are under **Advanced: period / low-pass**. Longer explanations, comparison prompts, data attribution, and the current Python call are in expandable sections below the main display. Effective window lengths remain directly below the chart. Slider values are restricted to valid odd windows; changing the period resets the manual window controls.

## Verification

The app passes `marimo check --strict` and Ruff checks. Programmatic marimo execution covers the lecture defaults, manual window extremes, all three periods, robust fitting on and off, and single-year display ranges. Reconstruction checks verify that the components sum to the observations; changing only the display range leaves the fit unchanged. Marimo’s HTML export completed successfully, and static plots were inspected. Browser interaction has not been tested.

November 3 layout revision: replaced the vertically separated controls and tall four-row plot with one responsive controls/chart view, a shallow 2×2 overview, and enlarged single-component views. Programmatic checks exercised all six views across periods 6/12/24, manual/automatic windows, both robust and overlay states, full-history and single-year ranges, and component reconstruction. HTML export and static-figure review passed. The fit logic and starting reference are unchanged. Actual browser layout, scrolling, and projected readability still require a manual check; no browser automation was used.

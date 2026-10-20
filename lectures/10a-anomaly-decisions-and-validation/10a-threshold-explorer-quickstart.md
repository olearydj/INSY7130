# Threshold Explorer

Move an anomaly-score threshold and inspect the selected wines, confusion matrix, precision, and recall. Compare LOF and Isolation Forest at the same review capacity. Low sensory ratings supply an external comparison criterion; the detectors use chemistry alone.

## Run It

Download [10a-threshold-explorer.py](10a-threshold-explorer.py) and [evidence-scores.csv](evidence-scores.csv) into the same folder. With [uv](https://docs.astral.sh/uv/) installed, open a terminal in that folder and run:

```sh
uvx --from 'marimo==0.25.1' marimo run --sandbox 10a-threshold-explorer.py
```

The script includes pinned dependencies. Launch once before class to allow installation. Keep the terminal open; Ctrl+C stops the app. Replace `run` with `edit` to inspect its code.

## Controls

- Select LOF or Isolation Forest. Each starts at its fiftieth-highest score.
- Drag the vertical boundary, click the score plot, or use the keyboard-accessible slider. The shaded region contains flagged records.
- Counts update while dragging. Release the boundary to update the detailed matrix, plots, and nearby-record table.
- Use the 25, 50, 100, All, and None buttons to compare workloads. Tied scores are selected together, so a requested capacity can include additional records.

The model and scores remain fixed when the threshold moves. Larger scores mean more unusual; the methods use different score scales.

## Data

Scores describe the 1,599 red-wine records in the [UCI Wine Quality dataset](https://archive.ics.uci.edu/dataset/186/wine+quality), contributed by Cortez and colleagues under CC BY 4.0. The [data notes](data/README.md) provide attribution and measurement context. The [lecture notebook](10a-anomaly-investigation.ipynb) recomputes scores from the included data. Keep its `data/` folder beside it when downloading the notebook.

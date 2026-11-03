# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo==0.25.1",
#     "numpy==2.5.2",
#     "pandas==3.0.5",
#     "matplotlib==3.11.1",
#     "statsmodels==0.14.6",
# ]
# ///

# ruff: noqa: E501, B018

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="full", app_title="STL Explorer: Nuclear Generation")


@app.cell(hide_code=True)
def _():
    from pathlib import Path
    from urllib.request import urlopen

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from statsmodels.tsa.seasonal import STL

    return Path, STL, mo, np, pd, plt, urlopen


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## STL Explorer · Nuclear Generation
    """)
    return


@app.cell(hide_code=True)
def _(Path, mo, pd, urlopen):
    _file = Path(mo.notebook_location()) / "data/us-nuclear-generation.csv"
    if _file.exists():
        _frame = pd.read_csv(_file)
    else:
        _url = "https://raw.githubusercontent.com/olearydj/INSY7130/main/lectures/11a-time-series-and-decomposition/data/us-nuclear-generation.csv"
        with urlopen(_url, timeout=30) as _response:
            _frame = pd.read_csv(_response)
    _frame["month"] = pd.to_datetime(_frame["month"], format="%b %Y")
    nuclear = _frame.set_index("month")["generation_gwh"]
    assert nuclear.index.equals(pd.date_range("2001-01-01", "2024-06-01", freq="MS"))
    assert nuclear.notna().all()
    return (nuclear,)


@app.cell(hide_code=True)
def _(STL, nuclear):
    baseline = STL(nuclear, period=12, seasonal=13, robust=True).fit()
    return (baseline,)


@app.cell(hide_code=True)
def _(mo):
    period = mo.ui.dropdown([6, 12, 24], value=12, label="Period (months per cycle)")
    seasonal = mo.ui.slider(7, 35, step=2, value=13, show_value=True, label="Seasonal window", full_width=True)
    robust = mo.ui.checkbox(True, label="Robust fitting")
    auto_trend = mo.ui.checkbox(True, label="Automatic trend window")
    auto_low = mo.ui.checkbox(True, label="Automatic low-pass window")
    compare = mo.ui.checkbox(True, label="Lecture overlay")
    years = mo.ui.range_slider(2001, 2024, step=1, value=[2007, 2016], show_value=True, label="Years displayed", full_width=True)
    view = mo.ui.dropdown(
        ["Decomposition", "Trend-cycle", "Seasonal", "Remainder", "Seasonal adjustment", "Robust weights"],
        value="Decomposition", label="View", full_width=True,
    )
    return auto_low, auto_trend, compare, period, robust, seasonal, view, years


@app.cell(hide_code=True)
def _(auto_low, auto_trend, mo, period):
    _minimum = period.value + 1
    trend = mo.ui.slider(_minimum, 85, step=2, value=max(21, _minimum), show_value=True, disabled=auto_trend.value, label="Trend window (months)", full_width=True)
    low_pass = mo.ui.slider(_minimum, 49, step=2, value=_minimum, show_value=True, disabled=auto_low.value, label="Low-pass window (months)", full_width=True)
    return low_pass, trend


@app.cell(hide_code=True)
def _(
    STL,
    auto_low,
    auto_trend,
    low_pass,
    np,
    nuclear,
    period,
    robust,
    seasonal,
    trend,
):
    settings = dict(
        period=period.value,
        seasonal=seasonal.value,
        trend=None if auto_trend.value else trend.value,
        low_pass=None if auto_low.value else low_pass.value,
        robust=robust.value,
    )
    model = STL(nuclear, **settings)
    fit = model.fit()
    np.testing.assert_allclose(fit.trend + fit.seasonal + fit.resid, nuclear)
    return fit, model, settings


@app.cell(hide_code=True)
def _(baseline, compare, fit, nuclear, plt, view, years):
    import matplotlib.dates as mdates

    _start, _end = (str(int(v)) for v in years.value)
    _slice = slice(_start, _end)
    _fields = {"Trend-cycle": ("trend", "C1"), "Seasonal": ("seasonal", "C2"), "Remainder": ("resid", "C3")}
    # Wide, shallow figures leave room for readable controls on a projector.
    with plt.rc_context({"font.size": 12, "axes.spines.top": False, "axes.spines.right": False}):
        if view.value == "Decomposition":
            figure, _axes = plt.subplots(2, 2, figsize=(10, 4.8), layout="constrained")
            _panels = list(zip(_axes.flat, ["Observed", *_fields], strict=True))
            plot_note = "All values in GWh. Panels have different vertical scales; both fits share a scale within each panel."
        else:
            figure, _ax = plt.subplots(figsize=(10, 4.8), layout="constrained")
            _panels = [(_ax, view.value)]
            plot_note = "Gray dashed: fixed lecture fit. Colored: current fit."

        for _ax, _label in _panels:
            if _label == "Observed":
                _ax.plot(nuclear.loc[_slice], color="0.45", lw=1.3)
            elif _label in _fields:
                _field, _color = _fields[_label]
                if compare.value:
                    _ax.plot(getattr(baseline, _field).loc[_slice], color="0.55", ls="--", lw=1.3, label="Lecture fit")
                _ax.plot(getattr(fit, _field).loc[_slice], color=_color, lw=1.6, label="Current fit")
                if _field != "trend":
                    _ax.axhline(0, color="0.8", lw=0.7)
                _ax.legend(loc="upper right", fontsize=10)
            elif _label == "Seasonal adjustment":
                _ax.plot(nuclear.loc[_slice], color="0.75", lw=1.1, label="Observed")
                if compare.value:
                    _ax.plot((nuclear - baseline.seasonal).loc[_slice], color="0.45", ls="--", lw=1.2, label="Adjusted: lecture")
                _ax.plot((nuclear - fit.seasonal).loc[_slice], color="C0", lw=1.6, label="Adjusted: current")
                _ax.plot(fit.trend.loc[_slice], color="C1", lw=2, label="Current trend")
                _ax.legend(loc="upper right", fontsize=10, ncol=2)
                plot_note = "Observed − seasonal = trend-cycle + remainder. Seasonal adjustment retains unusual departures."
            else:
                _ax.plot(fit.weights.loc[_slice], color="C3", marker=".", lw=0.7)
                _ax.set_ylim(-0.05, 1.05)
                plot_note = "Small weights reduce influence on robust smoothers; they are not error probabilities. Robust off: all weights equal one."
            _ax.set_title(_label, loc="left", fontsize=13)
            _ax.set_ylabel("Weight" if _label == "Robust weights" else "GWh")
            _locator = mdates.AutoDateLocator(minticks=3, maxticks=5)
            _ax.xaxis.set_major_locator(_locator)
            _ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(_locator))
        plt.close(figure)
    return figure, plot_note


@app.cell(hide_code=True)
def _(
    auto_low,
    auto_trend,
    compare,
    figure,
    low_pass,
    mo,
    model,
    period,
    plot_note,
    robust,
    seasonal,
    trend,
    view,
    years,
):
    _config = model.config
    _controls = mo.vstack([
        view,
        seasonal,
        auto_trend,
        trend,
        mo.hstack([robust, compare], wrap=True, justify="start"),
        years,
        mo.accordion({"Advanced: period / low-pass": mo.vstack([
            period, auto_low, low_pass,
            mo.md("Use period 12 for annual seasonality. Other periods deliberately assume a different cycle. Manual windows must be odd and greater than the period."),
        ])}),
    ], gap=0.45)
    _status = f"**Effective windows:** seasonal {_config['seasonal']} · trend {_config['trend']} · low-pass {_config['low_pass']}"
    if period.value != 12:
        _status += f" · **Experimental period: {period.value} months**"
    _plot = mo.vstack([figure, mo.md(plot_note), mo.md(_status)], gap=0.1)
    # The controls scroll independently on short/zoomed displays; the chart stays alongside.
    mo.Html(
        """<style>
        .stl-layout {display:flex; align-items:flex-start; gap:1rem; width:100%;}
        .stl-controls {flex:0 0 clamp(200px, 24vw, 250px); position:sticky; top:0.5rem;
          max-height:calc(100dvh - 100px); overflow-y:auto; padding:0.25rem 0.75rem 0.5rem 0;}
        .stl-chart {flex:1 1 0; min-width:0;}
        .stl-chart img {max-width:100%; height:auto;}
        @media (max-width:700px) and (orientation:portrait) {
          .stl-layout {flex-direction:column;}
          .stl-controls {position:static; flex:auto; width:100%; max-height:none; overflow:visible;}
          .stl-chart {width:100%;}
        }
        </style>"""
        + f'<div class="stl-layout"><aside class="stl-controls">{_controls.text}</aside>'
        + f'<section class="stl-chart">{_plot.text}</section></div>'
    )
    return


@app.cell(hide_code=True)
def _(mo, settings):
    _call = "STL(nuclear, " + ", ".join(f"{k}={v!r}" for k, v in settings.items()) + ").fit()"
    mo.accordion({
        "What the controls mean": mo.md("""
        - **Seasonal window:** larger values favor slower changes across cycles. At period 12, the smoother uses successive occurrences of the same calendar month, not consecutive months.
        - **Trend window:** larger values produce a smoother trend-cycle. Turn off automatic selection to choose the window.
        - **Low-pass window:** helps separate slower movement from seasonality; usually leave automatic.
        - **Years displayed:** changes only the visible range. Every fit uses all 282 monthly observations, January 2001–June 2024.
        - **Lecture overlay:** fixed `period=12`, `seasonal=13`, `robust=True` fit with automatic trend and low-pass windows. Changing controls never updates this reference.
        """),
        "Current Python call": mo.md(f"```python\n{_call}\n```"),
        "Try these comparisons": mo.md("""
        - Keep period 12, turn off automatic trend selection, hold trend at 21, and vary the seasonal window. Inspect the **Seasonal** view.
        - Hold seasonality fixed and vary the trend window. Compare **Trend-cycle** and **Remainder**.
        - Hold windows fixed, show 2011–2013, and toggle robust fitting. Inspect **Robust weights** and **Remainder**.
        - Switch to **Seasonal adjustment**. Which changes persist after recurring seasonality is removed?

        A smaller remainder alone does not identify a better decomposition. Ask whether the estimated components make sense for the analytical question.
        """),
        "Data and references": mo.md("""
        Monthly US nuclear generation in GWh, using the same series as lecture 11a. Starting settings match the lecture.

        Data: [Allen Downey's EIA snapshot](https://raw.githubusercontent.com/AllenDowney/ThinkStats/v3/data/Net_generation_for_all_sectors.csv), used in [Think Stats, Chapter 12](https://allendowney.github.io/ThinkStats/chap12.html). [Local data notes](data/README.md). [Statsmodels STL parameters](https://www.statsmodels.org/stable/generated/statsmodels.tsa.seasonal.STL.html).
        """),
    })
    return


if __name__ == "__main__":
    app.run()

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

# Ruff: preserve readable Markdown paragraphs and marimo's display expressions.
# ruff: noqa: E501, B018
import marimo

__generated_with = "0.25.1"
app = marimo.App(width="full", app_title="12b Forecast Explorer")


@app.cell
def _():
    from pathlib import Path
    from urllib.request import urlopen

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from statsmodels.tsa.holtwinters import ExponentialSmoothing

    return ExponentialSmoothing, Path, mo, np, pd, plt, urlopen


@app.cell
def _(mo):
    mo.md("""
    # Forecast, Observe, Update

    In 12b, exponential smoothing updates a level, and sometimes a slope and seasonal estimates, as observations arrive. Here you control how quickly those components change and inspect the forecast made **before** each observation.

    Choose a dataset and model. **Update** mode steps through **forecast → observe → update** as new observations arrive. **Forecast** mode holds the components fixed at a chosen origin and steps through future horizons. For seasonal models, select **Australian Holiday Trips**, which has four quarters per cycle.
    """)
    return


@app.cell
def _(Path, np, pd, urlopen):
    datasets = {
        "Illustrative Monthly Series": (None, "Value", 1),
        "Algerian Exports": ("algerian-exports.csv", "Exports (% of GDP)", 1),
        "Australian Population": ("australian-population.csv", "Population (millions)", 1),
        "Australian Holiday Trips": ("australian-holiday-trips.csv", "Trips (millions)", 4),
    }
    models = {
        "SES": (False, None, False),
        "Holt": (True, None, False),
        "Damped Holt": (True, None, True),
        "Additive Holt–Winters": (True, "add", False),
        "Multiplicative Holt–Winters": (True, "mul", False),
        "Damped Additive Holt–Winters": (True, "add", True),
        "Damped Multiplicative Holt–Winters": (True, "mul", True),
    }

    def load_series(name):
        filename, units, period = datasets[name]
        if filename is None:
            values = np.array(
                [
                    30.0,
                    32.0,
                    29.0,
                    31.0,
                    33.0,
                    30.0,
                    32.0,
                    31.0,
                    34.0,
                    32.0,
                    33.0,
                    32.0,
                    38.0,
                    41.0,
                    39.0,
                    43.0,
                    40.0,
                    42.0,
                    39.0,
                    41.0,
                ]
            )
            return values, [f"Month {i + 1}" for i in range(len(values))], units, period
        roots = [
            Path(__file__).resolve().parent,
            Path.cwd(),
            Path("content/lectures/12b-exponential-smoothing"),
            Path("lectures/12b-exponential-smoothing"),
        ]
        source = next(
            (root / "data" / filename for root in roots if (root / "data" / filename).is_file()),
            None,
        )
        if source is None:
            url = (
                "https://raw.githubusercontent.com/olearydj/INSY7130/main/"
                "lectures/12b-exponential-smoothing/data/" + filename
            )
            with urlopen(url, timeout=30) as response:
                raw = pd.read_csv(response)
        else:
            raw = pd.read_csv(source)
        values = raw.iloc[:, 1].to_numpy(dtype=float)
        if "Population" in name:
            values = values / 1_000_000
        if "Trips" in name:
            values = values / 1_000
        return values, raw.iloc[:, 0].astype(str).tolist(), units, period

    return datasets, load_series, models


@app.cell
def _(datasets, mo):
    dataset = mo.ui.dropdown(list(datasets), value="Illustrative Monthly Series", label="Dataset")
    dataset
    return (dataset,)


@app.cell
def _(dataset, load_series, mo, models):
    values, labels, units, period = load_series(dataset.value)
    available_models = list(models)
    model = mo.ui.dropdown(
        available_models, value="Additive Holt–Winters" if period > 1 else "SES", label="Model"
    )
    start = mo.ui.slider(
        12,
        len(values),
        value=12 if len(values) == 20 else len(values) - 12,
        step=1,
        show_value=True,
        label="Observations in Starting History",
    )
    horizon = mo.ui.slider(1, 40, value=8, step=1, show_value=True, label="Forecast Horizon")
    mo.vstack(
        [
            model,
            start,
            horizon,
            mo.md(
                f"**{dataset.value}** · {units} · "
                + (
                    "4 quarters per seasonal cycle."
                    if period == 4
                    else "For seasonal models, choose Australian Holiday Trips (quarterly, cycle = 4)."
                )
            ),
        ]
    )
    return horizon, labels, model, period, start, units, values


@app.cell
def _(ExponentialSmoothing, mo, model, models, period, start, values):
    has_trend, seasonal, damped = models[model.value]
    mo.stop(
        seasonal is not None and period < 2,
        mo.callout(
            "Select Australian Holiday Trips for this seasonal model. It has four quarterly observations per cycle; the other class series have no specified seasonal cycle.",
            kind="info",
        ),
    )
    reference = ExponentialSmoothing(
        values[: start.value],
        trend="add" if has_trend else None,
        seasonal=seasonal,
        seasonal_periods=period if seasonal else None,
        damped_trend=damped,
        initialization_method="estimated",
        bounds={"damping_trend": (0.8, 0.98)} if damped else None,
    ).fit()
    return damped, has_trend, reference, seasonal


@app.cell
def _(damped, has_trend, mo, reference, seasonal):
    mode = mo.ui.radio(
        ["Estimated on Starting History", "Choose Weights"],
        value="Choose Weights",
        inline=True,
        label="Parameter Mode",
    )
    alpha = mo.ui.slider(0.0, 1.0, step=0.05, value=0.3, show_value=True, label="Alpha: Level")
    beta = mo.ui.slider(
        0.0,
        1.0,
        step=0.05,
        value=0.2,
        show_value=True,
        disabled=not has_trend,
        label="Beta-star: Slope",
    )
    gamma = mo.ui.slider(
        0.0,
        1.0,
        step=0.05,
        value=0.1,
        show_value=True,
        disabled=seasonal is None,
        label="Gamma: Seasonality",
    )
    phi = mo.ui.slider(
        0.8, 1.0, step=0.01, value=0.9, show_value=True, disabled=not damped, label="Phi: Damping"
    )
    fit_ok = bool(reference.mle_retvals.get("success", True))
    return alpha, beta, fit_ok, gamma, mode, phi


@app.cell
def _(alpha, beta, fit_ok, gamma, mo, mode, phi):
    mo.vstack(
        [
            mode,
            mo.hstack([alpha, beta], widths="equal")
            if mode.value == "Choose Weights"
            else mo.md(""),
            mo.hstack([gamma, phi], widths="equal")
            if mode.value == "Choose Weights"
            else mo.md(""),
            mo.md(
                "The model is fitted using only the starting history. Its final components are the starting point for this exploration. In **Choose Weights**, the sliders apply to subsequent updates; the starting components stay fixed. In the estimated mode, the fitted weights stay fixed as new observations arrive. Neither mode refits at each step. Changing the dataset, model, or starting history starts a new experiment."
            ),
            mo.callout(
                "The initial fit did not converge. Try a longer starting history or another model; interpret these estimates cautiously.",
                kind="warn",
            )
            if not fit_ok
            else mo.md(""),
        ]
    )
    return


@app.cell
def _(alpha, beta, damped, gamma, has_trend, mode, phi, reference, seasonal):
    manual = mode.value == "Choose Weights"
    weights = {
        "alpha": alpha.value if manual else float(reference.params["smoothing_level"]),
        "beta": (beta.value if manual else float(reference.params["smoothing_trend"]))
        if has_trend
        else 0.0,
        "gamma": (gamma.value if manual else float(reference.params["smoothing_seasonal"]))
        if seasonal
        else 0.0,
        "phi": (phi.value if manual else float(reference.params["damping_trend"]))
        if damped
        else 1.0,
    }
    return (weights,)


@app.cell
def _(np):
    def forecast_path(state, steps, weights, has_trend, seasonal):
        level, slope, seasons = state
        ahead = np.arange(1, steps + 1)
        growth = np.cumsum(weights["phi"] ** ahead) * slope if has_trend else np.zeros(steps)
        base = level + growth
        if seasonal:
            effects = np.resize(seasons, steps)
            return base + effects if seasonal == "add" else base * effects
        return base

    def update_state(state, observation, weights, has_trend, seasonal):
        level, slope, seasons = state
        base = level + weights["phi"] * slope if has_trend else level
        adjusted = observation
        if seasonal == "add":
            adjusted -= seasons[0]
        elif seasonal == "mul":
            if base <= 0 or seasons[0] <= 0:
                raise ValueError(
                    "Multiplicative updates need positive level-and-slope projections and seasonal factors. Try smaller weights or another model."
                )
            adjusted /= seasons[0]
        new_level = weights["alpha"] * adjusted + (1 - weights["alpha"]) * base
        new_slope = (
            (weights["beta"] * (new_level - level) + (1 - weights["beta"]) * weights["phi"] * slope)
            if has_trend
            else 0.0
        )
        new_seasons = seasons.copy()
        if seasonal:
            signal = observation - base if seasonal == "add" else observation / base
            effect = weights["gamma"] * signal + (1 - weights["gamma"]) * seasons[0]
            new_seasons = np.r_[seasons[1:], effect]
        return new_level, new_slope, new_seasons

    def replay(observations, state, weights, has_trend, seasonal):
        states, predictions = [state], []
        for observation in observations:
            predictions.append(forecast_path(states[-1], 1, weights, has_trend, seasonal)[0])
            states.append(update_state(states[-1], observation, weights, has_trend, seasonal))
        return states, np.array(predictions)

    return forecast_path, replay


@app.cell
def _(
    forecast_origin,
    frame,
    has_trend,
    mo,
    np,
    period,
    reference,
    replay,
    seasonal,
    start,
    values,
    view_mode,
    weights,
):
    initial_state = (
        float(reference.level[-1]),
        float(reference.trend[-1]) if has_trend else 0.0,
        np.asarray(reference.season[-period:], dtype=float).copy() if seasonal else np.array([]),
    )
    replay_error = None
    try:
        revealed_count = (
            forecast_origin.value - start.value
            if view_mode.value == "Forecast"
            else frame.value // 3 + int(frame.value % 3 >= 1)
        )
        states, predictions = replay(
            values[start.value : start.value + revealed_count],
            initial_state,
            weights,
            has_trend,
            seasonal,
        )
        if not all(
            np.isfinite(s[0]) and np.isfinite(s[1]) and np.isfinite(s[2]).all() for s in states
        ):
            replay_error = "These settings produce non-finite components. Try smaller weights or another model."
    except ValueError as exc:
        states, predictions = [], np.array([])
        replay_error = str(exc)
    mo.stop(replay_error is not None, mo.callout(replay_error or "", kind="warn"))
    return predictions, states


@app.cell
def _(mo, start, values):
    frame = mo.ui.slider(
        0,
        3 * (len(values) - start.value),
        value=0,
        step=1,
        show_value=True,
        full_width=True,
        include_input=True,
        label="Frame",
    )
    return (frame,)


@app.cell
def _(mo):
    view_mode = mo.ui.radio(["Update", "Forecast"], value="Update", inline=True, label="View")
    return (view_mode,)


@app.cell
def _(horizon, mo, start, values):
    forecast_origin = mo.ui.slider(
        start.value,
        len(values),
        value=len(values),
        step=1,
        show_value=True,
        full_width=True,
        include_input=True,
        label="Observations Available at Forecast Origin",
    )
    forecast_step = mo.ui.slider(
        1,
        horizon.value,
        value=1,
        step=1,
        show_value=True,
        full_width=True,
        include_input=True,
        label="Periods Ahead (h)",
    )
    return forecast_origin, forecast_step


@app.cell
def _(
    forecast_path,
    forecast_origin,
    frame,
    has_trend,
    horizon,
    labels,
    np,
    seasonal,
    start,
    states,
    values,
    view_mode,
    weights,
):
    step, phase = (
        (forecast_origin.value - start.value, 0)
        if view_mode.value == "Forecast"
        else divmod(frame.value, 3)
    )
    origin = start.value + step
    final = origin == len(values)
    observed = not final and phase >= 1
    updated = not final and phase == 2
    incorporated = origin + int(updated)
    visible = origin + int(observed)
    before = states[step]
    after = states[step + 1] if updated else before
    old_path = forecast_path(before, horizon.value, weights, has_trend, seasonal)
    new_path = (
        forecast_path(after, horizon.value, weights, has_trend, seasonal) if updated else old_path
    )
    baseline = np.array(
        [values[i - 4] if seasonal else values[i - 1] for i in range(start.value, visible)]
    )
    phase_name = "Update" if updated else "Observe" if observed else "Forecast"
    next_label = labels[origin] if not final else "Next Period"
    return (
        after,
        baseline,
        before,
        final,
        incorporated,
        new_path,
        next_label,
        observed,
        old_path,
        origin,
        phase_name,
        updated,
        visible,
    )


@app.cell
def _(
    after,
    before,
    final,
    frame,
    forecast_origin,
    forecast_step,
    has_trend,
    labels,
    mo,
    next_label,
    observed,
    old_path,
    origin,
    phase_name,
    seasonal,
    units,
    updated,
    values,
    view_mode,
    weights,
):
    _text = f"### {phase_name}: {next_label}\n\nForecast made beforehand: **{old_path[0]:.3f}** {units}."
    if observed:
        _error = values[origin] - old_path[0]
        _text += f" Observation: **{values[origin]:.3f}**. Error (observed − forecast): **{_error:+.3f}**."
    elif not final:
        _text += " The next observation is hidden. What do you expect the update to do?"
    else:
        _text += (
            " All recorded observations have been incorporated; future observations are unknown."
        )
    if view_mode.value == "Forecast":
        _h = forecast_step.value
        _growth = (
            sum(weights["phi"] ** j for j in range(1, _h + 1)) * before[1] if has_trend else 0.0
        )
        _text = (
            f"### Forecast: {_h} Period{'s' if _h != 1 else ''} Ahead\n\n"
            f"History through **{labels[origin - 1]}**. "
            f"Point forecast: **{old_path[_h - 1]:.3f}** {units}. "
            "The origin stays fixed while h advances. No future observations enter these predictions."
        )
        _text += f"\n\nLevel {before[0]:.3f} + accumulated growth {_growth:.3f} = **{before[0] + _growth:.3f}**."
        if seasonal:
            _effect = before[2][(_h - 1) % len(before[2])]
            _text += f" Then {'add the seasonal effect' if seasonal == 'add' else 'multiply by the seasonal factor'} **{_effect:.3f}** for the matching season."
    _rows = [
        {
            "Component": "Level",
            "Before Observation": before[0],
            "After Update": after[0] if updated else None,
        }
    ]
    if has_trend:
        _rows.append(
            {
                "Component": "Slope per Period",
                "Before Observation": before[1],
                "After Update": after[1] if updated else None,
            }
        )
    if seasonal:
        _rows.append(
            {
                "Component": "Matching Seasonal Effect"
                if seasonal == "add"
                else "Matching Seasonal Factor",
                "Before Observation": before[2][0],
                "After Update": after[2][-1] if updated else None,
            }
        )
    _calc = ""
    if updated:
        _base = before[0] + weights["phi"] * before[1] if has_trend else before[0]
        _adjusted = (
            values[origin] - before[2][0]
            if seasonal == "add"
            else values[origin] / before[2][0]
            if seasonal == "mul"
            else values[origin]
        )
        _calc = (
            f"**Level update:** {weights['alpha']:.3f} × {_adjusted:.3f} + "
            f"(1 − {weights['alpha']:.3f}) × {_base:.3f} = **{after[0]:.3f}**. "
            "The first value is the seasonally adjusted observation when seasonality is included; the second is the previous level plus the damped slope, when a slope is included."
        )
        if has_trend:
            _calc += (
                f"\n\n**Slope update:** {weights['beta']:.3f} × "
                f"({after[0]:.3f} − {before[0]:.3f}) + "
                f"(1 − {weights['beta']:.3f}) × {weights['phi']:.3f} × "
                f"{before[1]:.3f} = **{after[1]:.3f}**."
            )
        if seasonal:
            _signal = values[origin] - _base if seasonal == "add" else values[origin] / _base
            _calc += (
                f"\n\n**Seasonal update:** {weights['gamma']:.3f} × {_signal:.3f} + "
                f"(1 − {weights['gamma']:.3f}) × {before[2][0]:.3f} = "
                f"**{after[2][-1]:.3f}**. The seasonal signal is the observation "
                + ("minus" if seasonal == "add" else "divided by")
                + " the previous level-and-slope projection. This revises the matching season; the next forecast uses the next season in the cycle."
            )
    _table = "| Component | Before | After |\n| :-- | --: | --: |\n"
    for _row in _rows:
        _after = _row["After Update"]
        _after_text = f"{_after:.3f}" if _after is not None else "—"
        _table += f"| {_row['Component']} | {_row['Before Observation']:.3f} | {_after_text} |\n"
    _controls = (
        [view_mode, forecast_origin, forecast_step]
        if view_mode.value == "Forecast"
        else [
            view_mode,
            frame,
            mo.md("**Forecast → Observe → Update** · Use arrow keys for one frame at a time."),
        ]
    )
    step_panel = mo.vstack(
        [
            *_controls,
            mo.md(_text),
            mo.md(_table) if view_mode.value == "Update" else mo.md(""),
        ],
        gap=0.5,
    ).style({"position": "sticky", "top": "1rem", "align-self": "start"})
    update_calculation = (
        mo.accordion({"Update Calculations": mo.md(_calc)}) if updated else mo.md("")
    )
    return step_panel, update_calculation


@app.cell
def _(
    forecast_step,
    has_trend,
    incorporated,
    labels,
    model,
    new_path,
    np,
    observed,
    old_path,
    origin,
    phase_name,
    plt,
    seasonal,
    start,
    states,
    units,
    updated,
    values,
    visible,
    view_mode,
):
    fig, axes = plt.subplots(
        2 if has_trend or seasonal else 1,
        1,
        figsize=(10, 4.6 if has_trend or seasonal else 4.0),
        gridspec_kw={"height_ratios": [3, 1]} if has_trend or seasonal else None,
        squeeze=False,
    )
    ax = axes[0, 0]
    ax.axvspan(-0.5, incorporated - 0.5, color="tab:blue", alpha=0.08, label="Incorporated History")
    ax.axvline(start.value - 0.5, color="0.5", ls=":", label="Starting History Ends")
    ax.plot(np.arange(visible), values[:visible], "o-", color="0.3", ms=3, label="Observed")
    _shown = forecast_step.value if view_mode.value == "Forecast" else len(old_path)
    ax.plot(
        np.arange(origin, origin + _shown),
        old_path[:_shown],
        "s--",
        color="tab:orange",
        ms=4,
        label="Forecast Made Beforehand",
    )
    if view_mode.value == "Forecast":
        ax.plot(
            origin + _shown - 1,
            old_path[_shown - 1],
            "s",
            color="tab:orange",
            ms=9,
            label=f"Current Horizon: {_shown}",
        )
    if observed:
        ax.plot(
            [origin, origin],
            [old_path[0], values[origin]],
            ":",
            color="tab:red",
            label="Forecast Error",
        )
    if updated:
        ax.plot(
            np.arange(origin + 1, origin + 1 + len(new_path)),
            new_path,
            "D-.",
            color="tab:green",
            ms=3,
            label="Forecast After Update",
        )
    _levels = [s[0] for s in states[: incorporated - start.value + 1]]
    ax.plot(
        np.arange(start.value - 1, incorporated),
        _levels,
        "D--",
        color="tab:green",
        ms=3,
        alpha=0.7,
        label="Updated Level",
    )
    ax.set_ylabel(units)
    ax.set_title(f"{model.value}: {phase_name}", pad=48)
    # Fixed horizontal extent; vertical limits use only visible data and issued forecasts.
    _right = (origin if view_mode.value == "Forecast" else len(values)) + len(old_path)
    _ticks = np.unique(np.linspace(0, _right - 1, 7, dtype=int))
    ax.set_xlim(-0.5, _right)
    ax.set_xticks(
        _ticks, [labels[t] if t < len(labels) else f"+{t - len(labels) + 1}" for t in _ticks]
    )
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.01), fontsize=8, ncol=3)
    if has_trend or seasonal:
        _component_ax = axes[1, 0]
        _x = np.arange(start.value - 1, incorporated)
        if has_trend:
            _component_ax.plot(
                _x, [s[1] for s in states[: len(_x)]], "o-", color="tab:purple", label="Slope"
            )
            _component_ax.set_ylabel("Slope per Period")
        if seasonal:
            _season_ax = _component_ax.twinx() if has_trend else _component_ax
            _sx = np.arange(start.value, incorporated)
            _season_ax.plot(
                _sx,
                [s[2][-1] for s in states[1 : len(_sx) + 1]],
                "D--",
                color="tab:brown",
                label="Updated Seasonal Component",
            )
            _season_ax.set_ylabel("Seasonal Effect" if seasonal == "add" else "Seasonal Factor")
            _season_ax.legend(loc="upper right", fontsize=8)
        _component_ax.set_xlim(start.value - 1.5, len(values))
        _component_ax.set_xlabel("Observation Position (Starting at 0)")
        if has_trend:
            _component_ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    plt.close(fig)
    return (fig,)


@app.cell
def _(fig, mo, step_panel, update_calculation):
    mo.vstack(
        [
            mo.md("## Step Through the Predictions"),
            mo.hstack(
                [step_panel, mo.as_html(fig)],
                widths=[1, 2.5],
                align="start",
                gap=1.5,
            ),
            update_calculation,
        ],
        gap=0.5,
    )
    return


@app.cell
def _(
    baseline,
    labels,
    mo,
    np,
    pd,
    predictions,
    seasonal,
    start,
    units,
    values,
    visible,
    view_mode,
    weights,
):
    mo.stop(
        view_mode.value == "Forecast",
        mo.md(
            "**Fixed-origin forecast:** the orange points extend the current level, slope, and matching seasonal estimates. Move **Periods Ahead (h)** to inspect each prediction. Switch to **Update** to reveal observations and compare one-step errors."
        ),
    )
    ledger = pd.DataFrame(
        {
            "Period": labels[start.value : visible],
            "Observed": values[start.value : visible],
            "Forecast Made Beforehand": predictions[: visible - start.value],
            "Baseline": baseline,
        }
    )
    ledger["Error (Observed − Forecast)"] = ledger["Observed"] - ledger["Forecast Made Beforehand"]
    _summary = "Reveal an observation to begin the error record."
    if len(ledger):
        _mae = np.mean(np.abs(ledger["Error (Observed − Forecast)"]))
        _baseline_mae = np.mean(np.abs(ledger["Observed"] - ledger["Baseline"]))
        _summary = f"Across {len(ledger)} revealed predictions, model MAE = **{_mae:.3f}**, baseline MAE = **{_baseline_mae:.3f}** {units}."
    mo.vstack(
        [
            mo.md(
                "## Inspect the Evidence\n\n"
                + _summary
                + " The baseline is "
                + (
                    "seasonal naive: the observation four quarters earlier."
                    if seasonal
                    else "naive: the latest observation."
                )
                + " These are successive one-step forecasts with updates between them. The longer plotted path holds the components fixed at one origin. Changing the plotted horizon does not change these one-step scores."
            ),
            mo.ui.table(
                ledger.round(3),
                selection=None,
                show_column_summaries=False,
                show_data_types=False,
                page_size=8,
            ),
            mo.md(
                f"**Active weights:** alpha {weights['alpha']:.3f}; beta-star {weights['beta']:.3f}; gamma {weights['gamma']:.3f}; phi {weights['phi']:.3f}. Unused weights have no effect. Gamma uses the lecture's previous level-and-slope seasonal update."
            ),
            mo.md("""
        ## Try a Controlled Comparison

        - **Responsiveness:** use the illustrative series with SES and 12 starting observations. Compare alpha 0.1 and 0.8. Predict the response to the rise in month 13 before revealing it.
        - **Trend and damping:** use Australian population. Compare SES, Holt, and damped Holt with the same starting history. Extend the horizon to 30 and explain which component creates the difference.
        - **Seasonality:** use holiday trips. Compare additive and multiplicative Holt–Winters, then change gamma while holding the other settings fixed. Which quarter's seasonal estimate changes at each update?

        Keep the same dataset, starting history, and revealed periods when comparing errors. Exploring these outcomes helps choose a model; it does not provide an untouched final evaluation set. Reserve a later period before making a final performance claim.

        Methods follow [Forecasting: Principles and Practice, Chapter 8](https://otexts.com/fpp3/exponential-smoothing.html). Initial fits use [statsmodels ExponentialSmoothing](https://www.statsmodels.org/stable/generated/statsmodels.tsa.holtwinters.ExponentialSmoothing.html). Historical class data and attribution are in [the data README](https://github.com/olearydj/INSY7130/blob/main/lectures/12b-exponential-smoothing/data/README.md).
        """),
        ]
    )
    return


if __name__ == "__main__":
    app.run()

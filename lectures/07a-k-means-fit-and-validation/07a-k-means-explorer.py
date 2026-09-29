# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.25,<0.26",
#     "matplotlib>=3.10,<4",
#     "numpy>=2.4,<3",
#     "scikit-learn>=1.8,<2",
# ]
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # K-Means: Change One Choice

    These are the same 72 simulated customers used in 06b and 07a. Each point
    records requests last term and average minutes per request. The data have no
    planted customer types. Change one control at a time and watch what K-means
    does to the **same observations**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    groups = mo.ui.slider(start=2, stop=6, step=1, value=2, show_value=True, label="Groups (K)")
    space = mo.ui.dropdown(
        options=["Standardized", "Original units"],
        value="Standardized",
        label="Distance measured in",
    )
    starts = mo.ui.dropdown(
        options=["1", "20"], value="1", label="Complete starts (n_init)"
    )
    seed_button = mo.ui.button(
        value=7, on_click=lambda seed: seed + 1, label="Try next seed"
    )
    mo.vstack([mo.hstack([groups, space, starts]), seed_button])
    return groups, seed_button, space, starts


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Try these comparisons:** Move $K$ from 2 to 3, then switch the distance
    space at $K=2$. With standardized distances and one start, try several seeds;
    then switch to 20 starts. When do the fitted regions change?
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import ListedColormap
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    from sklearn.preprocessing import StandardScaler

    rng = np.random.default_rng(7130)
    customers = np.column_stack(
        (rng.integers(1, 13, size=72), rng.integers(8, 65, size=72))
    )
    return KMeans, ListedColormap, StandardScaler, customers, np, plt, silhouette_score


@app.cell
def _(KMeans, StandardScaler, customers, groups, seed_button, space, starts):
    scaler = StandardScaler().fit(customers) if space.value == "Standardized" else None
    fitted_points = scaler.transform(customers) if scaler is not None else customers.astype(float)
    model = KMeans(
        n_clusters=groups.value,
        init="k-means++",
        n_init=int(starts.value),
        random_state=seed_button.value,
    ).fit(fitted_points)
    centers_in_original_units = (
        scaler.inverse_transform(model.cluster_centers_)
        if scaler is not None
        else model.cluster_centers_
    )
    return centers_in_original_units, fitted_points, model, scaler


@app.cell(hide_code=True)
def _(ListedColormap, centers_in_original_units, customers, groups, mo, model, np, plt, scaler):
    x_values = np.linspace(0.5, 12.5, 260)
    y_values = np.linspace(5, 67, 260)
    grid_x, grid_y = np.meshgrid(x_values, y_values)
    grid_in_original_units = np.column_stack((grid_x.ravel(), grid_y.ravel()))
    grid_for_model = (
        scaler.transform(grid_in_original_units)
        if scaler is not None
        else grid_in_original_units
    )
    regions = model.predict(grid_for_model).reshape(grid_x.shape)

    colors = ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#AA3377", "#66CCEE"]
    fig, ax = plt.subplots(figsize=(9, 5), layout="constrained")
    ax.contourf(
        grid_x,
        grid_y,
        regions,
        levels=np.arange(-0.5, groups.value + 0.5, 1),
        cmap=ListedColormap(colors[: groups.value]),
        alpha=0.22,
    )
    ax.contour(
        grid_x,
        grid_y,
        regions,
        levels=np.arange(0.5, groups.value - 0.5, 1),
        colors="0.35",
        linewidths=0.8,
    )
    for group in range(groups.value):
        members = customers[model.labels_ == group]
        ax.scatter(members[:, 0], members[:, 1], color=colors[group], s=35, alpha=0.85)
    ax.scatter(
        centers_in_original_units[:, 0],
        centers_in_original_units[:, 1],
        marker="X",
        color="black",
        s=150,
        label="Fitted centers",
    )
    ax.scatter(
        *customers[21],
        marker="*",
        color="#FFCC33",
        edgecolor="black",
        s=240,
        label="Customer 22",
    )
    for group, center in enumerate(centers_in_original_units):
        ax.annotate(str(group), center, xytext=(7, 6), textcoords="offset points")
    ax.set(
        xlim=(x_values.min(), x_values.max()),
        ylim=(y_values.min(), y_values.max()),
        xlabel="Requests last term",
        ylabel="Average minutes per request",
        title="Fitted groups and nearest-center regions",
    )
    ax.grid(alpha=0.15)
    ax.legend(loc="upper right")
    mo.output.append(mo.as_html(fig))
    return


@app.cell(hide_code=True)
def _(fitted_points, groups, mo, model, seed_button, silhouette_score, space, starts):
    silhouette = silhouette_score(fitted_points, model.labels_)
    mo.md(
        f"**This fit:** $K={groups.value}$; distance measured in **{space.value.lower()}**; "
        f"**{starts.value}** complete start(s); seed **{seed_button.value}**. "
        f"Inertia is **{model.inertia_:.1f}** and "
        f"mean silhouette is **{silhouette:.2f}**.\n\n"
        "A lower inertia at a larger $K$ is expected; it does not prove that the added "
        "group is useful. Inertia values from original and standardized coordinates use "
        "different units, so compare them only while the distance space stays fixed. "
        "Group numbers are arbitrary names."
    )
    return


if __name__ == "__main__":
    app.run()

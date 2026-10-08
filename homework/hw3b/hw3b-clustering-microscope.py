# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo==0.25.0",
#     "matplotlib==3.11.1",
#     "numpy==2.5.2",
#     "pandas==3.0.5",
#     "scikit-learn==1.9.0",
#     "scipy==1.18.0",
#     "threadpoolctl==3.6.0",
# ]
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="full", app_title="HW3B · Wholesale Customers")


@app.cell
def imports():
    import base64
    import gzip
    import hashlib
    import io
    import json
    import warnings
    from dataclasses import dataclass
    from html import escape

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy.cluster.hierarchy import cut_tree, dendrogram, fcluster, linkage
    from sklearn.cluster import DBSCAN, KMeans
    from sklearn.mixture import GaussianMixture
    from sklearn.preprocessing import StandardScaler
    from threadpoolctl import threadpool_limits

    return (
        DBSCAN,
        GaussianMixture,
        KMeans,
        StandardScaler,
        base64,
        cut_tree,
        dataclass,
        dendrogram,
        escape,
        fcluster,
        gzip,
        hashlib,
        io,
        json,
        linkage,
        mo,
        np,
        pd,
        plt,
        threadpool_limits,
        warnings,
    )


@app.cell
def data(base64, gzip, hashlib, io, np, pd, StandardScaler):
    # Exact HW3B student CSV, compressed for a standalone offline data source.
    # Cardoso (2013), UCI Wholesale Customers, DOI 10.24432/C5030X, CC BY 4.0.
    encoded_csv = (
        "H4sIAAAAAAAC/zWby44lS1JF5/4tMYjwt88RjJD4A4SaErSAbnRvM4CvZ63teSdVmXki/GHPbdvs/Ol/fv/bX//r"
        "12///Od/ff7+t1+///vzj3/+z/94/uG3v/7p12//y5/++n+//vL83a+//frt33795W+///M//ct///qNP/znn//0"
        "L7///usv5Xu+Oud5zhzzWWN+T/36U+fqz9faLvVZ71jP2d/7nDH3861Zn1ZP46c1S3tmG+3Z+93PmptX+zueNj5W"
        "270Xl6lzPN935tNr/Z7Z3/6Md/H+3mU8tc5vPKOzwfrOftrhV9Zez/j2KPM5/WODOg5/qPOZc/Lx4Zk+vsIy1b+2"
        "75xnnjWevl9+6y9LjsKhxjpP5+isw3Ofl22Nc9QxZ2HNM9vTZt/P/E7liG7u6cdbONJ8X176Xu+790ZcHwdZPlbf"
        "s8v3sRonGv3liXqQW+8vm5/lDZHAVxHB112l8uGoPNerx/Ncq3C5xo4IqnIJnuLET93raW6HoL+iRrjmemZFzF8/"
        "GxW8iGAu5DjfWhBZ7RNFnK6wOZqvKuexeXdyUA7wVp74PpZrGwm0g2InZ/pYYPnxiyJ90N04tcd1w3cji/2MvRD/"
        "5/FOQyUNSa6X+y6W5+R7vqi3VZd6UUetmEJdk6t8+yusvhbKqWjDc/ZHXdThyi8fs+MayAm1IhluxTJItqp5DtRL"
        "rc8YrLYXl3tRDgaK8ND5mKdU5chuz3e4TO8adef0tSHG3hrva9htRd08zfE+bWp0P+bQE92UGovsSGa5VlsYRdUk"
        "e0fqgxuUmBFPYyyNO42jLbDHiwmMVarugiEfnWnzT/sGP/WKxFhfBXrMzdPt7RrsUGCae6nc/MMi6tv1JZZeWtx+"
        "kC3arC8eh8Tbu1UrL9X5HvX9aqSIhhu0T1PlxG1+/tm/o3NfQKMVey+NO00Mk3ujQxydDVlxo6KDz/n7hyI1XF7b"
        "Gy2gicMveHfJKsujLj5ZTaf8OBb7aSssz4WG+jtLK5jXrbrKOrzO42yG/X/xrE+5KEsWbNxP8zpj+AsC7wrMzbbL"
        "zMoD/IH4ol1iDly+62qHs8+Bs+JKxaWGyw/f/HATnZ74wPPcuRgdpo482OfE0l7+xcrU9Sxdfb2emVDBNY2AI8JE"
        "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"
        "/v9OJvYJhTgAAA=="
    )
    source_bytes = gzip.decompress(base64.b64decode(encoded_csv))
    data_hash = hashlib.sha256(source_bytes).hexdigest()
    assert data_hash == "ef299e835566ae5f77143ff3ea4d8d1972e10c0fae1e5fec5e9553a52e34a69a"
    customers = pd.read_csv(io.BytesIO(source_bytes)).set_index("customer_id")
    features = ["Fresh", "Milk", "Grocery", "Frozen", "Detergents_Paper", "Delicassen"]
    X = StandardScaler().fit_transform(np.log1p(customers[features]))
    return X, customers, data_hash, features


@app.cell
def analysis_tools(
    DBSCAN,
    GaussianMixture,
    KMeans,
    cut_tree,
    dataclass,
    fcluster,
    linkage,
    np,
    pd,
    threadpool_limits,
    warnings,
):
    @dataclass
    class Fit:
        method: str
        settings: dict
        labels: object
        rows: object
        profiles: object
        tree: object
        probabilities: object
        converged: object
        messages: list

    def fit_customers(customers, X, features, method, settings):
        """Fit all six features once; views and selections never enter this function."""
        tree = None
        probabilities = None
        converged = None
        with threadpool_limits(limits=2), warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            if method == "K-means":
                model = KMeans(
                    n_clusters=settings["count"],
                    n_init=settings["starts"],
                    random_state=settings["seed"],
                ).fit(X)
                labels = model.labels_
            elif method == "Hierarchy":
                tree = linkage(X, method=settings["linkage"], metric="euclidean")
                if settings["cut"] == "Count":
                    labels = cut_tree(tree, n_clusters=settings["count"]).ravel()
                else:
                    labels = fcluster(tree, t=settings["height"], criterion="distance") - 1
            elif method == "DBSCAN":
                model = DBSCAN(
                    eps=settings["eps"],
                    min_samples=settings["min_samples"],
                ).fit(X)
                labels = model.labels_
            elif method == "Gaussian mixture":
                model = GaussianMixture(
                    n_components=settings["count"],
                    covariance_type=settings["covariance"],
                    n_init=settings["starts"],
                    random_state=settings["seed"],
                ).fit(X)
                labels = model.predict(X)
                probabilities = model.predict_proba(X)
                converged = bool(model.converged_)
            else:
                raise ValueError(method)
        rows = customers.copy()
        rows["Group"] = labels
        if probabilities is not None:
            for component in range(probabilities.shape[1]):
                rows[f"P(C{component})"] = probabilities[:, component]
            rows["Maximum membership"] = probabilities.max(axis=1)
        grouped = rows.groupby("Group")
        profiles = grouped[features].median()
        profiles.insert(0, "Customers", grouped.size())
        return Fit(
            method,
            dict(settings),
            labels,
            rows,
            profiles,
            tree,
            probabilities,
            converged,
            [str(w.message) for w in caught],
        )

    def selection_summary(customers, fit, features, mask, active):
        """Distinguish cleared selection from an active region containing zero points."""
        selected = customers.loc[mask]
        medians = pd.DataFrame(
            {
                "Selected": selected[features].median(),
                "All": customers[features].median(),
            }
        )
        medians["Difference (%)"] = 100 * (medians["Selected"] / medians["All"] - 1)
        groups = (
            pd.DataFrame(
                {
                    "Selected": pd.Series(fit.labels[mask]).value_counts(),
                    "All": pd.Series(fit.labels).value_counts(),
                }
            )
            .fillna(0)
            .astype(int)
            .sort_index()
        )
        return {
            "active": bool(active),
            "count": int(mask.sum()),
            "medians": medians,
            "groups": groups,
            "rows": fit.rows.loc[mask],
        }

    return Fit, fit_customers, selection_summary


@app.cell(hide_code=True)
def header(mo):
    mo.md("""
    ## HW3B · Wholesale Customers
    **Fit six spending categories. Inspect two at a time.** Select customers to compare
    their purchases with all 440 accounts. Selection changes the summaries, not the fit.
    """)
    return


@app.cell(hide_code=True)
def method_control(mo):
    method = mo.ui.dropdown(
        ["K-means", "Hierarchy", "DBSCAN", "Gaussian mixture"],
        value="K-means",
        label="Method",
    )
    return (method,)


@app.cell
def parameter_controls(method, mo):
    # Rebuild on method changes so each method opens at the homework baseline.
    if method.value == "K-means":
        fields = {
            "count": mo.ui.number(2, 8, value=3, label="Groups"),
            "starts": mo.ui.number(1, 50, value=20, label="Initializations"),
            "seed": mo.ui.number(0, 99999, value=7130, label="Seed"),
        }
    elif method.value == "Hierarchy":
        fields = {
            "linkage": mo.ui.dropdown(
                ["complete", "single", "average", "ward"],
                value="complete",
                label="Linkage",
            ),
            "cut": mo.ui.dropdown(["Count", "Height"], value="Count", label="Cut by"),
            "count": mo.ui.number(2, 8, value=3, label="Groups (count cut)"),
            "height": mo.ui.number(0, 100, value=10.0, step=0.1, label="Height (height cut)"),
        }
    elif method.value == "DBSCAN":
        fields = {
            "eps": mo.ui.slider(0.05, 2.5, value=0.8, step=0.05, label="Radius"),
            "min_samples": mo.ui.number(2, 40, value=8, label="Minimum count"),
        }
    else:
        fields = {
            "count": mo.ui.number(2, 8, value=3, label="Components"),
            "covariance": mo.ui.dropdown(
                ["full", "tied", "diag", "spherical"],
                value="full",
                label="Covariance",
            ),
            "starts": mo.ui.number(1, 50, value=10, label="Initializations"),
            "seed": mo.ui.number(0, 99999, value=7130, label="Seed"),
        }
    parameters = mo.ui.dictionary(fields)
    return (parameters,)


@app.cell(hide_code=True)
def axes_controls(features, mo):
    x_axis = mo.ui.dropdown(features, value="Fresh", label="Horizontal")
    y_axis = mo.ui.dropdown(features, value="Grocery", label="Vertical")
    return x_axis, y_axis


@app.cell(hide_code=True)
def controls_display(method, parameters, x_axis, y_axis, mo):
    mo.vstack(
        [
            mo.hstack([method, *parameters.values()], justify="start", gap=1, wrap=True),
            mo.hstack([x_axis, y_axis], justify="start", gap=1),
        ],
        gap=0.25,
    )
    return


@app.cell
def model_cell(X, customers, features, fit_customers, method, parameters):
    fit = fit_customers(customers, X, features, method.value, parameters.value)
    return (fit,)


@app.cell
def display_tools(escape, np, plt):
    colors = [
        "#0072B2",
        "#D55E00",
        "#009E73",
        "#CC79A7",
        "#E69F00",
        "#56B4E9",
        "#8073AC",
        "#444444",
    ]

    def group_name(group):
        return "Noise" if int(group) == -1 else f"Group {int(group)}"

    def group_color(group):
        return "#8a8a8a" if int(group) == -1 else colors[int(group) % len(colors)]

    def scatter_figure(customers, fit, x_name, y_name):
        # Linear plot coordinates are log10(spending); ticks display original units.
        # This keeps lasso polygon geometry exact even on a logarithmic spending view.
        x = np.log10(customers[x_name].to_numpy())
        y = np.log10(customers[y_name].to_numpy())
        fig, ax = plt.subplots(figsize=(6.3, 4.25), layout="constrained")
        for group in np.unique(fit.labels):
            mask = fit.labels == group
            ax.scatter(
                x[mask],
                y[mask],
                color=group_color(group),
                marker="x" if group == -1 else "o",
                s=23,
                alpha=0.75,
                linewidths=0.7,
                label=group_name(group),
            )
        ticks = [0, 1, 2, 3, 4, 5]
        tick_labels = ["1", "10", "100", "1,000", "10,000", "100,000"]
        ax.set_xticks(ticks, tick_labels)
        ax.set_yticks(ticks, tick_labels)
        ax.set_xlim(x.min() - 0.13, x.max() + 0.13)
        ax.set_ylim(y.min() - 0.13, y.max() + 0.13)
        ax.set_xlabel(f"{x_name.replace('_', ' / ')} spending (m.u.; log axis)")
        ax.set_ylabel(f"{y_name.replace('_', ' / ')} spending (m.u.; log axis)")
        ax.grid(alpha=0.12)
        ax.set_axisbelow(True)
        ax.set_title(f"{fit.method} · all six features fitted", fontsize=11, loc="left")
        # Group counts/colors live in the adjacent summary, avoiding a crowded legend.
        return fig, ax, x, y

    def compact_table(table, formats=None):
        formats = formats or {}
        headers = "".join(f"<th>{escape(str(c))}</th>" for c in table.columns)
        rows = []
        for index, row in table.iterrows():
            cells = []
            for name, value in row.items():
                if value is None or (isinstance(value, (float, np.floating)) and np.isnan(value)):
                    text = "—"
                else:
                    text = formats.get(name, lambda v: str(v))(value)
                cells.append(f"<td>{escape(text)}</td>")
            rows.append(f"<tr><th>{escape(str(index))}</th>{''.join(cells)}</tr>")
        return (
            '<table class="hw3b-table"><thead><tr><th></th>'
            + headers
            + "</tr></thead><tbody>"
            + "".join(rows)
            + "</tbody></table>"
        )

    def summary_html(summary, fit):
        active, count = summary["active"], summary["count"]
        heading = f"Selected: {count} / 440 customers" if active else "Select customers on the plot"
        caption = (
            "No customers in this region."
            if active and not count
            else "Selected and all-customer medians · original monetary units"
        )
        badges = []
        for group, row in summary["groups"].iterrows():
            selected_count = str(int(row["Selected"])) if active else "—"
            badges.append(
                '<span class="hw3b-badge">'
                f'<i style="background:{group_color(group)}"></i>{group_name(group)} '
                f"<b>{selected_count}</b> / {int(row['All'])}"
                "</span>"
            )
        median_table = summary["medians"].rename(index={"Detergents_Paper": "Detergents / paper"})
        table = compact_table(
            median_table,
            {
                "Selected": lambda v: f"{v:,.1f}",
                "All": lambda v: f"{v:,.1f}",
                "Difference (%)": lambda v: f"{v:+.0f}%",
            },
        )
        extra = ""
        if fit.probabilities is not None:
            selected_max = summary["rows"]["Maximum membership"]
            value = f"{selected_max.median():.3f}" if count else "—"
            extra = (
                f"<p>Median maximum membership: <b>{value}</b> selected / "
                f"{np.median(fit.probabilities.max(axis=1)):.3f} all.</p>"
            )
        return (
            '<section class="hw3b-summary"><h3>' + heading + "</h3>"
            '<p class="hw3b-small">Group counts: selected / all. Colors match the plot.</p>'
            '<div class="hw3b-badges">' + "".join(badges) + "</div>"
            f'<p class="hw3b-small">{caption}</p>' + table + extra + "</section>"
        )

    return compact_table, group_color, group_name, scatter_figure, summary_html


@app.cell(hide_code=True)
def plot_cell(customers, fit, mo, plt, scatter_figure, x_axis, y_axis):
    _figure, _axes, plot_x, plot_y = scatter_figure(customers, fit, x_axis.value, y_axis.value)
    scatter = mo.ui.matplotlib(_axes, debounce=False)
    plt.close(_figure)
    return plot_x, plot_y, scatter


@app.cell
def selected_cell(customers, features, fit, plot_x, plot_y, scatter, selection_summary):
    selection_active = bool(scatter.value)
    selection_mask = scatter.value.get_mask(plot_x, plot_y)
    summary = selection_summary(customers, fit, features, selection_mask, selection_active)
    return selection_active, selection_mask, summary


@app.cell(hide_code=True)
def main_view(fit, mo, scatter, summary, summary_html):
    _assigned = int((fit.labels != -1).sum())
    _groups = len(set(fit.labels) - {-1})
    _convergence = "" if fit.converged is None else f" · GMM converged: {fit.converged}"
    mo.vstack(
        [
            mo.md(
                f"**{_groups} groups · {_assigned}/440 assigned · {440 - _assigned} noise**"
                + _convergence
                + "  \nDrag a rectangle; Shift-drag a lasso. "
                + "Drag inside a selection to move it; Escape clears it."
            ),
            mo.hstack(
                [scatter, mo.Html(summary_html(summary, fit))],
                widths=[1.15, 1],
                align="start",
                gap=1,
                wrap=True,
            ),
        ],
        gap=0.25,
    )
    return


@app.cell(hide_code=True)
def styling(mo):
    mo.Html("""
    <style>
    .hw3b-summary {font-variant-numeric:tabular-nums; padding:0.4rem 0.7rem;
      border:1px solid #b8c8ce; border-radius:8px; min-width:330px;}
    .hw3b-summary h3 {margin:0 0 0.3rem; font-size:1.1rem;}
    .hw3b-small {font-size:0.8rem; margin:0.4rem 0; opacity:0.85;}
    .hw3b-table {width:100%; border-collapse:collapse; font-size:0.85rem;}
    .hw3b-table td,.hw3b-table th {padding:0.27rem 0.35rem; text-align:right;
      border-bottom:1px solid #dce3e6; white-space:nowrap;}
    .hw3b-table th:first-child {text-align:left; font-weight:500;}
    .hw3b-table thead th {font-size:0.76rem; font-weight:650;}
    .hw3b-badges {display:flex; flex-wrap:wrap; gap:0.25rem 0.65rem; font-size:0.8rem;
      max-height:4.8rem; overflow:auto;}
    .hw3b-badge i {display:inline-block; width:0.65rem; height:0.65rem;
      border-radius:50%; margin-right:0.2rem;}
    </style>
    """)
    return


@app.cell(hide_code=True)
def details(customers, features, fit, group_name, mo, summary):
    _profiles = fit.profiles.rename(index=group_name).round(1).reset_index()
    _selected_rows = summary["rows"].reset_index()
    mo.accordion(
        {
            "All fitted groups · counts and median spending": mo.vstack(
                [
                    mo.md(
                        "Medians describe hard-assigned customers. Noise is not an extra cluster."
                    ),
                    mo.ui.table(
                        _profiles, selection=None, page_size=10, show_column_summaries=False
                    ),
                ]
            ),
            "Selected customers · original spending and memberships": mo.ui.table(
                _selected_rows,
                selection=None,
                page_size=8,
                show_column_summaries=False,
            ),
        }
    )
    return


@app.cell(hide_code=True)
def tree_view(dendrogram, fit, mo, np, plt):
    if fit.tree is not None:
        _fig, _ax = plt.subplots(figsize=(9, 3.5), layout="constrained")
        dendrogram(fit.tree, truncate_mode="lastp", p=24, show_leaf_counts=True, ax=_ax)
        if fit.settings["cut"] == "Height":
            _height = fit.settings["height"]
        else:
            _k = fit.settings["count"]
            _lower = fit.tree[-_k, 2]
            _upper = fit.tree[-(_k - 1), 2]
            _height = (_lower + _upper) / 2 if _lower < _upper else np.nan
        if np.isfinite(_height):
            _ax.axhline(_height, linestyle="--", color="black", linewidth=1)
        _ax.set_ylabel("Linkage distance")
        _ax.set_xlabel("24 leaves; parentheses show customer counts")
        mo.accordion(
            {
                "Dendrogram · current cut": mo.vstack(
                    [
                        mo.md(
                            "The dashed line marks the cut where representable by height. "
                            "Branch colors use a display threshold, not group labels."
                        ),
                        mo.as_html(_fig),
                    ]
                ),
            }
        )
        plt.close(_fig)
    return


@app.cell(hide_code=True)
def export_record(data_hash, features, fit, json, mo, summary, x_axis, y_axis):
    _record = {
        "method": fit.method,
        "settings": fit.settings,
        "data_sha256": data_hash,
        "fit_features": features,
        "representation": "StandardScaler(log1p(spending))",
        "view": {"x": x_axis.value, "y": y_axis.value},
        "group_profiles": json.loads(fit.profiles.reset_index().to_json(orient="records")),
        "selection_active": summary["active"],
        "selected_count": summary["count"],
        "selected_customer_ids": summary["rows"].index.tolist(),
        "selection_medians": json.loads(summary["medians"].reset_index().to_json(orient="records")),
        "converged": fit.converged,
        "warnings": fit.messages,
    }
    mo.hstack(
        [
            mo.download(
                json.dumps(_record, indent=2).encode(),
                filename="hw3b-experiment.json",
                mimetype="application/json",
                label="Download this setting and findings",
            ),
            mo.download(
                summary["rows"].to_csv().encode(),
                filename="hw3b-selected-customers.csv",
                mimetype="text/csv",
                label="Download selected rows",
            ),
        ],
        justify="start",
        gap=1,
        wrap=True,
    )
    return


@app.cell(hide_code=True)
def provenance(fit, mo):
    if fit.messages:
        mo.output.append(mo.callout("; ".join(fit.messages), kind="warn"))
    mo.output.append(
        mo.md(
            "440 real wholesale accounts · annual spending in unspecified monetary units. "
            "[Cardoso (2013), UCI](https://doi.org/10.24432/C5030X), "
            "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). "
            "Channel and Region are excluded. The account-review scenario is proposed for HW3B. "
            "Group numbers/colors belong to each fit. Changing method or axes clears selection."
        )
    )
    return


if __name__ == "__main__":
    app.run()

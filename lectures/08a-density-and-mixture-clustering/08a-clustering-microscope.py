# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo==0.25.0",
#     "matplotlib==3.11.2",
#     "numpy==2.5.3",
#     "pandas==3.0.6",
#     "scikit-learn==1.9.1",
#     "scipy==1.18.1",
#     "threadpoolctl==3.7.0",
#     "wigglystuff==0.5.32",
# ]
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="full", app_title="08a Clustering Microscope")


@app.cell
def imports():
    from dataclasses import dataclass

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from matplotlib.colors import ListedColormap, to_hex
    from matplotlib.patches import Ellipse
    from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
    from scipy.spatial.distance import cdist
    from sklearn.cluster import DBSCAN, KMeans
    from sklearn.mixture import GaussianMixture
    from sklearn.preprocessing import StandardScaler
    from threadpoolctl import threadpool_limits

    thread_limit = threadpool_limits(limits=2)
    from sklearn.datasets import make_blobs, make_circles, make_moons
    from sklearn.metrics import silhouette_samples
    from wigglystuff import TangleSlider

    return (
        DBSCAN,
        GaussianMixture,
        StandardScaler,
        Ellipse,
        thread_limit,
        KMeans,
        ListedColormap,
        TangleSlider,
        cdist,
        dataclass,
        dendrogram,
        fcluster,
        linkage,
        make_blobs,
        make_circles,
        make_moons,
        mo,
        np,
        pd,
        plt,
        silhouette_samples,
        to_hex,
    )


@app.cell(hide_code=True)
def title(mo):
    mo.Html("""
    <div style="border-left:5px solid #0f766e;padding:0.3rem 1.1rem;margin:0.3rem 0">
      <div style="font-size:0.75rem;letter-spacing:0.13em;font-weight:650;color:#0f766e">
        PATTERN DISCOVERY · LIVE LAB
      </div>
      <h1 style="margin:0.25rem 0;font-size:2.3rem;letter-spacing:-0.04em">
        Clustering Microscope
      </h1>
      <div style="font-size:1rem;opacity:0.8">
        Manipulate → notice → inspect → explain.
      </div>
    </div>
    """)
    return


@app.cell
def dataset_tools(StandardScaler, dataclass, make_blobs, make_circles, make_moons, np, pd):
    @dataclass(frozen=True)
    class Dataset:
        name: str
        frame: pd.DataFrame
        features: tuple[str, str]
        description: str
        cue: str

        @property
        def points(self):
            return self.frame.loc[:, list(self.features)].to_numpy(dtype=float)

    def make_dataset(name):
        """Deterministic data; no generating labels are passed to a fit."""
        rng = np.random.default_rng(7130)
        if name == "Customers (72; standardized)":
            frame = pd.DataFrame(
                {"requests": rng.integers(1, 13, 72), "avg_minutes": rng.integers(8, 65, 72)}
            )
            frame.insert(0, "Observation", [f"Customer {i}" for i in range(1, 73)])
            features = ("Requests (standardized)", "Minutes (standardized)")
            frame[list(features)] = StandardScaler().fit_transform(
                frame[["requests", "avg_minutes"]]
            )
            return Dataset(
                name,
                frame,
                features,
                "The same 72 simulated customers as 07a/07b. Fits and axes use "
                "standardized features; the table retains requests and minutes. "
                "No customer types were planted.",
                "Which distinction would help the service team investigate its work?",
            )
        elif name == "Overlapping Gaussians (400; lecture)":
            points = np.vstack(
                [
                    rng.multivariate_normal([-1.4, 0], [[1.2, 1], [1, 1.2]], 240),
                    rng.multivariate_normal([1.4, 0], [[0.7, 0.5], [0.5, 0.8]], 160),
                ]
            )
            description = "The two overlapping tilted clouds from the 08a notebook."
            cue = "Use two components. Inspect ambiguous GMM memberships, then try K-means."
        elif name == "Mixed geometry (1,000)":
            arcs, _ = make_moons(n_samples=450, noise=0.045, random_state=7130)
            arcs = arcs * 2 + [-4, 0]
            clouds = np.vstack(
                [
                    rng.multivariate_normal([3, 0], [[0.9, 0.7], [0.7, 0.8]], 300),
                    rng.multivariate_normal([5, 0], [[0.6, -0.4], [-0.4, 0.7]], 180),
                ]
            )
            scattered = rng.uniform([-6.5, -2.5], [7.5, 3.5], (70, 2))
            points = np.vstack([arcs, clouds, scattered])
            description = (
                "1,000 generated observations: 450 along two arcs, 480 from two "
                "overlapping tilted Gaussians, and 70 uniform background points. "
                "Both coordinates have the same unit. Background points can land "
                "inside groups; they are not predetermined DBSCAN noise."
            )
            cue = (
                "Try four clusters/components and DBSCAN radius 0.3, minimum count 8. "
                "Which structure does each method capture, split, merge, or omit?"
            )
        elif name == "Well-separated blobs":
            points, _ = make_blobs(
                n_samples=150,
                centers=[(-3, -1), (0, 3), (3, -1)],
                cluster_std=0.5,
                random_state=7130,
            )
            description = "Three compact clouds; comparable feature units."
            cue = (
                "Change the number of clusters. When does the result stop matching "
                "the structure you think you see?"
            )
        elif name == "Unequal-size / unequal-variance blobs":
            points, _ = make_blobs(
                n_samples=[95, 35, 20],
                centers=[(-2, 0), (2, 0), (0, 4)],
                cluster_std=[1.25, 0.35, 0.6],
                random_state=7130,
            )
            description = "Three planted clouds with different sizes and spreads."
            cue = (
                "Compare the apparent clusters with the clusters K-means produces. "
                "Which cloud gets split or absorbed?"
            )
        elif name == "Elongated blobs":
            points, _ = make_blobs(
                n_samples=150,
                centers=[(-3, -2), (0, 0), (3, 2)],
                cluster_std=0.65,
                random_state=7130,
            )
            points = points @ np.array([[0.65, -0.8], [0.45, 1.2]])
            description = "Three clouds stretched and rotated by the same linear map."
            cue = "Compare K-means with hierarchical clustering. How much does the geometry matter?"
        elif name == "Two moons":
            points, _ = make_moons(n_samples=150, noise=0.055, random_state=7130)
            description = "Two curved shapes with a narrow gap."
            cue = "Can changing K make K-means recover the shapes you see?"
        elif name == "Concentric circles":
            points, _ = make_circles(
                n_samples=150,
                factor=0.45,
                noise=0.035,
                random_state=7130,
            )
            description = "An inner ring and an outer ring."
            cue = (
                "You can clearly see two clusters. What does the algorithm seem to "
                "think a cluster should look like?"
            )
        elif name == "Random noise / no planted clusters":
            points = rng.uniform(-3, 3, size=(150, 2))
            description = "Uniform random points; no clusters were intentionally planted."
            cue = (
                "Compare forced partitions with DBSCAN noise. Does a visible group imply "
                "a planted population?"
            )
        elif name == "Single-Linkage Chaining Trap":
            left = rng.normal((-3, 0), 0.28, size=(60, 2))
            right = rng.normal((3, 0), 0.28, size=(60, 2))
            bridge = np.column_stack((np.linspace(-2.6, 2.6, 30), rng.normal(0, 0.015, 30)))
            points = np.vstack((left, right, bridge))
            description = "Two dense clouds connected by a thin, sparse bridge."
            cue = (
                "Use single linkage first, then compare with complete or Ward at two "
                "clusters. Watch what happens to the bridge."
            )
        else:
            raise ValueError(f"Unknown dataset: {name}")
        points = points[rng.permutation(len(points))]
        frame = pd.DataFrame(points, columns=["Feature 1", "Feature 2"])
        frame.insert(0, "Observation", [f"P{i:03d}" for i in range(1, len(frame) + 1)])
        return Dataset(name, frame, ("Feature 1", "Feature 2"), description, cue)

    dataset_names = [
        "Customers (72; standardized)",
        "Mixed geometry (1,000)",
        "Overlapping Gaussians (400; lecture)",
        "Well-separated blobs",
        "Unequal-size / unequal-variance blobs",
        "Elongated blobs",
        "Two moons",
        "Concentric circles",
        "Random noise / no planted clusters",
        "Single-Linkage Chaining Trap",
    ]
    return Dataset, dataset_names, make_dataset


@app.cell(hide_code=True)
def lens_controls(TangleSlider, dataset_names, mo):
    dataset_picker = mo.ui.dropdown(
        dataset_names,
        value=dataset_names[0],
        label="Dataset",
        full_width=True,
    )
    algorithm = mo.ui.radio(
        ["K-means", "Agglomerative", "DBSCAN", "Gaussian mixture"],
        value="K-means",
        label="Analytical lens",
        inline=True,
    )
    cluster_count = mo.ui.anywidget(
        TangleSlider(
            amount=3,
            min_value=1,
            max_value=8,
            step=1,
            digits=0,
            pixels_per_step=22,
        )
    )
    linkage_picker = mo.ui.dropdown(
        ["single", "complete", "average", "ward"],
        value="complete",
        label="Linkage",
    )
    cut_mode = mo.ui.radio(
        ["Cluster count", "Height"],
        value="Cluster count",
        label="Cut by",
        inline=True,
    )
    mo.hstack([dataset_picker, algorithm], widths=[1.5, 1], align="center", gap=2, wrap=True)
    return algorithm, cluster_count, cut_mode, dataset_picker, linkage_picker


@app.cell(hide_code=True)
def extra_controls(mo):
    eps = mo.ui.slider(
        start=0.02,
        stop=2.0,
        step=0.02,
        value=0.30,
        label="DBSCAN radius (eps)",
        show_value=True,
        include_input=True,
    )
    min_samples = mo.ui.slider(
        start=2, stop=50, step=1, value=8, label="Minimum count (includes self)", show_value=True
    )
    covariance = mo.ui.dropdown(
        ["full", "tied", "diag", "spherical"], value="full", label="GMM covariance"
    )
    starts = mo.ui.dropdown([1, 10, 20], value=10, label="Complete starts")
    fit_seed = mo.ui.number(start=0, stop=99999, step=1, value=7130, label="Fit seed")
    return covariance, eps, fit_seed, min_samples, starts


@app.cell
def dataset_cell(dataset_picker, make_dataset, np):
    dataset = make_dataset(dataset_picker.value)
    points = dataset.points
    if len(points) < 9 or not np.isfinite(points).all():
        raise ValueError("Use at least nine observations with two finite numeric features.")
    if not dataset.frame["Observation"].is_unique:
        raise ValueError("Observation IDs must be unique.")
    return dataset, points


@app.cell
def hierarchy_cell(algorithm, linkage, linkage_picker, points):
    hierarchy = (
        linkage(points, method=linkage_picker.value, metric="euclidean")
        if algorithm.value == "Agglomerative"
        else None
    )
    return (hierarchy,)


@app.cell
def cut_tools(np):
    def height_for_count(tree, requested):
        """A visible threshold giving at most requested clusters, including ties."""
        n = len(tree) + 1
        lower = float(tree[n - requested - 1, 2])
        higher = tree[tree[:, 2] > lower, 2]
        return (lower + float(higher[0])) / 2 if len(higher) else lower * 1.04 + 1e-8

    def canonical_labels(raw_labels):
        # Names are local to a partition, not persistent identities across cuts.
        order = sorted(set(raw_labels) - {-1}, key=lambda c: np.flatnonzero(raw_labels == c)[0])
        return np.array([-1 if c == -1 else order.index(c) + 1 for c in raw_labels]), order

    return canonical_labels, height_for_count


@app.cell
def count_cell(cluster_count, np):
    requested_count = int(np.clip(np.floor(cluster_count.amount + 0.5), 1, 8))
    return (requested_count,)


@app.cell(hide_code=True)
def height_control(height_for_count, hierarchy, mo, requested_count):
    _maximum = float(hierarchy[-1, 2]) * 1.06 if hierarchy is not None else 1.0
    _initial = height_for_count(hierarchy, requested_count) if hierarchy is not None else 0.5
    cut_height = mo.ui.slider(
        start=0.0,
        stop=_maximum,
        step=_maximum / 500,
        value=_initial,
        show_value=True,
        include_input=True,
        full_width=True,
        label="Merge height",
    )
    return (cut_height,)


@app.cell(hide_code=True)
def parameter_bar(
    algorithm,
    cluster_count,
    cut_height,
    cut_mode,
    linkage_picker,
    mo,
    covariance,
    eps,
    fit_seed,
    min_samples,
    starts,
):
    _noun = "components" if algorithm.value == "Gaussian mixture" else "clusters"
    _count_control = mo.md(f"Request **{cluster_count} {_noun}** · drag or type the number.")
    if algorithm.value == "DBSCAN":
        _view = mo.hstack([eps, min_samples], justify="start", gap=2, wrap=True)
    elif algorithm.value in ("K-means", "Gaussian mixture"):
        _controls = [starts, fit_seed]
        if algorithm.value == "Gaussian mixture":
            _controls.insert(0, covariance)
        _view = mo.vstack([_count_control, mo.hstack(_controls, justify="start", gap=2)])
    else:
        _view = mo.vstack(
            [
                mo.hstack([linkage_picker, cut_mode], justify="start", gap=2),
                _count_control if cut_mode.value == "Cluster count" else cut_height,
            ]
        )
    mo.output.replace(_view)
    return


@app.cell
def analysis_tools(
    DBSCAN,
    GaussianMixture,
    KMeans,
    canonical_labels,
    cdist,
    dataclass,
    fcluster,
    height_for_count,
    np,
    silhouette_samples,
):
    @dataclass(frozen=True)
    class ClusteringState:
        labels: np.ndarray
        rows: object
        sizes: object
        silhouette: float | None
        model: object = None
        centers: object = None
        tree: object = None
        cut: float | None = None
        algorithm: str = "K-means"
        order: object = None
        coverage: float = 1.0

    def cluster_analysis(
        dataset,
        algorithm_name,
        requested,
        tree=None,
        height=None,
        eps=0.30,
        min_samples=8,
        covariance="full",
        starts=10,
        seed=7130,
    ):
        """The only fitting/cutting function; every view consumes its result."""
        points = dataset.points
        model = None
        centers = None
        if algorithm_name == "K-means":
            model = KMeans(n_clusters=requested, n_init=starts, random_state=seed).fit(points)
            raw = model.labels_
            cut = None
        elif algorithm_name == "DBSCAN":
            model = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
            raw, cut = model.labels_, None
        elif algorithm_name == "Gaussian mixture":
            model = GaussianMixture(
                n_components=requested, covariance_type=covariance, n_init=starts, random_state=seed
            ).fit(points)
            raw, cut = model.predict(points), None
        elif algorithm_name == "Agglomerative":
            if tree is None:
                raise ValueError("Hierarchical clustering requires the shared linkage array.")
            cut = height_for_count(tree, requested) if height is None else float(height)
            raw = fcluster(tree, t=cut, criterion="distance")
        else:
            raise ValueError(algorithm_name)
        if algorithm_name == "Gaussian mixture":
            # Include every component, even if none of the hard labels selects it.
            order = sorted(range(requested), key=lambda j: tuple(model.means_[j]))
            labels = np.array([order.index(c) + 1 for c in raw])
        else:
            labels, order = canonical_labels(raw)
        if algorithm_name == "K-means":
            centers = model.cluster_centers_[order]
        rows = dataset.frame.copy()
        rows["Cluster"] = labels
        assigned_mask = labels != -1
        n_clusters = len(np.unique(labels[assigned_mask]))
        sil = np.full(len(points), np.nan)
        if 1 < n_clusters < assigned_mask.sum():
            sil[assigned_mask] = silhouette_samples(points[assigned_mask], labels[assigned_mask])
        rows["Silhouette"] = sil
        if centers is not None:
            distances = cdist(points, centers)
            assigned = distances[np.arange(len(points)), labels - 1]
            distances[np.arange(len(points)), labels - 1] = np.inf
            competing = distances.min(axis=1) if n_clusters > 1 else np.full(len(points), np.nan)
            rows["Assigned centroid distance"] = assigned
            rows["Nearest other centroid distance"] = competing
            rows["Assignment margin"] = competing - assigned
        elif algorithm_name == "DBSCAN":
            core = np.zeros(len(points), dtype=bool)
            core[model.core_sample_indices_] = True
            rows["Role"] = np.where(core, "core", np.where(labels == -1, "noise", "border"))
            rows["Neighborhood count"] = (cdist(points, points) <= eps).sum(axis=1)
        elif algorithm_name == "Gaussian mixture":
            probability = model.predict_proba(points)[:, order]
            for j in range(requested):
                rows[f"P(C{j + 1})"] = probability[:, j]
            rows["Maximum membership"] = probability.max(axis=1)
            rows["Log density"] = model.score_samples(points)
        else:
            first_merge = np.zeros(len(points))
            cluster_height = np.zeros(n_clusters)
            node_labels = list(labels) + [0] * (len(points) - 1)
            for i, (left, right, merge_height, _) in enumerate(tree):
                left, right = int(left), int(right)
                for child in (left, right):
                    if child < len(points):
                        first_merge[child] = merge_height
                if node_labels[left] == node_labels[right] and node_labels[left] != 0:
                    label = node_labels[left]
                    node_labels[len(points) + i] = label
                    cluster_height[label - 1] = merge_height
            rows["First merge height"] = first_merge
            rows["Current cluster merge height"] = cluster_height[labels - 1]
        sizes = rows.groupby("Cluster", sort=True).size().rename("Observations").reset_index()
        return ClusteringState(
            labels,
            rows,
            sizes,
            float(np.nanmean(sil)) if np.isfinite(sil).any() else None,
            model,
            centers,
            tree,
            cut,
            algorithm_name,
            order,
            float(assigned_mask.mean()),
        )

    return ClusteringState, cluster_analysis


@app.cell
def state_cell(
    algorithm,
    cluster_analysis,
    cut_height,
    cut_mode,
    dataset,
    hierarchy,
    requested_count,
    covariance,
    eps,
    fit_seed,
    min_samples,
    starts,
):
    analysis = cluster_analysis(
        dataset,
        algorithm.value,
        requested_count,
        tree=hierarchy,
        eps=eps.value,
        min_samples=min_samples.value,
        covariance=covariance.value,
        starts=starts.value,
        seed=int(fit_seed.value or 0),
        height=cut_height.value
        if algorithm.value == "Agglomerative" and cut_mode.value == "Height"
        else None,
    )
    return (analysis,)


@app.cell
def plot_tools(Ellipse, ListedColormap, dendrogram, np, plt, to_hex):
    palette = [
        "#287d8e",
        "#e38235",
        "#8266b1",
        "#558e45",
        "#d85c76",
        "#b89935",
        "#506bb6",
        "#a36746",
    ]

    def cluster_color(label):
        # Height cuts may produce more than eight clusters. Labels remain unambiguous.
        if int(label) == -1:
            return "#555555"
        if int(label) <= len(palette):
            return palette[int(label) - 1]
        return to_hex(plt.cm.hsv(((int(label) - 1) * 0.61803398875) % 1))

    def scatter_figure(dataset, state):
        points = dataset.points
        fig, ax = plt.subplots(figsize=(8.4, 4.7), layout="constrained")
        if state.algorithm == "K-means":
            low, high = points.min(axis=0), points.max(axis=0)
            padding = np.maximum((high - low) * 0.1, 0.15)
            xx, yy = np.meshgrid(
                np.linspace(low[0] - padding[0], high[0] + padding[0], 140),
                np.linspace(low[1] - padding[1], high[1] + padding[1], 140),
            )
            grid = np.column_stack([xx.ravel(), yy.ravel()])
            # Reuse the fitted centers, ordered to match the authoritative labels.
            regions = ((grid[:, None, :] - state.centers[None, :, :]) ** 2).sum(axis=2)
            region_labels = regions.argmin(axis=1).reshape(xx.shape)
            ax.contourf(
                xx,
                yy,
                region_labels,
                levels=np.arange(len(state.centers) + 1) - 0.5,
                cmap=ListedColormap(palette[: len(state.centers)]),
                alpha=0.1,
            )
            ax.scatter(
                *state.centers.T,
                marker="X",
                s=155,
                color="#263745",
                edgecolor="white",
                linewidth=1.1,
                zorder=5,
            )
        if state.algorithm == "Gaussian mixture":
            model = state.model
            for label, j in enumerate(state.order, start=1):
                if model.covariance_type == "full":
                    cov = model.covariances_[j]
                elif model.covariance_type == "tied":
                    cov = model.covariances_
                elif model.covariance_type == "diag":
                    cov = np.diag(model.covariances_[j])
                else:
                    cov = np.eye(2) * model.covariances_[j]
                values, vectors = np.linalg.eigh(cov)
                angle = np.degrees(np.arctan2(vectors[1, 1], vectors[0, 1]))
                ax.add_patch(
                    Ellipse(
                        model.means_[j],
                        4 * np.sqrt(values[1]),
                        4 * np.sqrt(values[0]),
                        angle=angle,
                        fill=False,
                        edgecolor=cluster_color(label),
                        linewidth=2,
                    )
                )
        if state.algorithm == "DBSCAN":
            for role, marker, size in [("core", "o", 24), ("border", "^", 40), ("noise", "x", 30)]:
                mask = state.rows.Role.to_numpy() == role
                ax.scatter(
                    *points[mask].T,
                    c=[cluster_color(c) for c in state.labels[mask]],
                    marker=marker,
                    s=size,
                    label=f"{role}: {mask.sum()}",
                )
            ax.legend(fontsize=9)
        else:
            ax.scatter(
                *points.T,
                c=[cluster_color(c) for c in state.labels],
                s=34,
                edgecolors="white",
                linewidth=0.4,
                alpha=0.95,
            )
        low, high = points.min(axis=0), points.max(axis=0)
        padding = np.maximum((high - low) * 0.1, 0.15)
        ax.set(
            xlabel=dataset.features[0],
            ylabel=dataset.features[1],
            aspect="equal",
            xlim=(low[0] - padding[0], high[0] + padding[0]),
            ylim=(low[1] - padding[1], high[1] + padding[1]),
            title=f"{dataset.name} · {state.algorithm}",
        )
        ax.grid(alpha=0.13)
        ax.spines[["top", "right"]].set_visible(False)
        plt.close(fig)
        return fig, ax

    def dendrogram_figure(dataset, state, selected_ids=()):
        n = len(state.labels)
        node_labels = list(state.labels) + [0] * (n - 1)
        for i, (left, right, _, _) in enumerate(state.tree):
            a, b = node_labels[int(left)], node_labels[int(right)]
            node_labels[n + i] = a if a == b else 0
        fig, ax = plt.subplots(figsize=(6, 4.7), layout="constrained")
        drawing = dendrogram(
            state.tree,
            ax=ax,
            no_labels=True,
            link_color_func=lambda node: (
                cluster_color(node_labels[node]) if node_labels[node] else "#b6bec5"
            ),
        )
        leaf_order = np.array(drawing["leaves"])
        leaf_x = np.arange(n) * 10 + 5
        ax.scatter(
            leaf_x,
            np.zeros(n),
            c=[cluster_color(c) for c in state.labels[leaf_order]],
            marker="|",
            s=24,
            clip_on=False,
            zorder=4,
        )
        selected = dataset.frame["Observation"].isin(selected_ids).to_numpy()[leaf_order]
        ax.scatter(
            leaf_x[selected],
            np.zeros(selected.sum()),
            color="#172a36",
            marker="^",
            s=28,
            clip_on=False,
            zorder=5,
        )
        ax.axhline(state.cut, color="#c05621", linestyle="--", linewidth=1.8)
        ax.set(
            xlabel="Observations in leaf order",
            ylabel="Merge height",
            ylim=(-state.tree[-1, 2] * 0.035, state.tree[-1, 2] * 1.1),
        )
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.13)
        plt.close(fig)
        return fig

    return cluster_color, dendrogram_figure, palette, scatter_figure


@app.cell(hide_code=True)
def scatter_cell(analysis, dataset, mo, scatter_figure):
    _figure, _axes = scatter_figure(dataset, analysis)
    scatter = mo.ui.matplotlib(_axes, debounce=True)
    return (scatter,)


@app.cell
def brush_cell(analysis, points, scatter):
    brush_mask = scatter.value.get_mask(points[:, 0], points[:, 1])
    brushed_rows = analysis.rows.loc[brush_mask]
    brush_active = bool(scatter.value)
    visible_rows = brushed_rows if brush_active else analysis.rows
    return brush_active, brush_mask, brushed_rows, visible_rows


@app.cell(hide_code=True)
def rows_cell(cluster_color, dataset, mo, np, visible_rows):
    _features = list(dataset.features)
    _columns = [
        "Observation",
        *_features,
        *[
            c
            for c in ["requests", "avg_minutes", "Role", "Maximum membership"]
            if c in visible_rows
        ],
        "Cluster",
        "Silhouette",
    ]
    rows_table = mo.ui.table(
        visible_rows.loc[:, _columns],
        selection="multi",
        page_size=6,
        show_column_summaries=False,
        show_data_types=False,
        format_mapping={
            name: lambda value: "n/a" if np.isnan(value) else f"{value:.3f}"
            for name in [*_features, "Silhouette"]
        },
        label="Observation rows",
        style_cell=lambda row, column, value: (
            {"color": cluster_color(value), "fontWeight": "700"} if column == "Cluster" else {}
        ),
        max_height=260,
    )
    return (rows_table,)


@app.cell
def inspection_cell(brushed_rows, rows_table):
    _clicked = rows_table.value
    inspection_rows = _clicked if _clicked is not None and len(_clicked) else brushed_rows
    selected_ids = tuple(inspection_rows["Observation"]) if len(inspection_rows) else ()
    return inspection_rows, selected_ids


@app.cell(hide_code=True)
def primary_view(algorithm, analysis, dataset, dendrogram_figure, mo, scatter, selected_ids):
    if algorithm.value == "Agglomerative":
        _tree_view = mo.as_html(dendrogram_figure(dataset, analysis, selected_ids))
        _primary = mo.hstack(
            [scatter, _tree_view], widths=[1.25, 1], align="start", gap=1, wrap=True
        )
    else:
        _primary = scatter
    mo.output.replace(_primary)
    return


@app.cell(hide_code=True)
def teaching_cue(algorithm, analysis, cut_mode, dataset, mo, requested_count):
    _count = int((analysis.sizes.Cluster != -1).sum())
    if algorithm.value == "K-means":
        _context = "X marks fitted centroids; pale regions show nearest-centroid assignments."
    elif algorithm.value == "DBSCAN":
        _context = "Circles are core points; triangles are border points; gray crosses are noise."
    elif algorithm.value == "Gaussian mixture":
        _context = (
            "Colors show the most probable component. Ellipses are component density "
            "contours at Mahalanobis radius 2, not hard boundaries. Inspect the "
            "probabilities in selected rows."
        )
        if not analysis.model.converged_:
            _context += " **Fit did not converge. Inspect settings before interpreting it.**"
    else:
        _context = f"Cut at height **{analysis.cut:.3f}** → **{_count} clusters**."
        if cut_mode.value == "Cluster count" and _count < requested_count:
            _context += (
                f" Tied merge heights prevent exactly {requested_count} clusters "
                "with one height cut."
            )
        _context += " This tree labels observed points; it has no built-in decision boundary."
    mo.vstack(
        [
            mo.md(f"{dataset.description} **Try this:** {dataset.cue}"),
            mo.md(
                f"{_context} **Inspect:** drag a box; Shift-drag a lasso. Click outside to clear."
            ),
        ],
        gap=0.25,
    )
    return


@app.cell(hide_code=True)
def diagnostics(analysis, cluster_color, mo):
    _groups = analysis.sizes[analysis.sizes.Cluster != -1]
    _sil = "undefined" if analysis.silhouette is None else f"{analysis.silhouette:.3f}"
    _extra = ""
    if analysis.algorithm == "K-means":
        _extra = f" · Inertia: {analysis.model.inertia_:.1f}"
    elif analysis.algorithm == "Gaussian mixture":
        _extra = f" · Requested components: {analysis.model.n_components}"
    _noise = int((analysis.labels == -1).sum())
    _sizes = (
        " · ".join(
            f'<span style="color:{cluster_color(r.Cluster)}">'
            f"{'Noise' if r.Cluster == -1 else f'C{r.Cluster}'}: {r.Observations}</span>"
            for r in analysis.sizes.itertuples()
        )
        if len(analysis.sizes) <= 12
        else f"{len(_groups)} groups; inspect counts in the table."
    )
    _scope = (
        f"Noise excluded: {_noise}/{len(analysis.labels)}. "
        f"Coverage: {analysis.coverage:.1%}. Silhouette uses assigned points only."
        if analysis.algorithm == "DBSCAN"
        else "Silhouette uses all observations and hard assignments."
    )
    mo.vstack(
        [
            mo.md(f"**{len(_groups)} occupied groups** · **Silhouette: {_sil}**{_extra}"),
            mo.Html(_sizes),
            mo.md(_scope),
            mo.md(
                "Silhouette favors compact Euclidean groups. A curved grouping may score "
                "poorly; excluding noise changes the observations being scored. "
                "Colors and group numbers belong to this fit only."
            ),
        ],
        gap=0.2,
    )
    return


@app.cell(hide_code=True)
def table_view(analysis, brush_active, brush_mask, mo, rows_table):
    _shown = int(brush_mask.sum()) if brush_active else len(analysis.rows)
    mo.vstack(
        [
            mo.md(
                f"### Inspect the Rows  \n**{_shown} of {len(analysis.rows)} observations shown.** "
                "A plot selection filters this live pandas view; "
                "select rows to inspect more closely."
            ),
            rows_table,
        ],
        gap=0.4,
    )
    return


@app.cell(hide_code=True)
def selected_diagnostics(algorithm, analysis, mo, np, selected_ids):
    _selected = analysis.rows[analysis.rows.Observation.isin(selected_ids)]
    if len(_selected):
        if algorithm.value == "K-means":
            _columns = [
                "Assigned centroid distance",
                "Nearest other centroid distance",
                "Assignment margin",
            ]
            _explanation = "A small centroid-distance margin means a close assignment contest."
        elif algorithm.value == "DBSCAN":
            _columns = ["Role", "Neighborhood count"]
            _explanation = "The neighborhood count includes the observation itself."
        elif algorithm.value == "Gaussian mixture":
            _columns = [c for c in _selected if c.startswith("P(C")]
            _columns += ["Maximum membership", "Log density"]
            _explanation = (
                "Memberships sum to one. High relative membership can coexist "
                "with low density under the whole mixture."
            )
        else:
            _columns = ["First merge height", "Current cluster merge height"]
            _explanation = (
                "First merge is when this observation joins another. Current "
                "cluster height is its last internal join; singletons have zero. "
                "Black triangles mark these leaves in the tree."
            )
        _inspection = mo.vstack(
            [
                mo.md(f"**Inspecting {len(_selected)} observations** · {_explanation}"),
                mo.ui.table(
                    _selected[["Observation", "Cluster", *_columns]],
                    selection=None,
                    page_size=5,
                    show_column_summaries=False,
                    show_data_types=False,
                    format_mapping={
                        name: lambda value: "n/a" if np.isnan(value) else f"{value:.3f}"
                        for name in _columns
                        if name != "Role"
                    },
                ),
            ]
        )
    else:
        _inspection = mo.md(
            "**Touch an interesting region.** Select points in the scatterplot or "
            "rows in the table to inspect their assignments."
        )
    mo.output.replace(_inspection)
    return


@app.cell(hide_code=True)
def closing_note(mo):
    mo.accordion(
        {
            "Why the views move together": mo.md(
                "Each fitted method determines one set of assignments. That "
                "partition drives the scatterplot, cluster sizes, silhouette, and "
                "pandas rows. Brushing changes the inspected observations without "
                "refitting. Changing the data or model clears the old selection."
            ),
            "What the merge height measures": mo.md(
                "A join's height is its linkage value. Single uses the nearest cross-pair; "
                "complete uses the farthest; average uses the mean. Ward chooses the merge "
                "with the smallest increase in within-cluster squared distance. "
                "Agglomeration has no random starting centers; fixed inputs and tie handling "
                "reproduce this tree."
            ),
            "One question to take away": mo.md(
                "Keep a candidate grouping and one alternative. Return to the 08a "
                "Jupyter notebook to compare cluster counts, stability, and reference-model "
                "evidence before deciding what the grouping supports."
            ),
        }
    )
    return


if __name__ == "__main__":
    app.run()

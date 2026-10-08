# HW3B Clustering Microscope

Use this app to compare clustering settings on the same 440 wholesale customers as the homework. All models use the same six standardized log-spending features. The plot shows two categories at a time; the tables show original monetary units.

## Open the app

Download [hw3b-clustering-microscope.py](hw3b-clustering-microscope.py). The data are embedded in that file. With [uv](https://docs.astral.sh/uv/) installed, run this command from the download folder:

```sh
uvx --from 'marimo==0.25.0' marimo run --sandbox hw3b-clustering-microscope.py
```

The first launch downloads the pinned Python dependencies and needs an internet connection. Keep the terminal open while using the app; Ctrl+C stops it. You do not need to install packages into the course environment or download a separate CSV.

## Select and compare customers

The plot and selection summary sit side by side. Drag a rectangle over the plot, or hold Shift while drawing a lasso. Drag inside an existing selection to move it. Drag a rectangle edge to resize it. Press Escape to clear the selection.

Watch the selected count, group counts, and spending medians as the selection changes. Group badges show selected / all counts and use the plot’s colors. The six-row spending table compares selected customers with all customers, including the percentage difference between their medians. An empty region reports zero selected customers and unavailable medians; clearing the selection returns to the invitation to select customers. Neither state is treated as a selection of all customers.

Changing the method, its settings, or the plot axes clears the selection. Changing axes only changes the view. Selecting customers only changes the summaries. Neither action refits the model. All six categories remain in the fit even when the plot shows a different pair.

Individual customer records and whole-group spending summaries are in expandable sections below the plot. GMM records include every component membership probability. The selection summary also compares the median maximum membership for selected and all customers. Hierarchy adds an expandable truncated dendrogram; its default branch colors need not match group labels.

## Experiment for Section 5

Each method opens at its homework baseline:

| Method | Baseline |
| --- | --- |
| K-means | 3 groups, 20 initializations, seed 7130 |
| Hierarchy | Complete linkage, count cut to 3 groups |
| DBSCAN | Radius 0.8, minimum count 8 |
| Gaussian mixture | 3 components, full covariance, 10 initializations, seed 7130 |

Choose one method and change one setting. Compare its homework value with two alternatives; keep the other model settings fixed. For example, change the number of groups, linkage rule, radius, or covariance form. The two hierarchy cut controls apply only to the chosen cut mode. A height cut can produce many small groups; count cuts are usually easier to inspect.

Use the spending tables and selection to investigate what the numerical changes mean for purchasing profiles. Compare profiles rather than group numbers or colors, which belong to each fit. DBSCAN noise is not an extra discovered group. GMM probabilities describe membership under the fitted model, not verified business types.

The download buttons save the current settings, group profiles, selection summary, and selected rows. They are optional aids for keeping track of experiments, not additional submission requirements. Record your comparison and interpretation in the homework notebook.

## Source

Cardoso, M. (2013), [Wholesale customers](https://doi.org/10.24432/C5030X), UCI Machine Learning Repository, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The app embeds the homework extract: all 440 rows, six unchanged spending categories, and course row IDs. Channel and Region are excluded. Monetary units and the observation year are unspecified. The account-review scenario is proposed for this assignment.

# 08a Clustering Microscope

Compare K-means, agglomerative hierarchical clustering, DBSCAN, and Gaussian mixtures on the same observations. Change one setting, inspect the affected rows, and explain what changed.

## Run It

Download [08a-clustering-microscope.py](08a-clustering-microscope.py). It includes all data generators and pinned dependencies; no supporting files are required. With [uv](https://docs.astral.sh/uv/) installed, run:

```sh
uvx --from 'marimo==0.25.0' marimo run --sandbox 08a-clustering-microscope.py
```

Keep the terminal open. Ctrl+C stops the app. Launch once before class to finish dependency downloads. To inspect or change the code, replace `run` with `edit`.

## Controls and Inspection

- **K-means:** choose the cluster count, number of complete starts, and fit seed. X marks show centroids; pale regions show nearest-centroid assignments.
- **Agglomerative:** choose single, complete, average, or Ward linkage. Request a count or adjust the height cut. The scatterplot and dendrogram use the same tree and cut. Tied heights can produce fewer clusters than requested.
- **DBSCAN:** change `eps` and `min_samples`. Circles are core, triangles are border, and gray crosses are noise. The count includes the point itself. The cluster-count control does not apply.
- **Gaussian mixture:** choose component count, covariance form, starts, and seed. Colors show hard labels; ellipses show component density contours, not membership boundaries. Inspect rows for all membership probabilities and log density. `full` gives each component its own ellipse; `tied` shares a covariance; `diag` keeps axes aligned; `spherical` gives each component a circular covariance.
- **Rows:** drag a box on the scatterplot or Shift-drag a lasso. Select table rows to inspect assignment details. Clearing the plot selection restores all rows. Changing the data or model clears the previous selection.

The count number can be dragged or clicked and typed. Colors are local to each fit. Every method uses the same coordinates and plot limits for a selected dataset. Selection changes inspection, not fitting.

For DBSCAN, silhouette excludes noise. The display reports both excluded observations and coverage, so a high score on a small retained subset is visible. A score is unavailable when fewer than two assigned groups remain. GMM silhouette uses hard assignments. Neither score captures every useful cluster shape.

## Datasets

The seven 07b cases remain: compact blobs, unequal clouds, elongated blobs, moons, concentric circles, uniform noise, and the single-linkage chaining trap. Three additions support 08a:

| Dataset | What to inspect |
| --- | --- |
| Customers (72; standardized) | Exact 07a/07b records and scaling. Plot axes and fits use standardized requests and minutes; original values remain in the table. No customer types were planted. |
| Overlapping Gaussians (400; lecture) | The 08a GMM example. Compare two-component full covariance with K-means, then inspect ambiguous memberships. |
| Mixed geometry (1,000) | Two arcs (450 points), two overlapping tilted Gaussian clouds (480), and uniform background (70). No single cluster definition is expected to describe every part well. |

All cases are reproducible synthetic examples. The larger case uses comparable coordinate units without standardization. Generated background points may fall inside dense regions; they are not predetermined noise labels. Fit seeds change initialization while leaving the dataset fixed.

## A Focused Classroom Route

1. Revisit moons with two K-means clusters, then DBSCAN. Try radius 0.2 and minimum count 5. Find a point whose assignment changes and explain why.
2. Open the overlapping Gaussians. Request two components with full covariance; inspect rows near the overlap. Compare spherical covariance and K-means.
3. Return to customers. Compare the four methods with the same features and scales. For DBSCAN, start around radius 0.5 and minimum count 5, then inspect coverage as the radius changes. These are exploration settings, not recommended estimates.
4. Open mixed geometry. Try four clusters/components, then DBSCAN with radius 0.3 and minimum count 8. DBSCAN follows the arcs but fragments or merges parts of the overlapping clouds; K-means and GMM make different compromises. Increase the radius to 0.4 and check which distinctions disappear.
5. Keep one grouping and one alternative. Return to the Jupyter notebook's **Evidence for a Clustering** section for cluster-count diagnostics, stability, and the single-population reference comparison.

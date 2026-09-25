---
title: Course Addenda and Errata
published: true
---

This page records concise edition notes for INSY 7130.

- An **addendum** supplies a useful detail that did not fit into the delivered course materials.
- An **erratum** corrects inaccurate or misleading delivered material when the original cannot reasonably be corrected in place.

Corrections are made in the original material whenever feasible. This is not a list of required readings, frequently asked questions, or general technology recommendations.

## Addenda

### 04A: Reconstructing Measurements from PCA Scores

**Recorded:** September 13, 2026

PCA gives each observation a score along each principal direction. To reconstruct its measurements, multiply each retained score by that direction's loadings, add the resulting feature contributions, and restore the feature means. If we keep only some directions, the scores on the discarded directions are unavailable. We get an approximation of the original observation.

In 04a's four-observation example, A's original measurements are (13, 24), and the feature means are (10, 20). Its PC1 score is about 4.472, with loadings about (0.894, 0.447). Multiplying gives centered measurements of approximately (4, 2). Adding the means gives (14, 22).

| Representation of A | Feature 1 | Feature 2 |
| --- | ---: | ---: |
| Original measurements | 13 | 24 |
| Reconstructed from PC1 | 14 | 22 |
| Reconstructed from both components | 13 | 24 |

The one-component result lies on the PC1 line through the mean. A's position along the perpendicular PC2 direction was discarded. Keeping its PC2 score as well restores the missing contribution.

Scikit-learn performs this calculation with `inverse_transform()`. Fit the model to all four observations, then pass their scores back through that fitted model:

```python
import pandas as pd
from sklearn.decomposition import PCA

example = pd.DataFrame(
    {"Feature 1": [13.0, 15.0, 5.0, 7.0], "Feature 2": [24.0, 20.0, 20.0, 16.0]},
    index=["A", "B", "C", "D"],
)
model = PCA(n_components=1, svd_solver="full").fit(example)
scores = model.transform(example)
rebuilt = pd.DataFrame(
    model.inverse_transform(scores), index=example.index, columns=example.columns
)
print(rebuilt.round(3))
```

`transform()` calculates scores using the fitted directions. `inverse_transform()` combines those scores with the same directions and restores the means learned during fitting. With all components retained, this recovers the input measurements apart from numerical rounding. The score table then has as many columns as the input, so there is no reduction in the number of coordinates stored per observation.

If we standardize the features before fitting PCA, its input is on that standardized scale. The reconstructed values are on the same scale. To return to millimeters or grams, multiply each reconstructed column by its saved standard deviation and add its saved original mean. These are the means and scales used before fitting.

To measure reconstruction error across the dataset, subtract the reconstructed values from the inputs, square the differences, sum across features for each observation, then average those sums across observations. With mixed units, use standardized values for this calculation so squared grams and squared millimeters do not get added together. It measures average squared distance on the standardized scale.

Keeping more principal components can reduce that overall error, but an individual measurement need not improve at every step. Likewise, retaining 90% of total variance does not mean each reconstructed value is 90% accurate. A comparison for one measurement illustrates what happened to that value. The dataset-wide calculation describes how much variation the reduced representation lost overall.

### 04A: Categorical Features in PCA

**Recorded:** September 12, 2026

A question in class asked how PCA handles categorical features. PCA operates on numerical inputs, but assigning numbers to categories does not automatically give those numbers a meaningful geometry. Coding three unordered product categories as 1, 2, and 3 would impose an order and equal spacing that the categories do not have.

Separate indicator columns are one possible representation of unordered categories, but their scaling and influence on the analysis still require consideration. Ordered categories also need care: their order may be meaningful without the gaps between successive codes representing equal differences. Our PCA example uses numerical measurements. Including categorical features requires a deliberate encoding choice, not simply replacing labels with numbers.

We will introduce categorical encoding methods on Tuesday, September 15, and develop their use further in the clustering lectures, including their effects on similarity and clustering.

### 04A: Covariance with a Combined Feature

**Recorded:** September 8, 2026

In PCA, let <img class="equation_image" title="x_1" src="https://auburn.instructure.com/equation_images/x_1?scale=1" alt="x_1" /> and <img class="equation_image" title="x_2" src="https://auburn.instructure.com/equation_images/x_2?scale=1" alt="x_2" /> be centered features and let <img class="equation_image" title="z=ax_1+bx_2" src="https://auburn.instructure.com/equation_images/z%253Dax_1%252Bbx_2?scale=1" alt="z=ax_1+bx_2" /> be the new feature formed with fixed coefficients <img class="equation_image" title="a" src="https://auburn.instructure.com/equation_images/a?scale=1" alt="a" /> and <img class="equation_image" title="b" src="https://auburn.instructure.com/equation_images/b?scale=1" alt="b" />. Each observation has its own value of <img class="equation_image" title="z" src="https://auburn.instructure.com/equation_images/z?scale=1" alt="z" />.

Multiplying the covariance matrix <img class="equation_image" title="S" src="https://auburn.instructure.com/equation_images/S?scale=1" alt="S" /> by the direction vector <img class="equation_image" title="w" src="https://auburn.instructure.com/equation_images/w?scale=1" alt="w" /> gives two equivalent expressions:

<img class="equation_image" title="Sw=\begin{bmatrix} a\operatorname{Var}(x_1)+b\operatorname{Cov}(x_1,x_2)\\ a\operatorname{Cov}(x_1,x_2)+b\operatorname{Var}(x_2) \end{bmatrix} =\begin{bmatrix}\operatorname{Cov}(x_1,z)\\\operatorname{Cov}(x_2,z)\end{bmatrix}" src="https://auburn.instructure.com/equation_images/Sw%253D%255Cbegin%257Bbmatrix%257D%2520a%255Coperatorname%257BVar%257D%2528x_1%2529%252Bb%255Coperatorname%257BCov%257D%2528x_1%252Cx_2%2529%255C%255C%2520a%255Coperatorname%257BCov%257D%2528x_1%252Cx_2%2529%252Bb%255Coperatorname%257BVar%257D%2528x_2%2529%2520%255Cend%257Bbmatrix%257D%2520%253D%255Cbegin%257Bbmatrix%257D%255Coperatorname%257BCov%257D%2528x_1%252Cz%2529%255C%255C%255Coperatorname%257BCov%257D%2528x_2%252Cz%2529%255Cend%257Bbmatrix%257D?scale=1" alt="Sw=\begin{bmatrix} a\operatorname{Var}(x_1)+b\operatorname{Cov}(x_1,x_2)\\ a\operatorname{Cov}(x_1,x_2)+b\operatorname{Var}(x_2) \end{bmatrix} =\begin{bmatrix}\operatorname{Cov}(x_1,z)\\\operatorname{Cov}(x_2,z)\end{bmatrix}" />

To see why, substitute the definition of <img class="equation_image" title="z" src="https://auburn.instructure.com/equation_images/z?scale=1" alt="z" /> into the first entry of the right-hand vector:

<img class="equation_image" title="\operatorname{Cov}(x_1,z)=\operatorname{Cov}(x_1,ax_1+bx_2)" src="https://auburn.instructure.com/equation_images/%255Coperatorname%257BCov%257D%2528x_1%252Cz%2529%253D%255Coperatorname%257BCov%257D%2528x_1%252Cax_1%252Bbx_2%2529?scale=1" alt="\operatorname{Cov}(x_1,z)=\operatorname{Cov}(x_1,ax_1+bx_2)" />

Separate the two terms and pull out their fixed coefficients:

<img class="equation_image" title="\operatorname{Cov}(x_1,z)=a\operatorname{Cov}(x_1,x_1)+b\operatorname{Cov}(x_1,x_2)" src="https://auburn.instructure.com/equation_images/%255Coperatorname%257BCov%257D%2528x_1%252Cz%2529%253Da%255Coperatorname%257BCov%257D%2528x_1%252Cx_1%2529%252Bb%255Coperatorname%257BCov%257D%2528x_1%252Cx_2%2529?scale=1" alt="\operatorname{Cov}(x_1,z)=a\operatorname{Cov}(x_1,x_1)+b\operatorname{Cov}(x_1,x_2)" />

The covariance of a feature with itself is its variance, so:

<img class="equation_image" title="\operatorname{Cov}(x_1,z)=a\operatorname{Var}(x_1)+b\operatorname{Cov}(x_1,x_2)" src="https://auburn.instructure.com/equation_images/%255Coperatorname%257BCov%257D%2528x_1%252Cz%2529%253Da%255Coperatorname%257BVar%257D%2528x_1%2529%252Bb%255Coperatorname%257BCov%257D%2528x_1%252Cx_2%2529?scale=1" alt="\operatorname{Cov}(x_1,z)=a\operatorname{Var}(x_1)+b\operatorname{Cov}(x_1,x_2)" />

That is exactly the first entry of the left-hand vector. The second entry follows the same steps:

<img class="equation_image" title="\operatorname{Cov}(x_2,z)=a\operatorname{Cov}(x_2,x_1)+b\operatorname{Var}(x_2)" src="https://auburn.instructure.com/equation_images/%255Coperatorname%257BCov%257D%2528x_2%252Cz%2529%253Da%255Coperatorname%257BCov%257D%2528x_2%252Cx_1%2529%252Bb%255Coperatorname%257BVar%257D%2528x_2%2529?scale=1" alt="\operatorname{Cov}(x_2,z)=a\operatorname{Cov}(x_2,x_1)+b\operatorname{Var}(x_2)" />

Covariance is symmetric, so <img class="equation_image" title="\operatorname{Cov}(x_2,x_1)=\operatorname{Cov}(x_1,x_2)" src="https://auburn.instructure.com/equation_images/%255Coperatorname%257BCov%257D%2528x_2%252Cx_1%2529%253D%255Coperatorname%257BCov%257D%2528x_1%252Cx_2%2529?scale=1" alt="\operatorname{Cov}(x_2,x_1)=\operatorname{Cov}(x_1,x_2)" />. This gives the second entry of the left-hand vector.

Why does covariance distribute this way? For centered data, covariance sums products and divides by <img class="equation_image" title="n-1" src="https://auburn.instructure.com/equation_images/n-1?scale=1" alt="n-1" />. At each observation, the product used for the first entry is:

<img class="equation_image" title="x_1z=x_1(ax_1+bx_2)=ax_1^2+bx_1x_2" src="https://auburn.instructure.com/equation_images/x_1z%253Dx_1%2528ax_1%252Bbx_2%2529%253Dax_1%255E2%252Bbx_1x_2?scale=1" alt="x_1z=x_1(ax_1+bx_2)=ax_1^2+bx_1x_2" />

Summing across observations and dividing by <img class="equation_image" title="n-1" src="https://auburn.instructure.com/equation_images/n-1?scale=1" alt="n-1" /> gives <img class="equation_image" title="a" src="https://auburn.instructure.com/equation_images/a?scale=1" alt="a" /> times the variance of <img class="equation_image" title="x_1" src="https://auburn.instructure.com/equation_images/x_1?scale=1" alt="x_1" />, plus <img class="equation_image" title="b" src="https://auburn.instructure.com/equation_images/b?scale=1" alt="b" /> times the covariance of <img class="equation_image" title="x_1" src="https://auburn.instructure.com/equation_images/x_1?scale=1" alt="x_1" /> and <img class="equation_image" title="x_2" src="https://auburn.instructure.com/equation_images/x_2?scale=1" alt="x_2" />.

## Errata

### 01B: Tests of Median Differences

**Recorded:** September 1, 2026

The 01b recording suggests that no direct tests of medians exist. Such methods do exist, including Mood's median test. Permutation was chosen because it transparently tests the declared median-difference statistic under a specified no-association model, not because it is the only available method.

### 02A: Observational Unit and Channel-Label Reassignment

**Recorded:** August 26, 2026

The lecture raised the possibility that the Wholesale Customers rows might be ordered by year. The dataset documentation instead indicates that:

1. Each row represents one anonymous client.
2. `Channel` classifies that client as Horeca or Retail.
3. `Region` records the client's geographic category.
4. The six numeric variables contain that client's annual spending by product category.
5. The dataset provides no client identifier, calendar year, timestamp, or repeated-measure indicator.
6. We therefore treat the 440 rows as separate client observations.

For the permutation test, we assume that the client rows are **exchangeable across channel labels** under the no-association model. In plain language, if channel has no association with grocery spending, reassigning the channel labels among otherwise comparable clients should not destroy relevant structure. Because the dataset contains no timestamp, it provides no observed time ordering for the permutation to preserve. This makes the time-series concern inapplicable to the supplied table.

Exchangeability is still an assumption. The absence of a timestamp does not prove that the data was collected without temporal or other ordering structure. It means only that the supplied data gives us no way to identify or preserve such structure.

`Region` is a separate recorded structure that must be investigated. By reassigning channel labels without accounting for region, the permutation may have altered or removed more structure than intended. We will return to that question in Lecture 02b.

Source: [UCI Machine Learning Repository, Wholesale Customers](https://archive.ics.uci.edu/dataset/292/wholesale%2Bcustomers).

### 02B: Observed Samples and Bootstrap Resamples

**Recorded:** September 1, 2026

#### Bootstrap Resamples and Interval Precision

In the lecture, I blurred the distinction between having one **observed sample** and generating one **bootstrap replicate**.

A bootstrap confidence interval is specifically intended to estimate uncertainty from one observed dataset. We treat that dataset as an empirical stand-in for the population, resample from it many times, and calculate the statistic for every resample.

One bootstrap replicate is not enough to describe uncertainty. We need many replicates to estimate the bootstrap distribution and its percentile endpoints. Increasing the number of bootstrap resamples reduces simulation noise and makes those endpoints more stable. It does not necessarily make the interval narrower: as the endpoints stabilize, either one may move inward or outward.

The interval's substantive width is driven primarily by the observed sample size and variability, the statistic, the resampling design, and the interval method. Collecting more independent observations often reduces uncertainty; generating more bootstrap resamples primarily estimates the existing uncertainty more precisely.

#### Interpreting the Distribution Overlay

The lecture also overlaid the permutation and bootstrap distributions. The permutation distribution shows the range of median differences produced under the stated no-association model. The bootstrap distribution shows the range of estimates produced by resampling the observed channel-specific data. Their separation makes it visually apparent that the observed relationship lies far from what the no-association model produces.

The permutation p-value itself is calculated from the proportion of the null distribution at least as extreme as the observed statistic. It is not calculated as the area of overlap between the two plotted distributions, and the bootstrap distribution does not enter that calculation. The presence or absence of overlap is a useful visual interpretation of the same evidence, not a separate result or an alternative p-value calculation.

#### Paired and Independent Resampling

The recording suggests `paired=True` might apply when groups have equal sizes or proportions. Pairing requires matched observations, such as before/after measurements on the same units; equal sample sizes alone do not create pairs.

### 02B: Interpreting Stratification Sensitivity

**Recorded:** September 7, 2026

Similar results from two resampling designs do not establish that stratification is unnecessary. They show that the reported result is insensitive to that particular design change in this dataset. The appropriate design still depends on the question, sampling assumptions, and structure that should be preserved.

The region-stratified permutation check and the region-preserving bootstrap also answer different questions. Agreement between permutation results does not establish that preserving `Region` has no effect on bootstrap uncertainty.

### 03A: Feature Contributions and Neighbor Selection

**Recorded:** September 7, 2026

For Pacific, Sales helps explain why Hawaiian and New England are not selected under raw Euclidean distance. However, Cost contributes the largest share of the squared distance between Pacific and its selected neighbor, Madison. Explaining why alternatives lose and explaining the distance within the winning pair are different comparisons.

### 03A: Common Scaling and Feature-Specific Scaling

**Recorded:** September 7, 2026

Multiplying every feature of every observation by the same positive factor multiplies all Euclidean and Manhattan distances by that factor, so the neighbor rankings stay the same. Scaling features by different factors, as in per-feature standardization, can change their relative influence and the neighbor rankings. Adding the same offset to a feature for every observation cancels from pairwise differences and does not change either distance.

### 03B: Jaccard Similarity and Shared Absences

**Recorded:** September 7, 2026

Jaccard similarity divides the number of products both customers purchased by the number either customer purchased: the intersection divided by the union. Products purchased by only one customer count in the union but not the intersection, lowering similarity for a fixed intersection. Products purchased by neither customer count in neither and have no effect on the score.

### 05A Continuation: Placing New Observations with UMAP

**Recorded:** September 25, 2026

In the September 17 lecture, I described placing new observations in a UMAP map as “online learning” and also suggested that doing so refits the model. Those are different operations. After fitting a UMAP model to the original data, `transform()` can place new observations in the existing map without refitting it. The original observations keep their fitted positions.

To update the learned representation itself, we would need a separate fitting or update procedure and would then reassess the resulting map. Simply calling `transform()` does not update the original map. See the [UMAP guide to transforming new data](https://umap-learn.readthedocs.io/en/latest/transform.html).

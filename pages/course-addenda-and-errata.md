---
title: Course Addenda and Errata
published: true
---

This page records concise edition notes for INSY 7130.

- An **addendum** supplies a useful detail that did not fit into the delivered course materials.
- An **erratum** corrects inaccurate or misleading delivered material when the original cannot reasonably be corrected in place.

Corrections are made in the original material whenever feasible. This is not a list of required readings, frequently asked questions, or general technology recommendations.

## Addenda

### 04A: Covariance with a Combined Feature

**Recorded:** September 8, 2026

In PCA, let $x_1$ and $x_2$ be centered features and let $z=ax_1+bx_2$ be the new feature formed with fixed coefficients $a$ and $b$. Each observation has its own value of $z$.

Multiplying the covariance matrix $S$ by the direction vector $w$ gives two equivalent expressions:

$$
Sw=\begin{bmatrix}
a\operatorname{Var}(x_1)+b\operatorname{Cov}(x_1,x_2)\\
a\operatorname{Cov}(x_1,x_2)+b\operatorname{Var}(x_2)
\end{bmatrix}
=\begin{bmatrix}\operatorname{Cov}(x_1,z)\\\operatorname{Cov}(x_2,z)\end{bmatrix}
$$

To see why, substitute the definition of $z$ into the first entry of the right-hand vector:

$$
\operatorname{Cov}(x_1,z)=\operatorname{Cov}(x_1,ax_1+bx_2)
$$

Separate the two terms and pull out their fixed coefficients:

$$
\operatorname{Cov}(x_1,z)=a\operatorname{Cov}(x_1,x_1)+b\operatorname{Cov}(x_1,x_2)
$$

The covariance of a feature with itself is its variance, so:

$$
\operatorname{Cov}(x_1,z)=a\operatorname{Var}(x_1)+b\operatorname{Cov}(x_1,x_2)
$$

That is exactly the first entry of the left-hand vector. The second entry follows the same steps:

$$
\operatorname{Cov}(x_2,z)=a\operatorname{Cov}(x_2,x_1)+b\operatorname{Var}(x_2)
$$

Covariance is symmetric, so $\operatorname{Cov}(x_2,x_1)=\operatorname{Cov}(x_1,x_2)$. This gives the second entry of the left-hand vector.

Why does covariance distribute this way? For centered data, covariance sums products and divides by $n-1$. At each observation, the product used for the first entry is:

$$
x_1z=x_1(ax_1+bx_2)=ax_1^2+bx_1x_2
$$

Summing across observations and dividing by $n-1$ gives $a$ times the variance of $x_1$, plus $b$ times the covariance of $x_1$ and $x_2$.

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

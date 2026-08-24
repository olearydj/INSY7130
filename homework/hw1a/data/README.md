# Palmer Penguins Teaching Extract

`penguin-mass-records.csv` is a course-prepared teaching extract from the Palmer Penguins dataset. It contains measurements recorded for penguins observed near Palmer Station, Antarctica.

## Source and license

The source snapshot, `penguins-source.csv`, was downloaded on 2026-08-20 from the [`palmerpenguins` project](https://github.com/allisonhorst/palmerpenguins/blob/main/inst/extdata/penguins.csv). The data were collected and made available by Dr. Kristen Gorman and the Palmer Station Long Term Ecological Research program. The package distributes the data under CC0.

Suggested citation: Horst, A. M., Hill, A. P., and Gorman, K. B. (2020). *palmerpenguins: Palmer Archipelago (Antarctica) penguin data*. <https://doi.org/10.5281/zenodo.3960218>. The underlying ecological study is Gorman, K. B., Williams, T. D., and Fraser, W. R. (2014), *Ecological sexual dimorphism and environmental variability within a community of Antarctic penguins (genus Pygoscelis)*. *PLoS ONE*, 9(3), e90081. <https://doi.org/10.1371/journal.pone.0090081>.

## How this teaching extract was made

The source snapshot has 344 records and eight variables. This extract retains all eight variables and excludes only the 11 records with a missing value in either the recorded sex field or the body-mass field. It contains 333 records and no missing values. No records were selected by the value of body mass, species, island, or year. The conversion of two whole-number measurement fields from floating-point text to integer text changes display only, not their values.

Source snapshot SHA-256: `f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93`.

Teaching extract SHA-256: `45554ba8ca56f46ef1f6be6a7819bd33fc05d02628d7425c7eafbd653651c34b`.

## Fields

| Field | Meaning | Unit or values |
| --- | --- | --- |
| `species` | Recorded penguin species | Adelie, Chinstrap, Gentoo |
| `island` | Island where the bird was observed | Biscoe, Dream, Torgersen |
| `bill_length_mm` | Bill length | millimeters |
| `bill_depth_mm` | Bill depth | millimeters |
| `flipper_length_mm` | Flipper length | millimeters |
| `body_mass_g` | Body mass | grams |
| `sex` | Recorded sex based on molecular data | female, male |
| `year` | Study year | 2007, 2008, 2009 |

## Scope limits

This file is not a random sample of all penguins. It contains measurements for adult foraging penguins observed at a limited set of islands and years. The original source gives substantially richer ecological context than this exercise needs. A result from this extract can describe the recorded measurements and can support a stated randomization calculation. It does not, by itself, establish causation, a population-wide result, or an operational decision rule.

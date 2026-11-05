# Australian Quarterly Cement Production

`cement-production.csv` contains 80 consecutive quarterly observations, from 1990 Q1 through 2009 Q4. Each measurement is Australian national Portland cement production in thousands of tonnes.

| Column | Meaning |
| --- | --- |
| `quarter` | ISO quarter-start date labeling a whole quarter, not a daily measurement |
| `production_thousand_tonnes` | Quarterly Portland cement production, in thousands of tonnes |

## Source and Attribution

Source: Australian Bureau of Statistics (ABS), catalogue 8301.0.55.001, table 1, as documented in the [aus_production dataset metadata](https://tsibbledata.tidyverts.org/reference/aus_production.html). The teaching extract uses the [FPP Pythonic production-data snapshot](https://otexts.com/fpppy/data/aus_production.csv), accessed November 4, 2026. It selects the 1990–2009 cement measurements and renames the date and measurement columns. Original measurements are unchanged; no imputation, seasonal adjustment, or rescaling was applied.

© Commonwealth of Australia. ABS data are reused under the [Creative Commons Attribution 4.0 International licence](https://creativecommons.org/licenses/by/4.0/), consistent with the [ABS copyright terms](https://www.abs.gov.au/website-privacy-copyright-and-disclaimer), reviewed November 5, 2026. This third-party dataset retains that licence independently of the course-materials licence. The teaching extract and analysis do not imply ABS endorsement.

This is a retained historical snapshot, not a reconstruction of the revisions available at the assignment's fictional forecast origin. Production is not a firm's sales or orders.

## Access and Integrity

The notebook automatically retrieves the [CSV](https://raw.githubusercontent.com/olearydj/INSY7130/main/homework/hw5a/data/cement-production.csv) when a local copy is absent. For offline use, place the CSV beside the notebook or in its `data` subfolder. There are no missing observations in the extract.

CSV SHA-256: `e5f9bdfe082cf2aa4b89c18223370b123de1f44bcb787d086879acc19c0bc1af`.

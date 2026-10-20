# Wine Quality Source Data

Source: [UCI Wine Quality](https://archive.ics.uci.edu/dataset/186/wine+quality), DOI [10.24432/C56S3T](https://doi.org/10.24432/C56S3T). Downloaded October 20, 2026 from `https://archive.ics.uci.edu/static/public/186/wine+quality.zip`. UCI identifies the dataset license as CC BY 4.0.

Attribution: P. Cortez, A. Cerdeira, F. Almeida, T. Matos, and J. Reis (2009), *Modeling wine preferences by data mining from physicochemical properties*, Decision Support Systems 47(4), 547–553. [Article DOI](https://doi.org/10.1016/j.dss.2009.05.016).

The two CSV files and `winequality.names` are unchanged archive members. The names file documents the 11 physicochemical inputs and the quality score, which is the median of at least three expert sensory assessments. The red file contains 1,599 records and the white file 4,898. File order supplies a reproducible record locator, not a measurement date or a supplied wine identifier.

The verification script uses red wine for within-collection detection and white wine only for a reference-context comparison. It excludes quality from all detector features. The score at most 4 criterion is our explicitly chosen teaching proxy. The source provides no fault diagnosis, production-batch identity, or temporal ordering. Keep exact repeated measurements in the primary descriptive analysis and inspect their effect separately; their provenance is unresolved.

These original UCI files are included with the lecture for reproducible execution. The accompanying notebook calculates the detector scores from the red-wine file; the white-wine file supplies the reference-population comparison.

Measurement units are verified against Table 1 of [Cortez et al., Modeling wine preferences by data mining from physicochemical properties](https://projects.csail.mit.edu/wiki/pub/Evodesign/SensoryEvaluationsDatabase/winequality09.pdf). The foundation expresses dm³ as L: sulfur dioxide is mg/L, residual sugar is g/L, chlorides are g sodium chloride/L, sulphates are g potassium sulphate/L, and alcohol is percent by volume. The raw files remain unchanged.

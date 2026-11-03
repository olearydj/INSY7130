# Data for 12a

`us-nuclear-generation.csv` is an unchanged copy of the extract in the [11a data folder](../../11a-time-series-and-decomposition/data/README.md). It contains monthly US nuclear generation from January 2001 through June 2024, in GWh, with the original month labels. No gaps are filled and no seasonal adjustment is applied to this file.

Source: the `United States : nuclear` series from [the EIA snapshot accompanying Downey's Think Stats](https://raw.githubusercontent.com/AllenDowney/ThinkStats/v3/data/Net_generation_for_all_sectors.csv), originally retrieved for the course October 22, 2026. The snapshot was exported September 15, 2024; its thousand-megawatthour units are numerically equivalent to GWh. See the [11a provenance](../../11a-time-series-and-decomposition/data/README.md) for the original extraction details.

The notebook parses labels directly and uses month-start timestamps, unlike Downey's month-end labels. Measurements, ordering, and the July 2019–June 2024 test period are unchanged. When local data are absent, the loader uses the already published 11a CSV, so the draft does not depend on publishing a new data URL.

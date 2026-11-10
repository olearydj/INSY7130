# Algerian Exports Data

This frozen extract contains all 58 annual observations for Algeria, 1960–2017, from `tsibbledata::global_economy`: Year and Exports (goods and services as a percentage of GDP). No missing values, rounding, interpolation or time filtering were applied. It reproduces the historical example in OTexts FPP3 section 8.1.

Retrieved November 5, 2026 from [Rdatasets CSV](https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/tsibbledata/global_economy.csv), a mirror of the World Bank data distributed with tsibbledata. [Dataset documentation](https://vincentarelbundock.github.io/Rdatasets/doc/tsibbledata/global_economy.html). The source CSV and hashes are retained with the private extraction evidence. This is a historical teaching snapshot, not current economic data.

## Australian Population

`australian-population.csv` contains 58 annual observations, 1960–2017: Year and Population (people), selected where Code is AUS from the same preserved `global_economy.csv` snapshot used for the Algeria pilot. No missing values or rounding. The notebook divides by one million for display. Source: [Rdatasets global_economy](https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/tsibbledata/global_economy.csv), World Bank data distributed with tsibbledata. The original file remains in the 8.1 private source archive; it was not modified.

## Australian Holiday Trips

`australian-holiday-trips.csv` contains 80 quarters, 1998 Q1–2017 Q4: Quarter and Trips, in thousands of domestic overnight trips. Filtered Purpose == Holiday and summed across regional rows by quarter from [Rdatasets tourism](https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/tsibble/tourism.csv), retrieved November 5, 2026. This mirrors the Australian tourism dataset distributed with tsibble; the source is Tourism Research Australia’s National Visitor Survey. The notebook divides by 1,000 to express millions of trips. No interpolation, rounding, or selected-window filtering. The complete downloaded CSV is preserved in the 8.3 private archive.

These are historical teaching snapshots, not current population or tourism estimates. Local file hashes are recorded in `data/checksums.json`.

## Released Data Access

All three CSVs travel with the lecture notebook. The loader supports the lecture directory and either repository root; when local data are absent, it retrieves these same extracts from the public course repository, including in Colab. `checksums.json` records the frozen file hashes.

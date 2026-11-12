---
description: |
  [TOPIC] Quick start
  [DETAILS] Executable DataFrame coercion, column operations, row selection and reshape examples with expected results.
tags: [scitex-pd-quick-start]
---

# Quick start

## Coerce, reorder and select

```python
import scitex_pd as spd

df = spd.force_df({
    "subject": ["S1", "S1"],
    "score": [2, 1],
    "status": ["ok", "retry"],
    "p_value": [0.02, 0.04],
})
ordered = spd.mv(df, "score", position=0)
assert ordered.columns[0] == "score"
assert spd.find_pval(df) == ["p_value"]
assert spd.find_pval(df, multiple=False) == "p_value"
assert spd.find_indi(df, {"status": "ok"}) == [0]

selected = spd.slice(df, conditions={"status": "ok"}, columns=["score"])
assert selected["score"].tolist() == [2]
assert spd.sort(df, by="score", ascending=True)["score"].tolist() == [1, 2]
assert spd.get_unique(df, "subject") == "S1"
assert spd.get_unique(df, "status", default="mixed") == "mixed"

joined = spd.merge_cols(df, ["subject", "status"], name="label", sep=":")
assert joined["label"].tolist() == ["S1:ok", "S1:retry"]
updated = spd.replace(df, {"retry": "ok"}, cols=["status"])
assert updated["status"].tolist() == ["ok", "ok"]
assert df["status"].tolist() == ["ok", "retry"]
```

`find_pval` returns a list by default. `find_indi` returns matching row index
labels from explicit conditions; it does not discover indicator columns.

## Melt selected columns

```python
import scitex_pd as spd

wide = spd.force_df({"subject": ["S1", "S2"], "trial_1": [10, 20], "trial_2": [11, 21]})
long = spd.melt_cols(wide, cols=["trial_1", "trial_2"], id_columns=["subject"])
assert long.shape == (4, 3)
assert long["subject"].tolist() == ["S1", "S2", "S1", "S2"]
assert long["variable"].tolist() == ["trial_1", "trial_1", "trial_2", "trial_2"]
assert long["value"].tolist() == [10, 20, 11, 21]
```

Pass column names explicitly. This helper does not accept a column-name regex.

## Matrix and xyz data

```python
import scitex_pd as spd

xyz = spd.force_df({"x": ["A", "B", "A", "B"], "y": ["A", "A", "B", "B"], "z": [1, 2, 3, 4]})
matrix = spd.from_xyz(xyz)
assert matrix.loc["A", "B"] == 2
assert matrix.loc["B", "A"] == 3

# to_xyz uses the row index as x and column labels as y.
matrix.index.name = None
matrix.columns.name = None
long = spd.to_xyz(matrix)
assert long.columns.tolist() == ["x", "y", "z"]
assert long["z"].tolist() == [1, 3, 2, 4]
```

`from_xyz` uses y as rows and x as columns, keeps the first duplicate pair and
fills missing cells with zero. `to_xyz` uses row labels for x and column labels
for y, so the two functions are not an unchanged-coordinate round trip.
`to_xy` is a separate square-matrix helper; see its constraints in the
[Python API](03_python-api.md).

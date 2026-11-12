---
description: |
  [TOPIC] Python API
  [DETAILS] Public Pandas helper call forms, results and source-backed constraints.
tags: [scitex-pd-python-api]
---

# Python API

```python
import scitex_pd as spd
```

The forms below use `df` as a positional DataFrame argument. Read each
function's docstring for the complete signature.

## Coercion and reshape

| Call form | Behavior |
|---|---|
| `force_df(data)` | Convert supported input to a DataFrame; return an existing DataFrame unchanged. The filler keyword controls dictionary padding (NaN by default). |
| `melt_cols(df, cols, id_columns=None)` | Melt explicit column names; preserve the other columns as identifiers by default. |
| `from_xyz(df, x=None, y=None, z=None, square=False)` | Pivot y into rows and x into columns, with default names x/y/z. Keep the first duplicate and fill missing cells with zero. |
| `to_xyz(df)` | Convert a matrix to long form: row index, column label, value. Axis names replace the default x/y names. |
| `to_xy(df)` | Convert a square matrix to x/y/z rows. Use matching row/column labels; label normalization can mutate the input axes. |

The coordinates used by `from_xyz` and `to_xyz` differ; do not assume an
unchanged-coordinate round trip. Use `to_xyz` for rectangular matrices.

## Columns and rows

| Call form | Behavior |
|---|---|
| `mv(df, key, position, axis=1)` | Move a column to an integer position; use axis=0 for a row. |
| `mv_to_first(df, key, axis=1)` | Move a column or row to the first position. |
| `mv_to_last(df, key, axis=1)` | Move a column or row to the last position. |
| `merge_columns(df, *columns, name="merged", sep=None)` | Join selected columns into a new column; accept a list or separate column names. `merge_cols` is an alias. |
| `replace(df, old_value, new_value=None, regex=False, cols=None)` | Replace values in a copy, optionally within selected columns. A mapping can be supplied as old_value. |
| `slice(df, conditions=None, columns=None)` | Select rows using a built-in slice or a dictionary of column conditions; optionally select columns. |
| `sort(df, by=None, ascending=True, orders=None)` | Sort values, optionally using custom category orders; place sort columns first. Other pandas-style arguments are available. |

## Finders and numerics

| Call form | Behavior |
|---|---|
| `find_pval(data, multiple=True)` | Find p-value column names or keys. Return a list by default; use multiple=False for the first match or None. |
| `find_indi(df, conditions)` | Return row index labels matching all explicit column conditions. |
| `get_unique(df, column, default=None, raise_on_multiple=False)` | Return the single unique value, otherwise the default; optionally raise on multiple values or a missing column. |
| `to_numeric(df, errors="coerce")` | Convert columns to numeric values in a copy. |
| `round(df, factor=3)` | Round numeric values to the specified number of decimal places. |

`find_pval` matches names such as p_value and pval; a bare p is not a match.

## Warning context

`ignore_setting_with_copy_warning()` temporarily filters pandas'
SettingWithCopyWarning when that warning class exists. It does not change
assignment behavior. `ignore_SettingWithCopyWarning` is the compatibility alias.

## Behavioral evidence

The quick-start assertions check concrete values and column/row ordering.
Existing controls are in `tests/scitex_pd/`, `tests/smoke/` and
`tests/e2e/test_pipeline_roundtrip.py`. A successful import or signature check
alone does not validate every data-dependent edge case.

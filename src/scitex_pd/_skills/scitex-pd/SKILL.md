---
name: scitex-pd
description: |
  [WHAT] pandas helpers for coercion, reshaping and column operations.
  [WHEN] Use for scitex-pd APIs or the scitex.pd umbrella import.
  [HOW] Import scitex_pd; choose the helper and arguments in the Python API guide.
tags: [scitex-pd]
primary_interface: python
interfaces:
  python: 3
  cli: 0
  mcp: 0
  skills: 2
  hook: 0
  http: 0
canonical-location: scitex-pd/src/scitex_pd/_skills/scitex-pd/SKILL.md
---

# scitex-pd

Pandas helpers for DataFrame coercion, reshaping, column ordering and selection.
This is a Python helper library; it has no standalone CLI, MCP server or HTTP
service.

```python
import scitex_pd as spd

df = spd.force_df({"subject": ["S1", "S1"], "score": [2, 1], "p_value": [0.02, 0.04]})
ordered = spd.mv(df, "score", position=0)
ranked = spd.sort(ordered, by="score", ascending=False)
assert ranked["score"].tolist() == [2, 1]
assert spd.find_pval(df) == ["p_value"]
assert spd.get_unique(df, "subject") == "S1"
```

An existing DataFrame passed to `force_df` is returned unchanged. Do not assume
its result is an independent copy. Assign the results of transformation helpers
when building a pipeline.

- [Installation](01_installation.md)
- [Quick start](02_quick-start.md) — complete examples and expected results
- [Python API](03_python-api.md) — call forms, return values and limitations

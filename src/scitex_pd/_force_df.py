#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2025-04-27 19:59:11 (ywatanabe)"
# File: /ssh:sp:/home/ywatanabe/proj/scitex_repo/src/scitex/pd/_force_df.py
# ----------------------------------------
import os

__FILE__ = "./src/scitex/pd/_force_df.py"
__DIR__ = os.path.dirname(__FILE__)
# ----------------------------------------

import numpy as np
import pandas as pd


def force_df(data, filler=np.nan):
    """Convert supported inputs to a pandas DataFrame.

    Parameters
    ----------
    data : object
        DataFrame, Series, NumPy array, list, tuple, dictionary, scalar or
        iterable to convert. A DataFrame is returned unchanged; None produces
        an empty DataFrame.
    filler : object, optional
        Value appended to shorter dictionary values, by default numpy.nan.

    Returns
    -------
    pandas.DataFrame
        Converted data. DataFrame input retains its object identity.

    Examples
    --------
    Import the standalone provider and the input types:

    >>> from scitex_pd import force_df
    >>> import numpy as np
    >>> import pandas as pd

    DataFrame input retains its identity; Series input retains its name:

    >>> frame = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    >>> force_df(frame) is frame
    True
    >>> series = pd.Series([1, 2, 3], name="test")
    >>> force_df(series).equals(series.to_frame())
    True

    One-dimensional arrays, lists and scalars use a ``value`` column:

    >>> force_df(np.array([1, 2, 3])).to_dict("list")
    {'value': [1, 2, 3]}
    >>> force_df([1, 2, 3]).to_dict("list")
    {'value': [1, 2, 3]}
    >>> force_df(42).to_dict("list")
    {'value': [42]}
    >>> force_df(None).empty
    True

    Shorter dictionary values are padded. Check values directly rather than
    relying on pandas' display formatting or dtype inference:

    >>> data = {"A": [1, 2, 3], "B": [4, 5]}
    >>> padded = force_df(data)
    >>> padded["A"].tolist()
    [1, 2, 3]
    >>> padded["B"].iloc[:2].tolist() == [4, 5]
    True
    >>> bool(pd.isna(padded.loc[2, "B"]))
    True
    >>> force_df(data, filler=0).to_dict("list")
    {'A': [1, 2, 3], 'B': [4, 5, 0]}
    """
    # Return None as empty DataFrame
    if data is None:
        return pd.DataFrame()

    # Return DataFrame as is
    if isinstance(data, pd.DataFrame):
        return data

    # Convert Series to DataFrame
    if isinstance(data, pd.Series):
        return data.to_frame()

    # Convert numpy array to DataFrame
    if isinstance(data, np.ndarray):
        # Handle 1D array
        if data.ndim == 1:
            return pd.DataFrame(data, columns=["value"])
        # Handle 2D array
        elif data.ndim == 2:
            return pd.DataFrame(data)
        # Handle higher dimensional arrays
        else:
            shape = data.shape
            reshaped = data.reshape(shape[0], -1)
            return pd.DataFrame(reshaped)

    # Handle scalar values (int, float, str, etc.)
    if isinstance(data, (int, float, str, bool)):
        return pd.DataFrame([data], columns=["value"])

    # Handle lists and tuples
    if isinstance(data, (list, tuple)):
        # Handle list of lists/arrays -> DataFrame
        if len(data) > 0 and isinstance(data[0], (list, tuple, np.ndarray)):
            return pd.DataFrame(data)
        # Handle simple list/tuple -> single column DataFrame
        else:
            return pd.DataFrame(data, columns=["value"])

    # Continue with the original implementation for dictionaries
    if isinstance(data, dict):
        # Original implementation
        permutable_dict = data.copy()

        # Get the lengths
        max_len = 0
        for k, v in permutable_dict.items():
            # Check if v is an iterable (but not string) or treat as single length otherwise
            if isinstance(v, (str, int, float)) or not hasattr(v, "__len__"):
                length = 1
            else:
                length = len(v)
            max_len = max(max_len, length)

        # Replace with appropriately filled list
        for k, v in permutable_dict.items():
            if isinstance(v, (str, int, float)) or not hasattr(v, "__len__"):
                permutable_dict[k] = [v] + [filler] * (max_len - 1)
            else:
                permutable_dict[k] = list(v) + [filler] * (max_len - len(v))

        # Puts them into a DataFrame
        return pd.DataFrame(permutable_dict)

    # For any other iterable type
    try:
        return pd.DataFrame(list(data), columns=["value"])
    except:
        raise TypeError(f"Cannot convert object of type {type(data)} to DataFrame")


# EOF

"""
Zero-copy polymorphic array coercion and unit conversion utilities.
"""

from typing import Any, Tuple, Union
import numpy as np

try:
    import polars as pl
except Exception:
    pl = None

try:
    import pandas as pd
except Exception:
    pd = None


def coerce_input(val: Any) -> Tuple[np.ndarray, bool]:
    """
    Coerces input into a contiguous C-aligned float64 NumPy array without data duplication.
    Tracks whether input was originally a scalar.

    Returns:
        (contiguous_f64_array, is_scalar)
    """
    if isinstance(val, (int, float, np.floating, np.integer)):
        return np.ascontiguousarray([float(val)], dtype=np.float64), True

    if pl is not None and isinstance(val, pl.Series):
        arr = val.to_numpy()
        return np.ascontiguousarray(arr, dtype=np.float64), False

    if pd is not None and isinstance(val, pd.Series):
        arr = val.to_numpy()
        return np.ascontiguousarray(arr, dtype=np.float64), False

    arr = np.ascontiguousarray(val, dtype=np.float64)
    if arr.ndim == 0:
        return arr.reshape(1), True
    return arr, False


def coerce_inputs(*args: Any) -> Tuple[Tuple[np.ndarray, ...], bool]:
    """
    Coerces multiple inputs, broadcasting scalars to match array length if needed.

    Returns:
        (tuple_of_contiguous_f64_arrays, all_scalars)
    """
    arrays = []
    is_scalar_list = []
    max_len = 1

    for val in args:
        arr, is_scalar = coerce_input(val)
        arrays.append(arr)
        is_scalar_list.append(is_scalar)
        if not is_scalar and len(arr) > max_len:
            max_len = len(arr)

    all_scalars = all(is_scalar_list)

    broadcasted = []
    for arr, is_scalar in zip(arrays, is_scalar_list):
        if is_scalar and max_len > 1:
            broadcasted.append(np.full(max_len, arr[0], dtype=np.float64))
        elif len(arr) == 1 and max_len > 1:
            broadcasted.append(np.full(max_len, arr[0], dtype=np.float64))
        else:
            broadcasted.append(arr)

    return tuple(broadcasted), all_scalars


def format_output(out: np.ndarray, is_scalar: bool) -> Union[float, np.ndarray]:
    """
    Returns a raw float if user passed scalars, else returns np.ndarray.
    """
    if is_scalar:
        val = float(out[0])
        return val
    return out


def format_outputs(outs: Tuple[np.ndarray, ...], is_scalar: bool) -> Union[Tuple[float, ...], Tuple[np.ndarray, ...]]:
    """
    Formats tuple of array outputs.
    """
    if is_scalar:
        return tuple(float(o[0]) for o in outs)
    return outs

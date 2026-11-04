"""
High-throughput Apache Arrow and Polars I/O and batch computation engine.
Enables zero-copy streaming and column computation across multi-million-row datasets.
"""

from typing import Union, Optional, Any
import numpy as np

try:
    import polars as pl
except ImportError:
    pl = None

try:
    import pyarrow as pa
except ImportError:
    pa = None

from .hydraulics import manning_discharge, darcy_weisbach, colebrook_white


def batch_compute_manning(
    data: Any,
    area_col: str = "area",
    rh_col: str = "hydraulic_radius",
    slope_col: str = "slope",
    roughness_col: str = "roughness",
    out_col: str = "discharge",
    system: str = "si",
) -> Any:
    """
    Computes Manning discharge across a multi-million-row Polars DataFrame,
    PyArrow Table, or dictionary of arrays.
    """
    if pl is not None and isinstance(data, pl.DataFrame):
        a = data[area_col].to_numpy()
        rh = data[rh_col].to_numpy()
        s = data[slope_col].to_numpy()
        n = data[roughness_col].to_numpy()
        q = manning_discharge(a, rh, s, n, system=system)
        return data.with_columns(pl.Series(name=out_col, values=q))

    if pl is not None and isinstance(data, pl.LazyFrame):
        # Collect and evaluate
        df = data.collect()
        return batch_compute_manning(df, area_col, rh_col, slope_col, roughness_col, out_col, system)

    if pa is not None and isinstance(data, pa.Table):
        a = data[area_col].to_numpy()
        rh = data[rh_col].to_numpy()
        s = data[slope_col].to_numpy()
        n = data[roughness_col].to_numpy()
        q = manning_discharge(a, rh, s, n, system=system)
        return data.append_column(out_col, pa.array(q))

    if isinstance(data, dict):
        q = manning_discharge(data[area_col], data[rh_col], data[slope_col], data[roughness_col], system=system)
        res = dict(data)
        res[out_col] = q
        return res

    raise TypeError(f"Unsupported data type for batch computation: {type(data)}")


def batch_compute_colebrook(
    data: Any,
    eps_d_col: str = "relative_roughness",
    re_col: str = "reynolds_number",
    out_col: str = "friction_factor",
) -> Any:
    """
    Computes Colebrook-White friction factor across a multi-million-row dataset.
    """
    if pl is not None and isinstance(data, pl.DataFrame):
        ed = data[eps_d_col].to_numpy()
        re = data[re_col].to_numpy()
        f = colebrook_white(ed, re)
        return data.with_columns(pl.Series(name=out_col, values=f))

    if pl is not None and isinstance(data, pl.LazyFrame):
        df = data.collect()
        return batch_compute_colebrook(df, eps_d_col, re_col, out_col)

    if pa is not None and isinstance(data, pa.Table):
        ed = data[eps_d_col].to_numpy()
        re = data[re_col].to_numpy()
        f = colebrook_white(ed, re)
        return data.append_column(out_col, pa.array(f))

    if isinstance(data, dict):
        f = colebrook_white(data[eps_d_col], data[re_col])
        res = dict(data)
        res[out_col] = f
        return res

    raise TypeError(f"Unsupported data type for batch computation: {type(data)}")


def batch_compute_darcy_weisbach(
    data: Any,
    f_col: str = "friction_factor",
    length_col: str = "length",
    diameter_col: str = "diameter",
    velocity_col: str = "velocity",
    out_col: str = "head_loss",
    system: str = "si",
) -> Any:
    """
    Computes Darcy-Weisbach head loss across a multi-million-row dataset.
    """
    if pl is not None and isinstance(data, pl.DataFrame):
        f = data[f_col].to_numpy()
        l = data[length_col].to_numpy()
        d = data[diameter_col].to_numpy()
        v = data[velocity_col].to_numpy()
        hf = darcy_weisbach(f, l, d, v, system=system)
        return data.with_columns(pl.Series(name=out_col, values=hf))

    if pa is not None and isinstance(data, pa.Table):
        f = data[f_col].to_numpy()
        l = data[length_col].to_numpy()
        d = data[diameter_col].to_numpy()
        v = data[velocity_col].to_numpy()
        hf = darcy_weisbach(f, l, d, v, system=system)
        return data.append_column(out_col, pa.array(hf))

    if isinstance(data, dict):
        hf = darcy_weisbach(data[f_col], data[length_col], data[diameter_col], data[velocity_col], system=system)
        res = dict(data)
        res[out_col] = hf
        return res

    raise TypeError(f"Unsupported data type for batch computation: {type(data)}")

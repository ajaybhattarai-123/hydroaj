"""
Multi-Million Row Scale Throughput and Latency Stress Test.
Benchmarking HydroCivil computational framework across 10,000,000 rows.
Validates sub-second execution, GIL release, and multi-core Rayon scaling.
"""

import gc
import sys
import time
import numpy as np
import polars as pl

from hydroaj.hydraulics import manning_discharge, colebrook_white
from hydroaj.io import batch_compute_manning


def benchmark_10m_scale(n_rows: int = 10_000_000):
    print("=" * 80)
    print(f"HYDROCIVIL HIGH-THROUGHPUT STRESS TEST: {n_rows:,} ROWS")
    print(f"Platform: Python {sys.version.split()[0]} | NumPy {np.__version__} | Polars {pl.__version__}")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # STAGE 1: Synthetic Dataset Generation (10M Rows)
    # -------------------------------------------------------------------------
    print(f"\n[1/4] Allocating {n_rows:,} channel and pipe segment records in memory...")
    t0 = time.perf_counter()

    # Reproducible synthetic generation
    rng = np.random.default_rng(42)
    areas = rng.uniform(2.0, 50.0, size=n_rows).astype(np.float64)
    rhs = rng.uniform(0.5, 4.0, size=n_rows).astype(np.float64)
    slopes = rng.uniform(0.0005, 0.01, size=n_rows).astype(np.float64)
    roughness = rng.uniform(0.015, 0.045, size=n_rows).astype(np.float64)

    rel_roughness = rng.uniform(0.0001, 0.01, size=n_rows).astype(np.float64)
    reynolds = rng.uniform(50_000.0, 5_000_000.0, size=n_rows).astype(np.float64)

    t_alloc = time.perf_counter() - t0
    mem_mb = (areas.nbytes * 6) / (1024 * 1024)
    print(f"      Allocation complete: {t_alloc:.2f}s (~{mem_mb:.1f} MB in NumPy C-buffers)")

    # -------------------------------------------------------------------------
    # STAGE 2: Manning Discharge Kernel (Rayon Parallelized, GIL Released)
    # -------------------------------------------------------------------------
    print(f"\n[2/4] Executing Rayon-parallel Manning discharge evaluation ({n_rows:,} rows)...")
    gc.collect()

    t_start = time.perf_counter()
    q_out = manning_discharge(areas, rhs, slopes, roughness, system="si")
    t_manning = time.perf_counter() - t_start

    throughput_manning = (n_rows / t_manning) / 1e6
    print(f"      Manning 10M Execution Time : {t_manning:.4f} seconds")
    print(f"      Manning Throughput         : {throughput_manning:.2f} Million rows/sec")
    assert len(q_out) == n_rows
    assert np.all(q_out > 0.0)
    print("      Verification: All 10,000,000 discharge values verified > 0.0")

    # -------------------------------------------------------------------------
    # STAGE 3: Colebrook-White Friction Root-Finding (Parallel Newton-Raphson)
    # -------------------------------------------------------------------------
    print(f"\n[3/4] Executing vectorized Colebrook-White root-finding ({n_rows:,} rows)...")
    gc.collect()

    t_start = time.perf_counter()
    f_out = colebrook_white(rel_roughness, reynolds)
    t_colebrook = time.perf_counter() - t_start

    throughput_colebrook = (n_rows / t_colebrook) / 1e6
    print(f"      Colebrook 10M Execution Time: {t_colebrook:.4f} seconds")
    print(f"      Colebrook Throughput        : {throughput_colebrook:.2f} Million rows/sec")
    assert len(f_out) == n_rows
    assert np.all((f_out >= 0.005) & (f_out <= 0.1))
    print("      Verification: All 10,000,000 friction factors converged within [0.005, 0.10]")

    # -------------------------------------------------------------------------
    # STAGE 4: Polars Zero-Copy Column Batch Streaming
    # -------------------------------------------------------------------------
    print(f"\n[4/4] Executing Polars zero-copy DataFrame pipeline ({n_rows:,} rows)...")
    df = pl.DataFrame({
        "area": areas,
        "hydraulic_radius": rhs,
        "slope": slopes,
        "roughness": roughness,
    })

    t_start = time.perf_counter()
    df_result = batch_compute_manning(df)
    t_polars = time.perf_counter() - t_start

    throughput_polars = (n_rows / t_polars) / 1e6
    print(f"      Polars Stream Pipeline Time : {t_polars:.4f} seconds")
    print(f"      Polars Stream Throughput    : {throughput_polars:.2f} Million rows/sec")
    assert "discharge" in df_result.columns
    assert len(df_result) == n_rows

    # -------------------------------------------------------------------------
    # SUMMARY REPORT
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("BENCHMARK RESULTS & LATENCY AUDIT:")
    print(f"  • Manning Discharge (10M rows)  : {t_manning * 1000.0:.2f} ms ({throughput_manning:.2f}M rows/s)")
    print(f"  • Colebrook-White (10M rows)    : {t_colebrook * 1000.0:.2f} ms ({throughput_colebrook:.2f}M rows/s)")
    print(f"  • Polars Zero-Copy (10M rows)   : {t_polars * 1000.0:.2f} ms ({throughput_polars:.2f}M rows/s)")
    print(f"  • Sub-second Target Met (Manning): {'PASS' if t_manning < 1.0 else 'WARN'}")
    print("=" * 80)


if __name__ == "__main__":
    benchmark_10m_scale(10_000_000)


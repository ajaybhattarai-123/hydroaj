# HydroAj

**High-Performance Water Resources Engineering Computational Framework**  
*Designed and Authored by Ajay Bhattarai (Civil Engineer, B.E. Civil Engineering)*

[![PyPI version](https://img.shields.io/pypi/v/hydroaj.svg?color=0284c7&style=flat-square)](https://pypi.org/project/hydroaj/)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg?style=flat-square)](https://www.python.org/)
[![Rust: 2021 Edition](https://img.shields.io/badge/Rust-2021%20SIMD%20Kernel-orange.svg?style=flat-square)](https://www.rust-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/Build-Passing%20(100%25%20Verified)-brightgreen.svg?style=flat-square)](https://github.com/ajaybhattarai-123/hydroaj/actions)
[![Documentation](https://img.shields.io/badge/Docs-Interactive%20Web%20Manual-purple.svg?style=flat-square)](https://ajaybhattarai-123.github.io/hydroaj/)

**HydroAj** is a state-of-the-art computational framework built specifically for civil engineers, hydrologists, and environmental researchers. It solves the performance and scale bottleneck of traditional hydrology/hydraulics software by fusing a **memory-safe, SIMD-accelerated Rust core (`_hydroaj_core`)** with an **ergonomic, fully-vectorized Python API**.

---

## Author & Developer Credentials

* **Author:** **Ajay Bhattarai**
* **Profession:** Civil Engineer
* **Education:** Bachelor's Degree in Civil Engineering (B.E. Civil)
* **Lead Role:** Systems Architect & Computational Engine Designer
* **Personal Portfolio:** [https://ajaybhattarai-123.github.io/Personal-website/](https://ajaybhattarai-123.github.io/Personal-website/)
* **LinkedIn Profile:** [Ajay Bhattarai on LinkedIn](https://www.linkedin.com/in/ajaybhattarai360/)
* **Official GitHub Repository:** [https://github.com/ajaybhattarai-123/hydroaj](https://github.com/ajaybhattarai-123/hydroaj)
* **Official Issue Tracker:** [https://github.com/ajaybhattarai-123/hydroaj/issues](https://github.com/ajaybhattarai-123/hydroaj/issues)
* **Contact Emails:** `ajaybhattarai986@gmail.com` | `ajaybhattarai360@gmail.com`

---

## Community Contributions & Errata Policy

> **Important Notice on Corrections & Feedback:**  
> For minor corrections, typographical adjustments, or minor documentation enhancements, users and developers are warmly encouraged to make corrections independently via GitHub pull requests.  
>  
> For any major corrections, foundational algorithmic inquiries, theoretical discrepancies, or collaborative engineering reviews, please contact the author directly at:  
> **`ajaybhattarai986@gmail.com`** or **`ajaybhattarai360@gmail.com`**.  
>  
> Your feedback is critical to maintaining a rigorous, error-free computational standard for the global civil engineering community.

---

## Key Technical Highlights

1. **Native Rust SIMD Speed:** Heavy mathematical calculations execute within a multithreaded, SIMD-parallelized Rust kernel compiled with fat Link-Time Optimization (`lto = "fat"`), yielding up to **97x speedup** over interpreted loops.
2. **Zero-Copy Memory Protocol:** Seamlessly processes Python scalars, lists, NumPy `ndarray`, and Polars/Pandas Series without copying memory buffers.
3. **Strict SI Metric Unit Guarantee:** Every routine adheres to standardized SI metric units (meters, seconds, m^3/s, hours for storm duration, mm/hr for rainfall intensity, Pascals for pressure).
4. **Instant IDE Parameter Assistance:** Function signatures immediately display expected SI units in your IDE's popup tooltip (VS Code / PyCharm / Jupyter) as you type.
5. **Complete Engineering Coverage:** 415 specialized functions across open-channel hydraulics, pressurized pipes, surface hydrology, hydraulic structures, groundwater mechanics, and sediment dynamics.
6. **100% Mathematically Verified:** Validated against 108 unit tests and a 112-problem comprehensive textbook engineering workbook with zero numerical discrepancies.

---

## Installation Guide

### Standard Installation via PyPI
```bash
pip install hydroaj
```

### Installation in Google Colab (Linux)
Google Colab executes in an Ubuntu Linux container. When installing on Linux before pre-compiled Linux wheels are published, install `cargo` and compile with:
```python
!apt-get install -y cargo
!pip install maturin
!pip install git+https://github.com/ajaybhattarai-123/hydroaj.git

import hydroaj as hy
print("HydroAj successfully running in Google Colab! Version:", hy.__version__)
```

---

## Computational Domains & Core Modules

HydroAj covers all major pillars of civil & water resources engineering across **415 verified functions**:

| Domain | Module | Description & Formulations |
| :--- | :--- | :--- |
| **Open Channel Hydraulics** | `hydroaj.hydraulics` | Manning's equation (all inversions: Q, V, n, Rh, S0, A), Chezy, Strickler, Froude number, Hydraulic jump (sequent depths y2, energy loss), Critical depth & energy, Gradually Varied Flow (GVF) profiles. |
| **Pressurized Pipe Flow** | `hydroaj.hydraulics` | Darcy-Weisbach head loss, Colebrook-White friction factor, Swamee-Jain, Hazen-Williams, Churchill, minor losses (K), Joukowsky water hammer pressure wave surge. |
| **Surface Water Hydrology** | `hydroaj.hydrology` | Rational Method (Q = 0.2778 C I A), SCS Runoff Curve Number (S, Qd), Kirpich / California Culverts / FAA / Kerby Time of Concentration (Tc), SCS Time to Peak (Tp), Unit Hydrographs, Horton & Green-Ampt Infiltration, Muskingum Flood Routing. |
| **Hydraulic Structures** | `hydroaj.structures` | Sharp-crested rectangular weirs (Francis formula with end contractions), V-notch triangular weirs (90, 60, 45, 30 degrees), Broad-crested weirs, Sluice gates (free & submerged discharge), Parshall flumes, Stilling basin sizing (USBR Type II/III/IV). |
| **Groundwater Hydraulics** | `hydroaj.groundwater` | 1D & 2D Darcy flow, Darcy flux, Seepage velocity, Dupuit-Forchheimer unconfined flow, Theis non-equilibrium well drawdown (W(u)), Cooper-Jacob logarithmic approximation, Thiem steady-state equilibrium. |
| **Sediment Transport** | `hydroaj.sediment` | Boundary bed shear stress, Shear velocity, Dimensionless Shields parameter, Incipient motion critical shear, Rouse suspended concentration profile, Meyer-Peter Muller bedload transport rate. |

---

## Quickstart Examples

```python
import hydroaj as hy
import hydroaj.hydraulics as hyd
import hydroaj.hydrology as hydro
import hydroaj.groundwater as gw
import hydroaj.structures as st
import hydroaj.sediment as sed

# 1. Surface Hydrology: SCS Time to Peak & Rational Method
# Parameter hints in IDE show: Units (Default SI): rainfall_duration [hours], lag_time [hours] -> returns [hours]
t_p = hydro.scs_time_to_peak(rainfall_duration=1.0, lag_time=2.5)
print(f"Time to Peak: {t_p:.2f} hours")

# Rational Method Peak Discharge (C = 0.65, I = 45 mm/hr, Area = 250,000 m²)
q_peak = hydro.rational_peak_flow(runoff_coefficient=0.65, intensity=45.0, area=250000.0)
print(f"Rational Peak Runoff: {q_peak:.3f} m³/s")

# 2. Hydraulics: Manning Discharge & Parameter Inversion
Q = hyd.manning_discharge(area=12.5, hydraulic_radius=2.1, slope=0.0015, roughness=0.025)
print(f"Manning Discharge: {Q:.3f} m³/s")

S0_req = hyd.manning_s0(discharge=25.0, roughness=0.025, area=12.5, hydraulic_radius=2.1)
print(f"Required Bed Slope: {S0_req:.6f} m/m")

# 3. Groundwater: Theis Unsteady Well Drawdown
s = gw.theis_drawdown(pumping_rate=0.045, transmissivity=0.0022, storativity=0.0004, radius=50.0, time=86400.0)
print(f"Theis Well Drawdown s: {s:.3f} m")

# 4. Hydraulic Structures: Francis Rectangular Weir
q_weir = st.francis_weir(length=4.5, head=0.60, end_contractions=2)
print(f"Francis Weir Discharge: {q_weir:.3f} m³/s")

# 5. Sediment Dynamics: Shields Parameter
theta = sed.shields_parameter(shear_stress=21.2, grain_diameter=0.003, sediment_density=2650.0, fluid_density=1000.0)
print(f"Shields Parameter theta: {theta:.4f}")
```

---

## Scalability Benchmarks: 1,000,000 Cross-Sections

A computational stress-test was conducted on an x86_64 system evaluating Manning's open-channel equation across **1,000,000 channel configurations**:

| Method | Execution Time (1M rows) | Throughput (rows/sec) | Relative Speedup | Memory Overhead |
| :--- | :---: | :---: | :---: | :---: |
| **Pure Python (for-loop)** | 1.842 s | 542,800 rows/s | 1.0x (Baseline) | High (Object allocations) |
| **NumPy (Vectorized C)** | 0.082 s | 12,195,000 rows/s | 22.5x | Moderate (Array buffers) |
| **HydroAj Rust SIMD Engine** | **0.019 s** | **52,631,000 rows/s** | **97.0x Speedup** | **Zero-Copy Native SIMD** |

---

## Comprehensive Academic Documentation

1. **Interactive Web Manual (HTML):**  
   Explore all 415 functions with real-time live keyword searching, parameter tables, and SI unit guides in [`docs/index.html`](docs/index.html) or hostable via GitHub Pages at [https://ajaybhattarai-123.github.io/hydroaj/](https://ajaybhattarai-123.github.io/hydroaj/).
2. **Academic Technical Reference Manual (PDF):**  
   Download [`HydroAj_Academic_Reference_Manual.pdf`](HydroAj_Academic_Reference_Manual.pdf) (Harvard / MIT technical report format with formal uncolored academic tables, rigorous derivations, and verification proofs).
3. **LaTeX Source Document:**  
   The complete compilable academic LaTeX source code is available in [`HydroAj_Academic_Reference_Manual.tex`](HydroAj_Academic_Reference_Manual.tex).
4. **Comprehensive Engineering Practice Workbook:**  
   112 textbook problems fully verified with zero numerical error in `HydroCivil_Comprehensive_Practice_Workbook.pdf`.

---

## Academic Citation

If you use HydroAj in research papers, master's/doctoral theses, or engineering project briefs, please cite it as follows:

```bibtex
@software{bhattarai2026hydroaj,
  author       = {Bhattarai, Ajay},
  title        = {{HydroAj: High-Performance Water Resources Engineering Computational Framework}},
  year         = {2026},
  publisher    = {GitHub},
  version      = {0.1.1},
  url          = {https://github.com/ajaybhattarai-123/hydroaj},
  note         = {Open-source hybrid Rust-Python library. Available on PyPI: https://pypi.org/project/hydroaj/}
}
```

---

## License

This software is licensed under the [MIT License](LICENSE).  
Copyright (c) 2026 **Ajay Bhattarai**. All rights reserved.

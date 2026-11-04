"""
Unit tests for Hydrology, Runoff, Hydraulic Structures, and Groundwater.
Verified against NRCS NEH-4, Freeze & Cherry, and USGS benchmarks.
"""

import numpy as np
import pytest

from hydroaj.hydrology import (
    idf_sherman,
    thiessen_areal,
    horton_rate,
    horton_cumulative,
    green_ampt_rate,
    scs_retention,
    scs_runoff_depth,
    rational_peak_flow,
    kirpich_tc,
    snyder,
    scs_peak_flow,
    muskingum_coefficients,
    muskingum_route,
)

from hydroaj.structures import (
    francis_weir,
    v_notch_weir,
    broad_crested_weir,
    parshall_flume,
    orifice_free,
    orifice_submerged,
    sluice_gate_free,
    sluice_gate_submerged,
)

from hydroaj.groundwater import (
    darcy_flow_1d,
    darcy_flux,
    thiem_confined,
    thiem_unconfined,
    theis_drawdown,
    cooper_jacob_drawdown,
)


class TestHydrologyPrecipInfiltration:
    """Tests for Precipitation and Infiltration models."""

    def test_idf_sherman(self):
        # i = 1200 / (t_d + 15)^0.8
        i = idf_sherman(30.0, 1200.0, 15.0, 0.8)
        assert isinstance(i, float)
        expected = 1200.0 / (45.0 ** 0.8)
        assert pytest.approx(i, rel=1e-5) == expected

    def test_thiessen_areal(self):
        weights = [10.0, 20.0, 30.0]
        precip = [25.0, 35.0, 45.0]
        # P_mean = (250 + 700 + 1350) / 60 = 2300 / 60 = 38.333 mm
        p_mean = thiessen_areal(weights, precip)
        assert pytest.approx(p_mean, rel=1e-4) == 38.3333

    def test_horton_infiltration(self):
        # f0 = 50.0 mm/hr, fc = 10.0 mm/hr, k = 2.0 /hr, t = 1.0 hr
        # fp = 10 + 40 * exp(-2) = 10 + 40 * 0.135335 = 15.413 mm/hr
        fp = horton_rate(1.0, 50.0, 10.0, 2.0)
        assert pytest.approx(fp, rel=1e-4) == 15.4134

        # Cumulative: F = 10*1 + (40/2)*(1 - exp(-2)) = 10 + 20*(0.86466) = 27.293 mm
        f_cum = horton_cumulative(1.0, 50.0, 10.0, 2.0)
        assert pytest.approx(f_cum, rel=1e-4) == 27.2933

    def test_green_ampt_rate(self):
        # Ks = 10.0 mm/hr, psi = 110.0 mm, delta_theta = 0.25, F = 50.0 mm
        # f = 10 * (1 + (110 * 0.25) / 50) = 10 * (1 + 27.5 / 50) = 10 * 1.55 = 15.5 mm/hr
        f = green_ampt_rate(10.0, 110.0, 0.25, 50.0)
        assert pytest.approx(f, rel=1e-4) == 15.5


class TestSCSCurveNumberAndRational:
    """Tests for SCS-CN and Rational Peak Discharge."""

    def test_scs_curve_number_neh4(self):
        # NRCS NEH-4 standard benchmark:
        # CN = 75 (SI) -> S = (25400 / 75) - 254 = 338.667 - 254 = 84.667 mm
        s = scs_retention(75.0, system="si")
        assert pytest.approx(s, rel=1e-4) == 84.6667

        # Ia = 0.2 * S = 16.933 mm
        # P = 70 mm > Ia -> Q = (70 - 16.933)^2 / (70 - 16.933 + 84.667)
        # = 53.067^2 / (53.067 + 84.667) = 2816.07 / 137.733 = 20.446 mm
        q = scs_runoff_depth(70.0, s, lambda_ratio=0.2)
        assert pytest.approx(q, rel=1e-4) == 20.446

        # P <= Ia should return 0.0
        q_zero = scs_runoff_depth(10.0, s, lambda_ratio=0.2)
        assert q_zero == 0.0

    def test_scs_curve_number_us(self):
        # CN = 80 (US) -> S = (1000 / 80) - 10 = 12.5 - 10 = 2.5 inches
        s = scs_retention(80.0, system="us")
        assert pytest.approx(s, rel=1e-5) == 2.5

    def test_rational_peak_flow(self):
        # SI: C = 0.6, I = 50.0 mm/hr, A = 2.0 km^2
        # Q = 0.2778 * 0.6 * 50.0 * 2.0 = 16.668 m^3/s
        q = rational_peak_flow(0.6, 50.0, 2.0, system="si")
        assert pytest.approx(q, rel=1e-4) == 16.668

        # US: C = 0.6, I = 2.0 in/hr, A = 100 acres -> Q = 0.6 * 2.0 * 100 = 120 cfs
        q_us = rational_peak_flow(0.6, 2.0, 100.0, system="us")
        assert pytest.approx(q_us, rel=1e-4) == 120.0

    def test_kirpich_tc(self):
        # SI: L = 1000 m, S = 0.02
        tc = kirpich_tc(1000.0, 0.02, system="si")
        assert tc > 5.0 and tc < 30.0


class TestHydrographsAndRouting:
    """Tests for Snyder, SCS Unit Hydrographs, and Muskingum Routing."""

    def test_muskingum_coefficients_sum_to_one(self):
        # K = 12.0 hr, X = 0.2, dt = 6.0 hr
        # 2*K*(1-X) + dt = 2*12*0.8 + 6 = 19.2 + 6 = 25.2
        # C0 = (6 - 2*12*0.2) / 25.2 = (6 - 4.8) / 25.2 = 1.2 / 25.2 = 0.047619
        # C1 = (6 + 4.8) / 25.2 = 10.8 / 25.2 = 0.428571
        # C2 = (19.2 - 6) / 25.2 = 13.2 / 25.2 = 0.523810
        c0, c1, c2 = muskingum_coefficients(12.0, 0.2, 6.0)
        assert pytest.approx(c0 + c1 + c2, rel=1e-6) == 1.0
        assert pytest.approx(c0, rel=1e-4) == 0.047619
        assert pytest.approx(c1, rel=1e-4) == 0.428571
        assert pytest.approx(c2, rel=1e-4) == 0.523810

    def test_muskingum_hydrograph_routing(self):
        inflow = np.array([20.0, 50.0, 120.0, 90.0, 60.0, 35.0, 20.0])
        outflow = muskingum_route(inflow, travel_time_k=10.0, weighting_factor_x=0.2, time_step_dt=6.0)
        assert len(outflow) == len(inflow)
        assert outflow[0] == inflow[0]
        # Peak of outflow should lag and attenuate relative to inflow
        assert np.max(outflow) < np.max(inflow)


class TestHydraulicStructures:
    """Tests for Weirs, Flumes, Orifices, and Gates."""

    def test_francis_rectangular_weir(self):
        # L = 3.0 m, H = 0.5 m, n_e = 2
        # Q = 1.84 * (3.0 - 0.1 * 2 * 0.5) * (0.5)^1.5 = 1.84 * 2.9 * 0.35355 = 1.8865 m^3/s
        q = francis_weir(3.0, 0.5, contractions=2.0, system="si")
        assert pytest.approx(q, rel=1e-4) == 1.8865

    def test_v_notch_weir(self):
        # 90 degree V-notch (theta = 90 deg -> tan(45) = 1.0)
        # H = 0.3 m, Cd = 0.585, g = 9.80665
        q = v_notch_weir(90.0, 0.3, discharge_coeff=0.585, system="si")
        assert q > 0.0
        # Q proportional to H^2.5
        q2 = v_notch_weir(90.0, 0.6, discharge_coeff=0.585, system="si")
        assert pytest.approx(q2 / q, rel=1e-4) == (2.0 ** 2.5)

    def test_orifice_free_and_submerged(self):
        # Ao = 0.05 m^2, H = 4.0 m, Cd = 0.62
        # Q = 0.62 * 0.05 * sqrt(2 * 9.80665 * 4.0) = 0.031 * sqrt(78.4532) = 0.031 * 8.85738 = 0.27458 m^3/s
        q = orifice_free(0.05, 4.0, discharge_coeff=0.62, system="si")
        assert pytest.approx(q, rel=1e-4) == 0.27458

        # Submerged: H1 = 5.0, H2 = 1.0 -> Delta_H = 4.0 m
        q_sub = orifice_submerged(0.05, 5.0, 1.0, discharge_coeff=0.62, system="si")
        assert pytest.approx(q_sub, rel=1e-5) == q

    def test_sluice_gate_free(self):
        # b = 2.0 m, a = 0.4 m, y1 = 3.0 m, Cd = 0.6
        # Q = 0.6 * 2.0 * 0.4 * sqrt(2 * 9.80665 * 3.0) = 0.48 * 7.6707 = 3.6819 m^3/s
        q = sluice_gate_free(2.0, 0.4, 3.0, discharge_coeff=0.6, system="si")
        assert pytest.approx(q, rel=1e-4) == 3.6819


class TestGroundwater:
    """Tests for Darcy flow, Thiem equilibrium, and Theis well transient."""

    def test_darcy_flow_and_flux(self):
        # K = 1e-4 m/s, A = 100 m^2, dh/dl = -0.005
        # Q = -1e-4 * 100 * (-0.005) = 5e-5 m^3/s
        q = darcy_flow_1d(1e-4, 100.0, -0.005)
        assert pytest.approx(q, rel=1e-5) == 5e-5

        flux = darcy_flux(1e-4, -0.005)
        assert pytest.approx(flux, rel=1e-5) == 5e-7

    def test_thiem_confined(self):
        # T = 0.002 m^2/s, h1 = 20.0 m, h2 = 25.0 m, r1 = 10.0 m, r2 = 100.0 m
        # ln(100/10) = ln(10) = 2.302585
        # Q = (2 * pi * 0.002 * 5.0) / 2.302585 = 0.02728 m^3/s
        q = thiem_confined(0.002, 20.0, 25.0, 10.0, 100.0)
        assert pytest.approx(q, rel=1e-4) == 0.027288

    def test_theis_drawdown(self):
        # Benchmark Theis well test from Freeze & Cherry (1979) Chapter 8:
        # Q = 0.02 m^3/s, T = 0.001 m^2/s, S = 0.0002, r = 50.0 m, t = 86400 s (1 day)
        # u = (50^2 * 0.0002) / (4 * 0.001 * 86400) = 0.5 / 345.6 = 0.0014467
        # Since u < 0.01, Cooper-Jacob and Theis should agree within 0.1%!
        s_theis = theis_drawdown(0.02, 0.001, 0.0002, 50.0, 86400.0)
        s_cj = cooper_jacob_drawdown(0.02, 0.001, 0.0002, 50.0, 86400.0)
        assert isinstance(s_theis, float)
        assert s_theis > 0.0
        assert pytest.approx(s_theis, rel=0.005) == s_cj


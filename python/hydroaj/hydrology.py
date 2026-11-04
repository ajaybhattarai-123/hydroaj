"""
Surface Water Hydrology & Runoff API.
Provides polymorphic scalar and vectorized calculations backed by compiled Rust kernels.
"""
from typing import Any, Tuple, Union, Sequence, Optional
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import numpy as np
FloatOrArray = Union[float, int, Sequence[float], np.ndarray]
from . import _hydroaj_core as _core
from ._coercion import coerce_inputs, format_output, format_outputs
SCS_KS_SI = 25400.0
SCS_SUB_SI = 254.0
SCS_KS_US = 1000.0
SCS_SUB_US = 10.0
RATIONAL_K_SI = 0.2778
RATIONAL_K_US = 1.0
KIRPICH_K_SI = 0.01947
KIRPICH_K_US = 0.0078
SCS_PEAK_K_SI = 0.208
SCS_PEAK_K_US = 484.0

def idf_sherman(duration: FloatOrArray, a: FloatOrArray, b: FloatOrArray, c: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes idf sherman.
    Units (Default SI): duration [hours], a [SI units], b [SI units], c [SI units] -> returns [standard SI units]

    Formula:
    i = a / ((t_d + b)^c)

    Where (Default SI Units):
    - duration : Rainfall storm duration t_d [unit = hours]
    - a : Input parameter [unit = SI units]
    - b : Input parameter [unit = SI units]
    - c : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    duration : FloatOrArray
        Rainfall storm duration t_d [hours].
    a : FloatOrArray
        a [SI units].
    b : FloatOrArray
        b [SI units].
    c : FloatOrArray
        c [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t, a_v, b_v, c_v), is_scalar = coerce_inputs(duration, a, b, c)
    out = _core.idf_sherman(t, a_v, b_v, c_v)
    return format_output(out, is_scalar)

def thiessen_areal(weights: FloatOrArray, precip: FloatOrArray) -> float:
    """
    Thiessen polygon areal weighted mean rainfall:
    Units (Default SI): weights [SI units], precip [SI units] -> returns [standard SI units]

    Formula:
    thiessen_areal(weights, precip)

    Where (Default SI Units):
    - weights : Input parameter [unit = SI units]
    - precip : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    weights : FloatOrArray
        weights [SI units].
    precip : FloatOrArray
        precip [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (w, p), _ = coerce_inputs(weights, precip)
    return float(_core.thiessen_areal(w, p))

def horton_rate(time: FloatOrArray, initial_capacity: FloatOrArray, steady_capacity: FloatOrArray, decay_constant: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Horton infiltration rate: f_p = f_c + (f_0 - f_c) * exp(-k * t)
    Units (Default SI): time [hours], initial_capacity [mm/hr], steady_capacity [mm/hr], decay_constant [1/hr] -> returns [standard SI units]

    Formula:
    Horton infiltration rate: f_p = f_c + (f_0 - f_c) * exp(-k * t)

    Where (Default SI Units):
    - time : Elapsed infiltration or pumping time t [unit = hours]
    - initial_capacity : Initial Horton infiltration capacity f_0 [unit = mm/hr]
    - steady_capacity : Ultimate steady infiltration capacity f_c [unit = mm/hr]
    - decay_constant : Horton recession decay constant k [unit = 1/hr]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    time : FloatOrArray
        Elapsed infiltration or pumping time t [hours].
    initial_capacity : FloatOrArray
        Initial Horton infiltration capacity f_0 [mm/hr].
    steady_capacity : FloatOrArray
        Ultimate steady infiltration capacity f_c [mm/hr].
    decay_constant : FloatOrArray
        Horton recession decay constant k [1/hr].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t, f0, fc, k), is_scalar = coerce_inputs(time, initial_capacity, steady_capacity, decay_constant)
    out = _core.horton_rate(t, f0, fc, k)
    return format_output(out, is_scalar)

def horton_cumulative(time: FloatOrArray, initial_capacity: FloatOrArray, steady_capacity: FloatOrArray, decay_constant: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Horton cumulative infiltration: F = f_c * t + ((f_0 - f_c) / k) * (1 - exp(-k * t))
    Units (Default SI): time [hours], initial_capacity [mm/hr], steady_capacity [mm/hr], decay_constant [1/hr] -> returns [standard SI units]

    Formula:
    Horton cumulative infiltration: F = f_c * t + ((f_0 - f_c) / k) * (1 - exp(-k * t))

    Where (Default SI Units):
    - time : Elapsed infiltration or pumping time t [unit = hours]
    - initial_capacity : Initial Horton infiltration capacity f_0 [unit = mm/hr]
    - steady_capacity : Ultimate steady infiltration capacity f_c [unit = mm/hr]
    - decay_constant : Horton recession decay constant k [unit = 1/hr]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    time : FloatOrArray
        Elapsed infiltration or pumping time t [hours].
    initial_capacity : FloatOrArray
        Initial Horton infiltration capacity f_0 [mm/hr].
    steady_capacity : FloatOrArray
        Ultimate steady infiltration capacity f_c [mm/hr].
    decay_constant : FloatOrArray
        Horton recession decay constant k [1/hr].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t, f0, fc, k), is_scalar = coerce_inputs(time, initial_capacity, steady_capacity, decay_constant)
    out = _core.horton_cumulative(t, f0, fc, k)
    return format_output(out, is_scalar)

def green_ampt_rate(hydraulic_conductivity: FloatOrArray, suction_head: FloatOrArray, moisture_deficit: FloatOrArray, cumulative_depth: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes green ampt rate.
    Units (Default SI): hydraulic_conductivity [m/s], suction_head [m], moisture_deficit [dimensionless fraction], cumulative_depth [m] -> returns [standard SI units]

    Formula:
    f = K_s * (1 + (psi * delta_theta) / F)

    Where (Default SI Units):
    - hydraulic_conductivity : Darcy saturated hydraulic conductivity K [unit = m/s]
    - suction_head : Hydraulic head [unit = m]
    - moisture_deficit : Initial available soil moisture deficit Delta_theta [unit = dimensionless fraction]
    - cumulative_depth : Flow depth [unit = m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    hydraulic_conductivity : FloatOrArray
        Darcy saturated hydraulic conductivity K [m/s].
    suction_head : FloatOrArray
        suction_head [SI units].
    moisture_deficit : FloatOrArray
        Initial available soil moisture deficit Delta_theta [dimensionless fraction].
    cumulative_depth : FloatOrArray
        cumulative_depth [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (ks, psi, dt, f), is_scalar = coerce_inputs(hydraulic_conductivity, suction_head, moisture_deficit, cumulative_depth)
    out = _core.green_ampt_rate(ks, psi, dt, f)
    return format_output(out, is_scalar)

def scs_retention(curve_number: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    SCS Potential Maximum Retention S:
    Units (Default SI): curve_number [dimensionless (30 - 100)] -> returns [standard SI units]

    Formula:
    system : {'si', 'us'}, default='si'

    Where (Default SI Units):
    - curve_number : SCS Runoff Curve Number CN [unit = dimensionless (30 - 100)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    curve_number : FloatOrArray
        SCS Runoff Curve Number CN [dimensionless (30 - 100)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (cn,), is_scalar = coerce_inputs(curve_number)
    ks = SCS_KS_US if system.lower() == 'us' else SCS_KS_SI
    sub = SCS_SUB_US if system.lower() == 'us' else SCS_SUB_SI
    out = _core.scs_retention(cn, ks, sub)
    return format_output(out, is_scalar)

def scs_runoff_depth(precip: FloatOrArray, retention: FloatOrArray, lambda_ratio: FloatOrArray=0.2) -> Union[float, np.ndarray]:
    """
    Computes scs runoff depth.
    Units (Default SI): precip [SI units], retention [mm], lambda_ratio [SI units] -> returns [m]

    Formula:
    Q = ((P - I_a)^2) / (P - I_a + S) if P > I_a else 0.0; I_a = lambda_coef * S

    Where (Default SI Units):
    - precip : Input parameter [unit = SI units]
    - retention : Potential maximum soil retention S [unit = mm]
    - lambda_ratio : Input parameter [unit = SI units]
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    precip : FloatOrArray
        precip [SI units].
    retention : FloatOrArray
        Potential maximum soil retention S [mm].
    lambda_ratio : FloatOrArray
        lambda_ratio [SI units].

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (p, s, lam), is_scalar = coerce_inputs(precip, retention, lambda_ratio)
    out = _core.scs_runoff_depth(p, s, lam)
    return format_output(out, is_scalar)

def rational_peak_flow(runoff_coefficient: FloatOrArray, intensity: FloatOrArray, area: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes rational peak flow.
    Units (Default SI): runoff_coefficient [dimensionless], intensity [mm/hr], area [m^2] -> returns [standard SI units]

    Formula:
    Q = 0.2778 * C * I * A (SI: Q m^3/s, I mm/hr, A km^2) or Q = C * I * A (US: Q cfs, I in/hr, A acres)

    Where (Default SI Units):
    - runoff_coefficient : Input parameter [unit = dimensionless]
    - intensity : Design rainfall intensity I [unit = mm/hr]
    - area : Cross-sectional flow area A [unit = m^2]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    runoff_coefficient : FloatOrArray
        runoff_coefficient [SI units].
    intensity : FloatOrArray
        Design rainfall intensity I [mm/hr].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (c, i, a), is_scalar = coerce_inputs(runoff_coefficient, intensity, area)
    k_factor = RATIONAL_K_US if system.lower() == 'us' else RATIONAL_K_SI
    out = _core.rational_peak_flow(c, i, a, k_factor)
    return format_output(out, is_scalar)

def kirpich_tc(length: FloatOrArray, slope: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Kirpich time of concentration t_c (in minutes):
    Units (Default SI): length [m], slope [m/m (decimal)] -> returns [minutes]

    Formula:
    US: t_c = 0.0078 * L^0.77 * S^(-0.385) (L in ft)

    Where (Default SI Units):
    - length : Reach / conduit / flow path length L [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Time parameter [unit = minutes]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Time parameter [minutes]. Returns float for scalar inputs.
    """
    (l, s), is_scalar = coerce_inputs(length, slope)
    k_k = KIRPICH_K_US if system.lower() == 'us' else KIRPICH_K_SI
    out = _core.kirpich_tc(l, s, k_k)
    return format_output(out, is_scalar)

def snyder(basin_length: FloatOrArray, length_to_centroid: FloatOrArray, area: FloatOrArray, c_t: FloatOrArray=1.5, c_p: FloatOrArray=0.6, system: Literal['si', 'us']='si') -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Snyder's synthetic unit hydrograph parameters:
    Units (Default SI): basin_length [m], length_to_centroid [km], area [m^2], c_t [dimensionless (1.0 - 2.2)], c_p [dimensionless (0.4 - 0.8)] -> returns [standard SI units]

    Formula:
    system : {'si', 'us'}, default='si'

    Where (Default SI Units):
    - basin_length : Length [unit = m]
    - length_to_centroid : Channel length to basin centroid L_c [unit = km]
    - area : Cross-sectional flow area A [unit = m^2]
    - c_t : Snyder's basin lag coefficient C_t [unit = dimensionless (1.0 - 2.2)]
    - c_p : Snyder's peak coefficient C_p [unit = dimensionless (0.4 - 0.8)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    basin_length : FloatOrArray
        basin_length [SI units].
    length_to_centroid : FloatOrArray
        Channel length to basin centroid L_c [km].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    c_t : FloatOrArray
        Snyder's basin lag coefficient C_t [dimensionless (1.0 - 2.2)].
    c_p : FloatOrArray
        Snyder's peak coefficient C_p [dimensionless (0.4 - 0.8)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (l, lc, a, ct, cp), is_scalar = coerce_inputs(basin_length, length_to_centroid, area, c_t, c_p)
    k_sny = 1.0 if system.lower() == 'us' else 0.2778
    outs = _core.snyder(l, lc, a, ct, cp, k_sny)
    return format_outputs(outs, is_scalar)

def scs_peak_flow(area: FloatOrArray, time_to_peak: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    SCS Dimensionless Unit Hydrograph peak discharge:
    Units (Default SI): area [m^2], time_to_peak [hours] -> returns [standard SI units]

    Formula:
    US: q_p = (484.0 * A) / t_p (A in mi^2, t_p in hr, q_p in cfs)

    Where (Default SI Units):
    - area : Cross-sectional flow area A [unit = m^2]
    - time_to_peak : Time to hydrograph peak T_p [unit = hours]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    time_to_peak : FloatOrArray
        Time to hydrograph peak T_p [hours].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (a, tp), is_scalar = coerce_inputs(area, time_to_peak)
    k_scs = SCS_PEAK_K_US if system.lower() == 'us' else SCS_PEAK_K_SI
    out = _core.scs_peak_flow(a, tp, k_scs)
    return format_output(out, is_scalar)

def muskingum_coefficients(travel_time_k: FloatOrArray, weighting_factor_x: FloatOrArray, time_step_dt: FloatOrArray) -> Tuple[Union[float, np.ndarray], ...]:
    """
    Computes muskingum coefficients.
    Units (Default SI): travel_time_k [hours], weighting_factor_x [SI units], time_step_dt [hours] -> returns [standard SI units]

    Formula:
    C_0 = (dt - 2*K*X)/(2*K*(1-X) + dt); C_1 = (dt + 2*K*X)/(2*K*(1-X) + dt); C_2 = (2*K*(1-X) - dt)/(2*K*(1-X) + dt)

    Where (Default SI Units):
    - travel_time_k : Time parameter [unit = hours]
    - weighting_factor_x : Input parameter [unit = SI units]
    - time_step_dt : Time parameter [unit = hours]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    travel_time_k : FloatOrArray
        travel_time_k [SI units].
    weighting_factor_x : FloatOrArray
        weighting_factor_x [SI units].
    time_step_dt : FloatOrArray
        time_step_dt [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (k, x, dt), is_scalar = coerce_inputs(travel_time_k, weighting_factor_x, time_step_dt)
    outs = _core.muskingum_coefficients(k, x, dt)
    return format_outputs(outs, is_scalar)

def muskingum_route(inflow: FloatOrArray, travel_time_k: FloatOrArray, weighting_factor_x: FloatOrArray, time_step_dt: FloatOrArray, initial_outflow: FloatOrArray=None) -> np.ndarray:
    """
    Routes an inflow hydrograph series through a reach using Muskingum equation:
    Units (Default SI): inflow [SI units], travel_time_k [hours], weighting_factor_x [SI units], time_step_dt [hours], initial_outflow [SI units] -> returns [standard SI units]

    Formula:
    Q[j+1] = C_0 * I[j+1] + C_1 * I[j] + C_2 * Q[j]

    Where (Default SI Units):
    - inflow : Input parameter [unit = SI units]
    - travel_time_k : Time parameter [unit = hours]
    - weighting_factor_x : Input parameter [unit = SI units]
    - time_step_dt : Time parameter [unit = hours]
    - initial_outflow : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    inflow : FloatOrArray
        inflow [SI units].
    travel_time_k : FloatOrArray
        travel_time_k [SI units].
    weighting_factor_x : FloatOrArray
        weighting_factor_x [SI units].
    time_step_dt : FloatOrArray
        time_step_dt [SI units].
    initial_outflow : FloatOrArray
        initial_outflow [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (inf,), _ = coerce_inputs(inflow)
    if initial_outflow is None:
        initial_outflow = float(inf[0])
    return _core.muskingum_route(inf, float(travel_time_k), float(weighting_factor_x), float(time_step_dt), float(initial_outflow))

def scs_composite_cn(subareas: FloatOrArray, curve_numbers: FloatOrArray) -> float:
    """
    Computes scs composite cn.
    Units (Default SI): subareas [m^2], curve_numbers [SI units] -> returns [dimensionless]

    Formula:
    CN_bar = sum(A_i * CN_i) / sum(A_i)

    Where (Default SI Units):
    - subareas : Area [unit = m^2]
    - curve_numbers : Input parameter [unit = SI units]
    - Output : Runoff / discharge coefficient [unit = dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    subareas : FloatOrArray
        subareas [SI units].
    curve_numbers : FloatOrArray
        curve_numbers [SI units].

    Returns
    -------
    float | np.ndarray
        Runoff / discharge coefficient [dimensionless]. Returns float for scalar inputs.
    """
    a = np.ascontiguousarray(subareas, dtype=np.float64)
    cn = np.ascontiguousarray(curve_numbers, dtype=np.float64)
    return float(_core.scs_composite_cn(a, cn))

def scs_cn_amc_i(curve_number_amc2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes scs cn amc i.
    Units (Default SI): curve_number_amc2 [SI units] -> returns [standard SI units]

    Formula:
    CN_I = (4.2 * CN_II) / (10.0 - 0.058 * CN_II)

    Where (Default SI Units):
    - curve_number_amc2 : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    curve_number_amc2 : FloatOrArray
        curve_number_amc2 [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (cn2,), is_scalar = coerce_inputs(curve_number_amc2)
    out = _core.scs_cn_amc_i(cn2)
    return format_output(out, is_scalar)

def scs_cn_amc_iii(curve_number_amc2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes scs cn amc iii.
    Units (Default SI): curve_number_amc2 [SI units] -> returns [standard SI units]

    Formula:
    CN_III = (23.0 * CN_II) / (10.0 + 0.13 * CN_II)

    Where (Default SI Units):
    - curve_number_amc2 : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    curve_number_amc2 : FloatOrArray
        curve_number_amc2 [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (cn2,), is_scalar = coerce_inputs(curve_number_amc2)
    out = _core.scs_cn_amc_iii(cn2)
    return format_output(out, is_scalar)

def tr55_sheet_flow_time(sheet_roughness: FloatOrArray, flow_length: FloatOrArray, two_year_24hr_precip: FloatOrArray, land_slope: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes tr55 sheet flow time.
    Units (Default SI): sheet_roughness [SI units], flow_length [m], two_year_24hr_precip [SI units], land_slope [m/m] -> returns [standard SI units]

    Formula:
    T_t = (0.007 * (n * L)^0.8) / (P_2^0.5 * s^0.4) (hr)

    Where (Default SI Units):
    - sheet_roughness : Input parameter [unit = SI units]
    - flow_length : Length [unit = m]
    - two_year_24hr_precip : Input parameter [unit = SI units]
    - land_slope : Longitudinal bed slope / gradient [unit = m/m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    sheet_roughness : FloatOrArray
        sheet_roughness [SI units].
    flow_length : FloatOrArray
        flow_length [SI units].
    two_year_24hr_precip : FloatOrArray
        two_year_24hr_precip [SI units].
    land_slope : FloatOrArray
        land_slope [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (n, l, p2, s), is_scalar = coerce_inputs(sheet_roughness, flow_length, two_year_24hr_precip, land_slope)
    out = _core.tr55_sheet_flow_time(n, l, p2, s)
    return format_output(out, is_scalar)

def tr55_shallow_concentrated_velocity(land_slope: FloatOrArray, surface_coeff: FloatOrArray=16.1345) -> Union[float, np.ndarray]:
    """
    Computes tr55 shallow concentrated velocity.
    Units (Default SI): land_slope [m/m], surface_coeff [dimensionless] -> returns [m/s]

    Formula:
    V = k_surface * sqrt(s) (k=16.1345 unpaved, k=20.3282 paved in ft/s)

    Where (Default SI Units):
    - land_slope : Longitudinal bed slope / gradient [unit = m/m]
    - surface_coeff : Input parameter [unit = dimensionless]
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    land_slope : FloatOrArray
        land_slope [SI units].
    surface_coeff : FloatOrArray
        surface_coeff [SI units].

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (s, k), is_scalar = coerce_inputs(land_slope, surface_coeff)
    out = _core.tr55_shallow_concentrated_velocity(s, k)
    return format_output(out, is_scalar)

def gumbel_flood_frequency(sample_mean: FloatOrArray, sample_std: FloatOrArray, return_period: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes gumbel flood frequency.
    Units (Default SI): sample_mean [SI units], sample_std [SI units], return_period [years] -> returns [standard SI units]

    Formula:
    X_T = mean_X + K_T * std_X; K_T = -(sqrt(6)/pi) * (0.5772 + ln(ln(T / (T - 1))))

    Where (Default SI Units):
    - sample_mean : Input parameter [unit = SI units]
    - sample_std : Input parameter [unit = SI units]
    - return_period : Design recurrence interval / return period T [unit = years]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    sample_mean : FloatOrArray
        sample_mean [SI units].
    sample_std : FloatOrArray
        sample_std [SI units].
    return_period : FloatOrArray
        Design recurrence interval / return period T [years].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (mx, sx, t), is_scalar = coerce_inputs(sample_mean, sample_std, return_period)
    out = _core.gumbel_flood_frequency(mx, sx, t)
    return format_output(out, is_scalar)

def nash_cascade_iuh(time: FloatOrArray, number_reservoirs: FloatOrArray, storage_constant: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes nash cascade iuh.
    Units (Default SI): time [hours], number_reservoirs [SI units], storage_constant [SI units] -> returns [standard SI units]

    Formula:
    u(t) = (1 / (K * gamma(n))) * (t / K)^(n - 1) * exp(-t / K)

    Where (Default SI Units):
    - time : Elapsed infiltration or pumping time t [unit = hours]
    - number_reservoirs : Input parameter [unit = SI units]
    - storage_constant : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    time : FloatOrArray
        Elapsed infiltration or pumping time t [hours].
    number_reservoirs : FloatOrArray
        number_reservoirs [SI units].
    storage_constant : FloatOrArray
        storage_constant [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t, n_res, k), is_scalar = coerce_inputs(time, number_reservoirs, storage_constant)
    out = _core.nash_cascade_iuh(t, n_res, k)
    return format_output(out, is_scalar)

def hargreaves_samani_et0(extraterrestrial_radiation: FloatOrArray, mean_temp: FloatOrArray, max_temp: FloatOrArray, min_temp: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes hargreaves samani et0.
    Units (Default SI): extraterrestrial_radiation [SI units], mean_temp [SI units], max_temp [SI units], min_temp [SI units] -> returns [mm/day]

    Formula:
    ET_0 = 0.0023 * R_a * (T_mean + 17.8) * sqrt(T_max - T_min)

    Where (Default SI Units):
    - extraterrestrial_radiation : Input parameter [unit = SI units]
    - mean_temp : Input parameter [unit = SI units]
    - max_temp : Input parameter [unit = SI units]
    - min_temp : Input parameter [unit = SI units]
    - Output : Reference evapotranspiration [unit = mm/day]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    extraterrestrial_radiation : FloatOrArray
        extraterrestrial_radiation [SI units].
    mean_temp : FloatOrArray
        mean_temp [SI units].
    max_temp : FloatOrArray
        max_temp [SI units].
    min_temp : FloatOrArray
        min_temp [SI units].

    Returns
    -------
    float | np.ndarray
        Reference evapotranspiration [mm/day]. Returns float for scalar inputs.
    """
    (ra, tm, tmax, tmin), is_scalar = coerce_inputs(extraterrestrial_radiation, mean_temp, max_temp, min_temp)
    out = _core.hargreaves_samani_et0(ra, tm, tmax, tmin)
    return format_output(out, is_scalar)

def net_radiation_equivalent_evap(net_radiation_mj: FloatOrArray, latent_heat_vaporization: FloatOrArray=2450000.0, water_density: FloatOrArray=1000.0) -> Union[float, np.ndarray]:
    """
    Computes net radiation equivalent evap.
    Units (Default SI): net_radiation_mj [SI units], latent_heat_vaporization [SI units], water_density [SI units] -> returns [mm/day]

    Formula:
    R_n_mm = (R_n_MJ * 1e6) / (rho_w * lambda_latent)

    Where (Default SI Units):
    - net_radiation_mj : Input parameter [unit = SI units]
    - latent_heat_vaporization : Input parameter [unit = SI units]
    - water_density : Input parameter [unit = SI units]
    - Output : Reference evapotranspiration [unit = mm/day]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    net_radiation_mj : FloatOrArray
        net_radiation_mj [SI units].
    latent_heat_vaporization : FloatOrArray
        latent_heat_vaporization [SI units].
    water_density : FloatOrArray
        water_density [SI units].

    Returns
    -------
    float | np.ndarray
        Reference evapotranspiration [mm/day]. Returns float for scalar inputs.
    """
    (rn, lam), is_scalar = coerce_inputs(net_radiation_mj, latent_heat_vaporization)
    out = _core.net_radiation_equivalent_evap(rn, lam, water_density)
    return format_output(out, is_scalar)

def time_area_runoff_step(effective_excess_precip: FloatOrArray, isochrone_subarea: FloatOrArray, unit_conversion: FloatOrArray=0.278) -> float:
    """
    Computes time area runoff step.
    Units (Default SI): effective_excess_precip [SI units], isochrone_subarea [m^2], unit_conversion [SI units] -> returns [standard SI units]

    Formula:
    Q_j = sum(I_{j - k + 1} * A_k) * k_unit

    Where (Default SI Units):
    - effective_excess_precip : Input parameter [unit = SI units]
    - isochrone_subarea : Area [unit = m^2]
    - unit_conversion : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    effective_excess_precip : FloatOrArray
        effective_excess_precip [SI units].
    isochrone_subarea : FloatOrArray
        isochrone_subarea [SI units].
    unit_conversion : FloatOrArray
        unit_conversion [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    ie = np.ascontiguousarray(effective_excess_precip, dtype=np.float64)
    ak = np.ascontiguousarray(isochrone_subarea, dtype=np.float64)
    return float(_core.time_area_runoff_step(ie, ak, unit_conversion))
rational_q = rational_peak_flow

def rational_c(discharge: FloatOrArray, intensity: FloatOrArray, drainage_area: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes rational c.
    Units (Default SI): discharge [m^3/s], intensity [mm/hr], drainage_area [km^2 (or ha for Rational)] -> returns [dimensionless]

    Formula:
    C = Q / (k_rat * I * A)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - intensity : Design rainfall intensity I [unit = mm/hr]
    - drainage_area : Catchment drainage area A [unit = km^2 (or ha for Rational)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Runoff / discharge coefficient [unit = dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    intensity : FloatOrArray
        Design rainfall intensity I [mm/hr].
    drainage_area : FloatOrArray
        Catchment drainage area A [km^2 (or ha for Rational)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Runoff / discharge coefficient [dimensionless]. Returns float for scalar inputs.
    """
    (q, i, a), is_scalar = coerce_inputs(discharge, intensity, drainage_area)
    k = 1.008 if system.lower() == 'us' else 0.2778
    out = _core.rational_c(q, i, a, k)
    return format_output(out, is_scalar)
rational_runoff_coeff = rational_c

def rational_i(discharge: FloatOrArray, runoff_coeff: FloatOrArray, drainage_area: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Rainfall intensity i = Q / (k * C * A)
    Units (Default SI): discharge [m^3/s], runoff_coeff [dimensionless (0.05 - 0.95)], drainage_area [km^2 (or ha for Rational)] -> returns [standard SI units]

    Formula:
    Inversion: Rainfall intensity i = Q / (k * C * A)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - runoff_coeff : Rational runoff coefficient C [unit = dimensionless (0.05 - 0.95)]
    - drainage_area : Catchment drainage area A [unit = km^2 (or ha for Rational)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    runoff_coeff : FloatOrArray
        Rational runoff coefficient C [dimensionless (0.05 - 0.95)].
    drainage_area : FloatOrArray
        Catchment drainage area A [km^2 (or ha for Rational)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, c, a), is_scalar = coerce_inputs(discharge, runoff_coeff, drainage_area)
    k = 1.008 if system.lower() == 'us' else 0.2778
    out = _core.rational_i(q, c, a, k)
    return format_output(out, is_scalar)
rational_intensity = rational_i

def rational_a(discharge: FloatOrArray, runoff_coeff: FloatOrArray, intensity: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes rational a.
    Units (Default SI): discharge [m^3/s], runoff_coeff [dimensionless (0.05 - 0.95)], intensity [mm/hr] -> returns [km^2 if 'km' in fn else 'm^2']

    Formula:
    A = Q / (k_rat * C * I)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - runoff_coeff : Rational runoff coefficient C [unit = dimensionless (0.05 - 0.95)]
    - intensity : Design rainfall intensity I [unit = mm/hr]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Area [unit = km^2 if 'km' in fn else 'm^2']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    runoff_coeff : FloatOrArray
        Rational runoff coefficient C [dimensionless (0.05 - 0.95)].
    intensity : FloatOrArray
        Design rainfall intensity I [mm/hr].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Area [km^2 if 'km' in fn else 'm^2']. Returns float for scalar inputs.
    """
    (q, c, i), is_scalar = coerce_inputs(discharge, runoff_coeff, intensity)
    k = 1.008 if system.lower() == 'us' else 0.2778
    out = _core.rational_a(q, c, i, k)
    return format_output(out, is_scalar)
rational_drainage_area = rational_a
scs_cn_s = scs_retention

def scs_cn_cn(potential_retention: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes scs cn cn.
    Units (Default SI): potential_retention [SI units] -> returns [dimensionless]

    Formula:
    CN = k_cn1 / (S + k_cn2)

    Where (Default SI Units):
    - potential_retention : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Runoff / discharge coefficient [unit = dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    potential_retention : FloatOrArray
        potential_retention [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Runoff / discharge coefficient [dimensionless]. Returns float for scalar inputs.
    """
    (s,), is_scalar = coerce_inputs(potential_retention)
    factor = 1000.0 if system.lower() == 'us' else 25400.0
    offset = 10.0 if system.lower() == 'us' else 254.0
    out = _core.scs_cn_cn(s, factor, offset)
    return format_output(out, is_scalar)
scs_curve_number = scs_cn_cn
scs_cn_q = scs_runoff_depth

def scs_cn_p(runoff_depth: FloatOrArray, potential_retention: FloatOrArray, initial_abstraction_ratio: FloatOrArray=0.2) -> Union[float, np.ndarray]:
    """
    Computes scs cn p.
    Units (Default SI): runoff_depth [m], potential_retention [SI units], initial_abstraction_ratio [SI units] -> returns [standard SI units]

    Formula:
    P = lambda * S + (Q + sqrt(Q^2 + 4 * Q * S)) / 2

    Where (Default SI Units):
    - runoff_depth : Flow depth [unit = m]
    - potential_retention : Input parameter [unit = SI units]
    - initial_abstraction_ratio : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    runoff_depth : FloatOrArray
        runoff_depth [SI units].
    potential_retention : FloatOrArray
        potential_retention [SI units].
    initial_abstraction_ratio : FloatOrArray
        initial_abstraction_ratio [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, s, lam), is_scalar = coerce_inputs(runoff_depth, potential_retention, initial_abstraction_ratio)
    out = _core.scs_cn_p(q, s, lam)
    return format_output(out, is_scalar)
scs_precipitation = scs_cn_p

def horton_rate_fp(initial_capacity: FloatOrArray, steady_capacity: FloatOrArray, decay_constant: FloatOrArray, time: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes horton rate fp.
    Units (Default SI): initial_capacity [mm/hr], steady_capacity [mm/hr], decay_constant [1/hr], time [hours] -> returns [standard SI units]

    Formula:
    f_p = f_c + (f_0 - f_c) * exp(-k * t)

    Where (Default SI Units):
    - initial_capacity : Initial Horton infiltration capacity f_0 [unit = mm/hr]
    - steady_capacity : Ultimate steady infiltration capacity f_c [unit = mm/hr]
    - decay_constant : Horton recession decay constant k [unit = 1/hr]
    - time : Elapsed infiltration or pumping time t [unit = hours]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    initial_capacity : FloatOrArray
        Initial Horton infiltration capacity f_0 [mm/hr].
    steady_capacity : FloatOrArray
        Ultimate steady infiltration capacity f_c [mm/hr].
    decay_constant : FloatOrArray
        Horton recession decay constant k [1/hr].
    time : FloatOrArray
        Elapsed infiltration or pumping time t [hours].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (f0, fc, k, t), is_scalar = coerce_inputs(initial_capacity, steady_capacity, decay_constant, time)
    out = _core.horton_rate(t, f0, fc, k)
    return format_output(out, is_scalar)

def horton_rate_f0(rate_fp: FloatOrArray, rate_fc: FloatOrArray, decay_k: FloatOrArray, time_t: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Initial infiltration rate f_0 = f_c + (f_p - f_c) * exp(k * t)
    Units (Default SI): rate_fp [SI units], rate_fc [SI units], decay_k [SI units], time_t [hours] -> returns [standard SI units]

    Formula:
    Inversion: Initial infiltration rate f_0 = f_c + (f_p - f_c) * exp(k * t)

    Where (Default SI Units):
    - rate_fp : Input parameter [unit = SI units]
    - rate_fc : Input parameter [unit = SI units]
    - decay_k : Input parameter [unit = SI units]
    - time_t : Time parameter [unit = hours]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    rate_fp : FloatOrArray
        rate_fp [SI units].
    rate_fc : FloatOrArray
        rate_fc [SI units].
    decay_k : FloatOrArray
        decay_k [SI units].
    time_t : FloatOrArray
        time_t [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (fp, fc, k, t), is_scalar = coerce_inputs(rate_fp, rate_fc, decay_k, time_t)
    out = _core.horton_rate_f0(fp, fc, k, t)
    return format_output(out, is_scalar)
horton_initial_rate = horton_rate_f0

def horton_rate_fc(rate_fp: FloatOrArray, rate_f0: FloatOrArray, decay_k: FloatOrArray, time_t: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Steady infiltration capacity f_c = (f_p - f_0 * exp(-k*t)) / (1 - exp(-k*t))
    Units (Default SI): rate_fp [SI units], rate_f0 [SI units], decay_k [SI units], time_t [hours] -> returns [standard SI units]

    Formula:
    Inversion: Steady infiltration capacity f_c = (f_p - f_0 * exp(-k*t)) / (1 - exp(-k*t))

    Where (Default SI Units):
    - rate_fp : Input parameter [unit = SI units]
    - rate_f0 : Input parameter [unit = SI units]
    - decay_k : Input parameter [unit = SI units]
    - time_t : Time parameter [unit = hours]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    rate_fp : FloatOrArray
        rate_fp [SI units].
    rate_f0 : FloatOrArray
        rate_f0 [SI units].
    decay_k : FloatOrArray
        decay_k [SI units].
    time_t : FloatOrArray
        time_t [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (fp, f0, k, t), is_scalar = coerce_inputs(rate_fp, rate_f0, decay_k, time_t)
    out = _core.horton_rate_fc(fp, f0, k, t)
    return format_output(out, is_scalar)
horton_constant_rate = horton_rate_fc

def horton_rate_k(rate_fp: FloatOrArray, rate_f0: FloatOrArray, rate_fc: FloatOrArray, time_t: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes horton rate k.
    Units (Default SI): rate_fp [SI units], rate_f0 [SI units], rate_fc [SI units], time_t [hours] -> returns [standard SI units]

    Formula:
    k = -ln((f_p - f_c) / (f_0 - f_c)) / t

    Where (Default SI Units):
    - rate_fp : Input parameter [unit = SI units]
    - rate_f0 : Input parameter [unit = SI units]
    - rate_fc : Input parameter [unit = SI units]
    - time_t : Time parameter [unit = hours]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    rate_fp : FloatOrArray
        rate_fp [SI units].
    rate_f0 : FloatOrArray
        rate_f0 [SI units].
    rate_fc : FloatOrArray
        rate_fc [SI units].
    time_t : FloatOrArray
        time_t [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (fp, f0, fc, t), is_scalar = coerce_inputs(rate_fp, rate_f0, rate_fc, time_t)
    out = _core.horton_rate_k(fp, f0, fc, t)
    return format_output(out, is_scalar)
horton_decay_rate = horton_rate_k

def kirpich_s(time_of_concentration_min: FloatOrArray, flow_length: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Watershed slope S = (k * L^0.77 / t_c)^(1 / 0.385)
    Units (Default SI): time_of_concentration_min [hours], flow_length [m] -> returns [m/m]

    Formula:
    Inversion: Watershed slope S = (k * L^0.77 / t_c)^(1 / 0.385)

    Where (Default SI Units):
    - time_of_concentration_min : Time parameter [unit = hours]
    - flow_length : Length [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    time_of_concentration_min : FloatOrArray
        time_of_concentration_min [SI units].
    flow_length : FloatOrArray
        flow_length [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (tc, l), is_scalar = coerce_inputs(time_of_concentration_min, flow_length)
    k = KIRPICH_K_US if system.lower() == 'us' else KIRPICH_K_SI
    out = _core.kirpich_s(tc, l, k)
    return format_output(out, is_scalar)
kirpich_slope = kirpich_s

def kirpich_l(time_of_concentration_min: FloatOrArray, slope: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Flow path length L = (t_c * S^0.385 / k)^(1 / 0.77)
    Units (Default SI): time_of_concentration_min [hours], slope [m/m (decimal)] -> returns [km if 'km' in fn else 'm']

    Formula:
    Inversion: Flow path length L = (t_c * S^0.385 / k)^(1 / 0.77)

    Where (Default SI Units):
    - time_of_concentration_min : Time parameter [unit = hours]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    time_of_concentration_min : FloatOrArray
        time_of_concentration_min [SI units].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (tc, s), is_scalar = coerce_inputs(time_of_concentration_min, slope)
    k = KIRPICH_K_US if system.lower() == 'us' else KIRPICH_K_SI
    out = _core.kirpich_l(tc, s, k)
    return format_output(out, is_scalar)
kirpich_length = kirpich_l
scs_amc_cni = scs_cn_amc_i
scs_amc_cniii = scs_cn_amc_iii

def scs_amc_cnii_from_i(cn_i: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Normal condition CN_II from dry condition CN_I
    Units (Default SI): cn_i [SI units] -> returns [standard SI units]

    Formula:
    scs_amc_cnii_from_i(cn_i)

    Where (Default SI Units):
    - cn_i : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    cn_i : FloatOrArray
        cn_i [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (cni,), is_scalar = coerce_inputs(cn_i)
    out = _core.scs_amc_cnii_from_i(cni)
    return format_output(out, is_scalar)
scs_cn_ii_from_i = scs_amc_cnii_from_i

def scs_amc_cnii_from_iii(cn_iii: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Normal condition CN_II from wet condition CN_III
    Units (Default SI): cn_iii [SI units] -> returns [standard SI units]

    Formula:
    scs_amc_cnii_from_iii(cn_iii)

    Where (Default SI Units):
    - cn_iii : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    cn_iii : FloatOrArray
        cn_iii [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (cniii,), is_scalar = coerce_inputs(cn_iii)
    out = _core.scs_amc_cnii_from_iii(cniii)
    return format_output(out, is_scalar)
scs_cn_ii_from_iii = scs_amc_cnii_from_iii

def tr55_shallow_v(slope: FloatOrArray, surface_coeff: FloatOrArray=None, surface_type: FloatOrArray='unpaved', system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    TR-55 shallow concentrated flow velocity: V = k * sqrt(S)
    Units (Default SI): slope [m/m (decimal)], surface_coeff [dimensionless], surface_type [SI units] -> returns [m/s]

    Formula:
    TR-55 shallow concentrated flow velocity: V = k * sqrt(S)

    Where (Default SI Units):
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - surface_coeff : Input parameter [unit = dimensionless]
    - surface_type : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    surface_coeff : FloatOrArray
        surface_coeff [SI units].
    surface_type : FloatOrArray
        surface_type [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    if surface_coeff is None:
        is_us = system.lower() == 'us'
        if str(surface_type).lower() == 'paved':
            surface_coeff = 20.3282 if is_us else 6.196
        else:
            surface_coeff = 16.1345 if is_us else 4.918
    (s, k), is_scalar = coerce_inputs(slope, surface_coeff)
    out = _core.tr55_shallow_concentrated_velocity(s, k)
    return format_output(out, is_scalar)

def tr55_shallow_s(velocity: FloatOrArray, surface_coeff: FloatOrArray=None, surface_type: FloatOrArray='unpaved', system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Ground slope S = (V / k)^2
    Units (Default SI): velocity [m/s], surface_coeff [dimensionless], surface_type [SI units] -> returns [m/m]

    Formula:
    Inversion: Ground slope S = (V / k)^2

    Where (Default SI Units):
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - surface_coeff : Input parameter [unit = dimensionless]
    - surface_type : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    surface_coeff : FloatOrArray
        surface_coeff [SI units].
    surface_type : FloatOrArray
        surface_type [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    if surface_coeff is None:
        is_us = system.lower() == 'us'
        if str(surface_type).lower() == 'paved':
            surface_coeff = 20.3282 if is_us else 6.196
        else:
            surface_coeff = 16.1345 if is_us else 4.918
    (v,), is_scalar = coerce_inputs(velocity)
    k_val = float(surface_coeff)
    out = _core.tr55_shallow_s(v, k_val)
    return format_output(out, is_scalar)
tr55_shallow_slope = tr55_shallow_s

def hargreaves_et0(temp_mean_c: FloatOrArray, temp_max_c: FloatOrArray, temp_min_c: FloatOrArray, extraterrestrial_radiation: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Hargreaves reference ET: ET_0 = 0.0023 * R_a * (T_mean + 17.8) * sqrt(T_max - T_min)
    Units (Default SI): temp_mean_c [deg C], temp_max_c [deg C], temp_min_c [deg C], extraterrestrial_radiation [SI units] -> returns [mm/day]

    Formula:
    Hargreaves reference ET: ET_0 = 0.0023 * R_a * (T_mean + 17.8) * sqrt(T_max - T_min)

    Where (Default SI Units):
    - temp_mean_c : Mean air temperature T_mean [unit = deg C]
    - temp_max_c : Daily maximum air temperature T_max [unit = deg C]
    - temp_min_c : Daily minimum air temperature T_min [unit = deg C]
    - extraterrestrial_radiation : Input parameter [unit = SI units]
    - Output : Reference evapotranspiration [unit = mm/day]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    temp_mean_c : FloatOrArray
        Mean air temperature T_mean [deg C].
    temp_max_c : FloatOrArray
        Daily maximum air temperature T_max [deg C].
    temp_min_c : FloatOrArray
        Daily minimum air temperature T_min [deg C].
    extraterrestrial_radiation : FloatOrArray
        extraterrestrial_radiation [SI units].

    Returns
    -------
    float | np.ndarray
        Reference evapotranspiration [mm/day]. Returns float for scalar inputs.
    """
    (tm, tmax, tmin, ra), is_scalar = coerce_inputs(temp_mean_c, temp_max_c, temp_min_c, extraterrestrial_radiation)
    out = _core.hargreaves_samani_et0(ra, tm, tmax, tmin)
    return format_output(out, is_scalar)

def hargreaves_ra(et0: FloatOrArray, temp_mean_c: FloatOrArray, temp_max_c: FloatOrArray, temp_min_c: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Extraterrestrial radiation R_a = ET_0 / (0.0023 * (T_mean + 17.8) * sqrt(T_max - T_min))
    Units (Default SI): et0 [mm/day], temp_mean_c [deg C], temp_max_c [deg C], temp_min_c [deg C] -> returns [standard SI units]

    Formula:
    Inversion: Extraterrestrial radiation R_a = ET_0 / (0.0023 * (T_mean + 17.8) * sqrt(T_max - T_min))

    Where (Default SI Units):
    - et0 : Reference evapotranspiration ET_0 [unit = mm/day]
    - temp_mean_c : Mean air temperature T_mean [unit = deg C]
    - temp_max_c : Daily maximum air temperature T_max [unit = deg C]
    - temp_min_c : Daily minimum air temperature T_min [unit = deg C]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    et0 : FloatOrArray
        Reference evapotranspiration ET_0 [mm/day].
    temp_mean_c : FloatOrArray
        Mean air temperature T_mean [deg C].
    temp_max_c : FloatOrArray
        Daily maximum air temperature T_max [deg C].
    temp_min_c : FloatOrArray
        Daily minimum air temperature T_min [deg C].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (et, tm, tmx, tmn), is_scalar = coerce_inputs(et0, temp_mean_c, temp_max_c, temp_min_c)
    out = _core.hargreaves_ra(et, tm, tmx, tmn)
    return format_output(out, is_scalar)
hargreaves_radiation = hargreaves_ra

def faa_tc(length: FloatOrArray, slope: FloatOrArray, runoff_coeff: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes overland time of concentration Tc using the Federal Aviation Administration (FAA) equation.
    Units (Default SI): length [m], slope [m/m (decimal)], runoff_coeff [dimensionless (0.05 - 0.95)] -> returns [minutes]

    Formula:
    SI: T_c = (3.26 * (1.1 - C) * sqrt(L)) / (S^0.3333)  [L in m, S in %, Tc in min]

    Where (Default SI Units):
    - length : Reach / conduit / flow path length L [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - runoff_coeff : Rational runoff coefficient C [unit = dimensionless (0.05 - 0.95)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Time parameter [unit = minutes]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    runoff_coeff : FloatOrArray
        Rational runoff coefficient C [dimensionless (0.05 - 0.95)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Time parameter [minutes]. Returns float for scalar inputs.
    """
    (l, s, c), is_scalar = coerce_inputs(length, slope, runoff_coeff)
    k = 1.8 if system.lower() == 'us' else 3.26
    with np.errstate(all='ignore'):
        tc = np.where((l <= 0) | (s <= 0) | (c < 0) | (c > 1.1), np.nan, k * (1.1 - c) * np.sqrt(l) / s ** (1.0 / 3.0))
    return format_output(tc, is_scalar)

def faa_l(tc: FloatOrArray, slope: FloatOrArray, runoff_coeff: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Solves for flow length L from known FAA time of concentration.
    Units (Default SI): tc [minutes], slope [m/m (decimal)], runoff_coeff [dimensionless (0.05 - 0.95)] -> returns [km if 'km' in fn else 'm']

    Formula:
    faa_l(tc, slope, runoff_coeff, system)

    Where (Default SI Units):
    - tc : Time of concentration T_c [unit = minutes]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - runoff_coeff : Rational runoff coefficient C [unit = dimensionless (0.05 - 0.95)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    tc : FloatOrArray
        Time of concentration T_c [minutes].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    runoff_coeff : FloatOrArray
        Rational runoff coefficient C [dimensionless (0.05 - 0.95)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (t, s, c), is_scalar = coerce_inputs(tc, slope, runoff_coeff)
    k = 1.8 if system.lower() == 'us' else 3.26
    with np.errstate(all='ignore'):
        denom = k * (1.1 - c)
        l = np.where((t <= 0) | (s <= 0) | (denom <= 0), np.nan, (t * s ** (1.0 / 3.0) / denom) ** 2)
    return format_output(l, is_scalar)

def faa_s(tc: FloatOrArray, length: FloatOrArray, runoff_coeff: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Solves for slope S from known FAA time of concentration.
    Units (Default SI): tc [minutes], length [m], runoff_coeff [dimensionless (0.05 - 0.95)] -> returns [m/m]

    Formula:
    faa_s(tc, length, runoff_coeff, system)

    Where (Default SI Units):
    - tc : Time of concentration T_c [unit = minutes]
    - length : Reach / conduit / flow path length L [unit = m]
    - runoff_coeff : Rational runoff coefficient C [unit = dimensionless (0.05 - 0.95)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    tc : FloatOrArray
        Time of concentration T_c [minutes].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    runoff_coeff : FloatOrArray
        Rational runoff coefficient C [dimensionless (0.05 - 0.95)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (t, l, c), is_scalar = coerce_inputs(tc, length, runoff_coeff)
    k = 1.8 if system.lower() == 'us' else 3.26
    with np.errstate(all='ignore'):
        num = k * (1.1 - c) * np.sqrt(l)
        s = np.where((t <= 0) | (l <= 0) | (c < 0) | (c > 1.1), np.nan, (num / t) ** 3)
    return format_output(s, is_scalar)

def faa_c(tc: FloatOrArray, length: FloatOrArray, slope: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Solves for runoff coefficient C from known FAA time of concentration.
    Units (Default SI): tc [minutes], length [m], slope [m/m (decimal)] -> returns [dimensionless]

    Formula:
    faa_c(tc, length, slope, system)

    Where (Default SI Units):
    - tc : Time of concentration T_c [unit = minutes]
    - length : Reach / conduit / flow path length L [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Runoff / discharge coefficient [unit = dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    tc : FloatOrArray
        Time of concentration T_c [minutes].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Runoff / discharge coefficient [dimensionless]. Returns float for scalar inputs.
    """
    (t, l, s), is_scalar = coerce_inputs(tc, length, slope)
    k = 1.8 if system.lower() == 'us' else 3.26
    with np.errstate(all='ignore'):
        denom = k * np.sqrt(l)
        c = np.where((t <= 0) | (l <= 0) | (s <= 0), np.nan, 1.1 - t * s ** (1.0 / 3.0) / denom)
    return format_output(c, is_scalar)

def kerby_tc(length: FloatOrArray, slope: FloatOrArray, roughness_n: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes overland sheet flow time of concentration Tc using the Kerby-Hathaway equation.
    Units (Default SI): length [m], slope [m/m (decimal)], roughness_n [s/m^(1/3) (or Kerby retardance)] -> returns [minutes]

    Formula:
    SI: T_c = 1.439 * ((L * n) / sqrt(S))^0.467  [L in m, S in m/m, Tc in min]

    Where (Default SI Units):
    - length : Reach / conduit / flow path length L [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - roughness_n : Roughness coefficient n [unit = s/m^(1/3) (or Kerby retardance)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Time parameter [unit = minutes]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    roughness_n : FloatOrArray
        Roughness coefficient n [s/m^(1/3) (or Kerby retardance)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Time parameter [minutes]. Returns float for scalar inputs.
    """
    (l, s, n), is_scalar = coerce_inputs(length, slope, roughness_n)
    k = 0.828 if system.lower() == 'us' else 1.439
    with np.errstate(all='ignore'):
        tc = np.where((l <= 0) | (s <= 0) | (n <= 0), np.nan, k * (l * n / np.sqrt(s)) ** 0.467)
    return format_output(tc, is_scalar)

def kerby_l(tc: FloatOrArray, slope: FloatOrArray, roughness_n: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Solves for length L from known Kerby time of concentration.
    Units (Default SI): tc [minutes], slope [m/m (decimal)], roughness_n [s/m^(1/3) (or Kerby retardance)] -> returns [km if 'km' in fn else 'm']

    Formula:
    kerby_l(tc, slope, roughness_n, system)

    Where (Default SI Units):
    - tc : Time of concentration T_c [unit = minutes]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - roughness_n : Roughness coefficient n [unit = s/m^(1/3) (or Kerby retardance)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    tc : FloatOrArray
        Time of concentration T_c [minutes].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    roughness_n : FloatOrArray
        Roughness coefficient n [s/m^(1/3) (or Kerby retardance)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (t, s, n), is_scalar = coerce_inputs(tc, slope, roughness_n)
    k = 0.828 if system.lower() == 'us' else 1.439
    with np.errstate(all='ignore'):
        l = np.where((t <= 0) | (s <= 0) | (n <= 0), np.nan, np.sqrt(s) / n * (t / k) ** (1.0 / 0.467))
    return format_output(l, is_scalar)

def kerby_s(tc: FloatOrArray, length: FloatOrArray, roughness_n: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Solves for slope S from known Kerby time of concentration.
    Units (Default SI): tc [minutes], length [m], roughness_n [s/m^(1/3) (or Kerby retardance)] -> returns [m/m]

    Formula:
    kerby_s(tc, length, roughness_n, system)

    Where (Default SI Units):
    - tc : Time of concentration T_c [unit = minutes]
    - length : Reach / conduit / flow path length L [unit = m]
    - roughness_n : Roughness coefficient n [unit = s/m^(1/3) (or Kerby retardance)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    tc : FloatOrArray
        Time of concentration T_c [minutes].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    roughness_n : FloatOrArray
        Roughness coefficient n [s/m^(1/3) (or Kerby retardance)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (t, l, n), is_scalar = coerce_inputs(tc, length, roughness_n)
    k = 0.828 if system.lower() == 'us' else 1.439
    with np.errstate(all='ignore'):
        s = np.where((t <= 0) | (l <= 0) | (n <= 0), np.nan, (l * n / (t / k) ** (1.0 / 0.467)) ** 2)
    return format_output(s, is_scalar)

def kerby_n(tc: FloatOrArray, length: FloatOrArray, slope: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Solves for Kerby retardance roughness n from known time of concentration.
    Units (Default SI): tc [minutes], length [m], slope [m/m (decimal)] -> returns [s/m^(1/3) or dimensionless]

    Formula:
    kerby_n(tc, length, slope, system)

    Where (Default SI Units):
    - tc : Time of concentration T_c [unit = minutes]
    - length : Reach / conduit / flow path length L [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Roughness coefficient [unit = s/m^(1/3) or dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    tc : FloatOrArray
        Time of concentration T_c [minutes].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Roughness coefficient [s/m^(1/3) or dimensionless]. Returns float for scalar inputs.
    """
    (t, l, s), is_scalar = coerce_inputs(tc, length, slope)
    k = 0.828 if system.lower() == 'us' else 1.439
    with np.errstate(all='ignore'):
        n = np.where((t <= 0) | (l <= 0) | (s <= 0), np.nan, np.sqrt(s) / l * (t / k) ** (1.0 / 0.467))
    return format_output(n, is_scalar)

def bransby_williams_tc(length_km: FloatOrArray, area_km2: FloatOrArray, slope_m_per_km: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes time of concentration Tc using the Bransby-Williams equation (Australian / Commonwealth standard).
    Units (Default SI): length_km [km], area_km2 [km^2], slope_m_per_km [m/km] -> returns [minutes]

    Formula:
    T_c = (58.5 * L) / (A^0.1 * S^0.2)  [L in km, A in km^2, S in m/km, Tc in min]

    Where (Default SI Units):
    - length_km : Main channel path length L [unit = km]
    - area_km2 : Catchment watershed drainage area A [unit = km^2]
    - slope_m_per_km : Main channel gradient S [unit = m/km]
    - Output : Time parameter [unit = minutes]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length_km : FloatOrArray
        Main channel path length L [km].
    area_km2 : FloatOrArray
        Catchment watershed drainage area A [km^2].
    slope_m_per_km : FloatOrArray
        Main channel gradient S [m/km].

    Returns
    -------
    float | np.ndarray
        Time parameter [minutes]. Returns float for scalar inputs.
    """
    (l, a, s), is_scalar = coerce_inputs(length_km, area_km2, slope_m_per_km)
    with np.errstate(all='ignore'):
        tc = np.where((l <= 0) | (a <= 0) | (s <= 0), np.nan, 58.5 * l / (a ** 0.1 * s ** 0.2))
    return format_output(tc, is_scalar)

def bransby_williams_l(tc: FloatOrArray, area_km2: FloatOrArray, slope_m_per_km: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for channel length L from known Bransby-Williams time of concentration.
    Units (Default SI): tc [minutes], area_km2 [km^2], slope_m_per_km [m/km] -> returns [km if 'km' in fn else 'm']

    Formula:
    bransby_williams_l(tc, area_km2, slope_m_per_km)

    Where (Default SI Units):
    - tc : Time of concentration T_c [unit = minutes]
    - area_km2 : Catchment watershed drainage area A [unit = km^2]
    - slope_m_per_km : Main channel gradient S [unit = m/km]
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    tc : FloatOrArray
        Time of concentration T_c [minutes].
    area_km2 : FloatOrArray
        Catchment watershed drainage area A [km^2].
    slope_m_per_km : FloatOrArray
        Main channel gradient S [m/km].

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (t, a, s), is_scalar = coerce_inputs(tc, area_km2, slope_m_per_km)
    with np.errstate(all='ignore'):
        l = np.where((t <= 0) | (a <= 0) | (s <= 0), np.nan, t * a ** 0.1 * s ** 0.2 / 58.5)
    return format_output(l, is_scalar)

def bransby_williams_a(tc: FloatOrArray, length_km: FloatOrArray, slope_m_per_km: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for catchment area A from known Bransby-Williams time of concentration.
    Units (Default SI): tc [minutes], length_km [km], slope_m_per_km [m/km] -> returns [km^2 if 'km' in fn else 'm^2']

    Formula:
    bransby_williams_a(tc, length_km, slope_m_per_km)

    Where (Default SI Units):
    - tc : Time of concentration T_c [unit = minutes]
    - length_km : Main channel path length L [unit = km]
    - slope_m_per_km : Main channel gradient S [unit = m/km]
    - Output : Area [unit = km^2 if 'km' in fn else 'm^2']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    tc : FloatOrArray
        Time of concentration T_c [minutes].
    length_km : FloatOrArray
        Main channel path length L [km].
    slope_m_per_km : FloatOrArray
        Main channel gradient S [m/km].

    Returns
    -------
    float | np.ndarray
        Area [km^2 if 'km' in fn else 'm^2']. Returns float for scalar inputs.
    """
    (t, l, s), is_scalar = coerce_inputs(tc, length_km, slope_m_per_km)
    with np.errstate(all='ignore'):
        a = np.where((t <= 0) | (l <= 0) | (s <= 0), np.nan, (58.5 * l / (t * s ** 0.2)) ** 10.0)
    return format_output(a, is_scalar)

def bransby_williams_s(tc: FloatOrArray, length_km: FloatOrArray, area_km2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for slope S from known Bransby-Williams time of concentration.
    Units (Default SI): tc [minutes], length_km [km], area_km2 [km^2] -> returns [m/m]

    Formula:
    bransby_williams_s(tc, length_km, area_km2)

    Where (Default SI Units):
    - tc : Time of concentration T_c [unit = minutes]
    - length_km : Main channel path length L [unit = km]
    - area_km2 : Catchment watershed drainage area A [unit = km^2]
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    tc : FloatOrArray
        Time of concentration T_c [minutes].
    length_km : FloatOrArray
        Main channel path length L [km].
    area_km2 : FloatOrArray
        Catchment watershed drainage area A [km^2].

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (t, l, a), is_scalar = coerce_inputs(tc, length_km, area_km2)
    with np.errstate(all='ignore'):
        s = np.where((t <= 0) | (l <= 0) | (a <= 0), np.nan, (58.5 * l / (t * a ** 0.1)) ** 5.0)
    return format_output(s, is_scalar)

def tr55_channel_tc(length: FloatOrArray, velocity: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes channel flow travel time Tt = L / (60 * V) [Tt in min].
    Units (Default SI): length [m], velocity [m/s] -> returns [minutes]

    Formula:
    Computes channel flow travel time Tt = L / (60 * V) [Tt in min].

    Where (Default SI Units):
    - length : Reach / conduit / flow path length L [unit = m]
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - Output : Time parameter [unit = minutes]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].

    Returns
    -------
    float | np.ndarray
        Time parameter [minutes]. Returns float for scalar inputs.
    """
    (l, v), is_scalar = coerce_inputs(length, velocity)
    with np.errstate(all='ignore'):
        tt = np.where((l <= 0) | (v <= 0), np.nan, l / (60.0 * v))
    return format_output(tt, is_scalar)

def tr55_composite_tc(t_sheet: FloatOrArray, t_shallow: FloatOrArray, t_channel: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes total catchment time of concentration Tc = T_sheet + T_shallow + T_channel [min].
    Units (Default SI): t_sheet [minutes], t_shallow [minutes], t_channel [minutes] -> returns [minutes]

    Formula:
    Computes total catchment time of concentration Tc = T_sheet + T_shallow + T_channel [min].

    Where (Default SI Units):
    - t_sheet : Sheet flow travel time [unit = minutes]
    - t_shallow : Shallow concentrated flow travel time [unit = minutes]
    - t_channel : Open channel reach travel time [unit = minutes]
    - Output : Time parameter [unit = minutes]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    t_sheet : FloatOrArray
        Sheet flow travel time [minutes].
    t_shallow : FloatOrArray
        Shallow concentrated flow travel time [minutes].
    t_channel : FloatOrArray
        Open channel reach travel time [minutes].

    Returns
    -------
    float | np.ndarray
        Time parameter [minutes]. Returns float for scalar inputs.
    """
    (t1, t2, t3), is_scalar = coerce_inputs(t_sheet, t_shallow, t_channel)
    out = t1 + t2 + t3
    return format_output(out, is_scalar)

def dickens_q(area_km2: FloatOrArray, c_d: FloatOrArray=14.0) -> Union[float, np.ndarray]:
    """
    Computes maximum flood peak discharge Q using Dicken's formula.
    Units (Default SI): area_km2 [km^2], c_d [dimensionless (11.4 - 28.0)] -> returns [m^3/s]

    Formula:
    Q = C_D * A^(3/4)  [A in km^2, Q in m^3/s]

    Where (Default SI Units):
    - area_km2 : Catchment watershed drainage area A [unit = km^2]
    - c_d : Dicken's flood coefficient C_D [unit = dimensionless (11.4 - 28.0)]
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    area_km2 : FloatOrArray
        Catchment watershed drainage area A [km^2].
    c_d : FloatOrArray
        Dicken's flood coefficient C_D [dimensionless (11.4 - 28.0)].

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (a, cd), is_scalar = coerce_inputs(area_km2, c_d)
    with np.errstate(all='ignore'):
        q = np.where((a <= 0) | (cd <= 0), np.nan, cd * a ** 0.75)
    return format_output(q, is_scalar)

def dickens_cd(discharge: FloatOrArray, area_km2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for Dicken's coefficient C_D = Q / A^(3/4).
    Units (Default SI): discharge [m^3/s], area_km2 [km^2] -> returns [dimensionless]

    Formula:
    Inversion: Solves for Dicken's coefficient C_D = Q / A^(3/4).

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - area_km2 : Catchment watershed drainage area A [unit = km^2]
    - Output : Runoff / discharge coefficient [unit = dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    area_km2 : FloatOrArray
        Catchment watershed drainage area A [km^2].

    Returns
    -------
    float | np.ndarray
        Runoff / discharge coefficient [dimensionless]. Returns float for scalar inputs.
    """
    (q, a), is_scalar = coerce_inputs(discharge, area_km2)
    with np.errstate(all='ignore'):
        cd = np.where((q <= 0) | (a <= 0), np.nan, q / a ** 0.75)
    return format_output(cd, is_scalar)

def dickens_area(discharge: FloatOrArray, c_d: FloatOrArray=14.0) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for drainage area A = (Q / C_D)^(4/3).
    Units (Default SI): discharge [m^3/s], c_d [dimensionless (11.4 - 28.0)] -> returns [km^2 if 'km' in fn else 'm^2']

    Formula:
    Inversion: Solves for drainage area A = (Q / C_D)^(4/3).

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - c_d : Dicken's flood coefficient C_D [unit = dimensionless (11.4 - 28.0)]
    - Output : Area [unit = km^2 if 'km' in fn else 'm^2']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    c_d : FloatOrArray
        Dicken's flood coefficient C_D [dimensionless (11.4 - 28.0)].

    Returns
    -------
    float | np.ndarray
        Area [km^2 if 'km' in fn else 'm^2']. Returns float for scalar inputs.
    """
    (q, cd), is_scalar = coerce_inputs(discharge, c_d)
    with np.errstate(all='ignore'):
        a = np.where((q <= 0) | (cd <= 0), np.nan, (q / cd) ** (4.0 / 3.0))
    return format_output(a, is_scalar)

def ryves_q(area_km2: FloatOrArray, c_r: FloatOrArray=8.5) -> Union[float, np.ndarray]:
    """
    Computes maximum flood peak discharge Q using Ryves' formula (South India / flat plateau standard).
    Units (Default SI): area_km2 [km^2], c_r [dimensionless (6.8 - 10.2)] -> returns [m^3/s]

    Formula:
    Q = C_R * A^(2/3)  [A in km^2, Q in m^3/s]

    Where (Default SI Units):
    - area_km2 : Catchment watershed drainage area A [unit = km^2]
    - c_r : Ryves' flood coefficient C_R [unit = dimensionless (6.8 - 10.2)]
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    area_km2 : FloatOrArray
        Catchment watershed drainage area A [km^2].
    c_r : FloatOrArray
        Ryves' flood coefficient C_R [dimensionless (6.8 - 10.2)].

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (a, cr), is_scalar = coerce_inputs(area_km2, c_r)
    with np.errstate(all='ignore'):
        q = np.where((a <= 0) | (cr <= 0), np.nan, cr * a ** (2.0 / 3.0))
    return format_output(q, is_scalar)

def ryves_cr(discharge: FloatOrArray, area_km2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for Ryves' coefficient C_R = Q / A^(2/3).
    Units (Default SI): discharge [m^3/s], area_km2 [km^2] -> returns [dimensionless]

    Formula:
    Inversion: Solves for Ryves' coefficient C_R = Q / A^(2/3).

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - area_km2 : Catchment watershed drainage area A [unit = km^2]
    - Output : Runoff / discharge coefficient [unit = dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    area_km2 : FloatOrArray
        Catchment watershed drainage area A [km^2].

    Returns
    -------
    float | np.ndarray
        Runoff / discharge coefficient [dimensionless]. Returns float for scalar inputs.
    """
    (q, a), is_scalar = coerce_inputs(discharge, area_km2)
    with np.errstate(all='ignore'):
        cr = np.where((q <= 0) | (a <= 0), np.nan, q / a ** (2.0 / 3.0))
    return format_output(cr, is_scalar)

def ryves_area(discharge: FloatOrArray, c_r: FloatOrArray=8.5) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for drainage area A = (Q / C_R)^(3/2).
    Units (Default SI): discharge [m^3/s], c_r [dimensionless (6.8 - 10.2)] -> returns [km^2 if 'km' in fn else 'm^2']

    Formula:
    Inversion: Solves for drainage area A = (Q / C_R)^(3/2).

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - c_r : Ryves' flood coefficient C_R [unit = dimensionless (6.8 - 10.2)]
    - Output : Area [unit = km^2 if 'km' in fn else 'm^2']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    c_r : FloatOrArray
        Ryves' flood coefficient C_R [dimensionless (6.8 - 10.2)].

    Returns
    -------
    float | np.ndarray
        Area [km^2 if 'km' in fn else 'm^2']. Returns float for scalar inputs.
    """
    (q, cr), is_scalar = coerce_inputs(discharge, c_r)
    with np.errstate(all='ignore'):
        a = np.where((q <= 0) | (cr <= 0), np.nan, (q / cr) ** 1.5)
    return format_output(a, is_scalar)

def inglis_q(area_km2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes maximum flood discharge Q using Inglis' formula for fan-shaped catchments.
    Units (Default SI): area_km2 [km^2] -> returns [m^3/s]

    Formula:
    Q = (124 * A) / sqrt(A + 10.4)  [A in km^2, Q in m^3/s]

    Where (Default SI Units):
    - area_km2 : Catchment watershed drainage area A [unit = km^2]
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    area_km2 : FloatOrArray
        Catchment watershed drainage area A [km^2].

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (a,), is_scalar = coerce_inputs(area_km2)
    with np.errstate(all='ignore'):
        q = np.where(a <= 0, np.nan, 124.0 * a / np.sqrt(a + 10.4))
    return format_output(q, is_scalar)

def inglis_area(discharge: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for catchment area A algebraically from known Inglis discharge.
    Units (Default SI): discharge [m^3/s] -> returns [km^2 if 'km' in fn else 'm^2']

    Formula:
    inglis_area(discharge)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - Output : Area [unit = km^2 if 'km' in fn else 'm^2']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].

    Returns
    -------
    float | np.ndarray
        Area [km^2 if 'km' in fn else 'm^2']. Returns float for scalar inputs.
    """
    (q,), is_scalar = coerce_inputs(discharge)
    with np.errstate(all='ignore'):
        disc = q ** 4 + 4.0 * 15376.0 * 10.4 * q ** 2
        a = np.where(q <= 0, np.nan, (q ** 2 + np.sqrt(disc)) / (2.0 * 15376.0))
    return format_output(a, is_scalar)

def nawab_jung_q(area_km2: FloatOrArray, c_n: FloatOrArray=48.0) -> Union[float, np.ndarray]:
    """
    Computes maximum flood discharge Q using Nawab Jung Bahadur formula (Deccan plateau).
    Units (Default SI): area_km2 [km^2], c_n [dimensionless (48.0 - 60.0)] -> returns [m^3/s]

    Formula:
    Q = C_N * A^(5/6)  [A in km^2, Q in m^3/s]

    Where (Default SI Units):
    - area_km2 : Catchment watershed drainage area A [unit = km^2]
    - c_n : Nawab Jung coefficient C_N [unit = dimensionless (48.0 - 60.0)]
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    area_km2 : FloatOrArray
        Catchment watershed drainage area A [km^2].
    c_n : FloatOrArray
        Nawab Jung coefficient C_N [dimensionless (48.0 - 60.0)].

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (a, cn), is_scalar = coerce_inputs(area_km2, c_n)
    with np.errstate(all='ignore'):
        q = np.where((a <= 0) | (cn <= 0), np.nan, cn * a ** (5.0 / 6.0))
    return format_output(q, is_scalar)

def nawab_jung_cn(discharge: FloatOrArray, area_km2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for Nawab Jung coefficient C_N = Q / A^(5/6).
    Units (Default SI): discharge [m^3/s], area_km2 [km^2] -> returns [dimensionless]

    Formula:
    Inversion: Solves for Nawab Jung coefficient C_N = Q / A^(5/6).

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - area_km2 : Catchment watershed drainage area A [unit = km^2]
    - Output : Runoff / discharge coefficient [unit = dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    area_km2 : FloatOrArray
        Catchment watershed drainage area A [km^2].

    Returns
    -------
    float | np.ndarray
        Runoff / discharge coefficient [dimensionless]. Returns float for scalar inputs.
    """
    (q, a), is_scalar = coerce_inputs(discharge, area_km2)
    with np.errstate(all='ignore'):
        cn = np.where((q <= 0) | (a <= 0), np.nan, q / a ** (5.0 / 6.0))
    return format_output(cn, is_scalar)

def nawab_jung_area(discharge: FloatOrArray, c_n: FloatOrArray=48.0) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for drainage area A = (Q / C_N)^(6/5).
    Units (Default SI): discharge [m^3/s], c_n [dimensionless (48.0 - 60.0)] -> returns [km^2 if 'km' in fn else 'm^2']

    Formula:
    Inversion: Solves for drainage area A = (Q / C_N)^(6/5).

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - c_n : Nawab Jung coefficient C_N [unit = dimensionless (48.0 - 60.0)]
    - Output : Area [unit = km^2 if 'km' in fn else 'm^2']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    c_n : FloatOrArray
        Nawab Jung coefficient C_N [dimensionless (48.0 - 60.0)].

    Returns
    -------
    float | np.ndarray
        Area [km^2 if 'km' in fn else 'm^2']. Returns float for scalar inputs.
    """
    (q, cn), is_scalar = coerce_inputs(discharge, c_n)
    with np.errstate(all='ignore'):
        a = np.where((q <= 0) | (cn <= 0), np.nan, (q / cn) ** 1.2)
    return format_output(a, is_scalar)

def fuller_flood_q(area_sq_mi: FloatOrArray, return_period: FloatOrArray, c_f: FloatOrArray=1.5) -> Union[float, np.ndarray]:
    """
    Computes design flood peak discharge using Fuller's empirical frequency relationship.
    Units (Default SI): area_sq_mi [sq. mi], return_period [years], c_f [dimensionless] -> returns [m^3/s]

    Formula:
    Q_T = C_F * A^0.8 * (1 + 0.8 * log10(T))  [A in sq. mi, T in years, Q in cfs]

    Where (Default SI Units):
    - area_sq_mi : Catchment drainage area A [unit = sq. mi]
    - return_period : Design recurrence interval / return period T [unit = years]
    - c_f : Fuller's flood coefficient C_F [unit = dimensionless]
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    area_sq_mi : FloatOrArray
        Catchment drainage area A [sq. mi].
    return_period : FloatOrArray
        Design recurrence interval / return period T [years].
    c_f : FloatOrArray
        Fuller's flood coefficient C_F [dimensionless].

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (a, t, cf), is_scalar = coerce_inputs(area_sq_mi, return_period, c_f)
    with np.errstate(all='ignore'):
        q = np.where((a <= 0) | (t < 1.0) | (cf <= 0), np.nan, cf * a ** 0.8 * (1.0 + 0.8 * np.log10(t)))
    return format_output(q, is_scalar)

def fuller_return_period(discharge: FloatOrArray, area_sq_mi: FloatOrArray, c_f: FloatOrArray=1.5) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for return period T from known Fuller flood discharge.
    Units (Default SI): discharge [m^3/s], area_sq_mi [sq. mi], c_f [dimensionless] -> returns [standard SI units]

    Formula:
    fuller_return_period(discharge, area_sq_mi, c_f)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - area_sq_mi : Catchment drainage area A [unit = sq. mi]
    - c_f : Fuller's flood coefficient C_F [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    area_sq_mi : FloatOrArray
        Catchment drainage area A [sq. mi].
    c_f : FloatOrArray
        Fuller's flood coefficient C_F [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, a, cf), is_scalar = coerce_inputs(discharge, area_sq_mi, c_f)
    with np.errstate(all='ignore'):
        term = (q / (cf * a ** 0.8) - 1.0) / 0.8
        t = np.where((q <= 0) | (a <= 0) | (cf <= 0), np.nan, 10.0 ** term)
    return format_output(t, is_scalar)

def philip_rate(time: FloatOrArray, sorptivity: FloatOrArray, transmissivity_a: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes infiltration capacity fp(t) using Philip's Two-Term infiltration model (Philip, 1957).
    Units (Default SI): time [hours], sorptivity [mm / hr^0.5], transmissivity_a [mm/hr] -> returns [standard SI units]

    Formula:
    f_p(t) = 0.5 * S * t^(-1/2) + A  [S in mm/hr^0.5, A in mm/hr, t in hr]

    Where (Default SI Units):
    - time : Elapsed infiltration or pumping time t [unit = hours]
    - sorptivity : Philip's soil sorptivity parameter S [unit = mm / hr^0.5]
    - transmissivity_a : Philip's transmissivity factor A [unit = mm/hr]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    time : FloatOrArray
        Elapsed infiltration or pumping time t [hours].
    sorptivity : FloatOrArray
        Philip's soil sorptivity parameter S [mm / hr^0.5].
    transmissivity_a : FloatOrArray
        Philip's transmissivity factor A [mm/hr].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t, s, a), is_scalar = coerce_inputs(time, sorptivity, transmissivity_a)
    with np.errstate(all='ignore'):
        fp = np.where((t <= 0) | (s < 0) | (a < 0), np.nan, 0.5 * s / np.sqrt(t) + a)
    return format_output(fp, is_scalar)

def philip_cumulative(time: FloatOrArray, sorptivity: FloatOrArray, transmissivity_a: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes cumulative infiltration depth F(t) using Philip's Two-Term equation.
    Units (Default SI): time [hours], sorptivity [mm / hr^0.5], transmissivity_a [mm/hr] -> returns [standard SI units]

    Formula:
    F(t) = S * t^(1/2) + A * t  [F in mm, t in hr]

    Where (Default SI Units):
    - time : Elapsed infiltration or pumping time t [unit = hours]
    - sorptivity : Philip's soil sorptivity parameter S [unit = mm / hr^0.5]
    - transmissivity_a : Philip's transmissivity factor A [unit = mm/hr]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    time : FloatOrArray
        Elapsed infiltration or pumping time t [hours].
    sorptivity : FloatOrArray
        Philip's soil sorptivity parameter S [mm / hr^0.5].
    transmissivity_a : FloatOrArray
        Philip's transmissivity factor A [mm/hr].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t, s, a), is_scalar = coerce_inputs(time, sorptivity, transmissivity_a)
    with np.errstate(all='ignore'):
        f = np.where((t < 0) | (s < 0) | (a < 0), np.nan, s * np.sqrt(t) + a * t)
    return format_output(f, is_scalar)

def philip_sorptivity(cumulative_f: FloatOrArray, time: FloatOrArray, transmissivity_a: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for soil sorptivity S = (F - A * t) / sqrt(t).
    Units (Default SI): cumulative_f [mm], time [hours], transmissivity_a [mm/hr] -> returns [standard SI units]

    Formula:
    Inversion: Solves for soil sorptivity S = (F - A * t) / sqrt(t).

    Where (Default SI Units):
    - cumulative_f : Cumulative infiltrated water volume F [unit = mm]
    - time : Elapsed infiltration or pumping time t [unit = hours]
    - transmissivity_a : Philip's transmissivity factor A [unit = mm/hr]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    cumulative_f : FloatOrArray
        Cumulative infiltrated water volume F [mm].
    time : FloatOrArray
        Elapsed infiltration or pumping time t [hours].
    transmissivity_a : FloatOrArray
        Philip's transmissivity factor A [mm/hr].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (f, t, a), is_scalar = coerce_inputs(cumulative_f, time, transmissivity_a)
    with np.errstate(all='ignore'):
        s = np.where((t <= 0) | (f < 0), np.nan, (f - a * t) / np.sqrt(t))
    return format_output(s, is_scalar)

def kostiakov_rate(time: FloatOrArray, a_coeff: FloatOrArray, b_exponent: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes infiltration capacity rate using Kostiakov's empirical equation (Kostiakov, 1932).
    Units (Default SI): time [hours], a_coeff [dimensionless or mm/hr^b], b_exponent [dimensionless (0 < b < 1)] -> returns [standard SI units]

    Formula:
    f_p(t) = a * b * t^(b - 1)  [0 < b < 1, t in hr]

    Where (Default SI Units):
    - time : Elapsed infiltration or pumping time t [unit = hours]
    - a_coeff : Kostiakov empirical infiltration coefficient a [unit = dimensionless or mm/hr^b]
    - b_exponent : Kostiakov infiltration exponent b [unit = dimensionless (0 < b < 1)]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    time : FloatOrArray
        Elapsed infiltration or pumping time t [hours].
    a_coeff : FloatOrArray
        Kostiakov empirical infiltration coefficient a [dimensionless or mm/hr^b].
    b_exponent : FloatOrArray
        Kostiakov infiltration exponent b [dimensionless (0 < b < 1)].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t, a, b), is_scalar = coerce_inputs(time, a_coeff, b_exponent)
    with np.errstate(all='ignore'):
        fp = np.where((t <= 0) | (a <= 0) | (b <= 0) | (b >= 1.0), np.nan, a * b * t ** (b - 1.0))
    return format_output(fp, is_scalar)

def kostiakov_cumulative(time: FloatOrArray, a_coeff: FloatOrArray, b_exponent: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes cumulative infiltration depth using Kostiakov's power equation.
    Units (Default SI): time [hours], a_coeff [dimensionless or mm/hr^b], b_exponent [dimensionless (0 < b < 1)] -> returns [standard SI units]

    Formula:
    F(t) = a * t^b  [F in mm or cm, t in hr]

    Where (Default SI Units):
    - time : Elapsed infiltration or pumping time t [unit = hours]
    - a_coeff : Kostiakov empirical infiltration coefficient a [unit = dimensionless or mm/hr^b]
    - b_exponent : Kostiakov infiltration exponent b [unit = dimensionless (0 < b < 1)]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    time : FloatOrArray
        Elapsed infiltration or pumping time t [hours].
    a_coeff : FloatOrArray
        Kostiakov empirical infiltration coefficient a [dimensionless or mm/hr^b].
    b_exponent : FloatOrArray
        Kostiakov infiltration exponent b [dimensionless (0 < b < 1)].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t, a, b), is_scalar = coerce_inputs(time, a_coeff, b_exponent)
    with np.errstate(all='ignore'):
        f = np.where((t < 0) | (a <= 0) | (b <= 0) | (b >= 1.0), np.nan, a * t ** b)
    return format_output(f, is_scalar)

def kostiakov_time(cumulative_f: FloatOrArray, a_coeff: FloatOrArray, b_exponent: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for elapsed time t = (F / a)^(1 / b).
    Units (Default SI): cumulative_f [mm], a_coeff [dimensionless or mm/hr^b], b_exponent [dimensionless (0 < b < 1)] -> returns [standard SI units]

    Formula:
    Inversion: Solves for elapsed time t = (F / a)^(1 / b).

    Where (Default SI Units):
    - cumulative_f : Cumulative infiltrated water volume F [unit = mm]
    - a_coeff : Kostiakov empirical infiltration coefficient a [unit = dimensionless or mm/hr^b]
    - b_exponent : Kostiakov infiltration exponent b [unit = dimensionless (0 < b < 1)]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    cumulative_f : FloatOrArray
        Cumulative infiltrated water volume F [mm].
    a_coeff : FloatOrArray
        Kostiakov empirical infiltration coefficient a [dimensionless or mm/hr^b].
    b_exponent : FloatOrArray
        Kostiakov infiltration exponent b [dimensionless (0 < b < 1)].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (f, a, b), is_scalar = coerce_inputs(cumulative_f, a_coeff, b_exponent)
    with np.errstate(all='ignore'):
        t = np.where((f <= 0) | (a <= 0) | (b <= 0), np.nan, (f / a) ** (1.0 / b))
    return format_output(t, is_scalar)

def green_ampt_ponding_time(intensity: FloatOrArray, conductivity_k: FloatOrArray, suction_psi: FloatOrArray, moisture_deficit: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes time to surface ponding tp under constant rainfall intensity using Green-Ampt theory.
    Units (Default SI): intensity [mm/hr], conductivity_k [mm/hr], suction_psi [mm], moisture_deficit [dimensionless fraction] -> returns [standard SI units]

    Formula:
    t_p = (K * psi * Delta_theta) / (i * (i - K))  [Valid for i > K]

    Where (Default SI Units):
    - intensity : Design rainfall intensity I [unit = mm/hr]
    - conductivity_k : Saturated hydraulic conductivity K [unit = mm/hr]
    - suction_psi : Wetting front soil suction head psi [unit = mm]
    - moisture_deficit : Initial available soil moisture deficit Delta_theta [unit = dimensionless fraction]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    intensity : FloatOrArray
        Design rainfall intensity I [mm/hr].
    conductivity_k : FloatOrArray
        Saturated hydraulic conductivity K [mm/hr].
    suction_psi : FloatOrArray
        Wetting front soil suction head psi [mm].
    moisture_deficit : FloatOrArray
        Initial available soil moisture deficit Delta_theta [dimensionless fraction].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (i, k, psi, dtheta), is_scalar = coerce_inputs(intensity, conductivity_k, suction_psi, moisture_deficit)
    with np.errstate(all='ignore'):
        tp = np.where((i <= k) | (k <= 0) | (psi <= 0) | (dtheta <= 0), np.nan, k * psi * dtheta / (i * (i - k)))
    return format_output(tp, is_scalar)

def saturation_vapor_pressure(temp_c: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes saturation vapor pressure e_s(T) using the standard FAO-56 Tetens equation.
    Units (Default SI): temp_c [deg C] -> returns [standard SI units]

    Formula:
    e_s = 0.6108 * exp((17.27 * T) / (T + 237.3))  [e_s in kPa, T in deg C]

    Where (Default SI Units):
    - temp_c : Mean daily air temperature at 2 m height T [unit = deg C]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    temp_c : FloatOrArray
        Mean daily air temperature at 2 m height T [deg C].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t,), is_scalar = coerce_inputs(temp_c)
    with np.errstate(all='ignore'):
        es = 0.6108 * np.exp(17.27 * t / (t + 237.3))
    return format_output(es, is_scalar)

def vapor_pressure_slope(temp_c: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes the slope of the saturation vapor pressure curve Delta = d(e_s)/dT [kPa / deg C].
    Units (Default SI): temp_c [deg C] -> returns [m/m]

    Formula:
    Computes the slope of the saturation vapor pressure curve Delta = d(e_s)/dT [kPa / deg C].

    Where (Default SI Units):
    - temp_c : Mean daily air temperature at 2 m height T [unit = deg C]
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    temp_c : FloatOrArray
        Mean daily air temperature at 2 m height T [deg C].

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (t,), is_scalar = coerce_inputs(temp_c)
    es = 0.6108 * np.exp(17.27 * t / (t + 237.3))
    with np.errstate(all='ignore'):
        delta = 4098.0 * es / (t + 237.3) ** 2
    return format_output(delta, is_scalar)

def fao56_penman_monteith(net_radiation: FloatOrArray, temp_c: FloatOrArray, wind_speed_2m: FloatOrArray, es: FloatOrArray, ea: FloatOrArray, delta_slope: FloatOrArray, psychrometric_gamma: FloatOrArray, soil_heat_flux: FloatOrArray=0.0) -> Union[float, np.ndarray]:
    """
    Computes daily reference evapotranspiration ET_0 using the international FAO-56 Penman-Monteith equation.
    Units (Default SI): net_radiation [MJ / m^2 / day], temp_c [deg C], wind_speed_2m [m/s], es [kPa], ea [kPa], delta_slope [kPa / deg C], psychrometric_gamma [kPa / deg C], soil_heat_flux [MJ / m^2 / day] -> returns [standard SI units]

    Formula:
    ET_0 = [0.408 * Delta * (R_n - G) + gamma * (900 / (T + 273)) * u_2 * (e_s - e_a)] / [Delta + gamma * (1 + 0.34 * u_2)]

    Where (Default SI Units):
    - net_radiation : Net radiation at the crop surface R_n [unit = MJ / m^2 / day]
    - temp_c : Mean daily air temperature at 2 m height T [unit = deg C]
    - wind_speed_2m : Mean daily wind speed at 2 m height u_2 [unit = m/s]
    - es : Mean saturation vapor pressure e_s [unit = kPa]
    - ea : Actual atmospheric vapor pressure e_a [unit = kPa]
    - delta_slope : Slope of saturation vapor pressure curve Delta [unit = kPa / deg C]
    - psychrometric_gamma : Psychrometric constant gamma [unit = kPa / deg C]
    - soil_heat_flux : Soil heat flux density G [unit = MJ / m^2 / day]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    net_radiation : FloatOrArray
        Net radiation at the crop surface R_n [MJ / m^2 / day].
    temp_c : FloatOrArray
        Mean daily air temperature at 2 m height T [deg C].
    wind_speed_2m : FloatOrArray
        Mean daily wind speed at 2 m height u_2 [m/s].
    es : FloatOrArray
        Mean saturation vapor pressure e_s [kPa].
    ea : FloatOrArray
        Actual atmospheric vapor pressure e_a [kPa].
    delta_slope : FloatOrArray
        Slope of saturation vapor pressure curve Delta [kPa / deg C].
    psychrometric_gamma : FloatOrArray
        Psychrometric constant gamma [kPa / deg C].
    soil_heat_flux : FloatOrArray
        Soil heat flux density G [MJ / m^2 / day].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (rn, t, u2, es_v, ea_v, delta, gamma, g), is_scalar = coerce_inputs(net_radiation, temp_c, wind_speed_2m, es, ea, delta_slope, psychrometric_gamma, soil_heat_flux)
    with np.errstate(all='ignore'):
        num = 0.408 * delta * (rn - g) + gamma * (900.0 / (t + 273.0)) * u2 * (es_v - ea_v)
        denom = delta + gamma * (1.0 + 0.34 * u2)
        et0 = np.where(denom <= 0, np.nan, num / denom)
    return format_output(et0, is_scalar)

def fao56_net_radiation(et0: FloatOrArray, temp_c: FloatOrArray, wind_speed_2m: FloatOrArray, es: FloatOrArray, ea: FloatOrArray, delta_slope: FloatOrArray, psychrometric_gamma: FloatOrArray, soil_heat_flux: FloatOrArray=0.0) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for required net radiation R_n from known FAO-56 ET_0.
    Units (Default SI): et0 [mm/day], temp_c [deg C], wind_speed_2m [m/s], es [kPa], ea [kPa], delta_slope [kPa / deg C], psychrometric_gamma [kPa / deg C], soil_heat_flux [MJ / m^2 / day] -> returns [standard SI units]

    Formula:
    fao56_net_radiation(et0, temp_c, wind_speed_2m, es, ea, delta_slope, psychrometric_gamma, soil_heat_flux)

    Where (Default SI Units):
    - et0 : Reference evapotranspiration ET_0 [unit = mm/day]
    - temp_c : Mean daily air temperature at 2 m height T [unit = deg C]
    - wind_speed_2m : Mean daily wind speed at 2 m height u_2 [unit = m/s]
    - es : Mean saturation vapor pressure e_s [unit = kPa]
    - ea : Actual atmospheric vapor pressure e_a [unit = kPa]
    - delta_slope : Slope of saturation vapor pressure curve Delta [unit = kPa / deg C]
    - psychrometric_gamma : Psychrometric constant gamma [unit = kPa / deg C]
    - soil_heat_flux : Soil heat flux density G [unit = MJ / m^2 / day]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    et0 : FloatOrArray
        Reference evapotranspiration ET_0 [mm/day].
    temp_c : FloatOrArray
        Mean daily air temperature at 2 m height T [deg C].
    wind_speed_2m : FloatOrArray
        Mean daily wind speed at 2 m height u_2 [m/s].
    es : FloatOrArray
        Mean saturation vapor pressure e_s [kPa].
    ea : FloatOrArray
        Actual atmospheric vapor pressure e_a [kPa].
    delta_slope : FloatOrArray
        Slope of saturation vapor pressure curve Delta [kPa / deg C].
    psychrometric_gamma : FloatOrArray
        Psychrometric constant gamma [kPa / deg C].
    soil_heat_flux : FloatOrArray
        Soil heat flux density G [MJ / m^2 / day].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (et, t, u2, es_v, ea_v, delta, gamma, g), is_scalar = coerce_inputs(et0, temp_c, wind_speed_2m, es, ea, delta_slope, psychrometric_gamma, soil_heat_flux)
    with np.errstate(all='ignore'):
        denom_et = delta + gamma * (1.0 + 0.34 * u2)
        aero_term = gamma * (900.0 / (t + 273.0)) * u2 * (es_v - ea_v)
        rn = g + (et * denom_et - aero_term) / (0.408 * delta)
    return format_output(rn, is_scalar)

def priestley_taylor_et(net_radiation: FloatOrArray, temp_c: FloatOrArray, delta_slope: FloatOrArray, psychrometric_gamma: FloatOrArray, alpha: FloatOrArray=1.26, soil_heat_flux: FloatOrArray=0.0) -> Union[float, np.ndarray]:
    """
    Computes radiation-driven potential evapotranspiration using the Priestley-Taylor equation (1972).
    Units (Default SI): net_radiation [MJ / m^2 / day], temp_c [deg C], delta_slope [kPa / deg C], psychrometric_gamma [kPa / deg C], alpha [dimensionless (~1.26)], soil_heat_flux [MJ / m^2 / day] -> returns [standard SI units]

    Formula:
    ET = alpha * [Delta / (Delta + gamma)] * [(R_n - G) / lambda]  [lambda = 2.45 MJ/kg]

    Where (Default SI Units):
    - net_radiation : Net radiation at the crop surface R_n [unit = MJ / m^2 / day]
    - temp_c : Mean daily air temperature at 2 m height T [unit = deg C]
    - delta_slope : Slope of saturation vapor pressure curve Delta [unit = kPa / deg C]
    - psychrometric_gamma : Psychrometric constant gamma [unit = kPa / deg C]
    - alpha : Priestley-Taylor radiation coefficient alpha [unit = dimensionless (~1.26)]
    - soil_heat_flux : Soil heat flux density G [unit = MJ / m^2 / day]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    net_radiation : FloatOrArray
        Net radiation at the crop surface R_n [MJ / m^2 / day].
    temp_c : FloatOrArray
        Mean daily air temperature at 2 m height T [deg C].
    delta_slope : FloatOrArray
        Slope of saturation vapor pressure curve Delta [kPa / deg C].
    psychrometric_gamma : FloatOrArray
        Psychrometric constant gamma [kPa / deg C].
    alpha : FloatOrArray
        Priestley-Taylor radiation coefficient alpha [dimensionless (~1.26)].
    soil_heat_flux : FloatOrArray
        Soil heat flux density G [MJ / m^2 / day].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (rn, t, delta, gamma, alf, g), is_scalar = coerce_inputs(net_radiation, temp_c, delta_slope, psychrometric_gamma, alpha, soil_heat_flux)
    with np.errstate(all='ignore'):
        et = alf * (delta / (delta + gamma)) * ((rn - g) / 2.45)
    return format_output(et, is_scalar)

def blaney_criddle_et(temp_c: FloatOrArray, sunshine_p_percent: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes monthly reference evapotranspiration ET_0 using the FAO Blaney-Criddle formula.
    Units (Default SI): temp_c [deg C], sunshine_p_percent [dimensionless %] -> returns [standard SI units]

    Formula:
    ET_0 = p * (0.46 * T_mean + 8.13)  [ET_0 in mm/day, p is % of annual daytime hours]

    Where (Default SI Units):
    - temp_c : Mean daily air temperature at 2 m height T [unit = deg C]
    - sunshine_p_percent : Percentage of annual daytime hours p [unit = dimensionless %]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    temp_c : FloatOrArray
        Mean daily air temperature at 2 m height T [deg C].
    sunshine_p_percent : FloatOrArray
        Percentage of annual daytime hours p [dimensionless %].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t, p), is_scalar = coerce_inputs(temp_c, sunshine_p_percent)
    with np.errstate(all='ignore'):
        et = p * (0.46 * t + 8.13)
    return format_output(et, is_scalar)

def blaney_criddle_temp(et0: FloatOrArray, sunshine_p_percent: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for mean temperature T = (ET_0 / p - 8.13) / 0.46.
    Units (Default SI): et0 [mm/day], sunshine_p_percent [dimensionless %] -> returns [standard SI units]

    Formula:
    Inversion: Solves for mean temperature T = (ET_0 / p - 8.13) / 0.46.

    Where (Default SI Units):
    - et0 : Reference evapotranspiration ET_0 [unit = mm/day]
    - sunshine_p_percent : Percentage of annual daytime hours p [unit = dimensionless %]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    et0 : FloatOrArray
        Reference evapotranspiration ET_0 [mm/day].
    sunshine_p_percent : FloatOrArray
        Percentage of annual daytime hours p [dimensionless %].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (et, p), is_scalar = coerce_inputs(et0, sunshine_p_percent)
    with np.errstate(all='ignore'):
        t = np.where(p <= 0, np.nan, (et / p - 8.13) / 0.46)
    return format_output(t, is_scalar)

def scs_unit_hydrograph_peak(drainage_area: FloatOrArray, time_to_peak: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes peak discharge qp of the SCS / NRCS Dimensionless Unit Hydrograph.
    Units (Default SI): drainage_area [km^2 (or ha for Rational)], time_to_peak [hours] -> returns [m^3/s]

    Formula:
    SI: q_p = (0.208 * A) / T_p  [A in km^2, T_p in hr, q_p in m^3/s]

    Where (Default SI Units):
    - drainage_area : Catchment drainage area A [unit = km^2 (or ha for Rational)]
    - time_to_peak : Time to hydrograph peak T_p [unit = hours]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    drainage_area : FloatOrArray
        Catchment drainage area A [km^2 (or ha for Rational)].
    time_to_peak : FloatOrArray
        Time to hydrograph peak T_p [hours].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (a, tp), is_scalar = coerce_inputs(drainage_area, time_to_peak)
    k = 484.0 if system.lower() == 'us' else 0.208
    with np.errstate(all='ignore'):
        qp = np.where((a <= 0) | (tp <= 0), np.nan, k * a / tp)
    return format_output(qp, is_scalar)

def scs_uh_tp(discharge_peak: FloatOrArray, drainage_area: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Solves for time to peak T_p = (k * A) / q_p.
    Units (Default SI): discharge_peak [m^3/s], drainage_area [km^2 (or ha for Rational)] -> returns [standard SI units]

    Formula:
    Inversion: Solves for time to peak T_p = (k * A) / q_p.

    Where (Default SI Units):
    - discharge_peak : Hydrograph peak discharge Q_p [unit = m^3/s]
    - drainage_area : Catchment drainage area A [unit = km^2 (or ha for Rational)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge_peak : FloatOrArray
        Hydrograph peak discharge Q_p [m^3/s].
    drainage_area : FloatOrArray
        Catchment drainage area A [km^2 (or ha for Rational)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (qp, a), is_scalar = coerce_inputs(discharge_peak, drainage_area)
    k = 484.0 if system.lower() == 'us' else 0.208
    with np.errstate(all='ignore'):
        tp = np.where((qp <= 0) | (a <= 0), np.nan, k * a / qp)
    return format_output(tp, is_scalar)

def scs_uh_area(discharge_peak: FloatOrArray, time_to_peak: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Solves for drainage area A = (q_p * T_p) / k.
    Units (Default SI): discharge_peak [m^3/s], time_to_peak [hours] -> returns [km^2 if 'km' in fn else 'm^2']

    Formula:
    Inversion: Solves for drainage area A = (q_p * T_p) / k.

    Where (Default SI Units):
    - discharge_peak : Hydrograph peak discharge Q_p [unit = m^3/s]
    - time_to_peak : Time to hydrograph peak T_p [unit = hours]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Area [unit = km^2 if 'km' in fn else 'm^2']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge_peak : FloatOrArray
        Hydrograph peak discharge Q_p [m^3/s].
    time_to_peak : FloatOrArray
        Time to hydrograph peak T_p [hours].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Area [km^2 if 'km' in fn else 'm^2']. Returns float for scalar inputs.
    """
    (qp, tp), is_scalar = coerce_inputs(discharge_peak, time_to_peak)
    k = 484.0 if system.lower() == 'us' else 0.208
    with np.errstate(all='ignore'):
        a = np.where((qp <= 0) | (tp <= 0), np.nan, qp * tp / k)
    return format_output(a, is_scalar)

def scs_lag_time(tc: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes SCS basin lag time t_L = 0.6 * T_c.
    Units (Default SI): tc [minutes] -> returns [hours]

    Formula:
    Computes SCS basin lag time t_L = 0.6 * T_c.

    Where (Default SI Units):
    - tc : Time of concentration T_c [unit = minutes]
    - Output : Time parameter [unit = hours]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    tc : FloatOrArray
        Time of concentration T_c [minutes].

    Returns
    -------
    float | np.ndarray
        Time parameter [hours]. Returns float for scalar inputs.
    """
    (t,), is_scalar = coerce_inputs(tc)
    out = 0.6 * t
    return format_output(out, is_scalar)

def scs_time_to_peak(rainfall_duration: FloatOrArray, lag_time: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes time to peak T_p = 0.5 * D + t_L.
    Units (Default SI): rainfall_duration [hours], lag_time [hours] -> returns [hours]

    Formula:
    Computes time to peak T_p = 0.5 * D + t_L.

    Where (Default SI Units):
    - rainfall_duration : Excess rainfall storm duration D [unit = hours]
    - lag_time : Basin lag time t_L [unit = hours]
    - Output : Time parameter [unit = hours]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    rainfall_duration : FloatOrArray
        Excess rainfall storm duration D [hours].
    lag_time : FloatOrArray
        Basin lag time t_L [hours].

    Returns
    -------
    float | np.ndarray
        Time parameter [hours]. Returns float for scalar inputs.
    """
    (d, tl), is_scalar = coerce_inputs(rainfall_duration, lag_time)
    out = 0.5 * d + tl
    return format_output(out, is_scalar)

def snyder_lag_time(length: FloatOrArray, length_to_centroid: FloatOrArray, c_t: FloatOrArray=1.5) -> Union[float, np.ndarray]:
    """
    Computes Snyder's unit hydrograph basin lag time tp.
    Units (Default SI): length [m], length_to_centroid [km], c_t [dimensionless (1.0 - 2.2)] -> returns [hours]

    Formula:
    t_p = C_t * (L * L_c)^0.3  [t_p in hours]

    Where (Default SI Units):
    - length : Reach / conduit / flow path length L [unit = m]
    - length_to_centroid : Channel length to basin centroid L_c [unit = km]
    - c_t : Snyder's basin lag coefficient C_t [unit = dimensionless (1.0 - 2.2)]
    - Output : Time parameter [unit = hours]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    length_to_centroid : FloatOrArray
        Channel length to basin centroid L_c [km].
    c_t : FloatOrArray
        Snyder's basin lag coefficient C_t [dimensionless (1.0 - 2.2)].

    Returns
    -------
    float | np.ndarray
        Time parameter [hours]. Returns float for scalar inputs.
    """
    (l, lc, ct), is_scalar = coerce_inputs(length, length_to_centroid, c_t)
    with np.errstate(all='ignore'):
        tp = np.where((l <= 0) | (lc <= 0) | (ct <= 0), np.nan, ct * (l * lc) ** 0.3)
    return format_output(tp, is_scalar)

def snyder_peak_discharge(drainage_area: FloatOrArray, lag_time: FloatOrArray, c_p: FloatOrArray=0.6, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes Snyder's unit hydrograph peak discharge Qp.
    Units (Default SI): drainage_area [km^2 (or ha for Rational)], lag_time [hours], c_p [dimensionless (0.4 - 0.8)] -> returns [m^3/s]

    Formula:
    SI: Q_p = (2.78 * C_p * A) / t_p  [A in km^2, t_p in hr, Q_p in m^3/s]

    Where (Default SI Units):
    - drainage_area : Catchment drainage area A [unit = km^2 (or ha for Rational)]
    - lag_time : Basin lag time t_L [unit = hours]
    - c_p : Snyder's peak coefficient C_p [unit = dimensionless (0.4 - 0.8)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    drainage_area : FloatOrArray
        Catchment drainage area A [km^2 (or ha for Rational)].
    lag_time : FloatOrArray
        Basin lag time t_L [hours].
    c_p : FloatOrArray
        Snyder's peak coefficient C_p [dimensionless (0.4 - 0.8)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (a, tp, cp), is_scalar = coerce_inputs(drainage_area, lag_time, c_p)
    k = 640.0 if system.lower() == 'us' else 2.78
    with np.errstate(all='ignore'):
        qp = np.where((a <= 0) | (tp <= 0) | (cp <= 0), np.nan, k * cp * a / tp)
    return format_output(qp, is_scalar)

def snyder_hydrograph_widths(unit_peak_q: FloatOrArray) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Computes USACE Snyder unit hydrograph widths at 50% and 75% of peak discharge.
    Units (Default SI): unit_peak_q [SI units] -> returns [standard SI units]

    Formula:
    W_50 = 5.87 / (q_p)^1.08  [hr]

    Where (Default SI Units):
    - unit_peak_q : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    unit_peak_q : FloatOrArray
        unit_peak_q [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (qp,), is_scalar = coerce_inputs(unit_peak_q)
    with np.errstate(all='ignore'):
        w50 = np.where(qp <= 0, np.nan, 5.87 / qp ** 1.08)
        w75 = np.where(qp <= 0, np.nan, 3.35 / qp ** 1.08)
    return format_outputs((w50, w75), is_scalar)

def muskingum_cunge_parameters(length: FloatOrArray, slope: FloatOrArray, bottom_width: FloatOrArray, discharge: FloatOrArray, roughness_n: FloatOrArray, system: Literal['si', 'us']='si') -> Tuple[Union[float, np.ndarray], ...]:
    """
    Computes physically-based Muskingum-Cunge routing parameters: wave celerity c, travel time K, and weighting factor X.
    Units (Default SI): length [m], slope [m/m (decimal)], bottom_width [m], discharge [m^3/s], roughness_n [s/m^(1/3) (or Kerby retardance)] -> returns [standard SI units]

    Formula:
    muskingum_cunge_parameters(length, slope, bottom_width, discharge, roughness_n, system)

    Where (Default SI Units):
    - length : Reach / conduit / flow path length L [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - bottom_width : Channel base width b [unit = m]
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - roughness_n : Roughness coefficient n [unit = s/m^(1/3) (or Kerby retardance)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    bottom_width : FloatOrArray
        Channel base width b [m].
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    roughness_n : FloatOrArray
        Roughness coefficient n [s/m^(1/3) (or Kerby retardance)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (l, s, b, q, n), is_scalar = coerce_inputs(length, slope, bottom_width, discharge, roughness_n)
    k_manning = 1.486 if system.lower() == 'us' else 1.0
    with np.errstate(all='ignore'):
        y = (q * n / (k_manning * b * np.sqrt(s))) ** 0.6
        v = q / (b * y)
        c = 5.0 / 3.0 * v
        k = l / c
        x = 0.5 * (1.0 - q / (b * s * c * l))
        x = np.clip(x, 0.0, 0.5)
    return format_outputs((c, k, x), is_scalar)

def baseflow_lyne_hollick(streamflow: Sequence[float], alpha: float=0.925) -> Tuple[np.ndarray, np.ndarray]:
    """
    Separates total streamflow into quickflow (direct runoff) and baseflow using the Lyne-Hollick digital filter.
    Units (Default SI): streamflow [SI units], alpha [dimensionless (~1.26)] -> returns [standard SI units]

    Formula:
    baseflow_lyne_hollick(streamflow, alpha)

    Where (Default SI Units):
    - streamflow : Input parameter [unit = SI units]
    - alpha : Priestley-Taylor radiation coefficient alpha [unit = dimensionless (~1.26)]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    streamflow : FloatOrArray
        streamflow [SI units].
    alpha : FloatOrArray
        Priestley-Taylor radiation coefficient alpha [dimensionless (~1.26)].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    y = np.asarray(streamflow, dtype=np.float64)
    n = len(y)
    q = np.zeros(n, dtype=np.float64)
    b = np.zeros(n, dtype=np.float64)
    for i in range(1, n):
        term = y[i] - y[i - 1]
        q_val = alpha * q[i - 1] + (1.0 + alpha) / 2.0 * term
        q[i] = max(0.0, min(y[i], q_val))
        b[i] = y[i] - q[i]
    b[0] = y[0]
    return (q, b)

def gumbel_reduced_variate(return_period: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes Gumbel EV1 reduced variate y_T = -ln(-ln(1 - 1/T)).
    Units (Default SI): return_period [years] -> returns [standard SI units]

    Formula:
    Computes Gumbel EV1 reduced variate y_T = -ln(-ln(1 - 1/T)).

    Where (Default SI Units):
    - return_period : Design recurrence interval / return period T [unit = years]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    return_period : FloatOrArray
        Design recurrence interval / return period T [years].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t,), is_scalar = coerce_inputs(return_period)
    with np.errstate(all='ignore'):
        yt = np.where(t <= 1.0, np.nan, -np.log(-np.log(1.0 - 1.0 / t)))
    return format_output(yt, is_scalar)

def gumbel_return_period(reduced_variate: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for return period T = 1 / (1 - exp(-exp(-y_T))).
    Units (Default SI): reduced_variate [dimensionless] -> returns [standard SI units]

    Formula:
    Inversion: Solves for return period T = 1 / (1 - exp(-exp(-y_T))).

    Where (Default SI Units):
    - reduced_variate : Gumbel EV1 reduced variate y_T [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    reduced_variate : FloatOrArray
        Gumbel EV1 reduced variate y_T [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (yt,), is_scalar = coerce_inputs(reduced_variate)
    with np.errstate(all='ignore'):
        t = 1.0 / (1.0 - np.exp(-np.exp(-yt)))
    return format_output(t, is_scalar)

def gumbel_frequency_factor(return_period: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes Chow frequency factor K_T for Gumbel distribution.
    Units (Default SI): return_period [years] -> returns [standard SI units]

    Formula:
    gumbel_frequency_factor(return_period)

    Where (Default SI Units):
    - return_period : Design recurrence interval / return period T [unit = years]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    return_period : FloatOrArray
        Design recurrence interval / return period T [years].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t,), is_scalar = coerce_inputs(return_period)
    with np.errstate(all='ignore'):
        yt = np.where(t <= 1.0, np.nan, -np.log(-np.log(1.0 - 1.0 / t)))
        kt = (yt - 0.5772156649) / (np.pi / np.sqrt(6.0))
    return format_output(kt, is_scalar)

def gumbel_design_flood(mean: FloatOrArray, std_dev: FloatOrArray, return_period: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes design flood peak magnitude x_T = mean + K_T * std_dev.
    Units (Default SI): mean [m^3/s], std_dev [m^3/s], return_period [years] -> returns [standard SI units]

    Formula:
    Computes design flood peak magnitude x_T = mean + K_T * std_dev.

    Where (Default SI Units):
    - mean : Sample arithmetic mean of flood series [unit = m^3/s]
    - std_dev : Sample standard deviation of flood series [unit = m^3/s]
    - return_period : Design recurrence interval / return period T [unit = years]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    mean : FloatOrArray
        Sample arithmetic mean of flood series [m^3/s].
    std_dev : FloatOrArray
        Sample standard deviation of flood series [m^3/s].
    return_period : FloatOrArray
        Design recurrence interval / return period T [years].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (x_bar, sx, t), is_scalar = coerce_inputs(mean, std_dev, return_period)
    with np.errstate(all='ignore'):
        yt = -np.log(-np.log(1.0 - 1.0 / t))
        kt = (yt - 0.5772156649) / (np.pi / np.sqrt(6.0))
        xt = x_bar + kt * sx
    return format_output(xt, is_scalar)

def gumbel_return_period_from_flood(observed_flood: FloatOrArray, mean: FloatOrArray, std_dev: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Back-calculates return period T from observed flood discharge magnitude.
    Units (Default SI): observed_flood [m^3/s], mean [m^3/s], std_dev [m^3/s] -> returns [standard SI units]

    Formula:
    gumbel_return_period_from_flood(observed_flood, mean, std_dev)

    Where (Default SI Units):
    - observed_flood : Observed flood discharge magnitude x [unit = m^3/s]
    - mean : Sample arithmetic mean of flood series [unit = m^3/s]
    - std_dev : Sample standard deviation of flood series [unit = m^3/s]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    observed_flood : FloatOrArray
        Observed flood discharge magnitude x [m^3/s].
    mean : FloatOrArray
        Sample arithmetic mean of flood series [m^3/s].
    std_dev : FloatOrArray
        Sample standard deviation of flood series [m^3/s].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (xt, x_bar, sx), is_scalar = coerce_inputs(observed_flood, mean, std_dev)
    with np.errstate(all='ignore'):
        kt = (xt - x_bar) / sx
        yt = 0.5772156649 + kt * (np.pi / np.sqrt(6.0))
        t = 1.0 / (1.0 - np.exp(-np.exp(-yt)))
    return format_output(t, is_scalar)

def log_pearson_3_flood(log_mean: FloatOrArray, log_std_dev: FloatOrArray, skewness: FloatOrArray, return_period: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes design flood using Log-Pearson Type III distribution (USGS Bulletin 17C standard).
    Units (Default SI): log_mean [log10(m^3/s)], log_std_dev [log10(m^3/s)], skewness [dimensionless], return_period [years] -> returns [standard SI units]

    Formula:
    log_pearson_3_flood(log_mean, log_std_dev, skewness, return_period)

    Where (Default SI Units):
    - log_mean : Mean of base-10 logarithms of flood peaks [unit = log10(m^3/s)]
    - log_std_dev : Standard deviation of base-10 logarithms [unit = log10(m^3/s)]
    - skewness : Station skewness coefficient G [unit = dimensionless]
    - return_period : Design recurrence interval / return period T [unit = years]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    log_mean : FloatOrArray
        Mean of base-10 logarithms of flood peaks [log10(m^3/s)].
    log_std_dev : FloatOrArray
        Standard deviation of base-10 logarithms [log10(m^3/s)].
    skewness : FloatOrArray
        Station skewness coefficient G [dimensionless].
    return_period : FloatOrArray
        Design recurrence interval / return period T [years].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (y_bar, sy, g, t), is_scalar = coerce_inputs(log_mean, log_std_dev, skewness, return_period)
    with np.errstate(all='ignore'):
        p = 1.0 / t
        w = np.sqrt(-2.0 * np.log(p))
        z = w - (2.515517 + 0.802853 * w + 0.010328 * w ** 2) / (1.0 + 1.432788 * w + 0.189269 * w ** 2 + 0.001308 * w ** 3)
        kt = np.where(np.abs(g) < 0.0001, z, 2.0 / g * ((1.0 + g * z / 6.0 - g ** 2 / 36.0) ** 3 - 1.0))
        log_xt = y_bar + kt * sy
        xt = 10.0 ** log_xt
    return format_output(xt, is_scalar)

def weibull_plotting_position(rank: FloatOrArray, total_samples: FloatOrArray) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Computes empirical exceedance probability P and return period T using Weibull plotting position: P = m / (N + 1).
    Units (Default SI): rank [integer], total_samples [integer count] -> returns [standard SI units]

    Formula:
    Computes empirical exceedance probability P and return period T using Weibull plotting position: P = m / (N + 1).

    Where (Default SI Units):
    - rank : Statistical order rank m (1 for largest flood) [unit = integer]
    - total_samples : Total record length / sample size N [unit = integer count]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    rank : FloatOrArray
        Statistical order rank m (1 for largest flood) [integer].
    total_samples : FloatOrArray
        Total record length / sample size N [integer count].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (m, n), is_scalar = coerce_inputs(rank, total_samples)
    with np.errstate(all='ignore'):
        p = m / (n + 1.0)
        t = (n + 1.0) / m
    return format_outputs((p, t), is_scalar)

def gringorten_plotting_position(rank: FloatOrArray, total_samples: FloatOrArray) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Computes empirical plotting position using Gringorten formula: P = (m - 0.44) / (N + 0.12).
    Units (Default SI): rank [integer], total_samples [integer count] -> returns [standard SI units]

    Formula:
    Computes empirical plotting position using Gringorten formula: P = (m - 0.44) / (N + 0.12).

    Where (Default SI Units):
    - rank : Statistical order rank m (1 for largest flood) [unit = integer]
    - total_samples : Total record length / sample size N [unit = integer count]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    rank : FloatOrArray
        Statistical order rank m (1 for largest flood) [integer].
    total_samples : FloatOrArray
        Total record length / sample size N [integer count].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (m, n), is_scalar = coerce_inputs(rank, total_samples)
    with np.errstate(all='ignore'):
        p = (m - 0.44) / (n + 0.12)
        t = (n + 0.12) / (m - 0.44)
    return format_outputs((p, t), is_scalar)

def cunnane_plotting_position(rank: FloatOrArray, total_samples: FloatOrArray) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Computes empirical plotting position using Cunnane formula: P = (m - 0.4) / (N + 0.2).
    Units (Default SI): rank [integer], total_samples [integer count] -> returns [standard SI units]

    Formula:
    Computes empirical plotting position using Cunnane formula: P = (m - 0.4) / (N + 0.2).

    Where (Default SI Units):
    - rank : Statistical order rank m (1 for largest flood) [unit = integer]
    - total_samples : Total record length / sample size N [unit = integer count]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    rank : FloatOrArray
        Statistical order rank m (1 for largest flood) [integer].
    total_samples : FloatOrArray
        Total record length / sample size N [integer count].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (m, n), is_scalar = coerce_inputs(rank, total_samples)
    with np.errstate(all='ignore'):
        p = (m - 0.4) / (n + 0.2)
        t = (n + 0.2) / (m - 0.4)
    return format_outputs((p, t), is_scalar)

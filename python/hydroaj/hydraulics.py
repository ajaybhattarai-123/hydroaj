"""
Open Channel Hydraulics and Pressurized Pipe Flow API.
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
G_SI = 9.80665
G_US = 32.17405
MANNING_K_SI = 1.0
MANNING_K_US = 1.48608
HW_K_SI = 10.67
HW_K_US = 4.727
HW_V_K_SI = 0.849
HW_V_K_US = 1.318

def _get_gravity(system: str) -> float:
    return G_US if system.lower() == 'us' else G_SI

def _get_manning_k(system: str) -> float:
    return MANNING_K_US if system.lower() == 'us' else MANNING_K_SI

def manning_discharge(area: FloatOrArray, hydraulic_radius: FloatOrArray, slope: FloatOrArray, roughness: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes manning discharge.
    Units (Default SI): area [m^2], hydraulic_radius [m], slope [m/m (decimal)], roughness [s/m^(1/3)] -> returns [m^3/s]

    Formula:
    Q = (k / n) * A * (R_h)^(2/3) * S_0^(1/2)

    Where (Default SI Units):
    - area : Cross-sectional flow area A [unit = m^2]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - roughness : Manning roughness coefficient n [unit = s/m^(1/3)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    roughness : FloatOrArray
        Manning roughness coefficient n [s/m^(1/3)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (a, rh, s, n), is_scalar = coerce_inputs(area, hydraulic_radius, slope, roughness)
    k = _get_manning_k(system)
    out = _core.manning_discharge(a, rh, s, n, k)
    return format_output(out, is_scalar)

def manning_velocity(hydraulic_radius: FloatOrArray, slope: FloatOrArray, roughness: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes manning velocity.
    Units (Default SI): hydraulic_radius [m], slope [m/m (decimal)], roughness [s/m^(1/3)] -> returns [m/s]

    Formula:
    V = (k / n) * (R_h)^(2/3) * S_0^(1/2)

    Where (Default SI Units):
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - roughness : Manning roughness coefficient n [unit = s/m^(1/3)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    roughness : FloatOrArray
        Manning roughness coefficient n [s/m^(1/3)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (rh, s, n), is_scalar = coerce_inputs(hydraulic_radius, slope, roughness)
    k = _get_manning_k(system)
    out = _core.manning_velocity(rh, s, n, k)
    return format_output(out, is_scalar)

def strickler_velocity(hydraulic_radius: FloatOrArray, slope: FloatOrArray, k_st: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes strickler velocity.
    Units (Default SI): hydraulic_radius [m], slope [m/m (decimal)], k_st [m^(1/3)/s] -> returns [m/s]

    Formula:
    V = k_st * (R_h)^(2/3) * S_0^(1/2)

    Where (Default SI Units):
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - k_st : Strickler roughness coefficient k_st = 1 / n [unit = m^(1/3)/s]
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    k_st : FloatOrArray
        Strickler roughness coefficient k_st = 1 / n [m^(1/3)/s].

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (rh, s, kst), is_scalar = coerce_inputs(hydraulic_radius, slope, k_st)
    out = _core.strickler_velocity(rh, s, kst)
    return format_output(out, is_scalar)

def chezy_velocity(chezy_c: FloatOrArray, hydraulic_radius: FloatOrArray, slope: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes chezy velocity.
    Units (Default SI): chezy_c [m^(1/2)/s], hydraulic_radius [m], slope [m/m (decimal)] -> returns [m/s]

    Formula:
    V = C * (R_h * S_0)^(1/2)

    Where (Default SI Units):
    - chezy_c : Chézy resistance coefficient C [unit = m^(1/2)/s]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    chezy_c : FloatOrArray
        Chézy resistance coefficient C [m^(1/2)/s].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (c, rh, s), is_scalar = coerce_inputs(chezy_c, hydraulic_radius, slope)
    out = _core.chezy_velocity(c, rh, s)
    return format_output(out, is_scalar)

def kutter_chezy_c(hydraulic_radius: FloatOrArray, slope: FloatOrArray, roughness: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes kutter chezy c.
    Units (Default SI): hydraulic_radius [m], slope [m/m (decimal)], roughness [s/m^(1/3)] -> returns [dimensionless]

    Formula:
    C = (23.0 + 0.00155/S_0 + 1.0/n) / (1.0 + (23.0 + 0.00155/S_0) * (n / sqrt(R_h)))

    Where (Default SI Units):
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - roughness : Manning roughness coefficient n [unit = s/m^(1/3)]
    - Output : Runoff / discharge coefficient [unit = dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    roughness : FloatOrArray
        Manning roughness coefficient n [s/m^(1/3)].

    Returns
    -------
    float | np.ndarray
        Runoff / discharge coefficient [dimensionless]. Returns float for scalar inputs.
    """
    (rh, s, n), is_scalar = coerce_inputs(hydraulic_radius, slope, roughness)
    out = _core.kutter_chezy_c(rh, s, n)
    return format_output(out, is_scalar)

def bazin_chezy_c(hydraulic_radius: FloatOrArray, gamma: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes bazin chezy c.
    Units (Default SI): hydraulic_radius [m], gamma [SI units] -> returns [dimensionless]

    Formula:
    C = 87.0 / (1.0 + gamma / sqrt(R_h))

    Where (Default SI Units):
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - gamma : Input parameter [unit = SI units]
    - Output : Runoff / discharge coefficient [unit = dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    gamma : FloatOrArray
        gamma [SI units].

    Returns
    -------
    float | np.ndarray
        Runoff / discharge coefficient [dimensionless]. Returns float for scalar inputs.
    """
    (rh, g), is_scalar = coerce_inputs(hydraulic_radius, gamma)
    out = _core.bazin_chezy_c(rh, g)
    return format_output(out, is_scalar)

def geom_rectangular(bottom_width: FloatOrArray, depth: FloatOrArray) -> Tuple[Union[float, np.ndarray], ...]:
    """
    Computes geom rectangular.
    Units (Default SI): bottom_width [m], depth [m] -> returns [m]

    Formula:
    A = b * y; P = b + 2*y; R_h = A / P; T = b; D_h = y; y_bar = y / 2

    Where (Default SI Units):
    - bottom_width : Channel base width b [unit = m]
    - depth : Water flow depth y [unit = m]
    - Output : Geometric properties tuple (Area [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    bottom_width : FloatOrArray
        Channel base width b [m].
    depth : FloatOrArray
        Water flow depth y [m].

    Returns
    -------
    float | np.ndarray
        Geometric properties tuple (Area [m^2], Perimeter [m], Hydraulic Radius [m], Top Width [m], Depth [m]). Returns float for scalar inputs.
    """
    (b, y), is_scalar = coerce_inputs(bottom_width, depth)
    outs = _core.geom_rectangular(b, y)
    return format_outputs(outs, is_scalar)

def geom_trapezoidal(bottom_width: FloatOrArray, side_slope: FloatOrArray, depth: FloatOrArray) -> Tuple[Union[float, np.ndarray], ...]:
    """
    Computes geom trapezoidal.
    Units (Default SI): bottom_width [m], side_slope [dimensionless], depth [m] -> returns [m]

    Formula:
    A = (b + m*y)*y; P = b + 2*y*sqrt(1 + m^2); R_h = A / P; T = b + 2*m*y; D_h = A / T; y_bar = y*(2*b + m*y)/(3*(b + m*y))

    Where (Default SI Units):
    - bottom_width : Channel base width b [unit = m]
    - side_slope : Side slope ratio m (1V : mH) [unit = dimensionless]
    - depth : Water flow depth y [unit = m]
    - Output : Geometric properties tuple (Area [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    bottom_width : FloatOrArray
        Channel base width b [m].
    side_slope : FloatOrArray
    Side slope ratio m (1V : mH) [dimensionless].
    depth : FloatOrArray
        Water flow depth y [m].

    Returns
    -------
    float | np.ndarray
        Geometric properties tuple (Area [m^2], Perimeter [m], Hydraulic Radius [m], Top Width [m], Depth [m]). Returns float for scalar inputs.
    """
    (b, m, y), is_scalar = coerce_inputs(bottom_width, side_slope, depth)
    outs = _core.geom_trapezoidal(b, m, y)
    return format_outputs(outs, is_scalar)

def geom_triangular(side_slope: FloatOrArray, depth: FloatOrArray) -> Tuple[Union[float, np.ndarray], ...]:
    """
    Computes geom triangular.
    Units (Default SI): side_slope [dimensionless], depth [m] -> returns [m]

    Formula:
    A = m * y^2; P = 2*y*sqrt(1 + m^2); R_h = A / P; T = 2*m*y; D_h = y / 2; y_bar = y / 3

    Where (Default SI Units):
    - side_slope : Side slope ratio m (1V : mH) [unit = dimensionless]
    - depth : Water flow depth y [unit = m]
    - Output : Geometric properties tuple (Area [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    side_slope : FloatOrArray
    Side slope ratio m (1V : mH) [dimensionless].
    depth : FloatOrArray
        Water flow depth y [m].

    Returns
    -------
    float | np.ndarray
        Geometric properties tuple (Area [m^2], Perimeter [m], Hydraulic Radius [m], Top Width [m], Depth [m]). Returns float for scalar inputs.
    """
    (m, y), is_scalar = coerce_inputs(side_slope, depth)
    outs = _core.geom_triangular(m, y)
    return format_outputs(outs, is_scalar)

def geom_circular(diameter: FloatOrArray, depth: FloatOrArray) -> Tuple[Union[float, np.ndarray], ...]:
    """
    Computes geom circular.
    Units (Default SI): diameter [m], depth [m] -> returns [m]

    Formula:
    theta = 2*acos(1 - 2*y/D); A = (D^2 / 8)*(theta - sin(theta)); P = D*theta/2; R_h = A / P; T = D*sin(theta/2); D_h = A / T

    Where (Default SI Units):
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - depth : Water flow depth y [unit = m]
    - Output : Geometric properties tuple (Area [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    depth : FloatOrArray
        Water flow depth y [m].

    Returns
    -------
    float | np.ndarray
        Geometric properties tuple (Area [m^2], Perimeter [m], Hydraulic Radius [m], Top Width [m], Depth [m]). Returns float for scalar inputs.
    """
    (d, y), is_scalar = coerce_inputs(diameter, depth)
    outs = _core.geom_circular(d, y)
    return format_outputs(outs, is_scalar)

def geom_parabolic(top_width: FloatOrArray, depth: FloatOrArray) -> Tuple[Union[float, np.ndarray], ...]:
    """
    Computes geom parabolic.
    Units (Default SI): top_width [m], depth [m] -> returns [m]

    Formula:
    A = (2/3)*T*y; P = T + (8/3)*(y^2 / T); R_h = A / P; D_h = (2/3)*y; y_bar = (2/5)*y

    Where (Default SI Units):
    - top_width : Channel free-surface top width T [unit = m]
    - depth : Water flow depth y [unit = m]
    - Output : Geometric properties tuple (Area [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    top_width : FloatOrArray
        Channel free-surface top width T [m].
    depth : FloatOrArray
        Water flow depth y [m].

    Returns
    -------
    float | np.ndarray
        Geometric properties tuple (Area [m^2], Perimeter [m], Hydraulic Radius [m], Top Width [m], Depth [m]). Returns float for scalar inputs.
    """
    (t, y), is_scalar = coerce_inputs(top_width, depth)
    outs = _core.geom_parabolic(t, y)
    return format_outputs(outs, is_scalar)

def specific_energy(depth: FloatOrArray, discharge: FloatOrArray, area: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes specific energy.
    Units (Default SI): depth [m], discharge [m^3/s], area [m^2] -> returns [standard SI units]

    Formula:
    E = y + Q^2 / (2 * g * A^2)

    Where (Default SI Units):
    - depth : Water flow depth y [unit = m]
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - area : Cross-sectional flow area A [unit = m^2]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    depth : FloatOrArray
        Water flow depth y [m].
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (y, q, a), is_scalar = coerce_inputs(depth, discharge, area)
    g = _get_gravity(system)
    out = _core.specific_energy(y, q, a, g)
    return format_output(out, is_scalar)

def froude_number(discharge: FloatOrArray, area: FloatOrArray, top_width: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes froude number.
    Units (Default SI): discharge [m^3/s], area [m^2], top_width [m] -> returns [standard SI units]

    Formula:
    Fr = (Q / A) / sqrt(g * (A / T))

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - area : Cross-sectional flow area A [unit = m^2]
    - top_width : Channel free-surface top width T [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    top_width : FloatOrArray
        Channel free-surface top width T [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, a, t), is_scalar = coerce_inputs(discharge, area, top_width)
    g = _get_gravity(system)
    out = _core.froude_number(q, a, t, g)
    return format_output(out, is_scalar)

def specific_force(discharge: FloatOrArray, area: FloatOrArray, centroid_depth: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes specific force.
    Units (Default SI): discharge [m^3/s], area [m^2], centroid_depth [m] -> returns [standard SI units]

    Formula:
    M = Q^2 / (g * A) + y_bar * A

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - area : Cross-sectional flow area A [unit = m^2]
    - centroid_depth : Flow depth [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    centroid_depth : FloatOrArray
        centroid_depth [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, a, yb), is_scalar = coerce_inputs(discharge, area, centroid_depth)
    g = _get_gravity(system)
    out = _core.specific_force(q, a, yb, g)
    return format_output(out, is_scalar)

def critical_depth_rectangular(unit_discharge: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes critical depth rectangular.
    Units (Default SI): unit_discharge [m^3/s] -> returns [standard SI units]

    Formula:
    y_c = (q^2 / g)^(1/3)

    Where (Default SI Units):
    - unit_discharge : Volumetric discharge rate [unit = m^3/s]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    unit_discharge : FloatOrArray
        unit_discharge [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q,), is_scalar = coerce_inputs(unit_discharge)
    g = _get_gravity(system)
    out = _core.critical_depth_rectangular(q, g)
    return format_output(out, is_scalar)

def normal_depth_trapezoidal(discharge: FloatOrArray, bottom_width: FloatOrArray, side_slope: FloatOrArray, slope: FloatOrArray, roughness: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Solves normal depth y_n in trapezoidal channel via parallel Newton-Raphson.
    Units (Default SI): discharge [m^3/s], bottom_width [m], side_slope [dimensionless], slope [m/m (decimal)], roughness [s/m^(1/3)] -> returns [standard SI units]

    Formula:
    Canal side slope ratio m (1V : mH) [dimensionless in SI, dimensionless in US]. Bounds: >= 0.

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - bottom_width : Channel base width b [unit = m]
    - side_slope : Side slope ratio m (1V : mH) [unit = dimensionless]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - roughness : Manning roughness coefficient n [unit = s/m^(1/3)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    bottom_width : FloatOrArray
        Channel base width b [m].
    side_slope : FloatOrArray
    Side slope ratio m (1V : mH) [dimensionless].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    roughness : FloatOrArray
        Manning roughness coefficient n [s/m^(1/3)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, b, m, s, n), is_scalar = coerce_inputs(discharge, bottom_width, side_slope, slope, roughness)
    k = _get_manning_k(system)
    out = _core.normal_depth_trapezoidal(q, b, m, s, n, k)
    return format_output(out, is_scalar)

def belanger_conjugate_depth(initial_depth: FloatOrArray, froude_1: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes belanger conjugate depth.
    Units (Default SI): initial_depth [m], froude_1 [dimensionless] -> returns [m]

    Formula:
    y_2 = (y_1 / 2) * (sqrt(1 + 8 * Fr_1^2) - 1)

    Where (Default SI Units):
    - initial_depth : Supercritical initial depth y_1 [unit = m]
    - froude_1 : Supercritical inflow Froude number Fr_1 [unit = dimensionless]
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    initial_depth : FloatOrArray
        Supercritical initial depth y_1 [m].
    froude_1 : FloatOrArray
        Supercritical inflow Froude number Fr_1 [dimensionless].

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (y1, fr1), is_scalar = coerce_inputs(initial_depth, froude_1)
    out = _core.belanger_conjugate_depth(y1, fr1)
    return format_output(out, is_scalar)

def hydraulic_jump_head_loss(initial_depth: FloatOrArray, sequent_depth: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes hydraulic jump head loss.
    Units (Default SI): initial_depth [m], sequent_depth [m] -> returns [standard SI units]

    Formula:
    Delta_E = (y_2 - y_1)^3 / (4 * y_1 * y_2)

    Where (Default SI Units):
    - initial_depth : Supercritical initial depth y_1 [unit = m]
    - sequent_depth : Subcritical conjugate depth y_2 [unit = m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    initial_depth : FloatOrArray
        Supercritical initial depth y_1 [m].
    sequent_depth : FloatOrArray
        Subcritical conjugate depth y_2 [m].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (y1, y2), is_scalar = coerce_inputs(initial_depth, sequent_depth)
    out = _core.hydraulic_jump_head_loss(y1, y2)
    return format_output(out, is_scalar)

def hydraulic_jump_length(initial_depth: FloatOrArray, sequent_depth: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes hydraulic jump length.
    Units (Default SI): initial_depth [m], sequent_depth [m] -> returns [km if 'km' in fn else 'm']

    Formula:
    L_j = 6.0 * (y_2 - y_1)

    Where (Default SI Units):
    - initial_depth : Supercritical initial depth y_1 [unit = m]
    - sequent_depth : Subcritical conjugate depth y_2 [unit = m]
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    initial_depth : FloatOrArray
        Supercritical initial depth y_1 [m].
    sequent_depth : FloatOrArray
        Subcritical conjugate depth y_2 [m].

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (y1, y2), is_scalar = coerce_inputs(initial_depth, sequent_depth)
    out = _core.hydraulic_jump_length(y1, y2)
    return format_output(out, is_scalar)

def gvf_gradient(bed_slope: FloatOrArray, friction_slope: FloatOrArray, froude_number: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes gvf gradient.
    Units (Default SI): bed_slope [m/m], friction_slope [m/m], froude_number [dimensionless] -> returns [standard SI units]

    Formula:
    dy_dx = (S_0 - S_f) / (1 - Fr^2)

    Where (Default SI Units):
    - bed_slope : Longitudinal channel bed slope S_0 [unit = m/m]
    - friction_slope : Energy grade line friction slope S_f [unit = m/m]
    - froude_number : Froude number Fr = V / sqrt(g * D_h) [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    bed_slope : FloatOrArray
        Longitudinal channel bed slope S_0 [m/m].
    friction_slope : FloatOrArray
        Energy grade line friction slope S_f [m/m].
    froude_number : FloatOrArray
        Froude number Fr = V / sqrt(g * D_h) [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (s0, sf, fr), is_scalar = coerce_inputs(bed_slope, friction_slope, froude_number)
    out = _core.gvf_gradient(s0, sf, fr)
    return format_output(out, is_scalar)

def manning_friction_slope(discharge: FloatOrArray, roughness: FloatOrArray, area: FloatOrArray, hydraulic_radius: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes manning friction slope.
    Units (Default SI): discharge [m^3/s], roughness [s/m^(1/3)], area [m^2], hydraulic_radius [m] -> returns [m/m]

    Formula:
    S_f = (n^2 * Q^2) / (k^2 * A^2 * R_h^(4/3))

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - roughness : Manning roughness coefficient n [unit = s/m^(1/3)]
    - area : Cross-sectional flow area A [unit = m^2]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    roughness : FloatOrArray
        Manning roughness coefficient n [s/m^(1/3)].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (q, n, a, rh), is_scalar = coerce_inputs(discharge, roughness, area, hydraulic_radius)
    k = _get_manning_k(system)
    out = _core.manning_friction_slope(q, n, a, rh, k)
    return format_output(out, is_scalar)

def direct_step(energy_1: FloatOrArray, energy_2: FloatOrArray, bed_slope: FloatOrArray, friction_slope_1: FloatOrArray, friction_slope_2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Direct Step method reach length between two sections:
    Units (Default SI): energy_1 [SI units], energy_2 [SI units], bed_slope [m/m], friction_slope_1 [m/m], friction_slope_2 [m/m] -> returns [standard SI units]

    Formula:
    Delta_x = (E_2 - E_1) / (S_0 - 0.5 * (S_f1 + S_f2))

    Where (Default SI Units):
    - energy_1 : Input parameter [unit = SI units]
    - energy_2 : Input parameter [unit = SI units]
    - bed_slope : Longitudinal channel bed slope S_0 [unit = m/m]
    - friction_slope_1 : Longitudinal bed slope / gradient [unit = m/m]
    - friction_slope_2 : Longitudinal bed slope / gradient [unit = m/m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    energy_1 : FloatOrArray
        energy_1 [SI units].
    energy_2 : FloatOrArray
        energy_2 [SI units].
    bed_slope : FloatOrArray
        Longitudinal channel bed slope S_0 [m/m].
    friction_slope_1 : FloatOrArray
        friction_slope_1 [SI units].
    friction_slope_2 : FloatOrArray
        friction_slope_2 [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (e1, e2, s0, sf1, sf2), is_scalar = coerce_inputs(energy_1, energy_2, bed_slope, friction_slope_1, friction_slope_2)
    out = _core.direct_step(e1, e2, s0, sf1, sf2)
    return format_output(out, is_scalar)

def darcy_weisbach(friction_factor: FloatOrArray, length: FloatOrArray, diameter: FloatOrArray, velocity: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Darcy-Weisbach head loss: h_f = f * (L / D) * (V^2 / (2 * g))
    Units (Default SI): friction_factor [dimensionless], length [m], diameter [m], velocity [m/s] -> returns [standard SI units]

    Formula:
    Darcy-Weisbach head loss: h_f = f * (L / D) * (V^2 / (2 * g))

    Where (Default SI Units):
    - friction_factor : Darcy-Weisbach friction factor f [unit = dimensionless]
    - length : Reach / conduit / flow path length L [unit = m]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    friction_factor : FloatOrArray
        Darcy-Weisbach friction factor f [dimensionless].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (f, l, d, v), is_scalar = coerce_inputs(friction_factor, length, diameter, velocity)
    g = _get_gravity(system)
    out = _core.darcy_weisbach(f, l, d, v, g)
    return format_output(out, is_scalar)

def reynolds_number(velocity: FloatOrArray, diameter: FloatOrArray, kinematic_viscosity: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes reynolds number.
    Units (Default SI): velocity [m/s], diameter [m], kinematic_viscosity [SI units] -> returns [standard SI units]

    Formula:
    Re = (V * D) / nu

    Where (Default SI Units):
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - kinematic_viscosity : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    kinematic_viscosity : FloatOrArray
        kinematic_viscosity [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (v, d, nu), is_scalar = coerce_inputs(velocity, diameter, kinematic_viscosity)
    out = _core.reynolds_number(v, d, nu)
    return format_output(out, is_scalar)

def laminar_friction(reynolds: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Laminar friction factor: f = 64 / Re
    Units (Default SI): reynolds [dimensionless] -> returns [standard SI units]

    Formula:
    Laminar friction factor: f = 64 / Re

    Where (Default SI Units):
    - reynolds : Reynolds number Re = V * D / nu [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    reynolds : FloatOrArray
        Reynolds number Re = V * D / nu [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (re,), is_scalar = coerce_inputs(reynolds)
    out = _core.laminar_friction(re)
    return format_output(out, is_scalar)

def colebrook_white(relative_roughness: FloatOrArray, reynolds: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Vectorized iterative root-finding for Colebrook-White friction factor f:
    Units (Default SI): relative_roughness [SI units], reynolds [dimensionless] -> returns [standard SI units]

    Formula:
    1 / sqrt(f) = -2 * log10((eps/D)/3.7 + 2.51/(Re * sqrt(f)))

    Where (Default SI Units):
    - relative_roughness : Input parameter [unit = SI units]
    - reynolds : Reynolds number Re = V * D / nu [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    relative_roughness : FloatOrArray
        relative_roughness [SI units].
    reynolds : FloatOrArray
        Reynolds number Re = V * D / nu [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (ed, re), is_scalar = coerce_inputs(relative_roughness, reynolds)
    out = _core.colebrook_white(ed, re)
    return format_output(out, is_scalar)

def swamee_jain(relative_roughness: FloatOrArray, reynolds: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Swamee-Jain explicit friction factor approximation.
    Units (Default SI): relative_roughness [SI units], reynolds [dimensionless] -> returns [standard SI units]

    Formula:
    swamee_jain(relative_roughness, reynolds)

    Where (Default SI Units):
    - relative_roughness : Input parameter [unit = SI units]
    - reynolds : Reynolds number Re = V * D / nu [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    relative_roughness : FloatOrArray
        relative_roughness [SI units].
    reynolds : FloatOrArray
        Reynolds number Re = V * D / nu [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (ed, re), is_scalar = coerce_inputs(relative_roughness, reynolds)
    out = _core.swamee_jain(ed, re)
    return format_output(out, is_scalar)

def haaland(relative_roughness: FloatOrArray, reynolds: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Haaland explicit friction factor approximation.
    Units (Default SI): relative_roughness [SI units], reynolds [dimensionless] -> returns [standard SI units]

    Formula:
    haaland(relative_roughness, reynolds)

    Where (Default SI Units):
    - relative_roughness : Input parameter [unit = SI units]
    - reynolds : Reynolds number Re = V * D / nu [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    relative_roughness : FloatOrArray
        relative_roughness [SI units].
    reynolds : FloatOrArray
        Reynolds number Re = V * D / nu [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (ed, re), is_scalar = coerce_inputs(relative_roughness, reynolds)
    out = _core.haaland(ed, re)
    return format_output(out, is_scalar)

def churchill(relative_roughness: FloatOrArray, reynolds: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Churchill explicit friction factor covering all regimes (laminar, transition, turbulent).
    Units (Default SI): relative_roughness [SI units], reynolds [dimensionless] -> returns [standard SI units]

    Formula:
    churchill(relative_roughness, reynolds)

    Where (Default SI Units):
    - relative_roughness : Input parameter [unit = SI units]
    - reynolds : Reynolds number Re = V * D / nu [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    relative_roughness : FloatOrArray
        relative_roughness [SI units].
    reynolds : FloatOrArray
        Reynolds number Re = V * D / nu [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (ed, re), is_scalar = coerce_inputs(relative_roughness, reynolds)
    out = _core.churchill(ed, re)
    return format_output(out, is_scalar)

def wood(relative_roughness: FloatOrArray, reynolds: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Wood explicit friction factor approximation.
    Units (Default SI): relative_roughness [SI units], reynolds [dimensionless] -> returns [standard SI units]

    Formula:
    wood(relative_roughness, reynolds)

    Where (Default SI Units):
    - relative_roughness : Input parameter [unit = SI units]
    - reynolds : Reynolds number Re = V * D / nu [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    relative_roughness : FloatOrArray
        relative_roughness [SI units].
    reynolds : FloatOrArray
        Reynolds number Re = V * D / nu [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (ed, re), is_scalar = coerce_inputs(relative_roughness, reynolds)
    out = _core.wood(ed, re)
    return format_output(out, is_scalar)

def hazen_williams(length: FloatOrArray, discharge: FloatOrArray, c_coefficient: FloatOrArray, diameter: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Hazen-Williams head loss:
    Units (Default SI): length [m], discharge [m^3/s], c_coefficient [dimensionless], diameter [m] -> returns [standard SI units]

    Formula:
    h_f = (k_hw * L * Q^1.852) / (C^1.852 * D^4.87)

    Where (Default SI Units):
    - length : Reach / conduit / flow path length L [unit = m]
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - c_coefficient : Input parameter [unit = dimensionless]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    c_coefficient : FloatOrArray
        c_coefficient [SI units].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (l, q, c, d), is_scalar = coerce_inputs(length, discharge, c_coefficient, diameter)
    k_hw = HW_K_US if system.lower() == 'us' else HW_K_SI
    out = _core.hazen_williams(l, q, c, d, k_hw)
    return format_output(out, is_scalar)

def hazen_williams_velocity(c_coefficient: FloatOrArray, hydraulic_radius: FloatOrArray, slope: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes hazen williams velocity.
    Units (Default SI): c_coefficient [dimensionless], hydraulic_radius [m], slope [m/m (decimal)] -> returns [m/s]

    Formula:
    V = k_v * C * R_h^0.63 * S^0.54

    Where (Default SI Units):
    - c_coefficient : Input parameter [unit = dimensionless]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    c_coefficient : FloatOrArray
        c_coefficient [SI units].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (c, rh, s), is_scalar = coerce_inputs(c_coefficient, hydraulic_radius, slope)
    k_v = HW_V_K_US if system.lower() == 'us' else HW_V_K_SI
    out = _core.hazen_williams_velocity(c, rh, s, k_v)
    return format_output(out, is_scalar)

def minor_loss(loss_coefficient: FloatOrArray, velocity: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes minor loss.
    Units (Default SI): loss_coefficient [dimensionless], velocity [m/s] -> returns [standard SI units]

    Formula:
    h_m = K_L * V^2 / (2 * g)

    Where (Default SI Units):
    - loss_coefficient : Input parameter [unit = dimensionless]
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    loss_coefficient : FloatOrArray
        loss_coefficient [SI units].
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (k, v), is_scalar = coerce_inputs(loss_coefficient, velocity)
    g = _get_gravity(system)
    out = _core.minor_loss(k, v, g)
    return format_output(out, is_scalar)

def wave_celerity(bulk_modulus: FloatOrArray, density: FloatOrArray, elastic_modulus: FloatOrArray, diameter: FloatOrArray, wall_thickness: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Water hammer wave celerity: a = sqrt((K / rho) / (1 + (K / E) * (D / e)))
    Units (Default SI): bulk_modulus [SI units], density [kg/m^3 (~1000.0)], elastic_modulus [SI units], diameter [m], wall_thickness [SI units] -> returns [standard SI units]

    Formula:
    Water hammer wave celerity: a = sqrt((K / rho) / (1 + (K / E) * (D / e)))

    Where (Default SI Units):
    - bulk_modulus : Input parameter [unit = SI units]
    - density : Fluid mass density rho [unit = kg/m^3 (~1000.0)]
    - elastic_modulus : Input parameter [unit = SI units]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - wall_thickness : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    bulk_modulus : FloatOrArray
        bulk_modulus [SI units].
    density : FloatOrArray
        Fluid mass density rho [kg/m^3 (~1000.0)].
    elastic_modulus : FloatOrArray
        elastic_modulus [SI units].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    wall_thickness : FloatOrArray
        wall_thickness [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (k, rho, e, d, t), is_scalar = coerce_inputs(bulk_modulus, density, elastic_modulus, diameter, wall_thickness)
    out = _core.wave_celerity(k, rho, e, d, t)
    return format_output(out, is_scalar)

def joukowsky(celerity: FloatOrArray, delta_v: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Joukowsky pressure head rise: Delta_H = (a * Delta_V) / g
    Units (Default SI): celerity [SI units], delta_v [SI units] -> returns [standard SI units]

    Formula:
    Joukowsky pressure head rise: Delta_H = (a * Delta_V) / g

    Where (Default SI Units):
    - celerity : Input parameter [unit = SI units]
    - delta_v : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    celerity : FloatOrArray
        celerity [SI units].
    delta_v : FloatOrArray
        delta_v [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (a, dv), is_scalar = coerce_inputs(celerity, delta_v)
    g = _get_gravity(system)
    out = _core.joukowsky(a, dv, g)
    return format_output(out, is_scalar)

def critical_closure_time(length: FloatOrArray, celerity: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes critical closure time.
    Units (Default SI): length [m], celerity [SI units] -> returns [standard SI units]

    Formula:
    T_c = (2 * L) / a

    Where (Default SI Units):
    - length : Reach / conduit / flow path length L [unit = m]
    - celerity : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    celerity : FloatOrArray
        celerity [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (l, a), is_scalar = coerce_inputs(length, celerity)
    out = _core.critical_closure_time(l, a)
    return format_output(out, is_scalar)

def optimal_rectangular_section(depth: FloatOrArray) -> Tuple[Union[float, np.ndarray], ...]:
    """
    Computes optimal rectangular section.
    Units (Default SI): depth [m] -> returns [standard SI units]

    Formula:
    b = 2 * y; R_h = y / 2; A = 2 * y^2; P = 4 * y

    Where (Default SI Units):
    - depth : Water flow depth y [unit = m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    depth : FloatOrArray
        Water flow depth y [m].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (y,), is_scalar = coerce_inputs(depth)
    b, a, p, rh = _core.optimal_rectangular_section(y)
    return format_outputs((b, a, p, rh), is_scalar)

def optimal_trapezoidal_section(depth: FloatOrArray) -> Tuple[Union[float, np.ndarray], ...]:
    """
    Computes optimal trapezoidal section.
    Units (Default SI): depth [m] -> returns [standard SI units]

    Formula:
    m = 1 / sqrt(3); b = 2 * y * (sqrt(1 + m^2) - m); R_h = y / 2

    Where (Default SI Units):
    - depth : Water flow depth y [unit = m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    depth : FloatOrArray
        Water flow depth y [m].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (y,), is_scalar = coerce_inputs(depth)
    b, m, rh = _core.optimal_trapezoidal_section(y)
    return format_outputs((b, m, rh), is_scalar)

def optimal_triangular_section(depth: FloatOrArray) -> Tuple[Union[float, np.ndarray], ...]:
    """
    Computes optimal triangular section.
    Units (Default SI): depth [m] -> returns [standard SI units]

    Formula:
    m = 1.0; R_h = y / (2 * sqrt(2)); A = y^2; P = 2 * sqrt(2) * y

    Where (Default SI Units):
    - depth : Water flow depth y [unit = m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    depth : FloatOrArray
        Water flow depth y [m].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (y,), is_scalar = coerce_inputs(depth)
    a, p, rh = _core.optimal_triangular_section(y)
    return format_outputs((a, p, rh), is_scalar)

def critical_velocity(hydraulic_depth: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes critical velocity.
    Units (Default SI): hydraulic_depth [m] -> returns [m/s]

    Formula:
    V_c = sqrt(g * D_h)

    Where (Default SI Units):
    - hydraulic_depth : Flow depth [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    hydraulic_depth : FloatOrArray
        hydraulic_depth [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (dh,), is_scalar = coerce_inputs(hydraulic_depth)
    g = _get_gravity(system)
    out = _core.critical_velocity(dh, g)
    return format_output(out, is_scalar)

def critical_slope(roughness: FloatOrArray, critical_r_h: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes critical slope.
    Units (Default SI): roughness [s/m^(1/3)], critical_r_h [SI units] -> returns [m/m]

    Formula:
    S_c = (g * n^2) / (k^2 * R_hc^(4/3))

    Where (Default SI Units):
    - roughness : Manning roughness coefficient n [unit = s/m^(1/3)]
    - critical_r_h : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    roughness : FloatOrArray
        Manning roughness coefficient n [s/m^(1/3)].
    critical_r_h : FloatOrArray
        critical_r_h [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (n, rh), is_scalar = coerce_inputs(roughness, critical_r_h)
    g = _get_gravity(system)
    k = _get_manning_k(system)
    out = _core.critical_slope(n, rh, g, k)
    return format_output(out, is_scalar)

def gravity_wave_celerity(hydraulic_depth: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes gravity wave celerity.
    Units (Default SI): hydraulic_depth [m] -> returns [standard SI units]

    Formula:
    c = sqrt(g * D_h)

    Where (Default SI Units):
    - hydraulic_depth : Flow depth [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    hydraulic_depth : FloatOrArray
        hydraulic_depth [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (dh,), is_scalar = coerce_inputs(hydraulic_depth)
    g = _get_gravity(system)
    out = _core.gravity_wave_celerity(dh, g)
    return format_output(out, is_scalar)

def hydraulic_jump_efficiency(froude_1: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes hydraulic jump efficiency.
    Units (Default SI): froude_1 [dimensionless] -> returns [standard SI units]

    Formula:
    E_2_over_E_1 = ((1 + 8 * Fr_1^2)^(1.5) - 4 * Fr_1^2 + 1) / (8 * Fr_1^2 * (2 + Fr_1^2))

    Where (Default SI Units):
    - froude_1 : Supercritical inflow Froude number Fr_1 [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    froude_1 : FloatOrArray
        Supercritical inflow Froude number Fr_1 [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (fr,), is_scalar = coerce_inputs(froude_1)
    out = _core.hydraulic_jump_efficiency(fr)
    return format_output(out, is_scalar)

def hydraulic_jump_height(y_1: FloatOrArray, y_2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes hydraulic jump height.
    Units (Default SI): y_1 [m], y_2 [m] -> returns [standard SI units]

    Formula:
    h_j = y_2 - y_1

    Where (Default SI Units):
    - y_1 : Flow depth [unit = m]
    - y_2 : Flow depth [unit = m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    y_1 : FloatOrArray
        y_1 [SI units].
    y_2 : FloatOrArray
        y_2 [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (y1, y2), is_scalar = coerce_inputs(y_1, y_2)
    out = _core.hydraulic_jump_height(y1, y2)
    return format_output(out, is_scalar)

def critical_depth_triangular(discharge: FloatOrArray, side_slope: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes critical depth triangular.
    Units (Default SI): discharge [m^3/s], side_slope [dimensionless] -> returns [standard SI units]

    Formula:
    y_c = (2 * Q^2 / (g * m^2))^(1/5)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - side_slope : Side slope ratio m (1V : mH) [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    side_slope : FloatOrArray
    Side slope ratio m (1V : mH) [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, m), is_scalar = coerce_inputs(discharge, side_slope)
    g = _get_gravity(system)
    out = _core.critical_depth_triangular(q, m, g)
    return format_output(out, is_scalar)

def horton_einstein_composite_n(perimeters: FloatOrArray, roughnesses: FloatOrArray) -> float:
    """
    Computes horton einstein composite n.
    Units (Default SI): perimeters [SI units], roughnesses [SI units] -> returns [s/m^(1/3) or dimensionless]

    Formula:
    n_bar = (sum(P_i * n_i^1.5) / sum(P_i))^(2/3)

    Where (Default SI Units):
    - perimeters : Input parameter [unit = SI units]
    - roughnesses : Input parameter [unit = SI units]
    - Output : Roughness coefficient [unit = s/m^(1/3) or dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    perimeters : FloatOrArray
        perimeters [SI units].
    roughnesses : FloatOrArray
        roughnesses [SI units].

    Returns
    -------
    float | np.ndarray
        Roughness coefficient [s/m^(1/3) or dimensionless]. Returns float for scalar inputs.
    """
    p = np.ascontiguousarray(perimeters, dtype=np.float64)
    n = np.ascontiguousarray(roughnesses, dtype=np.float64)
    return float(_core.horton_einstein_composite_n(p, n))

def pavlovskii_composite_n(perimeters: FloatOrArray, roughnesses: FloatOrArray) -> float:
    """
    Computes pavlovskii composite n.
    Units (Default SI): perimeters [SI units], roughnesses [SI units] -> returns [s/m^(1/3) or dimensionless]

    Formula:
    n_bar = (sum(P_i * n_i^2) / sum(P_i))^(1/2)

    Where (Default SI Units):
    - perimeters : Input parameter [unit = SI units]
    - roughnesses : Input parameter [unit = SI units]
    - Output : Roughness coefficient [unit = s/m^(1/3) or dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    perimeters : FloatOrArray
        perimeters [SI units].
    roughnesses : FloatOrArray
        roughnesses [SI units].

    Returns
    -------
    float | np.ndarray
        Roughness coefficient [s/m^(1/3) or dimensionless]. Returns float for scalar inputs.
    """
    p = np.ascontiguousarray(perimeters, dtype=np.float64)
    n = np.ascontiguousarray(roughnesses, dtype=np.float64)
    return float(_core.pavlovskii_composite_n(p, n))

def culvert_inlet_unsubmerged(discharge: FloatOrArray, diameter: FloatOrArray, area: FloatOrArray, critical_energy: FloatOrArray, slope: FloatOrArray, k_coeff: FloatOrArray=0.0098, m_exp: FloatOrArray=2.0) -> Union[float, np.ndarray]:
    """
    Computes culvert inlet unsubmerged.
    Units (Default SI): discharge [m^3/s], diameter [m], area [m^2], critical_energy [SI units], slope [m/m (decimal)], k_coeff [dimensionless], m_exp [SI units] -> returns [standard SI units]

    Formula:
    HW_d = (H_c / D) + K * (Q / (A * sqrt(D)))^M - 0.5 * S

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - area : Cross-sectional flow area A [unit = m^2]
    - critical_energy : Input parameter [unit = SI units]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - k_coeff : Input parameter [unit = dimensionless]
    - m_exp : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    critical_energy : FloatOrArray
        critical_energy [SI units].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    k_coeff : FloatOrArray
        k_coeff [SI units].
    m_exp : FloatOrArray
        m_exp [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, d, a, hc, s, k, m), is_scalar = coerce_inputs(discharge, diameter, area, critical_energy, slope, k_coeff, m_exp)
    out = _core.culvert_inlet_unsubmerged(q, d, a, hc, s, k, m)
    return format_output(out, is_scalar)

def culvert_inlet_submerged(discharge: FloatOrArray, diameter: FloatOrArray, area: FloatOrArray, slope: FloatOrArray, c_coeff: FloatOrArray=0.0398, y_const: FloatOrArray=0.67) -> Union[float, np.ndarray]:
    """
    Computes culvert inlet submerged.
    Units (Default SI): discharge [m^3/s], diameter [m], area [m^2], slope [m/m (decimal)], c_coeff [s^2 / m^5], y_const [m] -> returns [standard SI units]

    Formula:
    HW_d = c * (Q / (A * sqrt(D)))^2 + Y - 0.5 * S

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - area : Cross-sectional flow area A [unit = m^2]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - c_coeff : Well turbulent screen loss coefficient C [unit = s^2 / m^5]
    - y_const : Flow depth [unit = m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    c_coeff : FloatOrArray
        Well turbulent screen loss coefficient C [s^2 / m^5].
    y_const : FloatOrArray
        y_const [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, d, a, s, c, y), is_scalar = coerce_inputs(discharge, diameter, area, slope, c_coeff, y_const)
    out = _core.culvert_inlet_submerged(q, d, a, s, c, y)
    return format_output(out, is_scalar)

def culvert_outlet_control_head(tailwater_term: FloatOrArray, total_losses: FloatOrArray, length: FloatOrArray, slope: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes culvert outlet control head.
    Units (Default SI): tailwater_term [SI units], total_losses [SI units], length [m], slope [m/m (decimal)] -> returns [m]

    Formula:
    HW_o = h_o + H - L * S_0; H = (1 + K_e + (29 * n^2 * L) / (R_h^(4/3))) * (V^2 / (2 * g))

    Where (Default SI Units):
    - tailwater_term : Input parameter [unit = SI units]
    - total_losses : Input parameter [unit = SI units]
    - length : Reach / conduit / flow path length L [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    tailwater_term : FloatOrArray
        tailwater_term [SI units].
    total_losses : FloatOrArray
        total_losses [SI units].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (ho, h, l, s0), is_scalar = coerce_inputs(tailwater_term, total_losses, length, slope)
    out = _core.culvert_outlet_control_head(ho, h, l, s0)
    return format_output(out, is_scalar)

def culvert_entrance_loss(entrance_coeff: FloatOrArray, velocity: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes culvert entrance loss.
    Units (Default SI): entrance_coeff [dimensionless], velocity [m/s] -> returns [standard SI units]

    Formula:
    h_e = K_e * V^2 / (2 * g)

    Where (Default SI Units):
    - entrance_coeff : Input parameter [unit = dimensionless]
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    entrance_coeff : FloatOrArray
        entrance_coeff [SI units].
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (ke, v), is_scalar = coerce_inputs(entrance_coeff, velocity)
    g = _get_gravity(system)
    out = _core.culvert_entrance_loss(ke, v, g)
    return format_output(out, is_scalar)

def hardy_cross_correction(sum_head_loss: FloatOrArray, sum_derivative: FloatOrArray, n_exp: FloatOrArray=2.0) -> Union[float, np.ndarray]:
    """
    Computes hardy cross correction.
    Units (Default SI): sum_head_loss [m], sum_derivative [SI units], n_exp [SI units] -> returns [standard SI units]

    Formula:
    delta_Q = -sum(r * Q * abs(Q)^(n - 1)) / (n * sum(r * abs(Q)^(n - 1)))

    Where (Default SI Units):
    - sum_head_loss : Hydraulic head [unit = m]
    - sum_derivative : Input parameter [unit = SI units]
    - n_exp : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    sum_head_loss : FloatOrArray
        sum_head_loss [SI units].
    sum_derivative : FloatOrArray
        sum_derivative [SI units].
    n_exp : FloatOrArray
        n_exp [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (shf, sdhf, n), is_scalar = coerce_inputs(sum_head_loss, sum_derivative, n_exp)
    out = _core.hardy_cross_correction(shf, sdhf, n)
    return format_output(out, is_scalar)

def equivalent_pipe_length(minor_loss_coeff: FloatOrArray, diameter: FloatOrArray, friction_factor: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes equivalent pipe length.
    Units (Default SI): minor_loss_coeff [dimensionless], diameter [m], friction_factor [dimensionless] -> returns [km if 'km' in fn else 'm']

    Formula:
    L_e = (K_L * D) / f

    Where (Default SI Units):
    - minor_loss_coeff : Input parameter [unit = dimensionless]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - friction_factor : Darcy-Weisbach friction factor f [unit = dimensionless]
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    minor_loss_coeff : FloatOrArray
        minor_loss_coeff [SI units].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    friction_factor : FloatOrArray
        Darcy-Weisbach friction factor f [dimensionless].

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (kl, d, f), is_scalar = coerce_inputs(minor_loss_coeff, diameter, friction_factor)
    out = _core.equivalent_pipe_length(kl, d, f)
    return format_output(out, is_scalar)

def equivalent_diameter_series(total_length: FloatOrArray, sum_ratio: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes equivalent diameter series.
    Units (Default SI): total_length [m], sum_ratio [SI units] -> returns [standard SI units]

    Formula:
    D_e = (L_total / sum(L_i / D_i^5))^(1/5)

    Where (Default SI Units):
    - total_length : Length [unit = m]
    - sum_ratio : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    total_length : FloatOrArray
        total_length [SI units].
    sum_ratio : FloatOrArray
        sum_ratio [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (lt, sld), is_scalar = coerce_inputs(total_length, sum_ratio)
    out = _core.equivalent_diameter_series(lt, sld)
    return format_output(out, is_scalar)

def parallel_pipes_distribution(total_discharge: FloatOrArray, branch_conductance: FloatOrArray, sum_conductance: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes parallel pipes distribution.
    Units (Default SI): total_discharge [m^3/s], branch_conductance [SI units], sum_conductance [SI units] -> returns [standard SI units]

    Formula:
    Q_i = Q_total * (sqrt(D_i^5 / L_i)) / sum(sqrt(D_j^5 / L_j))

    Where (Default SI Units):
    - total_discharge : Volumetric discharge rate [unit = m^3/s]
    - branch_conductance : Input parameter [unit = SI units]
    - sum_conductance : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    total_discharge : FloatOrArray
        total_discharge [SI units].
    branch_conductance : FloatOrArray
        branch_conductance [SI units].
    sum_conductance : FloatOrArray
        sum_conductance [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (qt, ki, sk), is_scalar = coerce_inputs(total_discharge, branch_conductance, sum_conductance)
    out = _core.parallel_pipes_distribution(qt, ki, sk)
    return format_output(out, is_scalar)

def water_horsepower(discharge: FloatOrArray, head: FloatOrArray, specific_weight: FloatOrArray=None, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes water horsepower.
    Units (Default SI): discharge [m^3/s], head [m], specific_weight [SI units] -> returns [standard SI units]

    Formula:
    P_w = (rho * g * Q * H) / 1000.0 (kW SI) or (gamma * Q * H) / 550.0 (hp US)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - head : Upstream / operating hydraulic head H [unit = m]
    - specific_weight : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    specific_weight : FloatOrArray
        specific_weight [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    if specific_weight is None:
        gam_val = 62.4 if system.lower() == 'us' else 9806.65
        specific_weight = gam_val
    (q, h, gam), is_scalar = coerce_inputs(discharge, head, specific_weight)
    divisor = 550.0 if system.lower() == 'us' else 1000.0
    out = _core.water_power(q, h, gam, divisor)
    return format_output(out, is_scalar)

def pump_brake_power(water_power: FloatOrArray, efficiency: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes pump brake power.
    Units (Default SI): water_power [SI units], efficiency [dimensionless decimal (0 - 1)] -> returns [standard SI units]

    Formula:
    P_b = P_w / eta

    Where (Default SI Units):
    - water_power : Input parameter [unit = SI units]
    - efficiency : Overall wire-to-water pump efficiency eta [unit = dimensionless decimal (0 - 1)]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    water_power : FloatOrArray
        water_power [SI units].
    efficiency : FloatOrArray
        Overall wire-to-water pump efficiency eta [dimensionless decimal (0 - 1)].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (pw, eff), is_scalar = coerce_inputs(water_power, efficiency)
    out = _core.pump_brake_power(pw, eff)
    return format_output(out, is_scalar)
manning_q = manning_discharge
manning_v = manning_velocity

def manning_n(discharge: FloatOrArray, area: FloatOrArray, hydraulic_radius: FloatOrArray, slope: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes manning n.
    Units (Default SI): discharge [m^3/s], area [m^2], hydraulic_radius [m], slope [m/m (decimal)] -> returns [s/m^(1/3) or dimensionless]

    Formula:
    n = (k / Q) * A * R_h^(2/3) * S_0^(1/2)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - area : Cross-sectional flow area A [unit = m^2]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Roughness coefficient [unit = s/m^(1/3) or dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Roughness coefficient [s/m^(1/3) or dimensionless]. Returns float for scalar inputs.
    """
    (q, a, rh, s), is_scalar = coerce_inputs(discharge, area, hydraulic_radius, slope)
    k = _get_manning_k(system)
    out = _core.manning_n(q, a, rh, s, k)
    return format_output(out, is_scalar)
manning_roughness = manning_n

def manning_s0(discharge: FloatOrArray, area: FloatOrArray, hydraulic_radius: FloatOrArray, roughness: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes manning s0.
    Units (Default SI): discharge [m^3/s], area [m^2], hydraulic_radius [m], roughness [s/m^(1/3)] -> returns [m/m]

    Formula:
    S_0 = ((Q * n) / (k * A * R_h^(2/3)))^2

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - area : Cross-sectional flow area A [unit = m^2]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - roughness : Manning roughness coefficient n [unit = s/m^(1/3)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    roughness : FloatOrArray
        Manning roughness coefficient n [s/m^(1/3)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (q, a, rh, n_val), is_scalar = coerce_inputs(discharge, area, hydraulic_radius, roughness)
    k = _get_manning_k(system)
    out = _core.manning_s0(q, a, rh, n_val, k)
    return format_output(out, is_scalar)
manning_slope = manning_s0

def manning_rh(discharge: FloatOrArray, area: FloatOrArray, slope: FloatOrArray, roughness: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes manning rh.
    Units (Default SI): discharge [m^3/s], area [m^2], slope [m/m (decimal)], roughness [s/m^(1/3)] -> returns [standard SI units]

    Formula:
    R_h = ((Q * n) / (k * A * S_0^(1/2)))^(3/2)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - area : Cross-sectional flow area A [unit = m^2]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - roughness : Manning roughness coefficient n [unit = s/m^(1/3)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    roughness : FloatOrArray
        Manning roughness coefficient n [s/m^(1/3)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, a, s, n_val), is_scalar = coerce_inputs(discharge, area, slope, roughness)
    k = _get_manning_k(system)
    out = _core.manning_rh(q, a, s, n_val, k)
    return format_output(out, is_scalar)
manning_hydraulic_radius = manning_rh

def manning_a(discharge: FloatOrArray, hydraulic_radius: FloatOrArray, slope: FloatOrArray, roughness: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes manning a.
    Units (Default SI): discharge [m^3/s], hydraulic_radius [m], slope [m/m (decimal)], roughness [s/m^(1/3)] -> returns [km^2 if 'km' in fn else 'm^2']

    Formula:
    A = (Q * n) / (k * R_h^(2/3) * S_0^(1/2))

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - roughness : Manning roughness coefficient n [unit = s/m^(1/3)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Area [unit = km^2 if 'km' in fn else 'm^2']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    roughness : FloatOrArray
        Manning roughness coefficient n [s/m^(1/3)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Area [km^2 if 'km' in fn else 'm^2']. Returns float for scalar inputs.
    """
    (q, rh, s, n_val), is_scalar = coerce_inputs(discharge, hydraulic_radius, slope, roughness)
    k = _get_manning_k(system)
    out = _core.manning_a(q, rh, s, n_val, k)
    return format_output(out, is_scalar)
manning_area = manning_a
strickler_v = strickler_velocity

def strickler_kst(velocity: FloatOrArray, hydraulic_radius: FloatOrArray, slope: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes strickler kst.
    Units (Default SI): velocity [m/s], hydraulic_radius [m], slope [m/m (decimal)] -> returns [standard SI units]

    Formula:
    k_st = V / (R_h^(2/3) * S_0^(1/2))

    Where (Default SI Units):
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (v, rh, s), is_scalar = coerce_inputs(velocity, hydraulic_radius, slope)
    out = _core.strickler_kst(v, rh, s)
    return format_output(out, is_scalar)
strickler_roughness = strickler_kst

def strickler_s0(velocity: FloatOrArray, k_st: FloatOrArray, hydraulic_radius: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes strickler s0.
    Units (Default SI): velocity [m/s], k_st [m^(1/3)/s], hydraulic_radius [m] -> returns [m/m]

    Formula:
    S_0 = (V / (k_st * R_h^(2/3)))^2

    Where (Default SI Units):
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - k_st : Strickler roughness coefficient k_st = 1 / n [unit = m^(1/3)/s]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    k_st : FloatOrArray
        Strickler roughness coefficient k_st = 1 / n [m^(1/3)/s].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (v, kst, rh), is_scalar = coerce_inputs(velocity, k_st, hydraulic_radius)
    out = _core.strickler_s0(v, kst, rh)
    return format_output(out, is_scalar)
strickler_slope = strickler_s0
chezy_v = chezy_velocity

def chezy_c(velocity: FloatOrArray, hydraulic_radius: FloatOrArray, slope: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes chezy c.
    Units (Default SI): velocity [m/s], hydraulic_radius [m], slope [m/m (decimal)] -> returns [dimensionless]

    Formula:
    C = V / sqrt(R_h * S_0)

    Where (Default SI Units):
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - Output : Runoff / discharge coefficient [unit = dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].

    Returns
    -------
    float | np.ndarray
        Runoff / discharge coefficient [dimensionless]. Returns float for scalar inputs.
    """
    (v, rh, s), is_scalar = coerce_inputs(velocity, hydraulic_radius, slope)
    out = _core.chezy_c(v, rh, s)
    return format_output(out, is_scalar)
chezy_coefficient = chezy_c

def chezy_s0(velocity: FloatOrArray, chezy_c: FloatOrArray, hydraulic_radius: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes chezy s0.
    Units (Default SI): velocity [m/s], chezy_c [m^(1/2)/s], hydraulic_radius [m] -> returns [m/m]

    Formula:
    S_0 = V^2 / (C^2 * R_h)

    Where (Default SI Units):
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - chezy_c : Chézy resistance coefficient C [unit = m^(1/2)/s]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    chezy_c : FloatOrArray
        Chézy resistance coefficient C [m^(1/2)/s].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (v, c_val, rh), is_scalar = coerce_inputs(velocity, chezy_c, hydraulic_radius)
    out = _core.chezy_s0(v, c_val, rh)
    return format_output(out, is_scalar)
chezy_slope = chezy_s0

def chezy_rh(velocity: FloatOrArray, chezy_c: FloatOrArray, slope: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Chézy hydraulic radius R_h = V^2 / (C^2 * S_0)
    Units (Default SI): velocity [m/s], chezy_c [m^(1/2)/s], slope [m/m (decimal)] -> returns [standard SI units]

    Formula:
    Inversion: Chézy hydraulic radius R_h = V^2 / (C^2 * S_0)

    Where (Default SI Units):
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - chezy_c : Chézy resistance coefficient C [unit = m^(1/2)/s]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    chezy_c : FloatOrArray
        Chézy resistance coefficient C [m^(1/2)/s].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (v, c_val, s), is_scalar = coerce_inputs(velocity, chezy_c, slope)
    out = _core.chezy_rh(v, c_val, s)
    return format_output(out, is_scalar)
chezy_hydraulic_radius = chezy_rh

def froude_fr(velocity: FloatOrArray, hydraulic_depth: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes froude fr.
    Units (Default SI): velocity [m/s], hydraulic_depth [m] -> returns [standard SI units]

    Formula:
    Fr = (Q / A) / sqrt(g * (A / T))

    Where (Default SI Units):
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - hydraulic_depth : Flow depth [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    hydraulic_depth : FloatOrArray
        hydraulic_depth [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (v, dh), is_scalar = coerce_inputs(velocity, hydraulic_depth)
    g = _get_gravity(system)
    return format_output(v / np.sqrt(g * dh), is_scalar)

def froude_v(fr: FloatOrArray, hydraulic_depth: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes froude v.
    Units (Default SI): fr [SI units], hydraulic_depth [m] -> returns [m/s]

    Formula:
    V = Fr * sqrt(g * D_h)

    Where (Default SI Units):
    - fr : Input parameter [unit = SI units]
    - hydraulic_depth : Flow depth [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    fr : FloatOrArray
        fr [SI units].
    hydraulic_depth : FloatOrArray
        hydraulic_depth [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (f_val, dh), is_scalar = coerce_inputs(fr, hydraulic_depth)
    g = _get_gravity(system)
    out = _core.froude_v(f_val, dh, g)
    return format_output(out, is_scalar)
froude_velocity = froude_v

def froude_dh(fr: FloatOrArray, velocity: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Hydraulic depth from Froude number D_h = V^2 / (g * Fr^2)
    Units (Default SI): fr [SI units], velocity [m/s] -> returns [standard SI units]

    Formula:
    Inversion: Hydraulic depth from Froude number D_h = V^2 / (g * Fr^2)

    Where (Default SI Units):
    - fr : Input parameter [unit = SI units]
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    fr : FloatOrArray
        fr [SI units].
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (f_val, v), is_scalar = coerce_inputs(fr, velocity)
    g = _get_gravity(system)
    out = _core.froude_dh(f_val, v, g)
    return format_output(out, is_scalar)
froude_hydraulic_depth = froude_dh

def specific_energy_e(depth: FloatOrArray, velocity: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes specific energy e.
    Units (Default SI): depth [m], velocity [m/s] -> returns [standard SI units]

    Formula:
    E = y + Q^2 / (2 * g * A^2)

    Where (Default SI Units):
    - depth : Water flow depth y [unit = m]
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    depth : FloatOrArray
        Water flow depth y [m].
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (y, v), is_scalar = coerce_inputs(depth, velocity)
    g = _get_gravity(system)
    return format_output(y + v * v / (2.0 * g), is_scalar)

def specific_energy_v(specific_energy: FloatOrArray, depth: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes specific energy v.
    Units (Default SI): specific_energy [SI units], depth [m] -> returns [m/s]

    Formula:
    V = sqrt(2 * g * (E - y))

    Where (Default SI Units):
    - specific_energy : Input parameter [unit = SI units]
    - depth : Water flow depth y [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    specific_energy : FloatOrArray
        specific_energy [SI units].
    depth : FloatOrArray
        Water flow depth y [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (e, y), is_scalar = coerce_inputs(specific_energy, depth)
    g = _get_gravity(system)
    out = _core.specific_energy_v(e, y, g)
    return format_output(out, is_scalar)
specific_energy_velocity = specific_energy_v
hydraulic_jump_y2 = belanger_conjugate_depth

def hydraulic_jump_fr1(depth_1: FloatOrArray, depth_2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes hydraulic jump fr1.
    Units (Default SI): depth_1 [m], depth_2 [m] -> returns [standard SI units]

    Formula:
    Fr_1 = sqrt(0.125 * ((2 * y_2 / y_1 + 1)^2 - 1))

    Where (Default SI Units):
    - depth_1 : Supercritical initial flow depth y_1 [unit = m]
    - depth_2 : Subcritical sequent flow depth y_2 [unit = m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    depth_1 : FloatOrArray
        Supercritical initial flow depth y_1 [m].
    depth_2 : FloatOrArray
        Subcritical sequent flow depth y_2 [m].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (y1, y2), is_scalar = coerce_inputs(depth_1, depth_2)
    out = _core.hydraulic_jump_fr1(y1, y2)
    return format_output(out, is_scalar)
hydraulic_jump_froude_1 = hydraulic_jump_fr1

def hydraulic_jump_y1(depth_2: FloatOrArray, froude_1: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes hydraulic jump y1.
    Units (Default SI): depth_2 [m], froude_1 [dimensionless] -> returns [standard SI units]

    Formula:
    y_1 = (y_2 / 2) * (sqrt(1 + 8 * Fr_2^2) - 1)

    Where (Default SI Units):
    - depth_2 : Subcritical sequent flow depth y_2 [unit = m]
    - froude_1 : Supercritical inflow Froude number Fr_1 [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    depth_2 : FloatOrArray
        Subcritical sequent flow depth y_2 [m].
    froude_1 : FloatOrArray
        Supercritical inflow Froude number Fr_1 [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (y2, fr), is_scalar = coerce_inputs(depth_2, froude_1)
    out = _core.hydraulic_jump_y1(y2, fr)
    return format_output(out, is_scalar)
hydraulic_jump_depth_1 = hydraulic_jump_y1

def critical_depth_rect_yc(discharge: FloatOrArray, bottom_width: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Critical depth rectangular channel: y_c = ((Q/b)^2 / g)^(1/3)
    Units (Default SI): discharge [m^3/s], bottom_width [m] -> returns [standard SI units]

    Formula:
    Critical depth rectangular channel: y_c = ((Q/b)^2 / g)^(1/3)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - bottom_width : Channel base width b [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    bottom_width : FloatOrArray
        Channel base width b [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, b), is_scalar = coerce_inputs(discharge, bottom_width)
    g = _get_gravity(system)
    q_unit = q / b
    out = _core.critical_depth_rectangular(q_unit, g)
    return format_output(out, is_scalar)

def critical_depth_rect_q(critical_depth: FloatOrArray, bottom_width: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Rectangular critical discharge Q = b * sqrt(g * y_c^3)
    Units (Default SI): critical_depth [m], bottom_width [m] -> returns [m^3/s]

    Formula:
    Inversion: Rectangular critical discharge Q = b * sqrt(g * y_c^3)

    Where (Default SI Units):
    - critical_depth : Flow depth [unit = m]
    - bottom_width : Channel base width b [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    critical_depth : FloatOrArray
        critical_depth [SI units].
    bottom_width : FloatOrArray
        Channel base width b [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (yc, b), is_scalar = coerce_inputs(critical_depth, bottom_width)
    g = _get_gravity(system)
    out = _core.critical_depth_rect_q(yc, b, g)
    return format_output(out, is_scalar)
critical_discharge_rectangular = critical_depth_rect_q
critical_depth_tri_yc = critical_depth_triangular

def critical_depth_tri_q(critical_depth: FloatOrArray, side_slope: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Triangular critical discharge Q = sqrt(0.5 * g * z^2 * y_c^5)
    Units (Default SI): critical_depth [m], side_slope [dimensionless] -> returns [m^3/s]

    Formula:
    Inversion: Triangular critical discharge Q = sqrt(0.5 * g * z^2 * y_c^5)

    Where (Default SI Units):
    - critical_depth : Flow depth [unit = m]
    - side_slope : Side slope ratio m (1V : mH) [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    critical_depth : FloatOrArray
        critical_depth [SI units].
    side_slope : FloatOrArray
    Side slope ratio m (1V : mH) [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (yc, z), is_scalar = coerce_inputs(critical_depth, side_slope)
    g = _get_gravity(system)
    out = _core.critical_depth_tri_q(yc, z, g)
    return format_output(out, is_scalar)
critical_discharge_triangular = critical_depth_tri_q
critical_velocity_vc = critical_velocity

def critical_velocity_dh(critical_velocity: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Critical hydraulic depth D_h = V_c^2 / g
    Units (Default SI): critical_velocity [m/s] -> returns [m/s]

    Formula:
    Inversion: Critical hydraulic depth D_h = V_c^2 / g

    Where (Default SI Units):
    - critical_velocity : Flow velocity [unit = m/s]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    critical_velocity : FloatOrArray
        critical_velocity [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (vc,), is_scalar = coerce_inputs(critical_velocity)
    g = _get_gravity(system)
    out = _core.critical_velocity_dh(vc, g)
    return format_output(out, is_scalar)
critical_hydraulic_depth = critical_velocity_dh
critical_slope_sc = critical_slope

def critical_slope_n(critical_slope: FloatOrArray, discharge: FloatOrArray, bottom_width: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Manning n corresponding to critical slope S_c for rectangular channel
    Units (Default SI): critical_slope [m/m], discharge [m^3/s], bottom_width [m] -> returns [s/m^(1/3) or dimensionless]

    Formula:
    system : {'si', 'us'}, default='si'

    Where (Default SI Units):
    - critical_slope : Longitudinal bed slope / gradient [unit = m/m]
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - bottom_width : Channel base width b [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Roughness coefficient [unit = s/m^(1/3) or dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    critical_slope : FloatOrArray
        critical_slope [SI units].
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    bottom_width : FloatOrArray
        Channel base width b [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Roughness coefficient [s/m^(1/3) or dimensionless]. Returns float for scalar inputs.
    """
    (sc, q, b), is_scalar = coerce_inputs(critical_slope, discharge, bottom_width)
    g = _get_gravity(system)
    k = _get_manning_k(system)
    out = _core.critical_slope_n(sc, q, b, g, k)
    return format_output(out, is_scalar)
critical_slope_roughness = critical_slope_n
darcy_weisbach_hf = darcy_weisbach
darcy_weisbach_head_loss = darcy_weisbach_hf

def darcy_weisbach_f(head_loss: FloatOrArray, length: FloatOrArray, diameter: FloatOrArray, velocity: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes darcy weisbach f.
    Units (Default SI): head_loss [m], length [m], diameter [m], velocity [m/s] -> returns [standard SI units]

    Formula:
    f = h_f * (2 * g * D) / (L * V^2)

    Where (Default SI Units):
    - head_loss : Energy friction head loss h_f [unit = m]
    - length : Reach / conduit / flow path length L [unit = m]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    head_loss : FloatOrArray
        Energy friction head loss h_f [m].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (hf, l, d, v), is_scalar = coerce_inputs(head_loss, length, diameter, velocity)
    g = _get_gravity(system)
    out = _core.darcy_weisbach_f(hf, l, d, v, g)
    return format_output(out, is_scalar)
darcy_weisbach_friction_factor = darcy_weisbach_f

def darcy_weisbach_d(head_loss: FloatOrArray, friction_factor: FloatOrArray, length: FloatOrArray, velocity: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes darcy weisbach d.
    Units (Default SI): head_loss [m], friction_factor [dimensionless], length [m], velocity [m/s] -> returns [mm if 'd50' in fn else 'm']

    Formula:
    D = f * (L / h_f) * (V^2 / (2 * g))

    Where (Default SI Units):
    - head_loss : Energy friction head loss h_f [unit = m]
    - friction_factor : Darcy-Weisbach friction factor f [unit = dimensionless]
    - length : Reach / conduit / flow path length L [unit = m]
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Diameter [unit = mm if 'd50' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    head_loss : FloatOrArray
        Energy friction head loss h_f [m].
    friction_factor : FloatOrArray
        Darcy-Weisbach friction factor f [dimensionless].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Diameter [mm if 'd50' in fn else 'm']. Returns float for scalar inputs.
    """
    (hf, f, l, v), is_scalar = coerce_inputs(head_loss, friction_factor, length, velocity)
    g = _get_gravity(system)
    out = _core.darcy_weisbach_d(hf, f, l, v, g)
    return format_output(out, is_scalar)
darcy_weisbach_diameter = darcy_weisbach_d

def darcy_weisbach_l(head_loss: FloatOrArray, friction_factor: FloatOrArray, diameter: FloatOrArray, velocity: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Pipe length L = (2 * g * D * h_f) / (f * V^2)
    Units (Default SI): head_loss [m], friction_factor [dimensionless], diameter [m], velocity [m/s] -> returns [km if 'km' in fn else 'm']

    Formula:
    Inversion: Pipe length L = (2 * g * D * h_f) / (f * V^2)

    Where (Default SI Units):
    - head_loss : Energy friction head loss h_f [unit = m]
    - friction_factor : Darcy-Weisbach friction factor f [unit = dimensionless]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    head_loss : FloatOrArray
        Energy friction head loss h_f [m].
    friction_factor : FloatOrArray
        Darcy-Weisbach friction factor f [dimensionless].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (hf, f, d, v), is_scalar = coerce_inputs(head_loss, friction_factor, diameter, velocity)
    g = _get_gravity(system)
    out = _core.darcy_weisbach_l(hf, f, d, v, g)
    return format_output(out, is_scalar)
darcy_weisbach_length = darcy_weisbach_l

def darcy_weisbach_v(head_loss: FloatOrArray, friction_factor: FloatOrArray, length: FloatOrArray, diameter: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes darcy weisbach v.
    Units (Default SI): head_loss [m], friction_factor [dimensionless], length [m], diameter [m] -> returns [m/s]

    Formula:
    V = sqrt((2 * g * D * h_f) / (f * L))

    Where (Default SI Units):
    - head_loss : Energy friction head loss h_f [unit = m]
    - friction_factor : Darcy-Weisbach friction factor f [unit = dimensionless]
    - length : Reach / conduit / flow path length L [unit = m]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    head_loss : FloatOrArray
        Energy friction head loss h_f [m].
    friction_factor : FloatOrArray
        Darcy-Weisbach friction factor f [dimensionless].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (hf, f, l, d), is_scalar = coerce_inputs(head_loss, friction_factor, length, diameter)
    g = _get_gravity(system)
    out = _core.darcy_weisbach_v(hf, f, l, d, g)
    return format_output(out, is_scalar)
darcy_weisbach_velocity = darcy_weisbach_v

def darcy_weisbach_q(head_loss: FloatOrArray, friction_factor: FloatOrArray, length: FloatOrArray, diameter: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes darcy weisbach q.
    Units (Default SI): head_loss [m], friction_factor [dimensionless], length [m], diameter [m] -> returns [m^3/s]

    Formula:
    Q = (pi * D^2 / 4) * sqrt((2 * g * D * h_f) / (f * L))

    Where (Default SI Units):
    - head_loss : Energy friction head loss h_f [unit = m]
    - friction_factor : Darcy-Weisbach friction factor f [unit = dimensionless]
    - length : Reach / conduit / flow path length L [unit = m]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    head_loss : FloatOrArray
        Energy friction head loss h_f [m].
    friction_factor : FloatOrArray
        Darcy-Weisbach friction factor f [dimensionless].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (hf, f, l, d), is_scalar = coerce_inputs(head_loss, friction_factor, length, diameter)
    g = _get_gravity(system)
    out = _core.darcy_weisbach_q(hf, f, l, d, g)
    return format_output(out, is_scalar)
darcy_weisbach_discharge = darcy_weisbach_q

def hazen_williams_hf(roughness_c: FloatOrArray, diameter: FloatOrArray, length: FloatOrArray, discharge: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes hazen williams hf.
    Units (Default SI): roughness_c [dimensionless (typically 80 - 150)], diameter [m], length [m], discharge [m^3/s] -> returns [m]

    Formula:
    h_f = (k_hw * L * Q^1.852) / (C^1.852 * D^4.87)

    Where (Default SI Units):
    - roughness_c : Hazen-Williams roughness coefficient C [unit = dimensionless (typically 80 - 150)]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - length : Reach / conduit / flow path length L [unit = m]
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    roughness_c : FloatOrArray
        Hazen-Williams roughness coefficient C [dimensionless (typically 80 - 150)].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (c, d, l, q), is_scalar = coerce_inputs(roughness_c, diameter, length, discharge)
    k_hw = HW_K_US if system.lower() == 'us' else HW_K_SI
    out = _core.hazen_williams(l, q, c, d, k_hw)
    return format_output(out, is_scalar)
hazen_williams_head_loss = hazen_williams_hf

def hazen_williams_q(head_loss: FloatOrArray, roughness_c: FloatOrArray, diameter: FloatOrArray, length: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes hazen williams q.
    Units (Default SI): head_loss [m], roughness_c [dimensionless (typically 80 - 150)], diameter [m], length [m] -> returns [m^3/s]

    Formula:
    Q = ((h_f * C^1.852 * D^4.87) / (k_hw * L))^(1 / 1.852)

    Where (Default SI Units):
    - head_loss : Energy friction head loss h_f [unit = m]
    - roughness_c : Hazen-Williams roughness coefficient C [unit = dimensionless (typically 80 - 150)]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - length : Reach / conduit / flow path length L [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    head_loss : FloatOrArray
        Energy friction head loss h_f [m].
    roughness_c : FloatOrArray
        Hazen-Williams roughness coefficient C [dimensionless (typically 80 - 150)].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (hf, c, d, l), is_scalar = coerce_inputs(head_loss, roughness_c, diameter, length)
    k_l = HW_K_US if system.lower() == 'us' else HW_K_SI
    out = _core.hazen_williams_q(hf, c, d, l, k_l)
    return format_output(out, is_scalar)
hazen_williams_discharge = hazen_williams_q

def hazen_williams_d(head_loss: FloatOrArray, discharge: FloatOrArray, roughness_c: FloatOrArray, length: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes hazen williams d.
    Units (Default SI): head_loss [m], discharge [m^3/s], roughness_c [dimensionless (typically 80 - 150)], length [m] -> returns [mm if 'd50' in fn else 'm']

    Formula:
    D = ((k_hw * L * Q^1.852) / (h_f * C^1.852))^(1 / 4.87)

    Where (Default SI Units):
    - head_loss : Energy friction head loss h_f [unit = m]
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - roughness_c : Hazen-Williams roughness coefficient C [unit = dimensionless (typically 80 - 150)]
    - length : Reach / conduit / flow path length L [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Diameter [unit = mm if 'd50' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    head_loss : FloatOrArray
        Energy friction head loss h_f [m].
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    roughness_c : FloatOrArray
        Hazen-Williams roughness coefficient C [dimensionless (typically 80 - 150)].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Diameter [mm if 'd50' in fn else 'm']. Returns float for scalar inputs.
    """
    (hf, q, c, l), is_scalar = coerce_inputs(head_loss, discharge, roughness_c, length)
    k_l = HW_K_US if system.lower() == 'us' else HW_K_SI
    out = _core.hazen_williams_d(hf, q, c, l, k_l)
    return format_output(out, is_scalar)
hazen_williams_diameter = hazen_williams_d

def hazen_williams_l(head_loss: FloatOrArray, discharge: FloatOrArray, roughness_c: FloatOrArray, diameter: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Pipe length L = (h_f * C^1.852 * D^4.8704) / (k_L * Q^1.852)
    Units (Default SI): head_loss [m], discharge [m^3/s], roughness_c [dimensionless (typically 80 - 150)], diameter [m] -> returns [km if 'km' in fn else 'm']

    Formula:
    Inversion: Pipe length L = (h_f * C^1.852 * D^4.8704) / (k_L * Q^1.852)

    Where (Default SI Units):
    - head_loss : Energy friction head loss h_f [unit = m]
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - roughness_c : Hazen-Williams roughness coefficient C [unit = dimensionless (typically 80 - 150)]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    head_loss : FloatOrArray
        Energy friction head loss h_f [m].
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    roughness_c : FloatOrArray
        Hazen-Williams roughness coefficient C [dimensionless (typically 80 - 150)].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (hf, q, c, d), is_scalar = coerce_inputs(head_loss, discharge, roughness_c, diameter)
    k_l = HW_K_US if system.lower() == 'us' else HW_K_SI
    out = _core.hazen_williams_l(hf, q, c, d, k_l)
    return format_output(out, is_scalar)
hazen_williams_length = hazen_williams_l

def hazen_williams_c(head_loss: FloatOrArray, discharge: FloatOrArray, diameter: FloatOrArray, length: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Hazen-Williams C = ((k_L * L * Q^1.852) / (h_f * D^4.8704))^(1 / 1.852)
    Units (Default SI): head_loss [m], discharge [m^3/s], diameter [m], length [m] -> returns [dimensionless]

    Formula:
    Inversion: Hazen-Williams C = ((k_L * L * Q^1.852) / (h_f * D^4.8704))^(1 / 1.852)

    Where (Default SI Units):
    - head_loss : Energy friction head loss h_f [unit = m]
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - length : Reach / conduit / flow path length L [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Runoff / discharge coefficient [unit = dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    head_loss : FloatOrArray
        Energy friction head loss h_f [m].
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Runoff / discharge coefficient [dimensionless]. Returns float for scalar inputs.
    """
    (hf, q, d, l), is_scalar = coerce_inputs(head_loss, discharge, diameter, length)
    k_l = HW_K_US if system.lower() == 'us' else HW_K_SI
    out = _core.hazen_williams_c(hf, q, d, l, k_l)
    return format_output(out, is_scalar)
hazen_williams_roughness = hazen_williams_c
hazen_williams_v = hazen_williams_velocity

def hazen_williams_s(velocity: FloatOrArray, roughness_c: FloatOrArray, hydraulic_radius: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Hydraulic slope S = (V / (k_v * C * R_h^0.63))^(1 / 0.54)
    Units (Default SI): velocity [m/s], roughness_c [dimensionless (typically 80 - 150)], hydraulic_radius [m] -> returns [m/m]

    Formula:
    Inversion: Hydraulic slope S = (V / (k_v * C * R_h^0.63))^(1 / 0.54)

    Where (Default SI Units):
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - roughness_c : Hazen-Williams roughness coefficient C [unit = dimensionless (typically 80 - 150)]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    roughness_c : FloatOrArray
        Hazen-Williams roughness coefficient C [dimensionless (typically 80 - 150)].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (v, c, rh), is_scalar = coerce_inputs(velocity, roughness_c, hydraulic_radius)
    k_v = HW_V_K_US if system.lower() == 'us' else HW_V_K_SI
    out = _core.hazen_williams_s(v, c, rh, k_v)
    return format_output(out, is_scalar)
hazen_williams_slope = hazen_williams_s
reynolds_re = reynolds_number

def reynolds_v(reynolds: FloatOrArray, diameter: FloatOrArray, kinematic_viscosity: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes reynolds v.
    Units (Default SI): reynolds [dimensionless], diameter [m], kinematic_viscosity [SI units] -> returns [m/s]

    Formula:
    V = (Re * nu) / D

    Where (Default SI Units):
    - reynolds : Reynolds number Re = V * D / nu [unit = dimensionless]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - kinematic_viscosity : Input parameter [unit = SI units]
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    reynolds : FloatOrArray
        Reynolds number Re = V * D / nu [dimensionless].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    kinematic_viscosity : FloatOrArray
        kinematic_viscosity [SI units].

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (r, d, nu), is_scalar = coerce_inputs(reynolds, diameter, kinematic_viscosity)
    out = _core.reynolds_v(r, d, nu)
    return format_output(out, is_scalar)
reynolds_velocity = reynolds_v

def reynolds_d(reynolds: FloatOrArray, velocity: FloatOrArray, kinematic_viscosity: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Diameter D = (Re * nu) / V
    Units (Default SI): reynolds [dimensionless], velocity [m/s], kinematic_viscosity [SI units] -> returns [mm if 'd50' in fn else 'm']

    Formula:
    Inversion: Diameter D = (Re * nu) / V

    Where (Default SI Units):
    - reynolds : Reynolds number Re = V * D / nu [unit = dimensionless]
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - kinematic_viscosity : Input parameter [unit = SI units]
    - Output : Diameter [unit = mm if 'd50' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    reynolds : FloatOrArray
        Reynolds number Re = V * D / nu [dimensionless].
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    kinematic_viscosity : FloatOrArray
        kinematic_viscosity [SI units].

    Returns
    -------
    float | np.ndarray
        Diameter [mm if 'd50' in fn else 'm']. Returns float for scalar inputs.
    """
    (r, v, nu), is_scalar = coerce_inputs(reynolds, velocity, kinematic_viscosity)
    out = _core.reynolds_d(r, v, nu)
    return format_output(out, is_scalar)
reynolds_diameter = reynolds_d
minor_loss_hm = minor_loss
minor_loss_head = minor_loss_hm

def minor_loss_kl(head_loss: FloatOrArray, velocity: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes minor loss kl.
    Units (Default SI): head_loss [m], velocity [m/s] -> returns [standard SI units]

    Formula:
    K_L = 2 * g * h_m / V^2

    Where (Default SI Units):
    - head_loss : Energy friction head loss h_f [unit = m]
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    head_loss : FloatOrArray
        Energy friction head loss h_f [m].
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (hm, v), is_scalar = coerce_inputs(head_loss, velocity)
    g = _get_gravity(system)
    out = _core.minor_loss_kl(hm, v, g)
    return format_output(out, is_scalar)
minor_loss_coeff = minor_loss_kl

def minor_loss_v(head_loss: FloatOrArray, loss_coeff: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Flow velocity V = sqrt((2 * g * h_m) / K_L)
    Units (Default SI): head_loss [m], loss_coeff [dimensionless] -> returns [m/s]

    Formula:
    Inversion: Flow velocity V = sqrt((2 * g * h_m) / K_L)

    Where (Default SI Units):
    - head_loss : Energy friction head loss h_f [unit = m]
    - loss_coeff : Input parameter [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    head_loss : FloatOrArray
        Energy friction head loss h_f [m].
    loss_coeff : FloatOrArray
        loss_coeff [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (hm, kl), is_scalar = coerce_inputs(head_loss, loss_coeff)
    g = _get_gravity(system)
    out = _core.minor_loss_v(hm, kl, g)
    return format_output(out, is_scalar)
minor_loss_velocity = minor_loss_v

def joukowsky_dp(celerity: FloatOrArray, delta_velocity: FloatOrArray, density: FloatOrArray=1000.0) -> Union[float, np.ndarray]:
    """
    Joukowsky water hammer pressure rise: Delta_P = rho * a * Delta_V
    Units (Default SI): celerity [SI units], delta_velocity [m/s], density [kg/m^3 (~1000.0)] -> returns [standard SI units]

    Formula:
    Joukowsky water hammer pressure rise: Delta_P = rho * a * Delta_V

    Where (Default SI Units):
    - celerity : Input parameter [unit = SI units]
    - delta_velocity : Flow velocity [unit = m/s]
    - density : Fluid mass density rho [unit = kg/m^3 (~1000.0)]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    celerity : FloatOrArray
        celerity [SI units].
    delta_velocity : FloatOrArray
        delta_velocity [SI units].
    density : FloatOrArray
        Fluid mass density rho [kg/m^3 (~1000.0)].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (a, dv, rho), is_scalar = coerce_inputs(celerity, delta_velocity, density)
    return format_output(rho * a * dv, is_scalar)
joukowsky_pressure = joukowsky_dp

def joukowsky_dv(delta_pressure: FloatOrArray, celerity: FloatOrArray, density: FloatOrArray=1000.0) -> Union[float, np.ndarray]:
    """
    Inversion: Velocity change delta_V = delta_P / (rho * a)
    Units (Default SI): delta_pressure [SI units], celerity [SI units], density [kg/m^3 (~1000.0)] -> returns [standard SI units]

    Formula:
    Inversion: Velocity change delta_V = delta_P / (rho * a)

    Where (Default SI Units):
    - delta_pressure : Input parameter [unit = SI units]
    - celerity : Input parameter [unit = SI units]
    - density : Fluid mass density rho [unit = kg/m^3 (~1000.0)]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    delta_pressure : FloatOrArray
        delta_pressure [SI units].
    celerity : FloatOrArray
        celerity [SI units].
    density : FloatOrArray
        Fluid mass density rho [kg/m^3 (~1000.0)].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (dp, a, rho), is_scalar = coerce_inputs(delta_pressure, celerity, density)
    out = _core.joukowsky_dv(dp, a, rho)
    return format_output(out, is_scalar)
joukowsky_delta_velocity = joukowsky_dv

def joukowsky_a(delta_pressure: FloatOrArray, delta_velocity: FloatOrArray, density: FloatOrArray=1000.0) -> Union[float, np.ndarray]:
    """
    Inversion: Acoustic wave speed a = delta_P / (rho * delta_V)
    Units (Default SI): delta_pressure [SI units], delta_velocity [m/s], density [kg/m^3 (~1000.0)] -> returns [km^2 if 'km' in fn else 'm^2']

    Formula:
    Inversion: Acoustic wave speed a = delta_P / (rho * delta_V)

    Where (Default SI Units):
    - delta_pressure : Input parameter [unit = SI units]
    - delta_velocity : Flow velocity [unit = m/s]
    - density : Fluid mass density rho [unit = kg/m^3 (~1000.0)]
    - Output : Area [unit = km^2 if 'km' in fn else 'm^2']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    delta_pressure : FloatOrArray
        delta_pressure [SI units].
    delta_velocity : FloatOrArray
        delta_velocity [SI units].
    density : FloatOrArray
        Fluid mass density rho [kg/m^3 (~1000.0)].

    Returns
    -------
    float | np.ndarray
        Area [km^2 if 'km' in fn else 'm^2']. Returns float for scalar inputs.
    """
    (dp, dv, rho), is_scalar = coerce_inputs(delta_pressure, delta_velocity, density)
    out = _core.joukowsky_a(dp, dv, rho)
    return format_output(out, is_scalar)
joukowsky_celerity = joukowsky_a
critical_closure_tc = critical_closure_time

def critical_closure_l(critical_time: FloatOrArray, celerity: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Pipe reach length L = (T_c * a) / 2
    Units (Default SI): critical_time [hours], celerity [SI units] -> returns [km if 'km' in fn else 'm']

    Formula:
    Inversion: Pipe reach length L = (T_c * a) / 2

    Where (Default SI Units):
    - critical_time : Time parameter [unit = hours]
    - celerity : Input parameter [unit = SI units]
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    critical_time : FloatOrArray
        critical_time [SI units].
    celerity : FloatOrArray
        celerity [SI units].

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (tc, a), is_scalar = coerce_inputs(critical_time, celerity)
    out = _core.critical_closure_l(tc, a)
    return format_output(out, is_scalar)
critical_closure_length = critical_closure_l

def critical_closure_a(critical_time: FloatOrArray, length: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Wave speed a = (2 * L) / T_c
    Units (Default SI): critical_time [hours], length [m] -> returns [km^2 if 'km' in fn else 'm^2']

    Formula:
    Inversion: Wave speed a = (2 * L) / T_c

    Where (Default SI Units):
    - critical_time : Time parameter [unit = hours]
    - length : Reach / conduit / flow path length L [unit = m]
    - Output : Area [unit = km^2 if 'km' in fn else 'm^2']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    critical_time : FloatOrArray
        critical_time [SI units].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].

    Returns
    -------
    float | np.ndarray
        Area [km^2 if 'km' in fn else 'm^2']. Returns float for scalar inputs.
    """
    (tc, l), is_scalar = coerce_inputs(critical_time, length)
    out = _core.critical_closure_a(tc, l)
    return format_output(out, is_scalar)
critical_closure_celerity = critical_closure_a
equivalent_pipe_le = equivalent_pipe_length

def equivalent_pipe_kl(length_equiv: FloatOrArray, diameter: FloatOrArray, friction_factor: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Minor loss coefficient K_L = (f * L_e) / D
    Units (Default SI): length_equiv [m], diameter [m], friction_factor [dimensionless] -> returns [standard SI units]

    Formula:
    Inversion: Minor loss coefficient K_L = (f * L_e) / D

    Where (Default SI Units):
    - length_equiv : Length [unit = m]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - friction_factor : Darcy-Weisbach friction factor f [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length_equiv : FloatOrArray
        length_equiv [SI units].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].
    friction_factor : FloatOrArray
        Darcy-Weisbach friction factor f [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (le, d, f), is_scalar = coerce_inputs(length_equiv, diameter, friction_factor)
    out = _core.equivalent_pipe_kl(le, d, f)
    return format_output(out, is_scalar)
equivalent_pipe_loss_coeff = equivalent_pipe_kl

def equivalent_pipe_f(length_equiv: FloatOrArray, loss_coeff: FloatOrArray, diameter: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Pipe friction factor f = (K_L * D) / L_e
    Units (Default SI): length_equiv [m], loss_coeff [dimensionless], diameter [m] -> returns [standard SI units]

    Formula:
    Inversion: Pipe friction factor f = (K_L * D) / L_e

    Where (Default SI Units):
    - length_equiv : Length [unit = m]
    - loss_coeff : Input parameter [unit = dimensionless]
    - diameter : Internal conduit / pipe diameter D [unit = m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length_equiv : FloatOrArray
        length_equiv [SI units].
    loss_coeff : FloatOrArray
        loss_coeff [SI units].
    diameter : FloatOrArray
        Internal conduit / pipe diameter D [m].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (le, kl, d), is_scalar = coerce_inputs(length_equiv, loss_coeff, diameter)
    out = _core.equivalent_pipe_f(le, kl, d)
    return format_output(out, is_scalar)
equivalent_pipe_friction_factor = equivalent_pipe_f
water_power_pw = water_horsepower

def water_power_q(power_w: FloatOrArray, head: FloatOrArray, specific_weight: FloatOrArray=None, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes water power q.
    Units (Default SI): power_w [SI units], head [m], specific_weight [SI units] -> returns [m^3/s]

    Formula:
    Q = (P_w * k_pow) / (gamma * H)

    Where (Default SI Units):
    - power_w : Input parameter [unit = SI units]
    - head : Upstream / operating hydraulic head H [unit = m]
    - specific_weight : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    power_w : FloatOrArray
        power_w [SI units].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    specific_weight : FloatOrArray
        specific_weight [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    if specific_weight is None:
        specific_weight = 62.4 if system.lower() == 'us' else 9806.65
    (pw, h, gam), is_scalar = coerce_inputs(power_w, head, specific_weight)
    divisor = 550.0 if system.lower() == 'us' else 1000.0
    out = _core.water_power_q(pw, h, gam, divisor)
    return format_output(out, is_scalar)
water_power_discharge = water_power_q

def water_power_h(power_w: FloatOrArray, discharge: FloatOrArray, specific_weight: FloatOrArray=None, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Hydraulic head H = (P_w * divisor) / (gamma * Q)
    Units (Default SI): power_w [SI units], discharge [m^3/s], specific_weight [SI units] -> returns [m]

    Formula:
    Inversion: Hydraulic head H = (P_w * divisor) / (gamma * Q)

    Where (Default SI Units):
    - power_w : Input parameter [unit = SI units]
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - specific_weight : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    power_w : FloatOrArray
        power_w [SI units].
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    specific_weight : FloatOrArray
        specific_weight [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    if specific_weight is None:
        specific_weight = 62.4 if system.lower() == 'us' else 9806.65
    (pw, q, gam), is_scalar = coerce_inputs(power_w, discharge, specific_weight)
    divisor = 550.0 if system.lower() == 'us' else 1000.0
    out = _core.water_power_h(pw, q, gam, divisor)
    return format_output(out, is_scalar)
water_power_head = water_power_h
pump_power_pb = pump_brake_power

def pump_power_pw(brake_power: FloatOrArray, efficiency: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Water power delivered P_w = P_b * eta
    Units (Default SI): brake_power [SI units], efficiency [dimensionless decimal (0 - 1)] -> returns [standard SI units]

    Formula:
    Inversion: Water power delivered P_w = P_b * eta

    Where (Default SI Units):
    - brake_power : Input parameter [unit = SI units]
    - efficiency : Overall wire-to-water pump efficiency eta [unit = dimensionless decimal (0 - 1)]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    brake_power : FloatOrArray
        brake_power [SI units].
    efficiency : FloatOrArray
        Overall wire-to-water pump efficiency eta [dimensionless decimal (0 - 1)].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (pb, eff), is_scalar = coerce_inputs(brake_power, efficiency)
    out = _core.pump_power_pw(pb, eff)
    return format_output(out, is_scalar)
pump_water_power = pump_power_pw

def pump_power_eta(water_power: FloatOrArray, brake_power: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Pump mechanical efficiency eta = P_w / P_b
    Units (Default SI): water_power [SI units], brake_power [SI units] -> returns [standard SI units]

    Formula:
    Inversion: Pump mechanical efficiency eta = P_w / P_b

    Where (Default SI Units):
    - water_power : Input parameter [unit = SI units]
    - brake_power : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    water_power : FloatOrArray
        water_power [SI units].
    brake_power : FloatOrArray
        brake_power [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (pw, pb), is_scalar = coerce_inputs(water_power, brake_power)
    out = _core.pump_power_eta(pw, pb)
    return format_output(out, is_scalar)
pump_efficiency = pump_power_eta

def lacey_silt_factor(d50_mm: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes Lacey's silt factor f from median alluvial sediment grain size.
    Units (Default SI): d50_mm [mm] -> returns [standard SI units]

    Formula:
    f = 1.76 * sqrt(d_50)  [d_50 in mm]

    Where (Default SI Units):
    - d50_mm : Median sediment grain size d_50 [unit = mm]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    d50_mm : FloatOrArray
        Median sediment grain size d_50 [mm].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (d,), is_scalar = coerce_inputs(d50_mm)
    with np.errstate(all='ignore'):
        f = np.where(d <= 0, np.nan, 1.76 * np.sqrt(d))
    return format_output(f, is_scalar)

def lacey_d50(silt_factor: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for sediment grain size d_50 = (f / 1.76)^2 [mm].
    Units (Default SI): silt_factor [dimensionless] -> returns [mm if 'd50' in fn else 'm']

    Formula:
    Inversion: Solves for sediment grain size d_50 = (f / 1.76)^2 [mm].

    Where (Default SI Units):
    - silt_factor : Lacey's silt factor f [unit = dimensionless]
    - Output : Diameter [unit = mm if 'd50' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    silt_factor : FloatOrArray
        Lacey's silt factor f [dimensionless].

    Returns
    -------
    float | np.ndarray
        Diameter [mm if 'd50' in fn else 'm']. Returns float for scalar inputs.
    """
    (f,), is_scalar = coerce_inputs(silt_factor)
    with np.errstate(all='ignore'):
        d = np.where(f <= 0, np.nan, (f / 1.76) ** 2)
    return format_output(d, is_scalar)

def lacey_regime_velocity(discharge: FloatOrArray, silt_factor: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes Lacey's regime non-silting, non-scouring velocity V.
    Units (Default SI): discharge [m^3/s], silt_factor [dimensionless] -> returns [m/s]

    Formula:
    V = ((Q * f^2) / 140)^(1/6)  [Q in m^3/s, V in m/s]

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - silt_factor : Lacey's silt factor f [unit = dimensionless]
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    silt_factor : FloatOrArray
        Lacey's silt factor f [dimensionless].

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (q, f), is_scalar = coerce_inputs(discharge, silt_factor)
    with np.errstate(all='ignore'):
        v = np.where((q <= 0) | (f <= 0), np.nan, (q * f ** 2 / 140.0) ** (1.0 / 6.0))
    return format_output(v, is_scalar)

def lacey_velocity_discharge(velocity: FloatOrArray, silt_factor: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for regime discharge Q = (140 * V^6) / f^2.
    Units (Default SI): velocity [m/s], silt_factor [dimensionless] -> returns [m^3/s]

    Formula:
    Inversion: Solves for regime discharge Q = (140 * V^6) / f^2.

    Where (Default SI Units):
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - silt_factor : Lacey's silt factor f [unit = dimensionless]
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    silt_factor : FloatOrArray
        Lacey's silt factor f [dimensionless].

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (v, f), is_scalar = coerce_inputs(velocity, silt_factor)
    with np.errstate(all='ignore'):
        q = np.where((v <= 0) | (f <= 0), np.nan, 140.0 * v ** 6 / f ** 2)
    return format_output(q, is_scalar)

def lacey_wetted_perimeter(discharge: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes Lacey's regime wetted perimeter P = 4.75 * sqrt(Q) [m].
    Units (Default SI): discharge [m^3/s] -> returns [standard SI units]

    Formula:
    Computes Lacey's regime wetted perimeter P = 4.75 * sqrt(Q) [m].

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q,), is_scalar = coerce_inputs(discharge)
    with np.errstate(all='ignore'):
        p = np.where(q <= 0, np.nan, 4.75 * np.sqrt(q))
    return format_output(p, is_scalar)

def lacey_perimeter_discharge(wetted_perimeter: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for regime discharge Q = (P / 4.75)^2.
    Units (Default SI): wetted_perimeter [m] -> returns [m^3/s]

    Formula:
    Inversion: Solves for regime discharge Q = (P / 4.75)^2.

    Where (Default SI Units):
    - wetted_perimeter : Wetted perimeter P [unit = m]
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    wetted_perimeter : FloatOrArray
        Wetted perimeter P [m].

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (p,), is_scalar = coerce_inputs(wetted_perimeter)
    with np.errstate(all='ignore'):
        q = np.where(p <= 0, np.nan, (p / 4.75) ** 2)
    return format_output(q, is_scalar)

def lacey_hydraulic_radius(discharge: FloatOrArray, silt_factor: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes Lacey's regime hydraulic radius R = 0.48 * (Q / f)^(1/3) [m].
    Units (Default SI): discharge [m^3/s], silt_factor [dimensionless] -> returns [standard SI units]

    Formula:
    Computes Lacey's regime hydraulic radius R = 0.48 * (Q / f)^(1/3) [m].

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - silt_factor : Lacey's silt factor f [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    silt_factor : FloatOrArray
        Lacey's silt factor f [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, f), is_scalar = coerce_inputs(discharge, silt_factor)
    with np.errstate(all='ignore'):
        r = np.where((q <= 0) | (f <= 0), np.nan, 0.48 * (q / f) ** (1.0 / 3.0))
    return format_output(r, is_scalar)

def lacey_regime_slope(discharge: FloatOrArray, silt_factor: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes Lacey's regime channel bed slope S.
    Units (Default SI): discharge [m^3/s], silt_factor [dimensionless] -> returns [m/m]

    Formula:
    S = f^(5/3) / (3340 * Q^(1/6))  [dimensionless m/m]

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - silt_factor : Lacey's silt factor f [unit = dimensionless]
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    silt_factor : FloatOrArray
        Lacey's silt factor f [dimensionless].

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (q, f), is_scalar = coerce_inputs(discharge, silt_factor)
    with np.errstate(all='ignore'):
        s = np.where((q <= 0) | (f <= 0), np.nan, f ** (5.0 / 3.0) / (3340.0 * q ** (1.0 / 6.0)))
    return format_output(s, is_scalar)

def lacey_slope_discharge(slope: FloatOrArray, silt_factor: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for regime discharge Q = (f^(5/3) / (3340 * S))^6.
    Units (Default SI): slope [m/m (decimal)], silt_factor [dimensionless] -> returns [m^3/s]

    Formula:
    Inversion: Solves for regime discharge Q = (f^(5/3) / (3340 * S))^6.

    Where (Default SI Units):
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - silt_factor : Lacey's silt factor f [unit = dimensionless]
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    silt_factor : FloatOrArray
        Lacey's silt factor f [dimensionless].

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (s, f), is_scalar = coerce_inputs(slope, silt_factor)
    with np.errstate(all='ignore'):
        q = np.where((s <= 0) | (f <= 0), np.nan, (f ** (5.0 / 3.0) / (3340.0 * s)) ** 6.0)
    return format_output(q, is_scalar)

def lacey_regime_scour_depth(discharge: FloatOrArray, silt_factor: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes Lacey's normal regime scour depth R_scour = 0.473 * (Q / f)^(1/3) [m].
    Units (Default SI): discharge [m^3/s], silt_factor [dimensionless] -> returns [m]

    Formula:
    Computes Lacey's normal regime scour depth R_scour = 0.473 * (Q / f)^(1/3) [m].

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - silt_factor : Lacey's silt factor f [unit = dimensionless]
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    silt_factor : FloatOrArray
        Lacey's silt factor f [dimensionless].

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (q, f), is_scalar = coerce_inputs(discharge, silt_factor)
    with np.errstate(all='ignore'):
        r = np.where((q <= 0) | (f <= 0), np.nan, 0.473 * (q / f) ** (1.0 / 3.0))
    return format_output(r, is_scalar)

def kennedy_critical_velocity(depth: FloatOrArray, cvr_m: FloatOrArray=1.0, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes non-silting critical velocity V_0 using Kennedy's formula.
    Units (Default SI): depth [m], cvr_m [dimensionless (0.7 - 1.3)] -> returns [m/s]

    Formula:
    SI: V_0 = 0.55 * m * y^0.64  [y in m, V_0 in m/s]

    Where (Default SI Units):
    - depth : Water flow depth y [unit = m]
    - cvr_m : Kennedy Critical Velocity Ratio m [unit = dimensionless (0.7 - 1.3)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    depth : FloatOrArray
        Water flow depth y [m].
    cvr_m : FloatOrArray
        Kennedy Critical Velocity Ratio m [dimensionless (0.7 - 1.3)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (y, m), is_scalar = coerce_inputs(depth, cvr_m)
    k = 0.84 if system.lower() == 'us' else 0.55
    with np.errstate(all='ignore'):
        v = np.where((y <= 0) | (m <= 0), np.nan, k * m * y ** 0.64)
    return format_output(v, is_scalar)

def kennedy_critical_depth(velocity: FloatOrArray, cvr_m: FloatOrArray=1.0, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Solves for flow depth y = (V_0 / (k * m))^(1 / 0.64).
    Units (Default SI): velocity [m/s], cvr_m [dimensionless (0.7 - 1.3)] -> returns [m]

    Formula:
    Inversion: Solves for flow depth y = (V_0 / (k * m))^(1 / 0.64).

    Where (Default SI Units):
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - cvr_m : Kennedy Critical Velocity Ratio m [unit = dimensionless (0.7 - 1.3)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    cvr_m : FloatOrArray
        Kennedy Critical Velocity Ratio m [dimensionless (0.7 - 1.3)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (v, m), is_scalar = coerce_inputs(velocity, cvr_m)
    k = 0.84 if system.lower() == 'us' else 0.55
    with np.errstate(all='ignore'):
        y = np.where((v <= 0) | (m <= 0), np.nan, (v / (k * m)) ** (1.0 / 0.64))
    return format_output(y, is_scalar)

def channel_expansion_loss(velocity_1: FloatOrArray, velocity_2: FloatOrArray, ke: FloatOrArray=0.5, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes open channel expansion transition energy head loss h_L = K_e * (V_1 - V_2)^2 / (2g).
    Units (Default SI): velocity_1 [m/s], velocity_2 [m/s], ke [dimensionless] -> returns [standard SI units]

    Formula:
    Computes open channel expansion transition energy head loss h_L = K_e * (V_1 - V_2)^2 / (2g).

    Where (Default SI Units):
    - velocity_1 : Upstream flow velocity V_1 [unit = m/s]
    - velocity_2 : Downstream flow velocity V_2 [unit = m/s]
    - ke : Channel expansion loss coefficient K_e [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    velocity_1 : FloatOrArray
        Upstream flow velocity V_1 [m/s].
    velocity_2 : FloatOrArray
        Downstream flow velocity V_2 [m/s].
    ke : FloatOrArray
        Channel expansion loss coefficient K_e [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (v1, v2, k_val), is_scalar = coerce_inputs(velocity_1, velocity_2, ke)
    g = 32.17405 if system.lower() == 'us' else 9.80665
    with np.errstate(all='ignore'):
        hl = k_val * (v1 - v2) ** 2 / (2.0 * g)
    return format_output(hl, is_scalar)

def channel_contraction_loss(velocity_1: FloatOrArray, velocity_2: FloatOrArray, kc: FloatOrArray=0.1, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes open channel contraction transition energy head loss h_L = K_c * |V_2^2 - V_1^2| / (2g).
    Units (Default SI): velocity_1 [m/s], velocity_2 [m/s], kc [dimensionless] -> returns [standard SI units]

    Formula:
    Computes open channel contraction transition energy head loss h_L = K_c * |V_2^2 - V_1^2| / (2g).

    Where (Default SI Units):
    - velocity_1 : Upstream flow velocity V_1 [unit = m/s]
    - velocity_2 : Downstream flow velocity V_2 [unit = m/s]
    - kc : Channel contraction loss coefficient K_c [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    velocity_1 : FloatOrArray
        Upstream flow velocity V_1 [m/s].
    velocity_2 : FloatOrArray
        Downstream flow velocity V_2 [m/s].
    kc : FloatOrArray
        Channel contraction loss coefficient K_c [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (v1, v2, k_val), is_scalar = coerce_inputs(velocity_1, velocity_2, kc)
    g = 32.17405 if system.lower() == 'us' else 9.80665
    with np.errstate(all='ignore'):
        hl = k_val * np.abs(v2 ** 2 - v1 ** 2) / (2.0 * g)
    return format_output(hl, is_scalar)

def blasius_friction_factor(reynolds: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes Darcy friction factor for smooth pipes in turbulent flow (Re < 10^5) using Blasius' formula:
    Units (Default SI): reynolds [dimensionless] -> returns [standard SI units]

    Formula:
    f = 0.3164 / Re^0.25

    Where (Default SI Units):
    - reynolds : Reynolds number Re = V * D / nu [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    reynolds : FloatOrArray
        Reynolds number Re = V * D / nu [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (re,), is_scalar = coerce_inputs(reynolds)
    with np.errstate(all='ignore'):
        f = np.where(re <= 0, np.nan, 0.3164 / re ** 0.25)
    return format_output(f, is_scalar)

def cavitation_index(pressure_abs: FloatOrArray, vapor_pressure: FloatOrArray, velocity: FloatOrArray, density: FloatOrArray=1000.0) -> Union[float, np.ndarray]:
    """
    Computes Thoma cavitation index sigma = (P_abs - P_v) / (0.5 * rho * V^2).
    Units (Default SI): pressure_abs [Pa (N/m^2)], vapor_pressure [Pa (N/m^2)], velocity [m/s], density [kg/m^3 (~1000.0)] -> returns [standard SI units]

    Formula:
    Computes Thoma cavitation index sigma = (P_abs - P_v) / (0.5 * rho * V^2).

    Where (Default SI Units):
    - pressure_abs : Absolute static fluid pressure P_abs [unit = Pa (N/m^2)]
    - vapor_pressure : Water vapor pressure P_v [unit = Pa (N/m^2)]
    - velocity : Mean cross-sectional flow velocity V [unit = m/s]
    - density : Fluid mass density rho [unit = kg/m^3 (~1000.0)]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    pressure_abs : FloatOrArray
        Absolute static fluid pressure P_abs [Pa (N/m^2)].
    vapor_pressure : FloatOrArray
        Water vapor pressure P_v [Pa (N/m^2)].
    velocity : FloatOrArray
        Mean cross-sectional flow velocity V [m/s].
    density : FloatOrArray
        Fluid mass density rho [kg/m^3 (~1000.0)].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (p, pv, v, rho), is_scalar = coerce_inputs(pressure_abs, vapor_pressure, velocity, density)
    with np.errstate(all='ignore'):
        sig = np.where(v <= 0, np.nan, (p - pv) / (0.5 * rho * v ** 2))
    return format_output(sig, is_scalar)

def cavitation_velocity(pressure_abs: FloatOrArray, vapor_pressure: FloatOrArray, sigma_critical: FloatOrArray, density: FloatOrArray=1000.0) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for maximum permissible velocity before cavitation occurs.
    Units (Default SI): pressure_abs [Pa (N/m^2)], vapor_pressure [Pa (N/m^2)], sigma_critical [dimensionless], density [kg/m^3 (~1000.0)] -> returns [m/s]

    Formula:
    cavitation_velocity(pressure_abs, vapor_pressure, sigma_critical, density)

    Where (Default SI Units):
    - pressure_abs : Absolute static fluid pressure P_abs [unit = Pa (N/m^2)]
    - vapor_pressure : Water vapor pressure P_v [unit = Pa (N/m^2)]
    - sigma_critical : Critical Thoma cavitation index sigma_c [unit = dimensionless]
    - density : Fluid mass density rho [unit = kg/m^3 (~1000.0)]
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    pressure_abs : FloatOrArray
        Absolute static fluid pressure P_abs [Pa (N/m^2)].
    vapor_pressure : FloatOrArray
        Water vapor pressure P_v [Pa (N/m^2)].
    sigma_critical : FloatOrArray
        Critical Thoma cavitation index sigma_c [dimensionless].
    density : FloatOrArray
        Fluid mass density rho [kg/m^3 (~1000.0)].

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (p, pv, sig, rho), is_scalar = coerce_inputs(pressure_abs, vapor_pressure, sigma_critical, density)
    with np.errstate(all='ignore'):
        v = np.where((p <= pv) | (sig <= 0), np.nan, np.sqrt((p - pv) / (0.5 * rho * sig)))
    return format_output(v, is_scalar)

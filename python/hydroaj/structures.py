"""
Hydraulic Structures Module API.
Provides polymorphic scalar and vectorized calculations for Weirs, Flumes, Orifices, and Sluice Gates.
"""
from typing import Any, Tuple, Union, Sequence, Optional
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import numpy as np
FloatOrArray = Union[float, int, Sequence[float], np.ndarray]
from . import _hydroaj_core as _core
from ._coercion import coerce_inputs, format_output
G_SI = 9.80665
G_US = 32.17405
FRANCIS_K_SI = 1.84
FRANCIS_K_US = 3.33

def _get_gravity(system: str) -> float:
    return G_US if system.lower() == 'us' else G_SI

def francis_weir(length: FloatOrArray, head: FloatOrArray, contractions: FloatOrArray=0.0, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Francis formula for sharp-crested rectangular weir:
    Units (Default SI): length [m], head [m], contractions [SI units] -> returns [standard SI units]

    Formula:
    SI: Q = 1.84 * (L - 0.1 * n_e * H) * H^(3/2) (m^3/s)

    Where (Default SI Units):
    - length : Reach / conduit / flow path length L [unit = m]
    - head : Upstream / operating hydraulic head H [unit = m]
    - contractions : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    contractions : FloatOrArray
        contractions [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (l, h, ne), is_scalar = coerce_inputs(length, head, contractions)
    k_f = FRANCIS_K_US if system.lower() == 'us' else FRANCIS_K_SI
    out = _core.francis_weir(l, h, ne, k_f)
    return format_output(out, is_scalar)

def v_notch_weir(notch_angle_deg: FloatOrArray, head: FloatOrArray, discharge_coeff: FloatOrArray=0.585, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes v notch weir.
    Units (Default SI): notch_angle_deg [minutes], head [m], discharge_coeff [dimensionless] -> returns [minutes]

    Formula:
    Q = (8/15) * C_d * sqrt(2 * g) * tan(theta / 2) * H^(5/2)

    Where (Default SI Units):
    - notch_angle_deg : Time parameter [unit = minutes]
    - head : Upstream / operating hydraulic head H [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Time parameter [unit = minutes]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    notch_angle_deg : FloatOrArray
        notch_angle_deg [SI units].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Time parameter [minutes]. Returns float for scalar inputs.
    """
    (ang_deg, h, cd), is_scalar = coerce_inputs(notch_angle_deg, head, discharge_coeff)
    ang_rad = np.radians(ang_deg)
    g = _get_gravity(system)
    out = _core.v_notch_weir(ang_rad, h, cd, g)
    return format_output(out, is_scalar)

def broad_crested_weir(length: FloatOrArray, head: FloatOrArray, discharge_coeff: FloatOrArray=0.848, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes broad crested weir.
    Units (Default SI): length [m], head [m], discharge_coeff [dimensionless] -> returns [standard SI units]

    Formula:
    Q = C_d * (2/3)^(3/2) * sqrt(g) * L * H^(3/2)

    Where (Default SI Units):
    - length : Reach / conduit / flow path length L [unit = m]
    - head : Upstream / operating hydraulic head H [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (l, h, cd), is_scalar = coerce_inputs(length, head, discharge_coeff)
    g = _get_gravity(system)
    out = _core.broad_crested_weir(l, h, cd, g)
    return format_output(out, is_scalar)

def parshall_flume(throat_width: FloatOrArray, head: FloatOrArray, coeff_c: FloatOrArray=2.32, exp_n: FloatOrArray=1.522) -> Union[float, np.ndarray]:
    """
    Parshall flume discharge: Q = C * W * H^n
    Units (Default SI): throat_width [m], head [m], coeff_c [dimensionless], exp_n [SI units] -> returns [standard SI units]

    Formula:
    Parshall flume discharge: Q = C * W * H^n

    Where (Default SI Units):
    - throat_width : Venturi / flume constricted throat width b_2 [unit = m]
    - head : Upstream / operating hydraulic head H [unit = m]
    - coeff_c : Input parameter [unit = dimensionless]
    - exp_n : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    throat_width : FloatOrArray
        Venturi / flume constricted throat width b_2 [m].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    coeff_c : FloatOrArray
        coeff_c [SI units].
    exp_n : FloatOrArray
        exp_n [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (w, h, c, exp), is_scalar = coerce_inputs(throat_width, head, coeff_c, exp_n)
    out = _core.parshall_flume(w, h, c, exp)
    return format_output(out, is_scalar)

def orifice_free(area: FloatOrArray, head: FloatOrArray, discharge_coeff: FloatOrArray=0.62, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Free orifice discharge: Q = C_d * A_o * sqrt(2 * g * H)
    Units (Default SI): area [m^2], head [m], discharge_coeff [dimensionless] -> returns [standard SI units]

    Formula:
    Free orifice discharge: Q = C_d * A_o * sqrt(2 * g * H)

    Where (Default SI Units):
    - area : Cross-sectional flow area A [unit = m^2]
    - head : Upstream / operating hydraulic head H [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (a, h, cd), is_scalar = coerce_inputs(area, head, discharge_coeff)
    g = _get_gravity(system)
    out = _core.orifice_free(a, h, cd, g)
    return format_output(out, is_scalar)

def orifice_submerged(area: FloatOrArray, upstream_head: FloatOrArray, downstream_head: FloatOrArray, discharge_coeff: FloatOrArray=0.62, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Submerged orifice discharge: Q = C_d * A_o * sqrt(2 * g * (H_1 - H_2))
    Units (Default SI): area [m^2], upstream_head [m], downstream_head [m], discharge_coeff [dimensionless] -> returns [standard SI units]

    Formula:
    Submerged orifice discharge: Q = C_d * A_o * sqrt(2 * g * (H_1 - H_2))

    Where (Default SI Units):
    - area : Cross-sectional flow area A [unit = m^2]
    - upstream_head : Hydraulic head [unit = m]
    - downstream_head : Hydraulic head [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    upstream_head : FloatOrArray
        upstream_head [SI units].
    downstream_head : FloatOrArray
        downstream_head [SI units].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (a, h1, h2, cd), is_scalar = coerce_inputs(area, upstream_head, downstream_head, discharge_coeff)
    g = _get_gravity(system)
    out = _core.orifice_submerged(a, h1, h2, cd, g)
    return format_output(out, is_scalar)

def sluice_gate_free(gate_width: FloatOrArray, gate_opening: FloatOrArray, upstream_depth: FloatOrArray, discharge_coeff: FloatOrArray=0.6, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Sluice gate free discharge: Q = C_d * b * a * sqrt(2 * g * y_1)
    Units (Default SI): gate_width [SI units], gate_opening [SI units], upstream_depth [m], discharge_coeff [dimensionless] -> returns [standard SI units]

    Formula:
    Sluice gate free discharge: Q = C_d * b * a * sqrt(2 * g * y_1)

    Where (Default SI Units):
    - gate_width : Input parameter [unit = SI units]
    - gate_opening : Input parameter [unit = SI units]
    - upstream_depth : Upstream approach flow depth y_1 [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    gate_width : FloatOrArray
        gate_width [SI units].
    gate_opening : FloatOrArray
        gate_opening [SI units].
    upstream_depth : FloatOrArray
        Upstream approach flow depth y_1 [m].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (b, a, y1, cd), is_scalar = coerce_inputs(gate_width, gate_opening, upstream_depth, discharge_coeff)
    g = _get_gravity(system)
    out = _core.sluice_gate_free(b, a, y1, cd, g)
    return format_output(out, is_scalar)

def sluice_gate_submerged(gate_width: FloatOrArray, gate_opening: FloatOrArray, upstream_depth: FloatOrArray, tailwater_depth: FloatOrArray, submerged_coeff: FloatOrArray=0.6, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Sluice gate submerged discharge: Q = C_s * b * a * sqrt(2 * g * (y_1 - y_2))
    Units (Default SI): gate_width [SI units], gate_opening [SI units], upstream_depth [m], tailwater_depth [m], submerged_coeff [dimensionless] -> returns [standard SI units]

    Formula:
    Sluice gate submerged discharge: Q = C_s * b * a * sqrt(2 * g * (y_1 - y_2))

    Where (Default SI Units):
    - gate_width : Input parameter [unit = SI units]
    - gate_opening : Input parameter [unit = SI units]
    - upstream_depth : Upstream approach flow depth y_1 [unit = m]
    - tailwater_depth : Flow depth [unit = m]
    - submerged_coeff : Input parameter [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    gate_width : FloatOrArray
        gate_width [SI units].
    gate_opening : FloatOrArray
        gate_opening [SI units].
    upstream_depth : FloatOrArray
        Upstream approach flow depth y_1 [m].
    tailwater_depth : FloatOrArray
        tailwater_depth [SI units].
    submerged_coeff : FloatOrArray
        submerged_coeff [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (b, a, y1, y2, cs), is_scalar = coerce_inputs(gate_width, gate_opening, upstream_depth, tailwater_depth, submerged_coeff)
    g = _get_gravity(system)
    out = _core.sluice_gate_submerged(b, a, y1, y2, cs, g)
    return format_output(out, is_scalar)

def ogee_spillway_discharge(discharge_coeff: FloatOrArray, effective_length: FloatOrArray, total_head: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes ogee spillway discharge.
    Units (Default SI): discharge_coeff [dimensionless], effective_length [m], total_head [m] -> returns [m^3/s]

    Formula:
    Q = C_o * L_e * H_e^(3/2)

    Where (Default SI Units):
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - effective_length : Length [unit = m]
    - total_head : Total operating head H [unit = m]
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    effective_length : FloatOrArray
        effective_length [SI units].
    total_head : FloatOrArray
        Total operating head H [m].

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (co, le, he), is_scalar = coerce_inputs(discharge_coeff, effective_length, total_head)
    out = _core.ogee_spillway_discharge(co, le, he)
    return format_output(out, is_scalar)

def ogee_discharge_coefficient(design_coeff: FloatOrArray, actual_head: FloatOrArray, design_head: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes ogee discharge coefficient.
    Units (Default SI): design_coeff [dimensionless], actual_head [m], design_head [m] -> returns [m^3/s]

    Formula:
    C = C_o * (H_e / H_o)^0.12

    Where (Default SI Units):
    - design_coeff : Input parameter [unit = dimensionless]
    - actual_head : Hydraulic head [unit = m]
    - design_head : Hydraulic head [unit = m]
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    design_coeff : FloatOrArray
        design_coeff [SI units].
    actual_head : FloatOrArray
        actual_head [SI units].
    design_head : FloatOrArray
        design_head [SI units].

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (co, he, ho), is_scalar = coerce_inputs(design_coeff, actual_head, design_head)
    out = _core.ogee_discharge_coefficient(co, he, ho)
    return format_output(out, is_scalar)

def spillway_effective_length(clear_length: FloatOrArray, n_piers: FloatOrArray=0.0, k_pier: FloatOrArray=0.02, k_abutment: FloatOrArray=0.1, total_head: FloatOrArray=0.0) -> Union[float, np.ndarray]:
    """
    Computes spillway effective length.
    Units (Default SI): clear_length [m], n_piers [SI units], k_pier [SI units], k_abutment [SI units], total_head [m] -> returns [km if 'km' in fn else 'm']

    Formula:
    L_e = L - 2.0 * (N * K_p + K_a) * H_e

    Where (Default SI Units):
    - clear_length : Length [unit = m]
    - n_piers : Input parameter [unit = SI units]
    - k_pier : Input parameter [unit = SI units]
    - k_abutment : Input parameter [unit = SI units]
    - total_head : Total operating head H [unit = m]
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    clear_length : FloatOrArray
        clear_length [SI units].
    n_piers : FloatOrArray
        n_piers [SI units].
    k_pier : FloatOrArray
        k_pier [SI units].
    k_abutment : FloatOrArray
        k_abutment [SI units].
    total_head : FloatOrArray
        Total operating head H [m].

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (l, np, kp, ka, he), is_scalar = coerce_inputs(clear_length, n_piers, k_pier, k_abutment, total_head)
    out = _core.spillway_effective_length(l, np, kp, ka, he)
    return format_output(out, is_scalar)

def chute_terminal_velocity(total_fall: FloatOrArray, head_loss: FloatOrArray=0.0, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes chute terminal velocity.
    Units (Default SI): total_fall [SI units], head_loss [m] -> returns [m/s]

    Formula:
    V = sqrt(2 * g * (Z_drop - H_loss))

    Where (Default SI Units):
    - total_fall : Input parameter [unit = SI units]
    - head_loss : Energy friction head loss h_f [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    total_fall : FloatOrArray
        total_fall [SI units].
    head_loss : FloatOrArray
        Energy friction head loss h_f [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (zd, hl), is_scalar = coerce_inputs(total_fall, head_loss)
    g = _get_gravity(system)
    out = _core.chute_terminal_velocity(zd, hl, g)
    return format_output(out, is_scalar)

def stilling_basin_length(sequent_depth: FloatOrArray, basin_coeff: FloatOrArray=4.3) -> Union[float, np.ndarray]:
    """
    Computes stilling basin length.
    Units (Default SI): sequent_depth [m], basin_coeff [dimensionless] -> returns [km if 'km' in fn else 'm']

    Formula:
    L_sb = k_basin * y_2 (USBR Type II: k=4.3; Type III: k=2.7)

    Where (Default SI Units):
    - sequent_depth : Subcritical conjugate depth y_2 [unit = m]
    - basin_coeff : Input parameter [unit = dimensionless]
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    sequent_depth : FloatOrArray
        Subcritical conjugate depth y_2 [m].
    basin_coeff : FloatOrArray
        basin_coeff [SI units].

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (y2, kb), is_scalar = coerce_inputs(sequent_depth, basin_coeff)
    out = _core.stilling_basin_length(y2, kb)
    return format_output(out, is_scalar)

def morning_glory_weir_flow(crest_radius: FloatOrArray, head_on_crest: FloatOrArray, discharge_coeff: FloatOrArray=2.0) -> Union[float, np.ndarray]:
    """
    Computes morning glory weir flow.
    Units (Default SI): crest_radius [SI units], head_on_crest [m], discharge_coeff [dimensionless] -> returns [standard SI units]

    Formula:
    Q = C * (2 * pi * R) * H^(3/2)

    Where (Default SI Units):
    - crest_radius : Input parameter [unit = SI units]
    - head_on_crest : Hydraulic head [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    crest_radius : FloatOrArray
        crest_radius [SI units].
    head_on_crest : FloatOrArray
        head_on_crest [SI units].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (r, h, c), is_scalar = coerce_inputs(crest_radius, head_on_crest, discharge_coeff)
    out = _core.morning_glory_weir_flow(r, h, c)
    return format_output(out, is_scalar)

def siphon_spillway_discharge(throat_area: FloatOrArray, operating_head: FloatOrArray, discharge_coeff: FloatOrArray=0.8, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes siphon spillway discharge.
    Units (Default SI): throat_area [m^2], operating_head [m], discharge_coeff [dimensionless] -> returns [m^3/s]

    Formula:
    Q = C_d * A_throat * sqrt(2 * g * H_operating)

    Where (Default SI Units):
    - throat_area : Area [unit = m^2]
    - operating_head : Hydraulic head [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    throat_area : FloatOrArray
        throat_area [SI units].
    operating_head : FloatOrArray
        operating_head [SI units].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (at, ho, cd), is_scalar = coerce_inputs(throat_area, operating_head, discharge_coeff)
    g = _get_gravity(system)
    out = _core.siphon_spillway_discharge(at, ho, cd, g)
    return format_output(out, is_scalar)

def drop_structure_depth(drop_height: FloatOrArray, unit_discharge: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes drop structure depth.
    Units (Default SI): drop_height [SI units], unit_discharge [m^3/s] -> returns [m]

    Formula:
    y_1 = 0.54 * h_d * (q^2 / (g * h_d^3))^0.425

    Where (Default SI Units):
    - drop_height : Input parameter [unit = SI units]
    - unit_discharge : Volumetric discharge rate [unit = m^3/s]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    drop_height : FloatOrArray
        drop_height [SI units].
    unit_discharge : FloatOrArray
        unit_discharge [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (hd, q), is_scalar = coerce_inputs(drop_height, unit_discharge)
    g = _get_gravity(system)
    out = _core.drop_structure_depth(hd, q, g)
    return format_output(out, is_scalar)

def tailwater_depth(discharge: FloatOrArray, rating_a: FloatOrArray, rating_b: FloatOrArray, base_elevation: FloatOrArray=0.0) -> Union[float, np.ndarray]:
    """
    Computes tailwater depth.
    Units (Default SI): discharge [m^3/s], rating_a [SI units], rating_b [SI units], base_elevation [SI units] -> returns [m]

    Formula:
    y_tw = a * Q^b + z_0

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - rating_a : Input parameter [unit = SI units]
    - rating_b : Input parameter [unit = SI units]
    - base_elevation : Input parameter [unit = SI units]
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    rating_a : FloatOrArray
        rating_a [SI units].
    rating_b : FloatOrArray
        rating_b [SI units].
    base_elevation : FloatOrArray
        base_elevation [SI units].

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (q, a, b, z0), is_scalar = coerce_inputs(discharge, rating_a, rating_b, base_elevation)
    out = _core.tailwater_depth(q, a, b, z0)
    return format_output(out, is_scalar)
francis_weir_q = francis_weir

def francis_weir_l(discharge: FloatOrArray, head: FloatOrArray, contractions: FloatOrArray=0.0, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Crest length L = Q / (k * H^1.5) + 0.1 * n_e * H
    Units (Default SI): discharge [m^3/s], head [m], contractions [SI units] -> returns [km if 'km' in fn else 'm']

    Formula:
    Inversion: Crest length L = Q / (k * H^1.5) + 0.1 * n_e * H

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - head : Upstream / operating hydraulic head H [unit = m]
    - contractions : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    contractions : FloatOrArray
        contractions [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (q, h, ne), is_scalar = coerce_inputs(discharge, head, contractions)
    k_f = FRANCIS_K_US if system.lower() == 'us' else FRANCIS_K_SI
    out = _core.francis_weir_l(q, h, ne, k_f)
    return format_output(out, is_scalar)
francis_weir_length = francis_weir_l
v_notch_weir_q = v_notch_weir

def v_notch_weir_h(discharge: FloatOrArray, notch_angle_deg: FloatOrArray, discharge_coeff: FloatOrArray=0.585, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes v notch weir h.
    Units (Default SI): discharge [m^3/s], notch_angle_deg [minutes], discharge_coeff [dimensionless] -> returns [minutes]

    Formula:
    H = (Q / ((8 / 15) * C_d * sqrt(2 * g) * tan(theta / 2)))^(2/5)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - notch_angle_deg : Time parameter [unit = minutes]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Time parameter [unit = minutes]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    notch_angle_deg : FloatOrArray
        notch_angle_deg [SI units].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Time parameter [minutes]. Returns float for scalar inputs.
    """
    (q, ang_deg, cd), is_scalar = coerce_inputs(discharge, notch_angle_deg, discharge_coeff)
    ang_rad = np.radians(ang_deg)
    g = _get_gravity(system)
    out = _core.v_notch_weir_h(q, ang_rad, cd, g)
    return format_output(out, is_scalar)
v_notch_weir_head = v_notch_weir_h

def v_notch_weir_cd(discharge: FloatOrArray, notch_angle_deg: FloatOrArray, head: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Discharge coefficient C_d = Q / ((8/15) * sqrt(2*g) * tan(theta/2) * H^(5/2))
    Units (Default SI): discharge [m^3/s], notch_angle_deg [minutes], head [m] -> returns [minutes]

    Formula:
    Inversion: Discharge coefficient C_d = Q / ((8/15) * sqrt(2*g) * tan(theta/2) * H^(5/2))

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - notch_angle_deg : Time parameter [unit = minutes]
    - head : Upstream / operating hydraulic head H [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Time parameter [unit = minutes]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    notch_angle_deg : FloatOrArray
        notch_angle_deg [SI units].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Time parameter [minutes]. Returns float for scalar inputs.
    """
    (q, ang_deg, h), is_scalar = coerce_inputs(discharge, notch_angle_deg, head)
    ang_rad = np.radians(ang_deg)
    g = _get_gravity(system)
    out = _core.v_notch_weir_cd(q, ang_rad, h, g)
    return format_output(out, is_scalar)
v_notch_weir_coeff = v_notch_weir_cd

def v_notch_weir_theta(discharge: FloatOrArray, head: FloatOrArray, discharge_coeff: FloatOrArray=0.585, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Notch angle theta (degrees) = 2 * arctan(Q / ((8/15) * C_d * sqrt(2*g) * H^(5/2)))
    Units (Default SI): discharge [m^3/s], head [m], discharge_coeff [dimensionless] -> returns [minutes]

    Formula:
    Inversion: Notch angle theta (degrees) = 2 * arctan(Q / ((8/15) * C_d * sqrt(2*g) * H^(5/2)))

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - head : Upstream / operating hydraulic head H [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Time parameter [unit = minutes]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Time parameter [minutes]. Returns float for scalar inputs.
    """
    (q, h, cd), is_scalar = coerce_inputs(discharge, head, discharge_coeff)
    g = _get_gravity(system)
    out = _core.v_notch_weir_theta(q, h, cd, g)
    out_deg = np.degrees(out)
    return format_output(out_deg, is_scalar)
v_notch_weir_angle = v_notch_weir_theta
broad_crested_weir_q = broad_crested_weir

def broad_crested_weir_h(discharge: FloatOrArray, length: FloatOrArray, discharge_coeff: FloatOrArray=0.848, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Upstream head H = (Q / (C_d * b * sqrt(g) * (2/3)^1.5))^(2/3)
    Units (Default SI): discharge [m^3/s], length [m], discharge_coeff [dimensionless] -> returns [m]

    Formula:
    Inversion: Upstream head H = (Q / (C_d * b * sqrt(g) * (2/3)^1.5))^(2/3)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - length : Reach / conduit / flow path length L [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (q, l, cd), is_scalar = coerce_inputs(discharge, length, discharge_coeff)
    g = _get_gravity(system)
    out = _core.broad_crested_weir_h(q, l, cd, g)
    return format_output(out, is_scalar)
broad_crested_weir_head = broad_crested_weir_h

def broad_crested_weir_l(discharge: FloatOrArray, head: FloatOrArray, discharge_coeff: FloatOrArray=0.848, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Weir crest length b = Q / (C_d * sqrt(g) * (2/3)^1.5 * H^1.5)
    Units (Default SI): discharge [m^3/s], head [m], discharge_coeff [dimensionless] -> returns [km if 'km' in fn else 'm']

    Formula:
    Inversion: Weir crest length b = Q / (C_d * sqrt(g) * (2/3)^1.5 * H^1.5)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - head : Upstream / operating hydraulic head H [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (q, h, cd), is_scalar = coerce_inputs(discharge, head, discharge_coeff)
    g = _get_gravity(system)
    out = _core.broad_crested_weir_l(q, h, cd, g)
    return format_output(out, is_scalar)
broad_crested_weir_crest_length = broad_crested_weir_l
orifice_free_q = orifice_free

def orifice_free_h(discharge: FloatOrArray, area: FloatOrArray, discharge_coeff: FloatOrArray=0.62, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Head above orifice H = (1 / (2 * g)) * (Q / (C_d * A_o))^2
    Units (Default SI): discharge [m^3/s], area [m^2], discharge_coeff [dimensionless] -> returns [m]

    Formula:
    Inversion: Head above orifice H = (1 / (2 * g)) * (Q / (C_d * A_o))^2

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - area : Cross-sectional flow area A [unit = m^2]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (q, a, cd), is_scalar = coerce_inputs(discharge, area, discharge_coeff)
    g = _get_gravity(system)
    out = _core.orifice_free_h(q, a, cd, g)
    return format_output(out, is_scalar)
orifice_free_head = orifice_free_h

def orifice_free_ao(discharge: FloatOrArray, head: FloatOrArray, discharge_coeff: FloatOrArray=0.62, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Orifice opening area A_o = Q / (C_d * sqrt(2 * g * H))
    Units (Default SI): discharge [m^3/s], head [m], discharge_coeff [dimensionless] -> returns [standard SI units]

    Formula:
    Inversion: Orifice opening area A_o = Q / (C_d * sqrt(2 * g * H))

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - head : Upstream / operating hydraulic head H [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
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
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, h, cd), is_scalar = coerce_inputs(discharge, head, discharge_coeff)
    g = _get_gravity(system)
    out = _core.orifice_free_ao(q, h, cd, g)
    return format_output(out, is_scalar)
orifice_free_area = orifice_free_ao
sluice_gate_free_q = sluice_gate_free

def sluice_gate_free_a(discharge: FloatOrArray, width: FloatOrArray, head_upstream: FloatOrArray, discharge_coeff: FloatOrArray=0.6, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Gate vertical opening height a = Q / (C_d * b * sqrt(2 * g * y_1))
    Units (Default SI): discharge [m^3/s], width [m], head_upstream [m], discharge_coeff [dimensionless] -> returns [km^2 if 'km' in fn else 'm^2']

    Formula:
    Inversion: Gate vertical opening height a = Q / (C_d * b * sqrt(2 * g * y_1))

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - width : Flume / gate clear opening width b [unit = m]
    - head_upstream : Hydraulic head [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Area [unit = km^2 if 'km' in fn else 'm^2']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    width : FloatOrArray
        Flume / gate clear opening width b [m].
    head_upstream : FloatOrArray
        head_upstream [SI units].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Area [km^2 if 'km' in fn else 'm^2']. Returns float for scalar inputs.
    """
    (q, b, y1, cd), is_scalar = coerce_inputs(discharge, width, head_upstream, discharge_coeff)
    g = _get_gravity(system)
    out = _core.sluice_gate_free_a(b, q, y1, cd, g)
    return format_output(out, is_scalar)
sluice_gate_free_opening = sluice_gate_free_a
ogee_spillway_q = ogee_spillway_discharge

def ogee_spillway_he(discharge: FloatOrArray, effective_length: FloatOrArray, discharge_coeff: FloatOrArray=2.2) -> Union[float, np.ndarray]:
    """
    Computes ogee spillway he.
    Units (Default SI): discharge [m^3/s], effective_length [m], discharge_coeff [dimensionless] -> returns [standard SI units]

    Formula:
    H_e = (Q / (C_o * L_e))^(2/3)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - effective_length : Length [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    effective_length : FloatOrArray
        effective_length [SI units].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, le, cd), is_scalar = coerce_inputs(discharge, effective_length, discharge_coeff)
    out = _core.ogee_spillway_he(q, le, cd)
    return format_output(out, is_scalar)
ogee_spillway_head = ogee_spillway_he

def ogee_spillway_le(discharge: FloatOrArray, design_head: FloatOrArray, discharge_coeff: FloatOrArray=2.2) -> Union[float, np.ndarray]:
    """
    Computes ogee spillway le.
    Units (Default SI): discharge [m^3/s], design_head [m], discharge_coeff [dimensionless] -> returns [standard SI units]

    Formula:
    L_e = Q / (C_o * H_e^(3/2))

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - design_head : Hydraulic head [unit = m]
    - discharge_coeff : Discharge coefficient C_d [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    design_head : FloatOrArray
        design_head [SI units].
    discharge_coeff : FloatOrArray
        Discharge coefficient C_d [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, he, cd), is_scalar = coerce_inputs(discharge, design_head, discharge_coeff)
    out = _core.ogee_spillway_le(q, he, cd)
    return format_output(out, is_scalar)
ogee_spillway_length = ogee_spillway_le
chute_velocity_v = chute_terminal_velocity

def chute_velocity_z(terminal_velocity: FloatOrArray, initial_velocity: FloatOrArray, initial_elevation: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Bed elevation Z = Z_0 - (V^2 - V_0^2) / (2 * g)
    Units (Default SI): terminal_velocity [m/s], initial_velocity [m/s], initial_elevation [SI units] -> returns [m/s]

    Formula:
    Inversion: Bed elevation Z = Z_0 - (V^2 - V_0^2) / (2 * g)

    Where (Default SI Units):
    - terminal_velocity : Flow velocity [unit = m/s]
    - initial_velocity : Flow velocity [unit = m/s]
    - initial_elevation : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    terminal_velocity : FloatOrArray
        terminal_velocity [SI units].
    initial_velocity : FloatOrArray
        initial_velocity [SI units].
    initial_elevation : FloatOrArray
        initial_elevation [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (v, v0, z0), is_scalar = coerce_inputs(terminal_velocity, initial_velocity, initial_elevation)
    g = _get_gravity(system)
    out = _core.chute_velocity_z(v, v0, z0, g)
    return format_output(out, is_scalar)
chute_elevation = chute_velocity_z

def stilling_basin_y2(initial_depth: FloatOrArray, froude_1: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes stilling basin y2.
    Units (Default SI): initial_depth [m], froude_1 [dimensionless] -> returns [standard SI units]

    Formula:
    y_2 = L_sb / k_basin

    Where (Default SI Units):
    - initial_depth : Supercritical initial depth y_1 [unit = m]
    - froude_1 : Supercritical inflow Froude number Fr_1 [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

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
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (y1, fr), is_scalar = coerce_inputs(initial_depth, froude_1)
    out = _core.stilling_basin_y2(y1, fr)
    return format_output(out, is_scalar)
stilling_basin_depth_2 = stilling_basin_y2

def stilling_basin_y1(sequent_depth: FloatOrArray, froude_1: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Stilling basin initial depth y_1 = y_2 / (0.5 * (sqrt(1 + 8 * Fr_1^2) - 1))
    Units (Default SI): sequent_depth [m], froude_1 [dimensionless] -> returns [standard SI units]

    Formula:
    Inversion: Stilling basin initial depth y_1 = y_2 / (0.5 * (sqrt(1 + 8 * Fr_1^2) - 1))

    Where (Default SI Units):
    - sequent_depth : Subcritical conjugate depth y_2 [unit = m]
    - froude_1 : Supercritical inflow Froude number Fr_1 [unit = dimensionless]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    sequent_depth : FloatOrArray
        Subcritical conjugate depth y_2 [m].
    froude_1 : FloatOrArray
        Supercritical inflow Froude number Fr_1 [dimensionless].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (y2, fr), is_scalar = coerce_inputs(sequent_depth, froude_1)
    out = _core.stilling_basin_y1(y2, fr)
    return format_output(out, is_scalar)
stilling_basin_depth_1 = stilling_basin_y1

def cipoletti_weir_q(length: FloatOrArray, head: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes discharge Q over a Cipoletti (trapezoidal 4V:1H) weir.
    Units (Default SI): length [m], head [m] -> returns [m^3/s]

    Formula:
    SI: Q = 1.860 * L * H^(3/2)  [L in m, H in m, Q in m^3/s]

    Where (Default SI Units):
    - length : Reach / conduit / flow path length L [unit = m]
    - head : Upstream / operating hydraulic head H [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (l, h), is_scalar = coerce_inputs(length, head)
    k = 3.367 if system.lower() == 'us' else 1.86
    with np.errstate(all='ignore'):
        q = np.where((l <= 0) | (h <= 0), np.nan, k * l * h ** 1.5)
    return format_output(q, is_scalar)

def cipoletti_weir_l(discharge: FloatOrArray, head: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Solves for required Cipoletti crest length L = Q / (k * H^1.5).
    Units (Default SI): discharge [m^3/s], head [m] -> returns [km if 'km' in fn else 'm']

    Formula:
    Inversion: Solves for required Cipoletti crest length L = Q / (k * H^1.5).

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - head : Upstream / operating hydraulic head H [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Length [unit = km if 'km' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Length [km if 'km' in fn else 'm']. Returns float for scalar inputs.
    """
    (q, h), is_scalar = coerce_inputs(discharge, head)
    k = 3.367 if system.lower() == 'us' else 1.86
    with np.errstate(all='ignore'):
        l = np.where((q <= 0) | (h <= 0), np.nan, q / (k * h ** 1.5))
    return format_output(l, is_scalar)

def cipoletti_weir_h(discharge: FloatOrArray, length: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Solves for head H = (Q / (k * L))^(2/3).
    Units (Default SI): discharge [m^3/s], length [m] -> returns [m]

    Formula:
    Inversion: Solves for head H = (Q / (k * L))^(2/3).

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - length : Reach / conduit / flow path length L [unit = m]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    length : FloatOrArray
        Reach / conduit / flow path length L [m].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (q, l), is_scalar = coerce_inputs(discharge, length)
    k = 3.367 if system.lower() == 'us' else 1.86
    with np.errstate(all='ignore'):
        h = np.where((q <= 0) | (l <= 0), np.nan, (q / (k * l)) ** (2.0 / 3.0))
    return format_output(h, is_scalar)

def sutro_weir_q(base_width: FloatOrArray, base_height: FloatOrArray, head: FloatOrArray, cd: FloatOrArray=0.62, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes discharge Q for a Sutro (proportional linear) weir.
    Units (Default SI): base_width [m], base_height [m], head [m], cd [dimensionless] -> returns [m^3/s]

    Formula:
    Q = C_d * b * sqrt(2 * g * a) * (H - a/3)

    Where (Default SI Units):
    - base_width : Sutro weir rectangular base width b [unit = m]
    - base_height : Sutro weir base vertical crest height a [unit = m]
    - head : Upstream / operating hydraulic head H [unit = m]
    - cd : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    base_width : FloatOrArray
        Sutro weir rectangular base width b [m].
    base_height : FloatOrArray
        Sutro weir base vertical crest height a [m].
    head : FloatOrArray
        Upstream / operating hydraulic head H [m].
    cd : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (b, a, h, cd_v), is_scalar = coerce_inputs(base_width, base_height, head, cd)
    g = 32.17405 if system.lower() == 'us' else 9.80665
    with np.errstate(all='ignore'):
        q = np.where((b <= 0) | (a <= 0) | (h < a), np.nan, cd_v * b * np.sqrt(2.0 * g * a) * (h - a / 3.0))
    return format_output(q, is_scalar)

def sutro_weir_h(discharge: FloatOrArray, base_width: FloatOrArray, base_height: FloatOrArray, cd: FloatOrArray=0.62, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Solves for required head H on Sutro weir.
    Units (Default SI): discharge [m^3/s], base_width [m], base_height [m], cd [dimensionless] -> returns [m]

    Formula:
    sutro_weir_h(discharge, base_width, base_height, cd, system)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - base_width : Sutro weir rectangular base width b [unit = m]
    - base_height : Sutro weir base vertical crest height a [unit = m]
    - cd : Discharge coefficient C_d [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    base_width : FloatOrArray
        Sutro weir rectangular base width b [m].
    base_height : FloatOrArray
        Sutro weir base vertical crest height a [m].
    cd : FloatOrArray
        Discharge coefficient C_d [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (q, b, a, cd_v), is_scalar = coerce_inputs(discharge, base_width, base_height, cd)
    g = 32.17405 if system.lower() == 'us' else 9.80665
    with np.errstate(all='ignore'):
        denom = cd_v * b * np.sqrt(2.0 * g * a)
        h = np.where((q <= 0) | (denom <= 0), np.nan, q / denom + a / 3.0)
    return format_output(h, is_scalar)

def hec18_pier_scour(pier_width: FloatOrArray, flow_depth: FloatOrArray, flow_velocity: FloatOrArray, k1: FloatOrArray=1.0, k2: FloatOrArray=1.0, k3: FloatOrArray=1.0, k4: FloatOrArray=1.0, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes bridge pier scour depth ys using the FHWA HEC-18 (Richardson & Davis CSU) formula.
    Units (Default SI): pier_width [m], flow_depth [m], flow_velocity [m/s], k1 [dimensionless], k2 [dimensionless], k3 [dimensionless], k4 [dimensionless] -> returns [standard SI units]

    Formula:
    y_s = 2.0 * K_1 * K_2 * K_3 * K_4 * y_1 * (a / y_1)^0.65 * Fr_1^0.43

    Where (Default SI Units):
    - pier_width : Bridge pier frontal width a [unit = m]
    - flow_depth : Upstream approach flow depth y_1 [unit = m]
    - flow_velocity : Upstream approach flow velocity V_1 [unit = m/s]
    - k1 : HEC-18 pier nose shape correction K_1 [unit = dimensionless]
    - k2 : HEC-18 flow angle of attack correction K_2 [unit = dimensionless]
    - k3 : HEC-18 bed condition correction K_3 [unit = dimensionless]
    - k4 : HEC-18 armoring bed sediment correction K_4 [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    pier_width : FloatOrArray
        Bridge pier frontal width a [m].
    flow_depth : FloatOrArray
        Upstream approach flow depth y_1 [m].
    flow_velocity : FloatOrArray
        Upstream approach flow velocity V_1 [m/s].
    k1 : FloatOrArray
        HEC-18 pier nose shape correction K_1 [dimensionless].
    k2 : FloatOrArray
        HEC-18 flow angle of attack correction K_2 [dimensionless].
    k3 : FloatOrArray
        HEC-18 bed condition correction K_3 [dimensionless].
    k4 : FloatOrArray
        HEC-18 armoring bed sediment correction K_4 [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (a, y, v, k1_v, k2_v, k3_v, k4_v), is_scalar = coerce_inputs(pier_width, flow_depth, flow_velocity, k1, k2, k3, k4)
    g = 32.17405 if system.lower() == 'us' else 9.80665
    with np.errstate(all='ignore'):
        fr = v / np.sqrt(g * y)
        ys = 2.0 * k1_v * k2_v * k3_v * k4_v * y * (a / y) ** 0.65 * fr ** 0.43
    return format_output(ys, is_scalar)

def hec18_pier_width(scour_depth: FloatOrArray, flow_depth: FloatOrArray, flow_velocity: FloatOrArray, k1: FloatOrArray=1.0, k2: FloatOrArray=1.0, k3: FloatOrArray=1.0, k4: FloatOrArray=1.0, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Solves for maximum permissible pier width 'a' for a given allowable scour depth.
    Units (Default SI): scour_depth [m], flow_depth [m], flow_velocity [m/s], k1 [dimensionless], k2 [dimensionless], k3 [dimensionless], k4 [dimensionless] -> returns [standard SI units]

    Formula:
    hec18_pier_width(scour_depth, flow_depth, flow_velocity, k1, k2, k3, k4, system)

    Where (Default SI Units):
    - scour_depth : Maximum local scour depth y_s [unit = m]
    - flow_depth : Upstream approach flow depth y_1 [unit = m]
    - flow_velocity : Upstream approach flow velocity V_1 [unit = m/s]
    - k1 : HEC-18 pier nose shape correction K_1 [unit = dimensionless]
    - k2 : HEC-18 flow angle of attack correction K_2 [unit = dimensionless]
    - k3 : HEC-18 bed condition correction K_3 [unit = dimensionless]
    - k4 : HEC-18 armoring bed sediment correction K_4 [unit = dimensionless]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    scour_depth : FloatOrArray
        Maximum local scour depth y_s [m].
    flow_depth : FloatOrArray
        Upstream approach flow depth y_1 [m].
    flow_velocity : FloatOrArray
        Upstream approach flow velocity V_1 [m/s].
    k1 : FloatOrArray
        HEC-18 pier nose shape correction K_1 [dimensionless].
    k2 : FloatOrArray
        HEC-18 flow angle of attack correction K_2 [dimensionless].
    k3 : FloatOrArray
        HEC-18 bed condition correction K_3 [dimensionless].
    k4 : FloatOrArray
        HEC-18 armoring bed sediment correction K_4 [dimensionless].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (ys, y, v, k1_v, k2_v, k3_v, k4_v), is_scalar = coerce_inputs(scour_depth, flow_depth, flow_velocity, k1, k2, k3, k4)
    g = 32.17405 if system.lower() == 'us' else 9.80665
    with np.errstate(all='ignore'):
        fr = v / np.sqrt(g * y)
        denom = 2.0 * k1_v * k2_v * k3_v * k4_v * y * fr ** 0.43
        a = y * (ys / denom) ** (1.0 / 0.65)
    return format_output(a, is_scalar)

"""
HydroAj: High-Performance Water Resources Engineering Framework by Ajay Bhattarai
Hybrid Rust + Python computational library.
"""

__version__ = "0.1.1"
__author__ = "Ajay Bhattarai (Civil Engineer, B.E. Civil Engineering)"
__email__ = "ajaybhattarai360@gmail.com"
__website__ = "https://ajaybhattarai-123.github.io/Personal-website/"
__linkedin__ = "https://www.linkedin.com/in/ajaybhattarai360/"
__repository__ = "https://github.com/ajaybhattarai-123/hydroaj"

from . import hydraulics
from . import hydrology
from . import structures
from . import groundwater
from . import sediment
from . import io

# Top-level direct imports for most frequent routines
from .hydraulics import (
    manning_discharge,
    manning_velocity,
    strickler_velocity,
    chezy_velocity,
    kutter_chezy_c,
    bazin_chezy_c,
    geom_rectangular,
    geom_trapezoidal,
    geom_triangular,
    geom_circular,
    geom_parabolic,
    specific_energy,
    froude_number,
    specific_force,
    critical_depth_rectangular,
    normal_depth_trapezoidal,
    belanger_conjugate_depth,
    hydraulic_jump_head_loss,
    hydraulic_jump_length,
    gvf_gradient,
    manning_friction_slope,
    direct_step,
    darcy_weisbach,
    reynolds_number,
    laminar_friction,
    colebrook_white,
    swamee_jain,
    haaland,
    churchill,
    wood,
    hazen_williams,
    hazen_williams_velocity,
    minor_loss,
    wave_celerity,
    joukowsky,
    critical_closure_time,
    optimal_rectangular_section,
    optimal_trapezoidal_section,
    optimal_triangular_section,
    critical_velocity,
    critical_slope,
    gravity_wave_celerity,
    hydraulic_jump_efficiency,
    hydraulic_jump_height,
    critical_depth_triangular,
    horton_einstein_composite_n,
    pavlovskii_composite_n,
    culvert_inlet_unsubmerged,
    culvert_inlet_submerged,
    culvert_outlet_control_head,
    culvert_entrance_loss,
    hardy_cross_correction,
    equivalent_pipe_length,
    equivalent_diameter_series,
    parallel_pipes_distribution,
    water_horsepower,
    pump_brake_power,
)

from .hydrology import (
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
    scs_composite_cn,
    scs_cn_amc_i,
    scs_cn_amc_iii,
    tr55_sheet_flow_time,
    tr55_shallow_concentrated_velocity,
    gumbel_flood_frequency,
    nash_cascade_iuh,
    hargreaves_samani_et0,
    net_radiation_equivalent_evap,
    time_area_runoff_step,
)

from .structures import (
    francis_weir,
    v_notch_weir,
    broad_crested_weir,
    parshall_flume,
    orifice_free,
    orifice_submerged,
    sluice_gate_free,
    sluice_gate_submerged,
    ogee_spillway_discharge,
    ogee_discharge_coefficient,
    spillway_effective_length,
    chute_terminal_velocity,
    stilling_basin_length,
    morning_glory_weir_flow,
    siphon_spillway_discharge,
    drop_structure_depth,
    tailwater_depth,
)

from .groundwater import (
    darcy_flow_1d,
    darcy_flux,
    thiem_confined,
    thiem_unconfined,
    theis_drawdown,
    cooper_jacob_drawdown,
)

from .sediment import (
    boundary_shear_stress,
    shear_velocity,
    shields_parameter,
    critical_shear_stress,
    lane_sediment_balance,
    meyer_peter_muller_bedload,
    rubey_settling_velocity,
    stokes_settling_velocity,
)

__all__ = [
    "hydraulics",
    "hydrology",
    "structures",
    "groundwater",
    "io",
    "manning_discharge",
    "manning_velocity",
    "strickler_velocity",
    "chezy_velocity",
    "kutter_chezy_c",
    "bazin_chezy_c",
    "geom_rectangular",
    "geom_trapezoidal",
    "geom_triangular",
    "geom_circular",
    "geom_parabolic",
    "specific_energy",
    "froude_number",
    "specific_force",
    "critical_depth_rectangular",
    "normal_depth_trapezoidal",
    "belanger_conjugate_depth",
    "hydraulic_jump_head_loss",
    "hydraulic_jump_length",
    "gvf_gradient",
    "manning_friction_slope",
    "direct_step",
    "darcy_weisbach",
    "reynolds_number",
    "laminar_friction",
    "colebrook_white",
    "swamee_jain",
    "haaland",
    "churchill",
    "wood",
    "hazen_williams",
    "hazen_williams_velocity",
    "minor_loss",
    "wave_celerity",
    "joukowsky",
    "critical_closure_time",
    "idf_sherman",
    "thiessen_areal",
    "horton_rate",
    "horton_cumulative",
    "green_ampt_rate",
    "scs_retention",
    "scs_runoff_depth",
    "rational_peak_flow",
    "kirpich_tc",
    "snyder",
    "scs_peak_flow",
    "muskingum_coefficients",
    "muskingum_route",
    "francis_weir",
    "v_notch_weir",
    "broad_crested_weir",
    "parshall_flume",
    "orifice_free",
    "orifice_submerged",
    "sluice_gate_free",
    "sluice_gate_submerged",
    "darcy_flow_1d",
    "darcy_flux",
    "thiem_confined",
    "thiem_unconfined",
    "theis_drawdown",
    "cooper_jacob_drawdown",
]



# Dedicated Bidirectional Inversions & Suffix Standards
from .hydraulics import (
    manning_q, manning_n, manning_s0, manning_rh, manning_a, manning_v,
    manning_roughness, manning_slope, manning_hydraulic_radius, manning_area,
    strickler_v, strickler_kst, strickler_s0, strickler_roughness, strickler_slope,
    chezy_v, chezy_c, chezy_s0, chezy_rh, chezy_coefficient, chezy_slope, chezy_hydraulic_radius,
    froude_fr, froude_v, froude_dh, froude_velocity, froude_hydraulic_depth,
    specific_energy_e, specific_energy_v, specific_energy_velocity,
    hydraulic_jump_y2, hydraulic_jump_fr1, hydraulic_jump_y1, hydraulic_jump_froude_1, hydraulic_jump_depth_1,
    critical_depth_rect_yc, critical_depth_rect_q, critical_discharge_rectangular,
    critical_depth_tri_yc, critical_depth_tri_q, critical_discharge_triangular,
    critical_velocity_vc, critical_velocity_dh, critical_hydraulic_depth,
    critical_slope_sc, critical_slope_n, critical_slope_roughness,
    darcy_weisbach_hf, darcy_weisbach_head_loss,
    darcy_weisbach_f, darcy_weisbach_friction_factor,
    darcy_weisbach_d, darcy_weisbach_diameter,
    darcy_weisbach_l, darcy_weisbach_length,
    darcy_weisbach_v, darcy_weisbach_velocity,
    darcy_weisbach_q, darcy_weisbach_discharge,
    hazen_williams_hf, hazen_williams_head_loss,
    hazen_williams_q, hazen_williams_discharge,
    hazen_williams_d, hazen_williams_diameter,
    hazen_williams_l, hazen_williams_length,
    hazen_williams_c, hazen_williams_roughness,
    hazen_williams_v, hazen_williams_s, hazen_williams_slope,
    reynolds_re, reynolds_v, reynolds_d, reynolds_velocity, reynolds_diameter,
    minor_loss_hm, minor_loss_head, minor_loss_kl, minor_loss_coeff, minor_loss_v, minor_loss_velocity,
    joukowsky_dp, joukowsky_pressure, joukowsky_dv, joukowsky_delta_velocity, joukowsky_a, joukowsky_celerity,
    critical_closure_tc, critical_closure_l, critical_closure_length, critical_closure_a, critical_closure_celerity,
    equivalent_pipe_le, equivalent_pipe_kl, equivalent_pipe_loss_coeff, equivalent_pipe_f, equivalent_pipe_friction_factor,
    water_power_pw, water_power_q, water_power_discharge, water_power_h, water_power_head,
    pump_power_pb, pump_power_pw, pump_water_power, pump_power_eta, pump_efficiency,
)

from .hydrology import (
    rational_q, rational_c, rational_i, rational_a,
    rational_runoff_coeff, rational_intensity, rational_drainage_area,
    scs_cn_s, scs_cn_cn, scs_curve_number, scs_cn_q, scs_cn_p, scs_precipitation,
    horton_rate_fp, horton_rate_f0, horton_rate_fc, horton_rate_k,
    horton_initial_rate, horton_constant_rate, horton_decay_rate,
    kirpich_s, kirpich_l, kirpich_slope, kirpich_length,
    scs_amc_cni, scs_amc_cniii, scs_amc_cnii_from_i, scs_amc_cnii_from_iii,
    scs_cn_ii_from_i, scs_cn_ii_from_iii,
    tr55_shallow_v, tr55_shallow_s, tr55_shallow_slope,
    hargreaves_et0, hargreaves_ra, hargreaves_radiation,
)

from .structures import (
    francis_weir_q, francis_weir_l, francis_weir_length,
    v_notch_weir_q, v_notch_weir_h, v_notch_weir_head, v_notch_weir_cd, v_notch_weir_coeff,
    v_notch_weir_theta, v_notch_weir_angle,
    broad_crested_weir_q, broad_crested_weir_h, broad_crested_weir_head, broad_crested_weir_l, broad_crested_weir_crest_length,
    orifice_free_q, orifice_free_h, orifice_free_head, orifice_free_ao, orifice_free_area,
    sluice_gate_free_q, sluice_gate_free_a, sluice_gate_free_opening,
    ogee_spillway_q, ogee_spillway_he, ogee_spillway_head, ogee_spillway_le, ogee_spillway_length,
    chute_velocity_v, chute_velocity_z, chute_elevation,
    stilling_basin_y2, stilling_basin_depth_2, stilling_basin_y1, stilling_basin_depth_1,
)

from .groundwater import (
    darcy_flow_q, darcy_flow_k, darcy_hydraulic_conductivity, darcy_flow_dh_dl, darcy_hydraulic_gradient,
    thiem_confined_q, thiem_confined_t, thiem_confined_transmissivity, thiem_confined_dh, thiem_confined_drawdown_diff,
    thiem_unconfined_q, thiem_unconfined_k, thiem_unconfined_conductivity,
    cooper_jacob_s, cooper_jacob_q, cooper_jacob_pumping_rate,
)

from .sediment import (
    boundary_shear_tau0, boundary_shear_s0, boundary_shear_slope, boundary_shear_rh, boundary_shear_hydraulic_radius,
    shields_param_theta, shields_param_tau0, shields_shear_stress, shields_param_d50, shields_grain_size,
    lane_balance_qs, lane_balance_s, lane_balance_slope,
    stokes_settling_ws, stokes_settling_d, stokes_settling_diameter,
)

# --- Extended Hydrology Suite ---
from .hydrology import (
    faa_tc, faa_l, faa_s, faa_c,
    kerby_tc, kerby_l, kerby_s, kerby_n,
    bransby_williams_tc, bransby_williams_l, bransby_williams_a, bransby_williams_s,
    tr55_channel_tc, tr55_composite_tc,
    dickens_q, dickens_cd, dickens_area,
    ryves_q, ryves_cr, ryves_area,
    inglis_q, inglis_area,
    nawab_jung_q, nawab_jung_cn, nawab_jung_area,
    fuller_flood_q, fuller_return_period,
    philip_rate, philip_cumulative, philip_sorptivity,
    kostiakov_rate, kostiakov_cumulative, kostiakov_time,
    green_ampt_ponding_time,
    saturation_vapor_pressure, vapor_pressure_slope,
    fao56_penman_monteith, fao56_net_radiation,
    priestley_taylor_et, blaney_criddle_et, blaney_criddle_temp,
    scs_unit_hydrograph_peak, scs_uh_tp, scs_uh_area, scs_lag_time, scs_time_to_peak,
    snyder_lag_time, snyder_peak_discharge, snyder_hydrograph_widths,
    muskingum_cunge_parameters, baseflow_lyne_hollick,
    gumbel_reduced_variate, gumbel_return_period, gumbel_frequency_factor,
    gumbel_design_flood, gumbel_return_period_from_flood,
    log_pearson_3_flood, weibull_plotting_position, gringorten_plotting_position, cunnane_plotting_position,
)

# --- Extended Hydraulics & Alluvial Regime Suite ---
from .hydraulics import (
    lacey_silt_factor, lacey_d50, lacey_regime_velocity, lacey_velocity_discharge,
    lacey_wetted_perimeter, lacey_perimeter_discharge, lacey_hydraulic_radius,
    lacey_regime_slope, lacey_slope_discharge, lacey_regime_scour_depth,
    kennedy_critical_velocity, kennedy_critical_depth,
    channel_expansion_loss, channel_contraction_loss,
    blasius_friction_factor, cavitation_index, cavitation_velocity,
)

# --- Extended Structures Suite ---
from .structures import (
    cipoletti_weir_q, cipoletti_weir_l, cipoletti_weir_h,
    sutro_weir_q, sutro_weir_h,
    hec18_pier_scour, hec18_pier_width,
)

# --- Extended Groundwater Suite ---
from .groundwater import (
    ghyben_herzberg_depth, ghyben_herzberg_head,
    jacob_well_drawdown, jacob_well_efficiency, jacob_well_b, jacob_well_c,
    hantush_leakage_factor, specific_capacity_to_transmissivity,
)

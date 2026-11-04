"""
Enriches docstrings and type annotations across all hydrocivil modules
for premier VS Code IntelliSense, signature help, and interactive help().
"""

import os
import re
import ast
import json

CATALOG_PATH = os.path.join(os.path.dirname(__file__), "formula_catalog.json")

# Parameter descriptions and units dictionary
PARAM_METADATA = {
    "area": ("Cross-sectional flow area A", "m^2", "ft^2", "> 0"),
    "hydraulic_radius": ("Hydraulic radius R_h = A / P", "m", "ft", "> 0"),
    "slope": ("Longitudinal channel bed / energy gradient S_0", "m/m", "ft/ft", ">= 0"),
    "roughness": ("Manning roughness coefficient n", "s/m^(1/3)", "s/ft^(1/3)", "0.009 - 0.150"),
    "discharge": ("Volumetric flow rate / discharge Q", "m^3/s", "ft^3/s", "> 0"),
    "velocity": ("Mean cross-sectional flow velocity V", "m/s", "ft/s", ">= 0"),
    "diameter": ("Internal pipe diameter D", "m", "ft", "> 0"),
    "length": ("Reach / conduit length L", "m", "ft", "> 0"),
    "friction_factor": ("Darcy-Weisbach friction factor f", "dimensionless", "dimensionless", "> 0"),
    "head_loss": ("Frictional energy head loss h_f", "m", "ft", ">= 0"),
    "head": ("Total upstream / operating hydraulic head H", "m", "ft", ">= 0"),
    "depth": ("Flow depth y", "m", "ft", ">= 0"),
    "initial_depth": ("Initial supercritical flow depth y_1 before jump", "m", "ft", "> 0"),
    "sequent_depth": ("Subcritical conjugate flow depth y_2 after jump", "m", "ft", "> 0"),
    "froude_1": ("Supercritical inflow Froude number Fr_1", "dimensionless", "dimensionless", "> 1.0"),
    "froude_number": ("Froude number Fr = V / sqrt(g * D_h)", "dimensionless", "dimensionless", ">= 0"),
    "reynolds_number": ("Reynolds number Re = V * D / nu", "dimensionless", "dimensionless", "> 0"),
    "roughness_c": ("Hazen-Williams roughness coefficient C", "dimensionless", "dimensionless", "typically 80 - 150"),
    "minor_loss_k": ("Minor head loss form resistance coefficient K_L", "dimensionless", "dimensionless", ">= 0"),
    "power": ("Pumping or hydro-turbine mechanical / electrical power P", "W or kW", "hp", ">= 0"),
    "efficiency": ("Pumping station overall wire-to-water efficiency eta", "decimal (0-1)", "decimal (0-1)", "0.0 - 1.0"),
    "c_mod": ("Pipe wall anchoring restraint parameter c_1", "dimensionless", "dimensionless", "0.7 - 1.25"),
    "wave_speed": ("Acoustic pressure wave celerity a", "m/s", "ft/s", "> 0"),
    "runoff_coeff": ("Rational runoff coefficient C", "dimensionless", "dimensionless", "0.05 - 0.95"),
    "intensity": ("Design rainfall intensity I", "mm/hr", "in/hr", "> 0"),
    "drainage_area": ("Catchment watershed drainage area A", "ha or km^2", "acres", "> 0"),
    "curve_number": ("SCS / NRCS runoff curve number CN", "dimensionless", "dimensionless", "30 - 100"),
    "precipitation": ("Cumulative rainfall storm depth P", "mm", "inches", ">= 0"),
    "retention": ("Potential maximum soil retention S", "mm", "inches", ">= 0"),
    "initial_rate": ("Initial Horton infiltration capacity f_0", "mm/hr", "in/hr", "> 0"),
    "steady_rate": ("Ultimate steady Horton infiltration capacity f_c", "mm/hr", "in/hr", ">= 0"),
    "decay_constant": ("Horton exponential recession decay factor k", "1/hr", "1/hr", "> 0"),
    "time": ("Elapsed infiltration / routing time t", "hr", "hr", ">= 0"),
    "transmissivity": ("Aquifer transmissivity T = K * b", "m^2/s", "ft^2/s", "> 0"),
    "hydraulic_conductivity": ("Darcy saturated hydraulic conductivity K", "m/s", "ft/s", "> 0"),
    "storativity": ("Aquifer storativity / storage coefficient S", "dimensionless", "dimensionless", "1e-5 - 0.3"),
    "radius_1": ("Radial observation distance to observation well 1 (r_1)", "m", "ft", "> 0"),
    "radius_2": ("Radial observation distance to observation well 2 (r_2)", "m", "ft", "> 0"),
    "delta_head": ("Piezometric drawdown difference (h_2 - h_1)", "m", "ft", "> 0"),
    "bottom_width": ("Channel bottom base width b", "m", "ft", "> 0"),
    "side_slope": ("Canal side slope ratio m (1V : mH)", "dimensionless", "dimensionless", ">= 0"),
    "top_width": ("Free surface top width T", "m", "ft", "> 0"),
    "contractions": ("Number of side end contractions n_e (0, 1, or 2)", "integer", "integer", "0, 1, or 2"),
    "notch_angle_deg": ("Apex angle of triangular V-notch weir theta", "degrees", "degrees", "20 - 120"),
    "discharge_coeff": ("Discharge coefficient C_d", "dimensionless", "dimensionless", "0.4 - 2.5"),
    "opening": ("Sluice gate vertical opening height w", "m", "ft", "> 0"),
    "width": ("Sluice gate / channel flume clear width b", "m", "ft", "> 0"),
    "system": ("Governing unit system ('si' for metric, 'us' for US customary)", "str", "str", "'si' or 'us'"),
}


def get_param_doc(pname: str) -> str:
    clean = pname.lower().strip()
    if clean == "system":
        return f"{pname} : {{'si', 'us'}}, default='si'\n        Unit system to apply ('si' for metric units, 'us' for US customary units)."
    if clean in PARAM_METADATA:
        desc, si, us, bounds = PARAM_METADATA[clean]
        return f"{pname} : FloatOrArray\n        {desc} [{si} in SI, {us} in US]. Bounds: {bounds}."
    
    # Heuristics
    if "system" in clean:
        return f"{pname} : {{'si', 'us'}}, default='si'\n        Unit system to apply ('si' for metric units, 'us' for US customary units)."
    if "slope" in clean or "s0" in clean:
        return f"{pname} : FloatOrArray\n        Longitudinal bed slope / hydraulic gradient S_0 [m/m or ft/ft]."
    if "roughness" in clean or "rough" in clean or clean == "n":
        return f"{pname} : FloatOrArray\n        Roughness resistance coefficient [s/m^(1/3) or dimensionless]."
    if "diam" in clean or clean == "d":
        return f"{pname} : FloatOrArray\n        Conduit / pipe diameter D [m in SI, ft in US]."
    if "length" in clean or clean == "l":
        return f"{pname} : FloatOrArray\n        Reach length L [m in SI, ft in US]."
    if "area" in clean or clean == "a":
        return f"{pname} : FloatOrArray\n        Cross-sectional area A [m^2 in SI, ft^2 in US]."
    if "depth" in clean or clean == "y":
        return f"{pname} : FloatOrArray\n        Water flow depth y [m in SI, ft in US]."
    if "head" in clean or clean == "h" or "hf" in clean:
        return f"{pname} : FloatOrArray\n        Total hydraulic head or head loss [m in SI, ft in US]."
    if "disch" in clean or clean == "q":
        return f"{pname} : FloatOrArray\n        Discharge / volumetric flow rate Q [m^3/s in SI, ft^3/s in US]."
    if "vel" in clean or clean == "v":
        return f"{pname} : FloatOrArray\n        Flow velocity V [m/s in SI, ft/s in US]."
    
    return f"{pname} : FloatOrArray\n        Input parameter {pname}."


def generate_docstring(func_name: str, params: list, cat_entry: dict = None, existing_doc: str = "") -> str:
    eq = ""
    desc = ""
    lit = ""
    
    if cat_entry:
        eq = cat_entry.get("governing_equation", "")
        desc = f"Computes {cat_entry.get('canonical_name', func_name).replace('_', ' ')}."
        lit = cat_entry.get("literature_source", "")
    elif existing_doc:
        first_line = existing_doc.strip().split("\n")[0]
        desc = first_line
        # Check if formula in existing doc
        lines = existing_doc.strip().split("\n")
        for line in lines:
            if "=" in line and ("Q" in line or "V" in line or "h_f" in line or "S_0" in line or "f" in line or "T" in line):
                eq = line.strip()
                break

    if not desc:
        desc = f"Calculates {func_name.replace('_', ' ')}."
    if not eq:
        eq = f"{func_name}({', '.join(params)})"

    param_docs = "\n    ".join([get_param_doc(p) for p in params])

    ret_type = "float | np.ndarray"
    ret_desc = "Computed numerical result. Returns float for scalar inputs, np.ndarray for array inputs."
    if "geom_" in func_name:
        ret_type = "Tuple[float | np.ndarray, ...]"
        ret_desc = "Geometric properties tuple (Area, Wetted Perimeter, Hydraulic Radius, Top Width, Hydraulic Depth)."
    elif "muskingum_coefficients" in func_name:
        ret_type = "Tuple[float | np.ndarray, float | np.ndarray, float | np.ndarray]"
        ret_desc = "Routing coefficients tuple (C_0, C_1, C_2)."

    doc = f'''"""
    {desc}

    Formula:
        {eq}

    Parameters
    ----------
    {param_docs}

    Returns
    -------
    {ret_type}
        {ret_desc}
    """'''
    return doc


def process_python_file(filepath: str, catalog: dict):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure header imports
    header_check = "FloatOrArray = Union[float, int, Sequence[float], np.ndarray]"
    if header_check not in content:
        # replace typing import
        old_import = "from typing import Any, Tuple, Union"
        new_import = "from typing import Any, Tuple, Union, Sequence, Optional\ntry:\n    from typing import Literal\nexcept ImportError:\n    from typing_extensions import Literal  # type: ignore\n\nFloatOrArray = Union[float, int, Sequence[float], np.ndarray]"
        if old_import in content:
            content = content.replace(old_import, new_import, 1)
        elif "from typing import Any, Union" in content:
            content = content.replace("from typing import Any, Union", new_import, 1)
        elif "from typing import" in content:
            # prepend FloatOrArray definition after typing import
            content = re.sub(r'(from typing import [^\n]+)', r'\1\ntry:\n    from typing import Literal\nexcept ImportError:\n    from typing_extensions import Literal  # type: ignore\n\nFloatOrArray = Union[float, int, Sequence[float], np.ndarray]', content, count=1)

    # Now update function signatures and docstrings
    tree = ast.parse(content)
    
    # We want to replace parameter annotations from Any to FloatOrArray
    # and system: str = "si" to system: Literal["si", "us"] = "si"
    # and replace/enhance docstrings
    
    # Pattern-based replacement for robustness
    # Find `def func_name(...) -> ...:`
    func_pattern = re.compile(r'def\s+([a-zA-Z0-9_]+)\s*\((.*?)\)\s*->\s*(.*?):\s*(?:"""(.*?)""")?', re.DOTALL)
    
    def replacer(match):
        fname = match.group(1)
        params_str = match.group(2)
        ret_str = match.group(3)
        old_doc = match.group(4) or ""
        
        if fname.startswith("_"):
            return match.group(0) # Keep private functions as is
            
        # Parse params
        params_lines = [p.strip() for p in params_str.split(",") if p.strip()]
        new_params = []
        param_names = []
        for p in params_lines:
            p_parts = p.split(":")
            pname = p_parts[0].strip()
            param_names.append(pname)
            
            if pname == "system":
                new_params.append('    system: Literal["si", "us"] = "si"')
            elif "=" in p:
                p_def = p.split("=")[1].strip()
                new_params.append(f'    {pname}: FloatOrArray = {p_def}')
            elif ":" in p:
                new_params.append(f'    {pname}: FloatOrArray')
            else:
                new_params.append(f'    {pname}: FloatOrArray')
                
        cat_entry = catalog.get(fname)
        new_doc = generate_docstring(fname, param_names, cat_entry, old_doc)
        
        formatted_params = ",\n".join(new_params)
        if formatted_params:
            formatted_params = "\n" + formatted_params + ",\n"
            
        return f"def {fname}({formatted_params}) -> {ret_str.strip()}:\n    {new_doc}"

    # Apply replacement
    content = func_pattern.sub(replacer, content)
    
    # Validate syntax with AST
    ast.parse(content)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully enriched: {filepath}")


def main():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        cat_list = json.load(f)
    catalog = {c["canonical_name"]: c for c in cat_list}
    
    module_dir = os.path.join(os.path.dirname(__file__), "..", "python", "hydrocivil")
    targets = [
        "hydraulics.py",
        "hydrology.py",
        "structures.py",
        "groundwater.py",
        "sediment.py"
    ]
    
    for t in targets:
        path = os.path.join(module_dir, t)
        if os.path.exists(path):
            process_python_file(path, catalog)


if __name__ == "__main__":
    main()

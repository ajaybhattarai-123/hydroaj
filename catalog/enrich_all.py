"""
Robust AST-driven Docstring & Type Annotation Enhancer for hydrocivil modules.
Ensures 100% syntactic validity and rich VS Code IntelliSense / help() formatting.
"""

import os
import ast
import json

CATALOG_PATH = os.path.join(os.path.dirname(__file__), "formula_catalog.json")

PARAM_DOCS = {
    "area": ("Cross-sectional flow area A", "m^2", "ft^2", "> 0"),
    "hydraulic_radius": ("Hydraulic radius R_h = A / P", "m", "ft", "> 0"),
    "slope": ("Longitudinal channel bed / energy gradient S_0", "m/m", "ft/ft", ">= 0"),
    "roughness": ("Manning roughness coefficient n", "s/m^(1/3)", "s/ft^(1/3)", "0.009 - 0.150"),
    "discharge": ("Volumetric flow rate / discharge Q", "m^3/s", "ft^3/s", "> 0"),
    "velocity": ("Mean cross-sectional flow velocity V", "m/s", "ft/s", ">= 0"),
    "diameter": ("Internal conduit / pipe diameter D", "m", "ft", "> 0"),
    "length": ("Reach / pipeline conduit length L", "m", "ft", "> 0"),
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
    "power": ("Mechanical / electrical power P", "W or kW", "hp", ">= 0"),
    "efficiency": ("Overall pump wire-to-water efficiency eta", "decimal (0-1)", "decimal (0-1)", "0.0 - 1.0"),
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
}


def build_param_line(pname: str) -> str:
    clean = pname.lower().strip()
    if clean == "system":
        return f"{pname} : {{'si', 'us'}}, default='si'\n        Unit system to apply ('si' for metric units, 'us' for US customary units)."
    if clean in PARAM_DOCS:
        desc, si, us, bounds = PARAM_DOCS[clean]
        return f"{pname} : FloatOrArray\n        {desc} [{si} in SI, {us} in US]. Bounds: {bounds}."
    
    # Heuristics
    if "slope" in clean or "s0" in clean:
        return f"{pname} : FloatOrArray\n        Longitudinal bed slope / hydraulic gradient S_0 [m/m or ft/ft]."
    if "roughness" in clean or "rough" in clean or clean in ("n", "c", "k_st"):
        return f"{pname} : FloatOrArray\n        Roughness resistance coefficient [s/m^(1/3) or dimensionless]."
    if "diam" in clean or clean == "d":
        return f"{pname} : FloatOrArray\n        Internal conduit diameter D [m in SI, ft in US]."
    if "length" in clean or clean == "l":
        return f"{pname} : FloatOrArray\n        Reach length L [m in SI, ft in US]."
    if "area" in clean or clean == "a":
        return f"{pname} : FloatOrArray\n        Cross-sectional area A [m^2 in SI, ft^2 in US]."
    if "depth" in clean or clean == "y":
        return f"{pname} : FloatOrArray\n        Water depth y [m in SI, ft in US]."
    if "head" in clean or clean == "h" or "hf" in clean:
        return f"{pname} : FloatOrArray\n        Hydraulic head or head loss [m in SI, ft in US]."
    if "disch" in clean or clean == "q":
        return f"{pname} : FloatOrArray\n        Discharge / volumetric flow rate Q [m^3/s in SI, ft^3/s in US]."
    if "vel" in clean or clean == "v":
        return f"{pname} : FloatOrArray\n        Mean flow velocity V [m/s in SI, ft/s in US]."
    
    return f"{pname} : FloatOrArray\n        Input parameter '{pname}'."


def generate_docstring(func_name: str, arg_names: list, cat_entry: dict, existing_doc: str) -> str:
    eq = ""
    desc = ""
    if cat_entry:
        eq = cat_entry.get("governing_equation", "")
        desc = f"Computes {func_name.replace('_', ' ')}."
    elif existing_doc:
        first = existing_doc.strip().split("\n")[0]
        desc = first
        for line in existing_doc.strip().split("\n"):
            if "=" in line and any(sym in line for sym in ["Q", "V", "h_f", "S_0", "f", "T", "y", "q"]):
                eq = line.strip()
                break

    if not desc:
        desc = f"Calculates {func_name.replace('_', ' ')}."
    if not eq:
        eq = f"{func_name}({', '.join(arg_names)})"

    param_docs = "\n    ".join([build_param_line(p) for p in arg_names])

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


class FunctionDocstringTransformer(ast.NodeTransformer):
    def __init__(self, catalog):
        super().__init__()
        self.catalog = catalog

    def visit_FunctionDef(self, node):
        if node.name.startswith("_"):
            return node

        # Extract arg names
        arg_names = [a.arg for a in node.args.args]

        # Update annotations to FloatOrArray or Literal
        for a in node.args.args:
            if a.arg == "system":
                a.annotation = ast.Subscript(
                    value=ast.Name(id="Literal", ctx=ast.Load()),
                    slice=ast.Tuple(
                        elts=[
                            ast.Constant(value="si"),
                            ast.Constant(value="us")
                        ],
                        ctx=ast.Load()
                    ),
                    ctx=ast.Load()
                )
            else:
                a.annotation = ast.Name(id="FloatOrArray", ctx=ast.Load())

        # Extract existing docstring if any
        existing_doc = ""
        doc_node = None
        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
            existing_doc = node.body[0].value.value
            doc_node = node.body[0]

        cat_entry = self.catalog.get(node.name)
        new_doc_str = generate_docstring(node.name, arg_names, cat_entry, existing_doc)
        
        # Clean indentation
        clean_doc_lines = [l.strip() for l in new_doc_str.replace('"""', '').strip().split("\n")]
        formatted_doc = "\n" + "\n".join("    " + l if l else "" for l in clean_doc_lines) + "\n    "

        new_doc_expr = ast.Expr(value=ast.Constant(value=formatted_doc))

        if doc_node is not None:
            node.body[0] = new_doc_expr
        else:
            node.body.insert(0, new_doc_expr)

        return node


def process_module(filepath: str, catalog: dict):
    with open(filepath, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)

    # Check / inject typing imports at top if missing
    has_float_or_array = any(
        isinstance(stmt, ast.Assign) and any(getattr(t, "id", None) == "FloatOrArray" for t in stmt.targets)
        for stmt in tree.body
    )
    if not has_float_or_array:
        # Prepend typing headers
        typing_header = """from typing import Any, Tuple, Union, Sequence, Optional
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
import numpy as np

FloatOrArray = Union[float, int, Sequence[float], np.ndarray]
"""
        header_tree = ast.parse(typing_header)
        tree.body = header_tree.body + tree.body

    transformer = FunctionDocstringTransformer(catalog)
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    new_src = ast.unparse(new_tree)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_src + "\n")
    print(f"Successfully processed: {filepath}")


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
            process_module(path, catalog)


if __name__ == "__main__":
    main()

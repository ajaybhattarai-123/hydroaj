//! Parallel batch root-finding solvers.
//!
//! Provides Newton-Raphson and Brent's method solvers that operate on
//! entire arrays in parallel using Rayon, releasing the GIL via PyO3.

use rayon::prelude::*;

/// Maximum iterations for Newton-Raphson convergence.
const NEWTON_MAX_ITER: usize = 100;
/// Convergence tolerance.
const NEWTON_TOL: f64 = 1e-12;
/// Perturbation for numerical derivative.
const NEWTON_DX: f64 = 1e-10;

/// Maximum iterations for Brent's method.
const BRENT_MAX_ITER: usize = 100;
/// Convergence tolerance for Brent's method.
const BRENT_TOL: f64 = 1e-12;

/// Parallel batch Newton-Raphson solver.
///
/// Given a function `f(x, params) -> f64` and its derivative `df(x, params) -> f64`,
/// solves f(x) = 0 for each element in the initial guess array.
///
/// Returns NaN for any element that fails to converge or encounters invalid values.
pub fn batch_newton_raphson<F, DF>(
    x0: &[f64],
    f: F,
    df: DF,
) -> Vec<f64>
where
    F: Fn(f64, usize) -> f64 + Sync,
    DF: Fn(f64, usize) -> f64 + Sync,
{
    x0.par_iter()
        .enumerate()
        .map(|(idx, &x_init)| {
            if x_init.is_nan() || x_init.is_infinite() {
                return f64::NAN;
            }
            let mut x = x_init;
            for _ in 0..NEWTON_MAX_ITER {
                let fx = f(x, idx);
                if fx.is_nan() || fx.is_infinite() {
                    return f64::NAN;
                }
                if fx.abs() < NEWTON_TOL {
                    return x;
                }
                let dfx = df(x, idx);
                if dfx.abs() < 1e-30 {
                    return f64::NAN; // derivative too small
                }
                let x_new = x - fx / dfx;
                if (x_new - x).abs() < NEWTON_TOL {
                    return x_new;
                }
                x = x_new;
            }
            f64::NAN // failed to converge
        })
        .collect()
}

/// Parallel batch Newton-Raphson solver using numerical differentiation.
///
/// Uses central differences to approximate the derivative automatically.
pub fn batch_newton_numerical<F>(
    x0: &[f64],
    f: F,
) -> Vec<f64>
where
    F: Fn(f64, usize) -> f64 + Sync,
{
    x0.par_iter()
        .enumerate()
        .map(|(idx, &x_init)| {
            if x_init.is_nan() || x_init.is_infinite() || x_init <= 0.0 {
                return f64::NAN;
            }
            let mut x = x_init;
            for _ in 0..NEWTON_MAX_ITER {
                let fx = f(x, idx);
                if fx.is_nan() || fx.is_infinite() {
                    return f64::NAN;
                }
                if fx.abs() < NEWTON_TOL {
                    return x;
                }
                // Central difference derivative
                let dx = NEWTON_DX.max(x.abs() * 1e-8);
                let dfx = (f(x + dx, idx) - f(x - dx, idx)) / (2.0 * dx);
                if dfx.abs() < 1e-30 {
                    return f64::NAN;
                }
                let x_new = x - fx / dfx;
                if x_new <= 0.0 {
                    // Bisect if Newton step goes negative
                    let x_new = x / 2.0;
                    if x_new < NEWTON_TOL {
                        return f64::NAN;
                    }
                    x = x_new;
                    continue;
                }
                if (x_new - x).abs() < NEWTON_TOL * x.abs().max(1.0) {
                    return x_new;
                }
                x = x_new;
            }
            x // return best estimate
        })
        .collect()
}

/// Parallel batch Brent's method solver.
///
/// Finds a root of f(x) = 0 in [a, b] for each element.
/// Requires that f(a) and f(b) have opposite signs.
pub fn batch_brent<F>(
    a: &[f64],
    b: &[f64],
    f: F,
) -> Vec<f64>
where
    F: Fn(f64, usize) -> f64 + Sync,
{
    a.par_iter()
        .zip(b.par_iter())
        .enumerate()
        .map(|(idx, (&a_val, &b_val))| {
            brent_single(a_val, b_val, |x| f(x, idx))
        })
        .collect()
}

/// Single-element Brent's method.
fn brent_single<F>(mut a: f64, mut b: f64, f: F) -> f64
where
    F: Fn(f64) -> f64,
{
    let mut fa = f(a);
    let mut fb = f(b);

    if fa.is_nan() || fb.is_nan() {
        return f64::NAN;
    }
    // Require sign change
    if fa * fb > 0.0 {
        return f64::NAN;
    }

    if fa.abs() < fb.abs() {
        std::mem::swap(&mut a, &mut b);
        std::mem::swap(&mut fa, &mut fb);
    }

    let mut c = a;
    let mut fc = fa;
    let mut d = b - a;
    let mut e = d;
    let mut _mflag = true;

    for _ in 0..BRENT_MAX_ITER {
        if fb.abs() < BRENT_TOL {
            return b;
        }
        if fa.abs() < BRENT_TOL {
            return a;
        }
        if (b - a).abs() < BRENT_TOL {
            return b;
        }

        let s;
        if (fa - fc).abs() > BRENT_TOL && (fb - fc).abs() > BRENT_TOL {
            // Inverse quadratic interpolation
            s = a * fb * fc / ((fa - fb) * (fa - fc))
                + b * fa * fc / ((fb - fa) * (fb - fc))
                + c * fa * fb / ((fc - fa) * (fc - fb));
        } else {
            // Secant method
            s = b - fb * (b - a) / (fb - fa);
        }

        // Conditions for bisection
        let cond1 = if a < b {
            s < (3.0 * a + b) / 4.0 || s > b
        } else {
            s > (3.0 * a + b) / 4.0 || s < b
        };

        if cond1 || (s - b).abs() >= (d).abs() / 2.0 {
            // Bisection
            let s_bisect = (a + b) / 2.0;
            d = b - a;
            e = d;
            let fs = f(s_bisect);
            if fs.is_nan() {
                return f64::NAN;
            }
            c = b;
            fc = fb;
            if fa * fs < 0.0 {
                b = s_bisect;
                fb = fs;
            } else {
                a = s_bisect;
                fa = fs;
            }
        } else {
            d = e;
            e = s - b;
            let fs = f(s);
            if fs.is_nan() {
                return f64::NAN;
            }
            c = b;
            fc = fb;
            if fa * fs < 0.0 {
                b = s;
                fb = fs;
            } else {
                a = s;
                fa = fs;
            }
        }

        if fa.abs() < fb.abs() {
            std::mem::swap(&mut a, &mut b);
            std::mem::swap(&mut fa, &mut fb);
        }
    }

    b
}


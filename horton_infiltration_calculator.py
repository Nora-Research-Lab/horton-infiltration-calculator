import numpy as np

def compute_horton(f0, fc, k, t_start, t_end, dt):
    """
    Compute infiltration using Horton's equation.

    Parameters
    ----------
    f0 : float
        Initial infiltration rate (mm/hr). Must be > fc.
    fc : float
        Steady infiltration rate (mm/hr). Must be positive.
    k : float
        Decay constant (1/hr). Must be positive.
    t_start : float
        Start time (hours). Must be >= 0.
    t_end : float
        End time (hours). Must be > t_start.
    dt : float
        Time step (hours). Must be positive.

    Returns
    -------
    dict with keys:
        t          : ndarray of time values
        f_t        : ndarray of infiltration rates
        F_t        : ndarray of cumulative infiltration
        fc         : steady rate (for plotting)
        F_total    : cumulative infiltration at t_end
        time_to_steady : first time when f(t) <= 1.05*fc, or None
    """
    # Input validation
    try:
        f0 = float(f0)
        fc = float(fc)
        k = float(k)
        t_start = float(t_start)
        t_end = float(t_end)
        dt = float(dt)
    except (TypeError, ValueError):
        raise ValueError("All inputs must be numeric.")

    if f0 <= fc:
        raise ValueError(f"Initial infiltration rate f0 ({f0}) must be greater than steady rate fc ({fc}).")
    if fc <= 0:
        raise ValueError("Steady infiltration rate fc must be positive.")
    if k <= 0:
        raise ValueError("Decay constant k must be positive.")
    if t_start < 0:
        raise ValueError("Start time t_start must be >= 0.")
    if t_end <= t_start:
        raise ValueError("End time t_end must be greater than start time t_start.")
    if dt <= 0:
        raise ValueError("Time step dt must be positive.")

    # Generate time vector
    t = np.arange(t_start, t_end + dt, dt)
    if len(t) == 0:
        raise ValueError("Time vector is empty. Check t_start, t_end, dt.")

    # Horton infiltration rate
    f_t = fc + (f0 - fc) * np.exp(-k * t)

    # Cumulative infiltration
    F_t = fc * t + (f0 - fc) / k * (1 - np.exp(-k * t))

    # Total infiltration at final time (last element)
    F_total = float(F_t[-1])

    # Time to reach near‑steady state (within 5% of fc)
    threshold = fc * 1.05
    indices = np.where(f_t <= threshold)[0]
    if len(indices) > 0:
        time_to_steady = float(t[indices[0]])
    else:
        time_to_steady = None

    return {
        "t": t,
        "f_t": f_t,
        "F_t": F_t,
        "fc": fc,
        "F_total": F_total,
        "time_to_steady": time_to_steady,
        "threshold_fc": threshold
    }

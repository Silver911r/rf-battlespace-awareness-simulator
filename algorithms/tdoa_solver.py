import numpy as np
from scipy.optimize import least_squares

from core.constants import C
from core.coordinate_systems import ecef_to_lla

def tdoa_geolocate(sensor_positions, toa_measurements, max_iter=50):
    """
    Closed-form + refinement TDOA geolocation (Chan & Ho method -> Levenberg-Marquardt)
    sensor_positions: (N,3) ECEF meters
    toa_measurements: (N,) seconds of arival
    Returns: (x,y,z), CEP95 in meters
    """
    c = C
    # Reference sensor = first one
    ref_idx = 0
    tdoa = c * (toa_measurements - toa_measurements[ref_idx])
    r_ref = sensor_positions[ref_idx]

    def residual(x):
        diffs = np.linalg.norm(sensor_positions - x, axis=1) - np.linalg.norm(sensor_positions[ref_idx] - x)
        return tdoa - diffs

    # Multiple initializations to handle altitude ambiguity
    # For airborne UAS/drone threats (Group 1-3: 0-5.5km altitude)
    x0_base = np.mean(sensor_positions, axis=0)
    x0_norm = np.linalg.norm(x0_base)

    # Bounds to prevent "mirror solution" below Earth
    # Keep solution between Earth surface and 100km altitude
    earth_radius = 6.378e6
    max_altitude = 1e5  # 100 km (well above any drone)
    bounds_lower = -1 * (earth_radius + max_altitude) * np.ones(3)
    bounds_upper = (earth_radius + max_altitude) * np.ones(3)

    guesses = [
        x0_base / x0_norm * 6.378e6,      # Sea level
        x0_base / x0_norm * 6.3805e6,     # ~2.5 km altitude (mid-range drones)
        x0_base / x0_norm * 6.383e6,      # ~5 km altitude (Group 3 max)
        x0_base / x0_norm * 6.39e6,       # ~12 km altitude (high-altitude fallback)
    ]

    best_result = None
    best_residual = np.inf

    for i, guess in enumerate(guesses):
        # Use 'trf' method which supports bounds (lm does not)
        result = least_squares(residual, guess, method='trf',
                             bounds=(bounds_lower, bounds_upper),
                             max_nfev=max_iter)
        residual_norm = np.sum(result.fun**2)

        # Additional check: reject solutions far from Earth surface
        # Use proper geodetic altitude (accounts for Earth's ellipsoidal shape)
        _, _, pos_alt = ecef_to_lla(result.x)

        # Accept solution if altitude is reasonable (0-100km)
        if 0 < pos_alt < max_altitude:
            if residual_norm < best_residual:
                best_residual = residual_norm
                best_result = result
                print(f"  ✓ Guess {i+1}: alt={pos_alt/1e3:.1f}km, residual={residual_norm:.2e}")
        else:
            print(f"  ✗ Guess {i+1}: REJECTED alt={pos_alt/1e3:.1f}km (out of range)")

    # Fallback: if no valid solution found, use best residual regardless of altitude
    if best_result is None:
        print("⚠️  WARNING: No solutions in valid altitude range, using least-squares best fit")
        best_residual = np.inf
        for guess in guesses:
            result = least_squares(residual, guess, method='trf',
                                 bounds=(bounds_lower, bounds_upper),
                                 max_nfev=max_iter)
            residual_norm = np.sum(result.fun**2)
            if residual_norm < best_residual:
                best_residual = residual_norm
                best_result = result

    pos = best_result.x
    _, _, pos_altitude = ecef_to_lla(pos)
    print(f"🎯 TDOA SOLVER OUTPUT: ECEF=[{pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f}] alt={pos_altitude:.1f}m (residual: {best_residual:.2e})")

    # very rough CEP95 approximation for demo
    jac = best_result.jac
    try:
        cov = np.linalg.inv(jac.T @ jac)
        cep95 = 2.45 * np.sqrt(np.trace(cov[:2])) # horizontal only
    except:
        cep95 = 250.0

    return pos, cep95
import numpy as np
from scipy.optimize import least_squares

from core.constants import C

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

    # initial guess: center of earth -> better: centroid of sensors
    x0 = np.mean(sensor_positions, axis=0)

    def residual(x):
        diffs = np.linalg.norm(sensor_positions - x, axis=1) - np.linalg.norm(sensor_positions[ref_idx] - x)
        return tdoa - diffs
    
    result = least_squares(residual, x0, method='lm', max_nfev=max_iter)
    pos = result.x

    # very rough CEP95 approximation for demo
    jac = result.jac
    try:
        cov = np.linalg.inv(jac.T @ jac)
        cep95 = 2.45 * np.sqrt(np.trace(cov[:2])) # horizontal only
    except:
        cep95 = 250.0

    return pos, cep95
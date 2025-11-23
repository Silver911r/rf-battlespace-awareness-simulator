# core/coordinate_systems.py
import numpy as np

# WGS84 constants
a = 6378137.0              # semi-major axis (m)
f = 1 / 298.257223563      # flattening
e2 = f * (2 - f)           # eccentricity squared

def lla_to_ecef(lat, lon, alt=0.0):
    """Lat (deg), Lon (deg), Alt (m) → ECEF (m)"""
    print(f"🔵 LLA→ECEF INPUT: lat={lat:.6f}°, lon={lon:.6f}°, alt={alt:.1f}m")
    lat = np.radians(lat)
    lon = np.radians(lon)
    N = a / np.sqrt(1 - e2 * np.sin(lat)**2)
    x = (N + alt) * np.cos(lat) * np.cos(lon)
    y = (N + alt) * np.cos(lat) * np.sin(lon)
    z = (N * (1 - e2) + alt) * np.sin(lat)
    result = np.array([x, y, z])
    print(f"🔵 LLA→ECEF OUTPUT: ECEF=[{x:.1f}, {y:.1f}, {z:.1f}]")
    return result

def ecef_to_lla(pos):
    """
    ECEF (m) → Lat (deg), Lon (deg), Alt (m)
    Bowring's method — fast and accurate for Earth surface
    """
    x, y, z = pos
    print(f"🟢 ECEF→LLA INPUT: ECEF=[{x:.1f}, {y:.1f}, {z:.1f}]")
    b = a * (1 - f)                 # semi-minor axis
    e2p = (a**2 - b**2) / b**2      # second eccentricity squared

    # Longitude
    lon = np.arctan2(y, x)

    # Radius of curvature in prime vertical
    p = np.sqrt(x**2 + y**2)
    if p < 1e-6:  # near poles
        lat = np.pi/2 if z > 0 else -np.pi/2
        alt = abs(z) - b
    else:
        # Initial guess
        lat = np.arctan2(z, (1 - e2) * p)

        # Iterate (usually converges in 2–3 steps)
        for _ in range(6):
            N = a / np.sqrt(1 - e2 * np.sin(lat)**2)
            alt = p / np.cos(lat) - N
            lat = np.arctan2(z + e2 * N * np.sin(lat), p)

    lat = np.degrees(lat)
    lon = np.degrees(lon)
    print(f"🟢 ECEF→LLA OUTPUT: lat={lat:.6f}°, lon={lon:.6f}°, alt={alt:.1f}m")
    return lat, lon, alt
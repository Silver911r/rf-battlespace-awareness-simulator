# sensors/rf_sensor.py
import numpy as np

class SatelliteSensor:
    def __init__(self, name, inclination_deg=53.0, altitude_km=550, 
                 raan_offset_deg=0.0, phase_offset_deg=0.0):
        self.name = name
        self.altitude = altitude_km * 1000.0
        self.radius = 6_378_137 + self.altitude
        self.inclination = np.radians(inclination_deg)
        self.raan = np.radians(raan_offset_deg)       # <─ NEW: different orbital planes
        self.phase = np.radians(phase_offset_deg)

    def position_ecef(self, t_seconds):
        angular_velocity = 15 * 2 * np.pi / 86400.0
        mean_anomaly = angular_velocity * t_seconds + self.phase

        # Position in orbital plane
        x_orb = self.radius * np.cos(mean_anomaly)
        y_orb = self.radius * np.sin(mean_anomaly)

        # Rotate by argument of perigee + RAAN (simple circular)
        cos_raan, sin_raan = np.cos(self.raan), np.sin(self.raan)
        x = x_orb * cos_raan - y_orb * sin_raan
        y = x_orb * sin_raan + y_orb * cos_raan
        z = y_orb * np.sin(self.inclination)

        return np.array([x, y, z])
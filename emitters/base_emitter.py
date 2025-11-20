from dataclasses import dataclass
import numpy as np
from core.coordinate_systems import lla_to_ecef

@dataclass
class Emitter:
    name: str
    lat: float
    lon: float
    alt: float = 0.0 # meters
    frequency: float = 1.3e9
    pulse_interval: float = 0.01 #seconds

    def position_ecef(self, t=None):
        return lla_to_ecef(self.lat, self.lon, self.alt)

    def transmit_times(self, sensor_positions_ecef):
        """Return transmit time at each sensor (propagation delay)"""
        distances = np.linalg.norm(sensor_positions_ecef - self.position_ecef(), axis=1)
        return distances / 299792458.0

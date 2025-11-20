import numpy as np

C = 299_792_458.0 # speed of light (m/s)
EARTH_RADIUS = 6371.0088e3 # wgs84 mean radius (m)
L_BAND = (1e9, 2e9) # common satcom / uas bands
S_BAND = (2e9, 4e9)
GPS_L1 = 1.57542e9
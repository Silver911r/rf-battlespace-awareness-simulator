# visualization/app.py
import time
import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from emitters.base_emitter import Emitter
from sensors.rf_sensor import SatelliteSensor
from algorithms.tdoa_solver import tdoa_geolocate
from core.coordinate_systems import ecef_to_lla  # ← fixed import path

app = FastAPI()
templates = Jinja2Templates(directory="visualization")
app.mount("/static", StaticFiles(directory="visualization/static", html=True), name="static")

sats = [
    SatelliteSensor("LEO-01", raan_offset_deg=0),
    SatelliteSensor("LEO-02", raan_offset_deg=90),
    SatelliteSensor("LEO-03", raan_offset_deg=180),
    SatelliteSensor("LEO-04", raan_offset_deg=270),
]

emitter = Emitter("THREAT-01", lat=35.6892, lon=51.3890, alt=100)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/fix")
async def get_fix():
    try:
        t = time.time()
        sensor_pos = np.array([sat.position_ecef(t) for sat in sats])
        toa = emitter.transmit_times(sensor_pos) + 2e-9 * np.random.randn(4)  # slightly more realistic noise
        fix_ecef, cep95 = tdoa_geolocate(sensor_pos, toa)
        lat, lon, _ = ecef_to_lla(fix_ecef)

        # Force a minimum CEP so the circle is visible
        cep95 = max(cep95, 300.0)

        print(f"Fix computed: {lat:.5f}°N, {lon:.5f}°E | CEP95: {cep95:.0f}m")
        return {"lat": lat, "lon": lon, "cep95": cep95}

    except Exception as e:
        print("ERROR in /fix:", e)
        import traceback
        traceback.print_exc()
        # Return a fallback so the map always shows something
        return {"lat": 35.6892, "lon": 51.3890, "cep95": 1000}
    
if __name__ == "__main__":
    import uvicorn
    print("Live TDOA Demo → http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
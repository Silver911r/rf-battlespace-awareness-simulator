# main.py
import uvicorn

if __name__ == "__main__":
    print("Launching RF Battlespace Awareness Simulator")
    print("→ http://127.0.0.1:8000")
    uvicorn.run(
        "visualization.app:app",   # module:app_object
        host="127.0.0.1",
        port=8000,
        reload=True,               # auto-restart on code changes
        log_level="info"
    )
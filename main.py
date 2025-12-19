from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import swisseph as swe

app = FastAPI(
    title="astro-engine",
    version="0.1",
    description="Deterministic astrology calculation engine"
)

# CORS (open for demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/calculate")
def calculate(
    year: int,
    month: int,
    day: int,
    hour: float,
    lat: float,
    lon: float
):
    # Julian day
    jd = swe.julday(year, month, day, hour)

    # Set location
    swe.set_topo(lon, lat, 0)

    # Example: Sun position
    sun_pos, _ = swe.calc_ut(jd, swe.SUN)

    return {
        "input": {
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "lat": lat,
            "lon": lon
        },
        "chart": {
            "sun_longitude": sun_pos[0]
        },
        "dashas": {}
    }

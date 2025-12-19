from fastapi import FastAPI
import swisseph as swe

app = FastAPI()
swe.set_ephe_path(".")

@app.get("/calculate")
def calculate(year: int, month: int, day: int, hour: float, lat: float, lon: float):
    jd = swe.julday(year, month, day, hour)

    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN
    }

    result = {}
    for name, pid in planets.items():
        lon = swe.calc_ut(jd, pid)[0][0]
        result[name] = {
            "longitude": round(lon, 4),
            "sign": int(lon // 30) + 1
        }

    return {
        "jd": jd,
        "planets": result,
        "engine": "Swiss Ephemeris"
    }

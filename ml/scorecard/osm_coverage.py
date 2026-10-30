"""Phase 0 scorecard: measure OpenStreetMap coverage per city.

Usage:
  python scorecard/osm_coverage.py --cities London Tokyo
  python scorecard/osm_coverage.py            # all 10 cities
"""
import argparse
import hashlib
import json
import math
import time
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).parent
CACHE = HERE / "cache"
OUT = HERE / "results"
CACHE.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
HEADERS = {"User-Agent": "tomorrowhood-scorecard/0.1 (personal research; contact: reetam2308@gmail.com)"}

CITIES = {
    "London": (51.5074, -0.1278),
    "New York": (40.7300, -73.9900),
    "Tokyo": (35.6812, 139.7671),
    "Singapore": (1.3000, 103.8400),
    "Melbourne": (-37.8136, 144.9631),
    "San Francisco": (37.7749, -122.4194),
    "Paris": (48.8566, 2.3522),
    "Seoul": (37.5665, 126.9780),
    "Berlin": (52.5200, 13.4050),
    "Toronto": (43.6532, -79.3832),
    "Singapore-2": (1.3343, 103.8563),
}

# metric -> Overpass selectors (ways only for buildings; relations are excluded,
# which biases every city the same way)
METRICS = {
    "buildings": ['way["building"]'],
    "bld_levels": ['way["building"]["building:levels"]'],
    "bld_height": ['way["building"]["height"]'],
    "bld_address": ['way["building"]["addr:housenumber"]'],
    "amenities": ['node["amenity"]'],
    "shops": ['node["shop"]'],
    "transit_stops": ['node["highway"="bus_stop"]',
                      'node["railway"~"^(station|tram_stop|subway_entrance)$"]'],
    "parks": ['nwr["leisure"="park"]'],
    "cycleways": ['way["highway"="cycleway"]'],
    "trees": ['node["natural"="tree"]'],
}


def bbox(lat, lon, half_km):
    dlat = half_km / 111.0
    dlon = half_km / (111.0 * math.cos(math.radians(lat)))
    return lat - dlat, lon - dlon, lat + dlat, lon + dlon


def build_query(selectors, b):
    s, w, n, e = b
    body = "".join(f"{sel}({s:.5f},{w:.5f},{n:.5f},{e:.5f});" for sel in selectors)
    return f"[out:json][timeout:180];({body});out count;"


def run_query(q):
    f = CACHE / f"{hashlib.sha1(q.encode()).hexdigest()}.json"
    if f.exists():
        return json.loads(f.read_text())
    last = None
    for attempt in range(4):
        for url in ENDPOINTS:
            try:
                r = requests.post(url, data={"data": q}, headers=HEADERS, timeout=200)
                if r.status_code == 200:
                    data = r.json()
                    if data.get("elements"):
                        f.write_text(json.dumps(data))
                        time.sleep(2)  # be polite to the free server
                        return data
                    last = f"{url} -> empty result: {data.get('remark')}"
                else:
                    last = f"{url} -> HTTP {r.status_code}"
            except (requests.RequestException, ValueError) as ex:
                last = f"{url} -> {ex}"
        time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"Overpass failed: {last}")


def count(selectors, b):
    data = run_query(build_query(selectors, b))
    return int(data["elements"][0]["tags"]["total"])


def measure(city, half_km):
    lat, lon = CITIES[city]
    b = bbox(lat, lon, half_km)
    row = {"city": city, "area_km2": (2 * half_km) ** 2}
    for name, sels in METRICS.items():
        row[name] = count(sels, b)
        print(f"  {city:14s} {name:14s} {row[name]}")
    return row


def derive(df):
    out = df[["city", "area_km2"]].copy()
    for c in ["buildings", "amenities", "shops", "transit_stops", "parks", "cycleways", "trees"]:
        out[f"{c}_per_km2"] = (df[c] / df["area_km2"]).round(1)
    b = df["buildings"].where(df["buildings"] > 0)
    for c, name in [("bld_levels", "pct_levels"), ("bld_height", "pct_height"),
                    ("bld_address", "pct_address")]:
        out[name] = (100 * df[c] / b).round(1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cities", nargs="*", default=list(CITIES))
    ap.add_argument("--half-km", type=float, default=3.0)
    args = ap.parse_args()

    rows = [measure(c, args.half_km) for c in args.cities]
    new = pd.DataFrame(rows)
    path = OUT / "osm_counts.csv"
    if path.exists():
        old = pd.read_csv(path)
        old = old[~old["city"].isin(new["city"])]
        new = pd.concat([old, new], ignore_index=True)
    new.to_csv(path, index=False)

    report = derive(new)
    report.to_csv(OUT / "osm_report.csv", index=False)
    pd.set_option("display.width", 200)
    print("\n", report.to_string(index=False))


if __name__ == "__main__":
    main()
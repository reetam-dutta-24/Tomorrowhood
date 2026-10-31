"""Phase 1, step 1: build the H3 hexagon grid for a city.

Usage (from the ml folder):
  python pipeline/make_grid.py --city London --res 9 --preview
"""
import argparse
import json
import time
from pathlib import Path

import geopandas as gpd
import h3
import requests
from shapely.geometry import Polygon, shape

ROOT = Path(__file__).resolve().parents[1]  # the ml folder
DATA = ROOT / "data"
BOUNDARIES = DATA / "boundaries"
GRIDS = DATA / "grids"
for d in (BOUNDARIES, GRIDS):
    d.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "tomorrowhood/0.1 (personal research; contact: reetam2308@gmail.com)"}

# Text used to find each city's outline in OpenStreetMap's geocoder (Nominatim).
CITY_QUERIES = {
    "London": "Greater London, United Kingdom",
}


def slug(city):
    return city.lower().replace(" ", "_")


def fetch_boundary(city):
    """Return the city outline as a shapely geometry (lon, lat), cached on disk."""
    path = BOUNDARIES / f"{slug(city)}.geojson"
    if path.exists():
        return shape(json.loads(path.read_text())["geometry"])
    r = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": CITY_QUERIES[city], "format": "jsonv2",
                "polygon_geojson": 1, "limit": 5},
        headers=HEADERS, timeout=60,
    )
    r.raise_for_status()
    for hit in r.json():
        geom = hit.get("geojson")
        if geom and geom["type"] in ("Polygon", "MultiPolygon"):
            feature = {"type": "Feature",
                       "properties": {"name": hit["display_name"]},
                       "geometry": geom}
            path.write_text(json.dumps(feature))
            print("Boundary found:", hit["display_name"])
            time.sleep(1)  # be polite to the free geocoder
            return shape(geom)
    raise RuntimeError("No polygon boundary found; refine CITY_QUERIES")


def build_grid(boundary, res):
    """Fill the boundary with H3 cells; return a GeoDataFrame, one row per cell."""
    cells = sorted(h3.geo_to_cells(boundary, res))
    rows = []
    for c in cells:
        lat, lng = h3.cell_to_latlng(c)
        ring = h3.cell_to_boundary(c)  # list of (lat, lng)
        rows.append({
            "h3": c,
            "h3_res8": h3.cell_to_parent(c, 8) if res >= 8 else None,
            "lat": lat,
            "lng": lng,
            "area_km2": h3.cell_area(c, "km^2"),
            "geometry": Polygon([(lo, la) for la, lo in ring]),
        })
    return gpd.GeoDataFrame(rows, crs="EPSG:4326")


def check_coverage(grid, boundary):
    """Compare total hexagon area to the true boundary area (should be near 1.0)."""
    b = gpd.GeoSeries([boundary], crs="EPSG:4326")
    b_km2 = b.to_crs(b.estimate_utm_crs()).area.iloc[0] / 1e6
    g_km2 = grid["area_km2"].sum()
    print(f"Boundary area : {b_km2:,.1f} km2")
    print(f"Hexagon area  : {g_km2:,.1f} km2 ({len(grid):,} cells)")
    print(f"Coverage ratio: {g_km2 / b_km2:.3f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", default="London")
    ap.add_argument("--res", type=int, default=9)
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()

    boundary = fetch_boundary(args.city)
    grid = build_grid(boundary, args.res)
    check_coverage(grid, boundary)

    out = GRIDS / f"{slug(args.city)}_res{args.res}.parquet"
    grid.to_parquet(out)
    print("Saved:", out)

    if args.preview:
        ax = grid.plot(edgecolor="white", linewidth=0.1, figsize=(10, 10))
        ax.set_axis_off()
        png = GRIDS / f"{slug(args.city)}_res{args.res}.png"
        ax.figure.savefig(png, dpi=150, bbox_inches="tight")
        print("Preview:", png)


if __name__ == "__main__":
    main()
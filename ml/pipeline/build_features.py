"""Phase 1, step 3: count what is in each hexagon, with DuckDB.

Usage (from the ml folder):
  python pipeline/build_features.py --city London --res 9 --preview
"""
import argparse
from pathlib import Path

import duckdb
import geopandas as gpd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]  # the ml folder
DATA = ROOT / "data"
OUT = DATA / "features"
OUT.mkdir(parents=True, exist_ok=True)

# feature name -> SQL condition on the points table
COUNTS = {
    "buildings": "cls='building'",
    "bld_levels": "cls='building' AND has_levels",
    "bld_height": "cls='building' AND has_height",
    "bld_addr": "cls='building' AND has_addr",
    "amenities": "cls='amenity'",
    "cafes": "cls='amenity' AND sub='cafe'",
    "restaurants": "cls='amenity' AND sub IN ('restaurant','fast_food','food_court')",
    "nightlife": "cls='amenity' AND sub IN ('bar','pub','nightclub')",
    "schools": "cls='amenity' AND sub IN ('school','college','university')",
    "healthcare": "cls='amenity' AND sub IN ('hospital','clinic','doctors','pharmacy')",
    "banks_atms": "cls='amenity' AND sub IN ('bank','atm')",
    "shops": "cls='shop'",
    "groceries": "cls='shop' AND sub IN ('supermarket','convenience','greengrocer')",
    "parks": "cls='leisure' AND sub='park'",
    "gyms": "cls='leisure' AND sub='fitness_centre'",
    "sports": "cls='leisure' AND sub IN ('sports_centre','pitch','swimming_pool')",
    "playgrounds": "cls='leisure' AND sub='playground'",
    "transit_stops": "cls='transit'",
    "trees": "cls='tree'",
    "stay_options": "cls='tourism' AND sub IN ('hotel','hostel','motel','guest_house','apartment')",
    "museums": "cls='tourism' AND sub='museum'",
}
PLAIN = [n for n in COUNTS if not n.startswith("bld_")]


def slug(city):
    return city.lower().replace(" ", "_")


def derived_sql(table):
    """Add densities (per km2) and building-tag shares (0 to 1) to a counts table."""
    dens = ",\n    ".join(f"{n}::DOUBLE / area_km2 AS {n}_per_km2" for n in PLAIN)
    shares = ",\n    ".join(
        f"CASE WHEN buildings > 0 THEN bld_{k}::DOUBLE / buildings END AS pct_{k}"
        for k in ("levels", "height", "addr")
    )
    return f"SELECT *,\n    {dens},\n    {shares}\nFROM {table}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", default="London")
    ap.add_argument("--res", type=int, default=9)
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()

    s = slug(args.city)
    grid = DATA / "grids" / f"{s}_res{args.res}.parquet"
    pois = DATA / "pois" / f"{s}_res{args.res}.parquet"
    for p in (grid, pois):
        if not p.exists():
            raise SystemExit(f"Missing file: {p}")

    con = duckdb.connect()
    agg = ",\n        ".join(f"COUNT(*) FILTER (WHERE {c}) AS {n}" for n, c in COUNTS.items())
    filled = ", ".join(f"COALESCE(p.{n}, 0)::INTEGER AS {n}" for n in COUNTS)

    # LEFT JOIN from the grid so empty hexagons stay in the table with zeros
    con.execute(f"""
        CREATE TABLE cells AS
        SELECT g.h3, g.h3_res8, g.lat, g.lng, g.area_km2, {filled}
        FROM read_parquet('{grid.as_posix()}') AS g
        LEFT JOIN (
            SELECT h3, {agg}
            FROM read_parquet('{pois.as_posix()}')
            GROUP BY h3
        ) AS p ON p.h3 = g.h3
    """)

    # Roll up to resolution 8 by SUMMING counts (never by averaging percentages)
    sums = ", ".join(f"SUM({n})::INTEGER AS {n}" for n in COUNTS)
    con.execute(f"""
        CREATE TABLE cells8 AS
        SELECT h3_res8 AS h3, COUNT(*)::INTEGER AS n_cells9,
               SUM(area_km2) AS area_km2, AVG(lat) AS lat, AVG(lng) AS lng, {sums}
        FROM cells GROUP BY h3_res8
    """)

    for label, table in (("res9", "cells"), ("res8", "cells8")):
        out = OUT / f"{s}_{label}.parquet"
        con.execute(f"COPY ({derived_sql(table)}) TO '{out.as_posix()}' (FORMAT parquet)")
        print("Saved:", out)

    print(con.sql("""
        SELECT COUNT(*) AS hexagons, SUM(buildings) AS buildings,
               SUM(amenities) AS amenities,
               COUNT(*) FILTER (WHERE buildings = 0) AS hexes_without_buildings
        FROM cells"""))
    print(con.sql("""
        SELECT ROUND(lat, 4) AS lat, ROUND(lng, 4) AS lng, amenities
        FROM cells ORDER BY amenities DESC LIMIT 5"""))
    print(con.sql("""
        SELECT COUNT(*) AS res8_cells, ROUND(AVG(n_cells9), 1) AS avg_children
        FROM cells8"""))

    if args.preview:
        gdf = gpd.read_parquet(grid)
        df = con.sql("SELECT h3, amenities / area_km2 AS density FROM cells").df()
        gdf = gdf.merge(df, on="h3")
        gdf["log_density"] = np.log1p(gdf["density"])  # log scale so the centre doesn't wash out the rest
        ax = gdf.plot(column="log_density", cmap="magma", linewidth=0,
                      figsize=(10, 10), legend=True)
        ax.set_axis_off()
        ax.set_title(f"{args.city}: amenities per km2 (log scale)")
        png = OUT / f"{s}_amenities_res{args.res}.png"
        ax.figure.savefig(png, dpi=150, bbox_inches="tight")
        print("Preview:", png)


if __name__ == "__main__":
    main()
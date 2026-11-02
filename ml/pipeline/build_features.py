"""Phase 1, step 3 (v2): count what is in each hexagon by taxonomy group, with DuckDB.

Usage (from the ml folder):
  python pipeline/build_features.py --city London --res 9 --preview
"""
import argparse
from pathlib import Path

import duckdb
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

from taxonomy import COMPOSITES, taxonomy_frame

ROOT = Path(__file__).resolve().parents[1]  # the ml folder
DATA = ROOT / "data"
OUT = DATA / "features"
OUT.mkdir(parents=True, exist_ok=True)

# Building counts and tag completeness (not part of the amenity taxonomy)
BUILD = {
    "buildings": "p.cls='building'",
    "bld_levels": "p.cls='building' AND p.has_levels",
    "bld_height": "p.cls='building' AND p.has_height",
    "bld_addr": "p.cls='building' AND p.has_addr",
    # hotels rated 4 stars or more (the star tag is free text, so odd values are skipped)
    "upscale_hotels": "p.cls='tourism' AND p.sub='hotel' AND TRY_CAST(p.stars AS DOUBLE) >= 4",
}


def slug(city):
    return city.lower().replace(" ", "_")


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

    tax = taxonomy_frame()
    groups = sorted(set(tax["grp"]))
    exprs = {**BUILD, **{g: f"t.grp='{g}'" for g in groups}}
    cols = list(exprs)
    all_cols = cols + list(COMPOSITES)
    plain = [c for c in all_cols if not c.startswith("bld_")]

    con = duckdb.connect()
    con.register("taxo", tax)

    agg = ",\n        ".join(f"COUNT(*) FILTER (WHERE {c}) AS {n}" for n, c in exprs.items())
    filled = ", ".join(f"COALESCE(a.{n}, 0)::INTEGER AS {n}" for n in cols)
    comp = ", ".join(
        "(" + " + ".join(f"COALESCE(a.{c}, 0)" for c in parts) + f")::INTEGER AS {name}"
        for name, parts in COMPOSITES.items()
    )

    # One pass over the points: tag each with its group, count per hexagon.
    # LEFT JOIN from the grid so empty hexagons stay in the table with zeros.
    con.execute(f"""
        CREATE TABLE cells AS
        SELECT g.h3, g.h3_res8, g.lat, g.lng, g.area_km2, {filled}, {comp}
        FROM read_parquet('{grid.as_posix()}') AS g
        LEFT JOIN (
            SELECT p.h3, {agg}
            FROM read_parquet('{pois.as_posix()}') AS p
            LEFT JOIN taxo AS t ON p.cls = t.cls AND p.sub = t.sub
            GROUP BY p.h3
        ) AS a ON a.h3 = g.h3
    """)

    # Roll up to resolution 8 by SUMMING counts (never by averaging percentages)
    sums = ", ".join(f"SUM({n})::INTEGER AS {n}" for n in all_cols)
    con.execute(f"""
        CREATE TABLE cells8 AS
        SELECT h3_res8 AS h3, COUNT(*)::INTEGER AS n_cells9,
               SUM(area_km2) AS area_km2, AVG(lat) AS lat, AVG(lng) AS lng, {sums}
        FROM cells GROUP BY h3_res8
    """)

    def derived(table):
        dens = ",\n    ".join(f"{n}::DOUBLE / area_km2 AS {n}_per_km2" for n in plain)
        shares = ",\n    ".join(
            f"CASE WHEN buildings > 0 THEN bld_{k}::DOUBLE / buildings END AS pct_{k}"
            for k in ("levels", "height", "addr"))
        return f"SELECT *,\n    {dens},\n    {shares}\nFROM {table}"

    for label, table in (("res9", "cells"), ("res8", "cells8")):
        out = OUT / f"{s}_{label}.parquet"
        con.execute(f"COPY ({derived(table)}) TO '{out.as_posix()}' (FORMAT parquet)")
        print("Saved:", out)

    df = con.sql("SELECT * FROM cells").df()
    print(f"\nHexagons: {len(df):,} | without buildings: {(df['buildings'] == 0).sum():,}")
    print("\nTotals by group:")
    print(df[all_cols].sum().sort_values(ascending=False).to_string())
    for col in ("everyday_services", "leisure_modern_upscale"):
        print(f"\nTop 5 hexagons by {col}:")
        print(df.nlargest(5, col)[["lat", "lng", col]].round(4).to_string(index=False))

    if args.preview:
        gdf = gpd.read_parquet(grid).merge(
            df[["h3", "everyday_services", "leisure_modern_upscale", "area_km2"]], on="h3")
        fig, axes = plt.subplots(1, 2, figsize=(18, 8))
        for ax, col, title in ((axes[0], "everyday_services", "Everyday services"),
                               (axes[1], "leisure_modern_upscale", "Leisure, modern and upscale")):
            gdf.assign(v=np.log1p(gdf[col] / gdf["area_km2"])).plot(
                column="v", cmap="magma", linewidth=0, ax=ax, legend=True)
            ax.set_axis_off()
            ax.set_title(f"{args.city}: {title} per km2 (log scale)")
        png = OUT / f"{s}_groups_res{args.res}.png"
        fig.savefig(png, dpi=130, bbox_inches="tight")
        print("Preview:", png)


if __name__ == "__main__":
    main()
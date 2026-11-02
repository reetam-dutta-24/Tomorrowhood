"""Phase 1, step 5: neighbourhood-context ('access') features.

For every hexagon, add up counts in the hexagons around it (rings of neighbours).
Ring 1 is about 300 m (doorstep); ring 4 is about 1.2 km (a 15-minute walk as the crow flies).

Usage (from the ml folder):
  python pipeline/build_access.py --city London --preview
"""
import argparse
from pathlib import Path

import geopandas as gpd
import h3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]  # the ml folder
DATA = ROOT / "data"
OUT = DATA / "features"

RINGS = {"k1": 1, "k4": 4}
ESSENTIALS = ["healthcare", "education", "food_drink", "daily_services",
              "everyday_retail", "green_outdoor", "transport"]
META = {"h3", "h3_res8", "lat", "lng", "area_km2", "n_cells9"}


def slug(city):
    return city.lower().replace(" ", "_")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", default="London")
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()
    s = slug(args.city)

    df = pd.read_parquet(OUT / f"{s}_res9.parquet")
    count_cols = [c for c in df.columns
                  if c not in META and not c.endswith("_per_km2")
                  and not c.startswith(("pct_", "bld_"))]
    cells = df["h3"].tolist()
    index = {c: i for i, c in enumerate(cells)}
    X = df[count_cols].to_numpy(dtype=np.float64)
    area = df["area_km2"].to_numpy()

    new = {}
    for label, k in RINGS.items():
        S = np.zeros_like(X)
        A = np.zeros(len(df))
        for i, c in enumerate(cells):
            # neighbours that exist in the grid (cells outside the boundary are skipped)
            idx = [index[n] for n in h3.grid_disk(c, k) if n in index]
            S[i] = X[idx].sum(axis=0)
            A[i] = area[idx].sum()
        for j, col in enumerate(count_cols):
            new[f"{col}_{label}"] = S[:, j]
        new[f"area_{label}_km2"] = A  # actual area included, so edge tiles are not unfairly low

    for label in RINGS:
        present = np.column_stack([new[f"{e}_{label}"] > 0 for e in ESSENTIALS])
        new[f"essentials_{label}"] = present.sum(axis=1)

    out = pd.concat([df[["h3", "h3_res8", "lat", "lng"]], pd.DataFrame(new)], axis=1)
    out["lmu_density_k4"] = out["leisure_modern_upscale_k4"] / out["area_k4_km2"]
    path = OUT / f"{s}_access.parquet"
    out.to_parquet(path)
    print("Saved:", path, f"({out.shape[0]:,} rows, {out.shape[1]} columns)")

    for label in RINGS:
        vc = out[f"essentials_{label}"].value_counts(normalize=True).sort_index() * 100
        print(f"\nEssentials present within {label} (0 to 7), % of hexagons:")
        print(vc.round(1).to_string())
    print("\nTop 5 hexagons by leisure/modern/upscale density within 15 minutes:")
    print(out.nlargest(5, "lmu_density_k4")[["lat", "lng", "lmu_density_k4"]].round(3).to_string(index=False))

    if args.preview:
        gdf = gpd.read_parquet(DATA / "grids" / f"{s}_res9.parquet")[["h3", "geometry"]].merge(
            out[["h3", "essentials_k1", "lmu_density_k4"]], on="h3")
        fig, axes = plt.subplots(1, 2, figsize=(18, 8))
        gdf.plot(column="essentials_k1", cmap="viridis", linewidth=0, ax=axes[0], legend=True)
        axes[0].set_title(f"{args.city}: essentials within ~300 m (0 to 7)")
        gdf.assign(v=np.log1p(gdf["lmu_density_k4"])).plot(
            column="v", cmap="magma", linewidth=0, ax=axes[1], legend=True)
        axes[1].set_title(f"{args.city}: leisure/modern/upscale per km2, within ~1.2 km (log)")
        for ax in axes:
            ax.set_axis_off()
        png = OUT / f"{s}_access.png"
        fig.savefig(png, dpi=130, bbox_inches="tight")
        print("Preview:", png)


if __name__ == "__main__":
    main()
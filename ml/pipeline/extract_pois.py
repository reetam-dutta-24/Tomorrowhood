"""Phase 1, step 2 (v2): turn a city's OpenStreetMap extract into a flat 'points table',
each row tagged with its H3 hexagon. Keeps every subtype; the taxonomy decides what counts.

Usage (from the ml folder):
  python pipeline/extract_pois.py --city London --res 9
"""
import argparse
from pathlib import Path

import h3
import osmium
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]  # the ml folder
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "pois"
OUT.mkdir(parents=True, exist_ok=True)

RAIL = {"station", "tram_stop", "subway_entrance"}

SCHEMA = pa.schema([
    ("osm_type", pa.string()), ("osm_id", pa.int64()),
    ("lat", pa.float64()), ("lng", pa.float64()), ("h3", pa.string()),
    ("cls", pa.string()), ("sub", pa.string()),
    ("has_levels", pa.bool_()), ("has_height", pa.bool_()), ("has_addr", pa.bool_()),
    ("cuisine", pa.string()), ("stars", pa.string()),
])
COLS = [f.name for f in SCHEMA]
BATCH = 200_000  # rows held in memory before writing to disk


def slug(city):
    return city.lower().replace(" ", "_")


def classify(tags):
    """Return the (class, subtype) pairs an OSM object belongs to."""
    out = []
    for key in ("amenity", "shop", "leisure", "tourism"):
        v = tags.get(key)
        if v:
            out.append((key, v))
    if tags.get("highway") == "bus_stop":
        out.append(("transit", "bus_stop"))
    v = tags.get("railway")
    if v in RAIL:
        out.append(("transit", v))
    if tags.get("natural") == "tree":
        out.append(("tree", "tree"))
    if tags.get("office") == "coworking":
        out.append(("office", "coworking"))
    return out


class Collector(osmium.SimpleHandler):
    def __init__(self, res, writer):
        super().__init__()
        self.res = res
        self.writer = writer
        self.buf = {c: [] for c in COLS}
        self.counts = {}

    def add(self, osm_type, osm_id, lat, lng, cls, sub,
            lv=False, ht=False, ad=False, cuisine=None, stars=None):
        b = self.buf
        b["osm_type"].append(osm_type)
        b["osm_id"].append(osm_id)
        b["lat"].append(lat)
        b["lng"].append(lng)
        b["h3"].append(h3.latlng_to_cell(lat, lng, self.res))
        b["cls"].append(cls)
        b["sub"].append(sub)
        b["has_levels"].append(lv)
        b["has_height"].append(ht)
        b["has_addr"].append(ad)
        b["cuisine"].append(cuisine)
        b["stars"].append(stars)
        self.counts[cls] = self.counts.get(cls, 0) + 1
        if len(b["osm_id"]) >= BATCH:
            self.flush()

    def flush(self):
        if self.buf["osm_id"]:
            self.writer.write_table(pa.table(self.buf, schema=SCHEMA))
            self.buf = {c: [] for c in COLS}

    def node(self, n):
        if not n.tags:
            return
        pairs = classify(n.tags)
        if not pairs or not n.location.valid():
            return
        cuisine, stars = n.tags.get("cuisine"), n.tags.get("stars")
        for cls, sub in pairs:
            self.add("n", n.id, n.location.lat, n.location.lon, cls, sub,
                     cuisine=cuisine, stars=stars)

    def way(self, w):
        tags = w.tags
        if not tags:
            return
        is_building = "building" in tags
        pairs = classify(tags)
        if not is_building and not pairs:
            return
        try:
            lats = [nd.location.lat for nd in w.nodes]
            lons = [nd.location.lon for nd in w.nodes]
        except osmium.InvalidLocationError:
            return
        if not lats:
            return
        lat = sum(lats) / len(lats)
        lng = sum(lons) / len(lons)
        if is_building:
            self.add("w", w.id, lat, lng, "building", tags.get("building"),
                     "building:levels" in tags, "height" in tags,
                     "addr:housenumber" in tags)
        cuisine, stars = tags.get("cuisine"), tags.get("stars")
        for cls, sub in pairs:
            self.add("w", w.id, lat, lng, cls, sub, cuisine=cuisine, stars=stars)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", default="London")
    ap.add_argument("--res", type=int, default=9)
    args = ap.parse_args()

    pbf = RAW / f"{slug(args.city)}.osm.pbf"
    if not pbf.exists():
        raise SystemExit(f"Download the extract first: {pbf}")
    out = OUT / f"{slug(args.city)}_res{args.res}.parquet"

    with pq.ParquetWriter(out, SCHEMA) as writer:
        c = Collector(args.res, writer)
        c.apply_file(str(pbf), locations=True)  # locations=True lets ways find their corners
        c.flush()
    print("Rows by class:", dict(sorted(c.counts.items(), key=lambda kv: -kv[1])))
    print("Saved:", out)


if __name__ == "__main__":
    main()
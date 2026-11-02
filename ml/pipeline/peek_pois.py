"""Quick sanity check of a points table with DuckDB.
Usage: python pipeline/peek_pois.py data/pois/london_res9.parquet
"""
import sys

import duckdb

f = sys.argv[1]
print(duckdb.sql(f"""
    SELECT cls, COUNT(*) AS rows, COUNT(DISTINCT h3) AS hexagons
    FROM read_parquet('{f}') GROUP BY cls ORDER BY rows DESC"""))
print(duckdb.sql(f"""
    SELECT ROUND(100*AVG(has_levels::INT),1) AS pct_levels,
           ROUND(100*AVG(has_height::INT),1) AS pct_height,
           ROUND(100*AVG(has_addr::INT),1)   AS pct_address
    FROM read_parquet('{f}') WHERE cls='building'"""))
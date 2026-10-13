<strong>Close-first:</strong> Vector tiles look simple until the third MoveTo command flips a ring and your choropleth becomes a fish-eye puzzle. This guide walks the eight checkpoints the [Elysia Tools MVT / PMTiles Auditor](https://elysiatools.com/en/tools/mvt-mapbox-vector-tile-pmtiles-google-mvt-projection-and-tilelive-encoding-auditor) hits before it signs a tile green — from the protobuf Layer/Feature/Value tables through PMTiles v3 root+leaf run-length directories — so a Mapbox GL JS render, a MapLibre style, and a Tippecanoe pipeline all agree on what a tile is.

Vector tiles are a contract, not a black box. A `.mvt` or `.pbf` tile promises geometric features at a specific zoom level, a fixed Web Mercator bounding box, a typed Value table, and a tag index — each layer wired into the next. The Mapbox Vector Tile Specification 2.x spells the format out, but the spec leaves the auditor plenty of room. A tile can claim a feature with a polygon ring, return a `ClosePath` command, and still emit a ring that crosses itself at the projection seam. The audit's job is to catch all of that, and the auditor walk below is the order it does it in.

## What the Mapbox Vector Tile Specification 2.x Actually Promises (and Where Tiles Lie)

The Mapbox Vector Tile Specification 2.x is a layered document:

- A `tile` is a protobuf message containing zero or more `layer` entries.
- Each `layer` holds a `features` array, a `keys` array, a `values` array, and an `extent` integer (most producers default to 4096).
- Each `feature` has an `id`, a list of `tags` (paired key/value indexes), and a `type` (NONE=0, UNKNOWN=1, POINT=2, LINESTRING=3, POLYGON=4).
- Geometry is encoded as a command stream: `MoveTo(count)`, `LineTo(count)`, `ClosePath`.

That's the contract. Where tiles lie:

- An `UNKNOWN` type is technically allowed but treated as POINT by every renderer, masking a real bug.
- A feature's tag list can reference a keys[3] that's missing from `keys` if a producer writes them out of order — older tippecanoe versions did this until 1.31.
- A `ClosePath` command doesn't carry coordinates — it implicitly closes to the last `MoveTo`. If the previous MoveTo had `count=2` and only one of those was inside the tile extent, the polygon ring can drift off-edge by the time the renderer snaps back.

Elysia Tools audits every layer entry against the spec before walking geometry. The [Mapbox Vector Tile Specification 2.x](https://elysiatools.com/en/tools/mvt-mapbox-vector-tile-pmtiles-google-mvt-projection-and-tilelive-encoding-auditor) auditor reads the raw protobuf tables, computes the layer's tag-key index, and confirms that every `feature.tags[i]` resolves cleanly to either an int, float, double, string, bool, or geoposition value. Anything that points past `values.length` is flagged as `MISSING_TAG_INDEX`, which is a real defect class — not noise.

## The Three Layers Every Auditor Walks Before Trusting a Tile

Before geometry is touched, the auditor validates the three structural layers of the protobuf envelope:

1. **Tile envelope layer** — verify `Tile.Layers` is a non-null array, that the tile's overall payload is within `tile_size_budget`, and that there is at least one layer for z>=0 tiles (z=0 tiles can be empty, but z>=4 with zero layers is a bug).
2. **Layer metadata** — confirm each `layer.name`, `layer.extent` (must be 256, 512, 1024, 2048, or 4096 — any other value triggers `EXTENT_NON_POWER_OF_TWO`), and `layer.version` (must equal 2; version 1 from 2014 has incompatible tag encoding).
3. **Feature index tables** — walk `keys[]`, `values[]`, and confirm there are no duplicates. Duplicate `keys` produces a renderer that picks whichever index it scans last; duplicate `values` silently re-encodes the same string with no real loss but bloat.

These three layers are walked in this order for a reason. The order guarantees that the auditor never trusts a feature's `tags` array before it has confirmed the `keys` and `values` tables are sane. Producers that invert this order (some legacy Tippecanoe pre-1.32) produce tiles that pass a `tags[i] != 0` check but fail when `key[tag[i]]` is dereferenced.

## MoveTo / LineTo / ClosePath: The Geometry Command Stream is Where Tiles Lie About Their Topology

This is the layer auditors skip and where tiles lie most often.

The command stream is a flat array of integers where each command begins with a command-id (1=MoveTo, 2=LineTo, 7=ClosePath) packed with the count via zigzag + varint. Every command is followed by `count` coordinate pairs as zigzag + varint integers, with each pair (dx, dy) a delta from the previous position scaled by `2 * extent / tile_size`.

What goes wrong:

- **Implicit MoveTo with zero count.** Some libs emit `MoveTo(0)` and then `LineTo(2)` expecting the renderer to start from the "current" pen position (which is undefined). The auditor flags this as `STRAY_LINETO_NO_MOVETO`.
- **Excess coord pairs.** A `MoveTo(2)` followed by 3 coord pairs because the producer forgot the closing one — Mapbox GL JS truncates, MapLibre renders the extra as a phantom vertex.
- **ClosePath after empty pen.** `ClosePath` only does anything if the last MoveTo had at least one coord pair. After a `MoveTo(0)` and a series of `LineTo`s, `ClosePath` closes back to the undefined pen — a real defect for any polygon ring.

The auditor walks every command, tracks the pen, and rejects any sequence where the geometry cannot be reconstructed to a closed ring or open line without warning.

## Ring Winding and the OpenStreetMap Polygon Bug That Survives 0-to-65535

Spec 2.x says: clockwise rings fill, counter-clockwise rings are holes. Real-world shapes mix both, and OpenStreetMap polygons ship with the OSM convention (exterior CCW, interior CW) — the opposite of the spec's renderer expectation.

The bug: many producers do not flip OSM-imported polygons before serving them in Mapbox tiles. A polygon imported from OSM with `natural=water` ends up with an exterior ring that maplibre renders as a hole. The auditor detects this by:

- Computing the signed area of each ring with the shoelace formula.
- Comparing the absolute sum of positive-area vs negative-area rings against the layer's expected winding.
- Flagging `RING_WINDING_INVERTED` and pointing at the affected feature id.

## Web Mercator vs Google XYZ Bounds: Why Your Z=0 Tile Sits Half in the Sea

Z=0, X=0, Y=0 is supposed to cover the world from -180° to 180° longitude and ~85.05°N to ~85.05°S latitude. But Google XYZ scheme swaps Y: Y=0 is the top (north) at z=0, Y=1 is the bottom (south). TMS does it the other way around.

Most renderers accept either, but a tippecanoe pipeline that produces an XYZ tile and a renderer that assumes TMS will render the antipodal seam at the wrong line of longitude. The auditor checks:

- For XYZ: `y_origin == -1 * (1 << z) + 1 + y`
- For TMS: `y_origin == y`

Z=0 lands you in either ocean or the Americas, depending on which convention the producer used. Z>=4 lets the auditor cross-check by sampling two adjacent tiles at the same `y` and verifying `abs(tile_a.bbox_max_y - tile_b.bbox_min_y) < 1e-6`.

## PMTiles v3 Directories: Decoding the Root-Leaf RLE Without Leaking the Tile Cache

PMTiles v3 packs entire tile pyramids into a single archive. The directory is a B-tree of run-length-encoded entries pointing at offsets within the file. Auditing PMTiles means:

- Parse the header (`PMTiles v3` magic, root_directory_offset, root_directory_length, json_metadata, leaf_directories).
- Walk the root directory using the v3 spec's B+tree sharding: each internal entry is `(min_tile_id, max_tile_id, offset, length, run_length)`.
- For each entry, attempt a length-bounded read; if the entry's `length` is 0, the tile is treated as missing (a real PMTiles feature, not a defect).
- For leaf directories, decode the run-length and confirm adjacent entries do not overlap.

Common defects:

- `ROOT_LEAF_OVERLAP` — two run-length entries claim the same tile ID.
- `TILE_OFFSET_PAST_EOF` — an offset points past the file size.
- `MISSING_HEADER_MAGIC` — a v2 archive mislabeled as v3.

The auditor handles each, and for `MISSING_HEADER_MAGIC` suggests whether to upgrade the producer or downgrade the auditor to v2.

## Tile-Size vs Feature-Count Budgets: How PMTiles Auditor Catches a 47 KB Polygon Town

Vector tiles have no hard size limit per se, but a tile payload above ~500 KB has trouble with CDN caching, gzip compression, and HTTP/2 multiplexing. Tippecanoe's `--maximum-tile-bytes` defaults to 500 KB. PMTiles archives store tile sizes directly in their directory entries, so a PMTiles auditor can flag every oversized tile before a renderer even asks for it.

Beyond raw size, the auditor also watches feature-count budgets:

- A polygon-heavy administrative layer (counties, ZIP codes) should not exceed ~2,000 features per z=10 tile for sane render performance.
- A road network tile should not exceed ~5,000 features at z=14.
- A POI (points-of-interest) layer is allowed up to ~20,000 per z=14 tile — but only if the producer sets a `clipped` flag and skips nodes that fall outside the tile's clipped bbox.

A 47 KB tile at z=8 with 1,400 polygon features is technically spec-compliant but will be flagged `FEATURE_COUNT_BUDGET_EXCEEDED`.

## Pairing the Auditor With Tilelive, Tippecanoe, and MapLibre Style JSON

The auditor is one piece of a four-piece pipeline:

1. **Tippecanoe** produces `.mvt` tiles from GeoJSON / FlatGeobuf sources.
2. **PMTiles** archives those tiles into a single file for cheap static hosting.
3. **Tilelive** serves the archive behind a `tile.json` route.
4. **MapLibre Style JSON** consumes the archive and renders the map.

The auditor inserts itself between 1 and 2, and again between 2 and 3. Between 1 and 2 it audits the per-zoom tile stream; between 2 and 3 it audits the archive directory and the tile-size budget. Together these catch:

- Spec drift in newer Tippecanoe versions.
- Pre-v3 PMTiles legacy archives.
- Tilelive cache invalidation regressions when the directory is regenerated.

Pair it with the [Elysia Tools MVT / PMTiles auditor](https://elysiatools.com/en/tools/mvt-mapbox-vector-tile-pmtiles-google-mvt-projection-and-tilelive-encoding-auditor), set budgets that match your CDN tier, and the next time a tile claims a polygon ring that crosses the equator, you will see `RING_WINDING_INVERTED` instead of a fish-eye render. For more tools spanning maps, encoding, and protocol-level inspection, see [Elysia Tools](https://elysiatools.com/en/tools).

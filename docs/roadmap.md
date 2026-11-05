# Roadmap

OEI Core follows semantic versioning. Each milestone is independently usable.

## 0.1.0 — Energy Data Integration and Validation Engine

- CSV and JSON import with SHA-256 hashing
- Declarative YAML mapping with named transforms
- Field-level validation and quality report
- CSV and JSON export with embedded provenance
- FastAPI and Typer interfaces
- Model adapter protocol and OSeMOSYS adapter

## 0.2.0 — Container, persistence, standards, governance (current)

- Production Docker image with healthcheck and non-root user
- SQLite provenance store with `--record`, `provenance-list`, and
  `provenance-show`
- `docs/interoperability.md` aligning OEI with W3C PROV, Frictionless Data,
  OEMetadata, and FAIR principles
- `MAINTAINERS.md`, `CODEOWNERS`, issue templates, and PR template
- Institutional pilot brief (`docs/pilot.md`)

## 0.3.x — Model adapters and standard exports

- PyPSA adapter (power-system optimisation)
- pandapower adapter (network analysis)
- Frictionless Data `Table Schema` export
- Unit-aware mapping transforms (kW ↔ MW, MWh ↔ GWh, MJ ↔ kWh)
- Contributor and keyword fields added to `Provenance`

## 0.4.x — Spatial analysis and PROV

- GeoPandas integration for geographic fields
- W3C PROV-JSON export
- OnSSET and Energy Access Explorer input compatibility
- WKT and GeoJSON importers and exporters

## 0.5.x — Interactive prototype

- Streamlit UI for exploring harmonised datasets
- Plotly charts for quality reports and time series
- Report export (HTML / PDF)

## 1.0.0 — Stable interface

- Frozen data model and mapping schema
- Reproducible workflow runner (recorded runs, cached intermediates)
- Scenario comparison across sources
- Published documentation site and PyPI release
- Formal OEMetadata conformance test in CI
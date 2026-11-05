# Changelog

## [Unreleased]

### Added

## [0.2.2] - 2026-11-05

### Fixed

- Release workflow: simplified `pip-licenses` invocation to avoid shell escaping issues. Removed `--with-license-file` and `--no-license-path`.

## [0.2.1] - 2026-11-05

### Fixed

- Release workflow: added `--with-license-file` to `pip-licenses` so `--no-license-path` is accepted. The `v0.2.0` release failed at the `Generate THIRD_PARTY_NOTICES.md` step before building any artifacts.

## [0.2.0]

### Added

- `Dockerfile`, `docker-compose.yml`, `.dockerignore` — production container image (multi-stage, non-root, healthcheck) and CI smoke test.
- `oei.provenance.SqliteStore` — persistent provenance store with SQLite backend.
- `oei harmonise --record` — persist provenance and quality report.
- `oei provenance-list` — list recorded provenance entries.
- `oei provenance-show <id>` — print a stored provenance record as JSON.
- `docs/interoperability.md` — alignment with W3C PROV, Frictionless Data, OEMetadata, and FAIR principles.
- `docs/pilot.md` — one-page institutional pilot brief.
- `MAINTAINERS.md` — governance, responsibilities, and maintainer nomination path.

## [0.1.0] - 2026-11-04

### Added

- CSV and JSON dataset importers with SHA-256 provenance hashing.
- Declarative YAML mapping engine.
- Field-level validation and quality report generation.
- CSV and JSON exporters with embedded provenance.
- FastAPI `/v1/health` and `/v1/harmonise` endpoints.
- Typer-based CLI (`oei harmonise`).
- Model adapter protocol for PyPSA, OSeMOSYS, pandapower, and future integrations.
- Example Kenya generation datasets and mappings.
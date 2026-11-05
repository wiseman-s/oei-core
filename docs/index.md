# OEI Core

OEI Core is the first component of the Open Energy Intelligence project — an
open-source bridge between energy data and energy modelling tools.

It imports, maps, validates and exports harmonised energy datasets with full
provenance. It starts with Kenya and is designed for global use.

## What it does

- Imports CSV and JSON energy datasets.
- Maps them into a shared OEI data model via declarative YAML configurations.
- Validates fields, types, units and data quality.
- Records provenance (source, retrieval time, licence, SHA-256 hash,
  transformations).
- Exports harmonised datasets to CSV and JSON.
- Exposes a REST API and a CLI.
- Persists provenance to a local SQLite store.
- Provides an adapter protocol for PyPSA, OSeMOSYS, pandapower and other
  models.

## First milestone

OEI Core 0.1.0 — Energy Data Integration and Validation Engine.

Two differently structured energy datasets are mapped into a shared schema,
validated, quality-reported, and exported with provenance preserved.

## Current release

**OEI Core 0.2.0** adds a production Docker image, a SQLite provenance store,
explicit alignment with W3C PROV, Frictionless Data and OEMetadata, and a
governance and pilot framework.

## Not a dashboard

OEI is not another standalone dashboard. It is a shared integration and
validation layer that connects existing tools and datasets, complementing
ecosystems such as [OpenGrid](https://opengrid.org/) rather than duplicating
them.

## Author

OEI Core is created and maintained by Simon Wanyoike
([@wiseman-s](https://github.com/wiseman-s)).
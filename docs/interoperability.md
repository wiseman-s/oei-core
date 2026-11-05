# Interoperability

OEI Core is designed to interoperate with existing open standards rather than
invent a new one. This document states OEI's alignment with the standards most
relevant to energy-data work and records where OEI currently diverges.

## Principles

1. **Adopt, don't invent.** Where a mature standard exists, OEI's data model
   maps onto it. OEI's own schema is a thin, opinionated projection, not a
   competitor.
2. **Preserve provenance verbatim.** Source metadata is stored and exposed as
   received. OEI never rewrites a source's metadata; it wraps it.
3. **Round-trip fidelity.** Exporting a dataset back to a standard format
   preserves all fields that were imported.
4. **Explicit gaps.** Where OEI does not yet implement a standard, this file
   says so.

## Alignment matrix

| Standard | Scope | OEI status | Where in code |
| -------- | ----- | ---------- | ------------- |
| **W3C PROV** | Provenance model (`Entity`, `Activity`, `Agent`) | **Aligned (subset)** — OEI's `Provenance` + `ProvenanceStep` map to `Entity` + `Activity`. `Agent` (software + person) is implicit in `schema_version`. | `src/oei/models/provenance.py` |
| **Frictionless Data Table Schema** | Column-level field definitions | **Aligned** — `FieldSpec.name`, `type`, `unit` map to Frictionless `name`, `type`, `unit`. `required` maps to `constraints.required`. | `src/oei/models/field.py` |
| **OEMetadata (Open Energy Platform)** | Energy-specific dataset metadata | **Partial** — OEI records `source_name`, `source_uri`, `source_licence`, `retrieved_at`. OEMetadata requires `title`, `description`, `contributors`, `resources`, `spatial`, `temporal`, `keywords`, `licenses`. | `src/oei/models/provenance.py` |
| **OEP Table Schema** | OEP tabular schema conventions | **Compatible** — OEI emits CSV with headers and per-column units; importable by OEP's `Table` reader after a mapping. | `src/oei/io/csv_writer.py` |
| **Dublin Core** | General metadata (title, creator, licence, date) | **Partial** — `source_name`, `source_uri`, `source_licence`, `retrieved_at` map to `Title`, `Source`, `License`, `Date`. | `src/oei/models/provenance.py` |
| **SPDX licence identifiers** | Licence strings | **Required** — `MappingConfig.source_licence` must be an SPDX identifier. | `src/oei/mapping/mapping_config.py` |
| **CF Conventions** | Climate / meteorological data | **Not implemented** — future adapter for NASA POWER outputs. | — |
| **EnergyPlus / IDF** | Building energy models | **Not implemented** — out of scope for 0.2.x. | — |
| **OpenAPI 3.1** | HTTP API description | Compliant — `/openapi.json` validated in CI. | `src/oei/api/app.py` |

## W3C PROV mapping

OEI's provenance model is a strict subset of W3C PROV:

| OEI | W3C PROV |
| --- | -------- |
| `Provenance` (whole object) | `prov:Entity` |
| `Provenance.source_hash` | `prov:value` (content hash of the source) |
| `Provenance.source_uri` | `prov:atLocation` |
| `Provenance.retrieved_at` | `prov:generatedAtTime` |
| `Provenance.schema_version` | `prov:wasGeneratedBy` → software agent version |
| `ProvenanceStep` | `prov:Activity` |
| `ProvenanceStep.applied_at` | `prov:endedAtTime` |
| `ProvenanceStep.operation` | `prov:type` |

OEI does not yet emit PROV-JSON or PROV-O. Planned for `0.4.0`.

## Frictionless Data mapping

`FieldSpec` maps directly to a Frictionless `field` descriptor:

```yaml
# OEI FieldSpec
name: capacity_mw
type: float
unit: MW
required: true
minimum: 0
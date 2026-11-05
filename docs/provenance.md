# Provenance

Every dataset records source name, URI, licence, retrieval time, SHA-256 hash and an ordered list of transformation steps. The hash is computed from the raw source bytes, so downstream outputs can always be traced back to the exact input used.

## Persistent provenance store

OEI records provenance in memory for every run and can persist it to a local SQLite database for auditing and trend analysis.

### Recording a run

```bash
oei harmonise examples/data/kenya_generation_a.csv examples/mappings/source_a.yaml --record
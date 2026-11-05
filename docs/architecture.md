# Architecture

`io` → `mapping` → `validation` → `export`, wired through `models` and exposed via `api` and `cli`. Every stage receives and returns typed Pydantic objects so provenance and quality are never lost.

## Persistence layer

OEI Core is stateless by default: files in, files out. Persistence is opt-in via the `--record` flag, which writes provenance and quality reports to a local SQLite database through `oei.provenance.SqliteStore`.

The store implements a `ProvenanceStore` protocol so deployments can swap in Postgres without changing call sites:

```python
from oei.provenance import ProvenanceStore, SqliteStore


def record_run(store: ProvenanceStore, dataset, report):
    return store.record(dataset, report)


record_run(
    SqliteStore("~/.oei/provenance.db"),
    dataset,
    report,
)
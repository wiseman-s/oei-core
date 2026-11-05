"""Round-trip integration test: CSV → OEI → OSeMOSYS tables → OEI → CSV."""

from __future__ import annotations

from pathlib import Path

from oei.adapters.osemosys import OSeMOSYSAdapter
from oei.io.csv_reader import read_csv
from oei.io.csv_writer import write_csv
from oei.mapping.engine import apply_mapping
from oei.mapping.mapping_config import MappingConfig


def test_end_to_end_roundtrip(tmp_path: Path) -> None:
    source = Path("examples/data/kenya_generation_a.csv")
    mapping = Path("examples/mappings/source_a.yaml")
    frame, digest = read_csv(source)
    config = MappingConfig.from_yaml(mapping)
    dataset = apply_mapping(frame, config, digest)

    adapter = OSeMOSYSAdapter()
    outputs = adapter.to_model_inputs(dataset)
    restored = adapter.from_model_outputs(outputs)

    out = tmp_path / "osemosys_roundtrip.csv"
    write_csv(restored, out)
    assert out.exists()
    assert "technology" in out.read_text(encoding="utf-8")

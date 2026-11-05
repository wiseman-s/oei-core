"""Tests for the HTTP API."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from oei.api.app import create_app


def _write_files(tmp_path: Path) -> tuple[Path, Path]:
    data = tmp_path / "data.csv"
    data.write_text(
        "date,plant,capacity_mw\n2024-01-01,Olkaria I,45.0\n",
        encoding="utf-8",
    )
    mapping = tmp_path / "mapping.yaml"
    mapping.write_text(
        """
source_name: demo
source_licence: CC-BY-4.0
source_uri: https://example.org/demo.csv
schema_fields:
  - name: timestamp
    type: timestamp
  - name: plant_name
    type: string
  - name: capacity_mw
    type: float
    minimum: 0
mappings:
  - source: date
    target: timestamp
  - source: plant
    target: plant_name
  - source: capacity_mw
    target: capacity_mw
""",
        encoding="utf-8",
    )
    return data, mapping


def test_health() -> None:
    client = TestClient(create_app())
    assert client.get("/v1/health").json() == {"status": "ok"}


def test_harmonise_endpoint(tmp_path: Path) -> None:
    data, mapping = _write_files(tmp_path)
    client = TestClient(create_app())
    response = client.post(
        "/v1/harmonise",
        json={
            "source_path": str(data),
            "source_format": "csv",
            "mapping_path": str(mapping),
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["row_count"] == 1
    assert body["is_valid"] is True


def test_harmonise_rejects_bad_format(tmp_path: Path) -> None:
    data, mapping = _write_files(tmp_path)
    client = TestClient(create_app())
    response = client.post(
        "/v1/harmonise",
        json={
            "source_path": str(data),
            "source_format": "xml",
            "mapping_path": str(mapping),
        },
    )
    assert response.status_code == 400

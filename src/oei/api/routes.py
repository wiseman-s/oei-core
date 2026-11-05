"""HTTP routes for OEI Core."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from oei.io.csv_reader import read_csv
from oei.io.json_reader import read_json_records
from oei.mapping.engine import apply_mapping
from oei.mapping.mapping_config import MappingConfig
from oei.validation.quality_report import build_quality_report

router = APIRouter()


class HarmoniseRequest(BaseModel):
    source_path: str
    source_format: str
    mapping_path: str


class HarmoniseResponse(BaseModel):
    dataset_name: str
    row_count: int
    error_count: int
    warning_count: int
    is_valid: bool
    provenance_hash: str


@router.get("/health")
def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}


@router.post("/harmonise", response_model=HarmoniseResponse)
def harmonise(request: HarmoniseRequest) -> HarmoniseResponse:
    """Load a source dataset, apply a mapping and return a quality summary."""
    source_path = Path(request.source_path)
    mapping_path = Path(request.mapping_path)

    try:
        if request.source_format == "csv":
            frame, digest = read_csv(source_path)
        elif request.source_format == "json":
            frame, digest = read_json_records(source_path)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported source format.",
            )

        config = MappingConfig.from_yaml(mapping_path)
        dataset = apply_mapping(frame, config, digest)
        report = build_quality_report(dataset)

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return HarmoniseResponse(
        dataset_name=dataset.name,
        row_count=len(dataset.records),
        error_count=report.error_count,
        warning_count=report.warning_count,
        is_valid=report.is_valid,
        provenance_hash=dataset.provenance.source_hash,
    )

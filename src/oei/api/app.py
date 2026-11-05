"""FastAPI application factory for OEI Core."""

from __future__ import annotations

from fastapi import FastAPI

from oei import __version__
from oei.api.routes import router
from oei.config import load_settings


def create_app() -> FastAPI:
    """Create and configure the OEI FastAPI application."""
    settings = load_settings()
    app = FastAPI(
        title="OEI Core",
        version=__version__,
        description=(
            "Open Energy Intelligence Core: import, map, validate and export "
            "harmonised energy datasets with full provenance."
        ),
        license_info={"name": "Apache-2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0"},
    )
    app.state.settings = settings
    app.include_router(router, prefix="/v1")
    return app


app = create_app()

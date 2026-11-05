# OEI Core

[![CI](https://github.com/wiseman-s/oei-core/actions/workflows/ci.yml/badge.svg)](https://github.com/wiseman-s/oei-core/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/badge/pypi-oei--core-blue)](https://pypi.org/project/oei-core/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](pyproject.toml)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](Dockerfile)

**Open Energy Intelligence Core** is an open-source integration and validation
engine for energy data. It maps heterogeneous CSV and JSON energy datasets into
a shared schema, validates them, records full provenance, and exports harmonised
results through a Python library, a CLI, and a REST API.

- Status: `0.2.0` (beta)
- Licence: Apache-2.0
- Python: 3.10+
- Starting point: Kenya, local-first on Windows 11, zero-cost development
- Long-term ambition: a globally reusable Digital Public Good for the energy
  sector

## Why

Energy information is scattered across spreadsheets, databases, reports and
modelling tools. Data uses different column names, units, time intervals,
geographic references and definitions, which makes it hard to combine datasets,
check completeness, prepare model inputs, trace results back to sources, or
reproduce an analysis.

OEI provides a shared integration and validation layer — it does not replace
specialist modelling software such as PyPSA or OSeMOSYS, it connects to them.

## Install

```bash
python -m pip install -e ".[dev]"
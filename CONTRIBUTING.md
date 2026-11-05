# Contributing to OEI Core

Maintained by Simon Wanyoike ([@wiseman-s](https://github.com/wiseman-s),
alphageek254@gmail.com).

Thank you for considering a contribution. OEI Core aims to be a high-quality,
internationally reusable open-source project, and your help makes that possible.

## Before you start

1. Read [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
2. Open an issue before starting substantial changes so we can align on scope.
3. For bug reports, include:
   - OEI Core version (`oei --help` prints it, or `python -c "import oei; print(oei.__version__)"`)
   - Python version and OS
   - A minimal reproduction (source dataset + mapping YAML if relevant)
   - The full traceback

## Development workflow

```bash
python -m venv .venv
source .venv/bin/activate        # or .venv\Scripts\activate on Windows
python -m pip install -e ".[dev]"
pre-commit install
# Maintainers

## Current maintainers

| Name | GitHub | Email | Role | Areas |
| ---- | ------ | ----- | ---- | ----- |
| Simon Wanyoike | [@wiseman-s](https://github.com/wiseman-s) | alphageek254@gmail.com | Lead maintainer | All areas; final review authority |

We are actively looking for co-maintainers. See "Becoming a maintainer" below.

## Responsibilities

Maintainers are expected to:

1. Review pull requests within 5 working days.
2. Triage new issues within 5 working days.
3. Keep CI green on `main` at all times.
4. Respond to security reports per `SECURITY.md`.
5. Prepare releases following `CHANGELOG.md` and `docs/roadmap.md`.
6. Represent OEI in upstream communities (OpenGrid, PyPSA, OSeMOSYS, OEP)
   where relevant.

## Decision making

- **Small changes** (bug fixes, docs, tests, dependency bumps): one maintainer
  review is sufficient.
- **Feature changes** (new adapters, new CLI commands, schema changes): two
  maintainer approvals, or one maintainer + one domain expert.
- **Breaking changes** (schema field removals, API breakage, licence changes):
  requires a GitHub issue open for at least 14 days with an RFC-style
  description, and two maintainer approvals.
- **Disputes**: the lead maintainer makes the final call and documents the
  decision in the relevant issue.

## Becoming a maintainer

Contributors who demonstrate sustained, high-quality involvement may be invited
to become maintainers. Signals we look for:

- **5+ merged non-trivial pull requests** across at least 2 areas (e.g. code
  and tests, or docs and adapters).
- **Consistent, respectful review participation** on others' PRs.
- **Aligned values**: the design principles in `README.md` and the scope in
  `docs/roadmap.md`.
- **Domain expertise** relevant to an area (energy modelling, geospatial,
  metadata standards, or a specific country's data).

If you are interested, open an issue titled `maintainer nomination: <name>` and
describe your contributions. Existing maintainers will respond within 14 days.

## Emeritus maintainers

Former maintainers are listed here when they step back. Their past contributions
are acknowledged in `CHANGELOG.md`.

*(none yet)*

## Contact

- General: open an issue at <https://github.com/wiseman-s/oei-core/issues>
- Security: see `SECURITY.md`
- Conduct: see `CODE_OF_CONDUCT.md`
- Maintainer coordination: open an issue titled `maintainers: <topic>`
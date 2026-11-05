# Security Policy

## Supported versions

OEI Core is pre-1.0. Only the latest `0.2.x` release receives security updates.

| Version | Supported |
| ------- | --------- |
| 0.2.x   | yes       |
| 0.1.x   | no        |
| < 0.1   | no        |

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security problems.

Report privately using GitHub's
[private vulnerability reporting](https://github.com/wiseman-s/oei-core/security/advisories/new)
or email **alphageek254@gmail.com**.

Include:

- Affected version
- A minimal reproduction (source dataset, mapping YAML, or API request)
- Impact assessment
- Any suggested mitigation

We aim to:

- Acknowledge reports within 5 working days
- Provide an initial assessment within 10 working days
- Release a fix within 30 days for critical issues

## Scope

OEI Core processes untrusted CSV and JSON files. Report anything that could lead
to code execution, denial of service, path traversal, or silent data corruption.
Security issues in third-party dependencies should be reported upstream; we will
update affected dependencies promptly.

## Out of scope

- Issues in data provided by third parties (report to the data provider)
- Misconfiguration of self-hosted deployments
- Vulnerabilities requiring physical access to the host
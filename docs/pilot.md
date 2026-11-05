# OEI Core Pilot

*A one-page brief for energy institutions considering a pilot with OEI Core.*

## The problem

Your institution stores energy data across spreadsheets, PDFs, databases and
vendor systems. Combining them requires manual reconciliation. Producing a
reproducible analysis takes weeks, and nobody can prove afterwards which version
of which file was used.

## The OEI pilot

A **6–12 week pilot** with one institution, one country, one concrete analysis.

**You provide:**

- 2–5 energy datasets (generation, capacity, demand, or network), in whatever
  format they already exist.
- One staff member as a point of contact, ~2 hours per week.
- One analysis question you want answered ("How much geothermal capacity was
  available in 2023?" or "Which counties have the highest unserved demand?").

**OEI provides, at no cost:**

- Mapping of your datasets into a shared, validated schema.
- A quality report showing missing values, unit mismatches, and inconsistencies.
- A provenance record for every output, so any result can be traced back to its
  exact source file and mapping.
- A repeatable workflow: next year's data is processed with the same mapping,
  producing directly comparable results.
- Public attribution in the OEI repository and documentation (with your consent).

**You get:**

- A reproducible analysis you can defend in meetings and audits.
- Data-quality visibility you didn't have before.
- A free, Apache-2.0-licensed tool your team keeps after the pilot ends.
- Input into OEI's roadmap for the next 6–12 months.

**OEI gets:**

- A documented case study with real data.
- A reference the project can cite when applying for further funding.
- Feedback that shapes `0.2.x` and `0.3.x` features.

## Scope of a pilot

| Phase | Duration | What happens | Deliverable |
| ----- | -------- | ------------ | ----------- |
| **1. Discovery** | Week 1 | Kick-off call; you share a small sample of each dataset; we agree on the analysis question | Signed scope agreement (1 page) |
| **2. Data mapping** | Weeks 2–4 | OEI team writes mapping YAML for each source; you review | 2–5 mapping files, quality report per source |
| **3. Validation** | Weeks 4–6 | We run validation, produce quality reports, agree on fixes | Quality report; cleaned export |
| **4. Analysis** | Weeks 6–9 | We run the agreed analysis on harmonised data | Analysis output + reproducible script |
| **5. Handover** | Weeks 9–12 | Training session for your team; final report | 90-minute training; 2-page report |

## What we ask of you

- **Data publication terms.** We will not redistribute your data without
  explicit written permission. The mapping files and processing steps may be
  public (they contain no raw data), but datasets themselves remain yours.
- **Attribution.** If the pilot produces a public output, we would like to name
  your institution as the pilot partner. You may decline.
- **Feedback.** A 30-minute call at weeks 6 and 12.

## What we will not do

- **We will not sell, resell, or commercialise your data.**
- **We will not publish analysis results without your review and approval.**
- **We will not lock you into proprietary formats.** All OEI outputs are plain
  CSV and JSON; you own them.
- **We will not disappear.** OEI Core is Apache-2.0-licensed; you may fork it.

## Contact

Open an issue on GitHub titled **"Pilot inquiry: <institution name>"** or email
`pilots@oei-project.example`. We aim to respond within 7 days.
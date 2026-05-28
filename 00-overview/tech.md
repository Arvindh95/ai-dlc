# Tech

_Target stack, code repository, and runtime environments. Set at kickoff. Updated when stack changes — record significant changes via ADR in `design/adrs/`._

## Code repository
- **URL:** TBD-set-at-kickoff (e.g. `https://github.com/<org>/<project-slug>`)
- **Default branch:** TBD-set-at-kickoff (e.g. `main`)
- **Visibility:** TBD-set-at-kickoff (private / internal / public)
- **This requirements repo URL:** TBD-set-at-kickoff

## Target stack

| Layer | Choice | Version | Notes |
|-------|--------|---------|-------|
| Frontend | TBD-set-at-kickoff | — | — |
| Backend | TBD-set-at-kickoff | — | — |
| Database | TBD-set-at-kickoff | — | — |
| Cache / queue | TBD-set-at-kickoff | — | — |
| Auth | TBD-set-at-kickoff | — | — |
| Hosting | TBD-set-at-kickoff | — | AWS / Azure / on-prem / hybrid |
| CI/CD | TBD-set-at-kickoff | — | — |
| Observability | TBD-set-at-kickoff | — | logs, metrics, tracing |

## Environments

| Env | URL | Owner | Auto-deploy from | Access |
|-----|-----|-------|------------------|--------|
| dev | TBD-set-at-kickoff | Tech Lead | `main` | team-only |
| staging / UAT | TBD-set-at-kickoff | Tech Lead | release tag | team + client |
| prod | TBD-set-at-kickoff | Tech Lead | manual promote | client + DevOps |

## Notes
- Stack changes after kickoff require an ADR in `design/adrs/`.
- Env URL changes go in Change Log below, no ADR needed.

## Change Log
- 2026-05-28: Template created.

# Security & Data Classification

_Fill in during kickoff. DPO sign-off required before development starts._

## Data classification (per data type the system will handle)
| Data type | Sensitivity | Storage | Retention | Cross-border |
|-----------|-------------|---------|-----------|--------------|
| TBD-set-at-kickoff (e.g., customer name + email) | PDPA-personal | Encrypted at rest | 7 years | No |

## AI usage rules
- **Never paste raw PII into Claude prompts.** Use redaction script before pasting logs / extracts.
- **No client data in third-party LLMs other than Claude** (per Censof AI policy).
- **Audit log:** every AI-generated record cites source MD + model + date in footer.

## Compliance frameworks applicable
- PDPA (Malaysia)
- TBD-set-at-kickoff (industry-specific — e.g., BNM RMiT, MDEC, ISO 27001)

## Secrets management
- Production secrets: TBD-set-at-kickoff (e.g., Azure Key Vault / AWS Secrets Manager)
- **Never commit secrets** — `.gitignore` covers `.env`, `*.key`, `*.pem`
- Rotation cadence: TBD-set-at-kickoff

## DPO contact
- **Name:** TBD-set-at-kickoff
- **Email:** TBD-set-at-kickoff
- **Escalation SLA:** 24h for data-breach suspicion

## Change Log
- 2026-05-26: Template created.

"""Per-record frontmatter validator. Run in CI."""
import sys
import yaml
import re
from pathlib import Path

REQUIRED_FIELDS = {
    "requirements":    ["id", "title", "status", "priority", "team", "created", "last_updated"],
    "tasks":           ["id", "title", "status", "team", "req_ref", "sprint", "estimate_hours", "last_updated"],
    "feedback":        ["id", "sprint_raised", "source", "type", "severity", "status", "related_req"],
    "spec":            ["id", "title", "status", "version", "last_updated", "covers_req"],
    "design":          ["id", "title", "status", "version", "last_updated"],
    "adrs":            ["id", "title", "status", "date", "deciders"],
    "decisions":       ["id", "date", "type", "participants", "status"],
    "incidents":       ["id", "date", "severity", "incident_commander", "data_loss", "data_breach", "status"],
    "change-requests": ["id", "type", "raised_by", "raised_date", "affects_req", "status"],
    "raw-inputs":      ["id", "source_type", "source_date", "captured_by", "status"],
}

CONDITIONAL_REQUIRED = {
    "tasks": [
        ("assignee", lambda fm: fm.get("status") != "todo"),
    ],
    "requirements": [
        ("approved",    lambda fm: fm.get("status") in
            ["approved", "in-dev", "ready-for-acceptance", "done"]),
        ("approved_by", lambda fm: fm.get("status") in
            ["approved", "in-dev", "ready-for-acceptance", "done"]),
        ("implemented", lambda fm: fm.get("status") == "done"),
    ],
    "raw-inputs": [
        ("generated_reqs", lambda fm: fm.get("status") in
            ["partially-processed", "fully-processed"]),
    ],
}

STATUS_VALUES = {
    "requirements":    ["draft", "approved", "in-dev", "ready-for-acceptance", "done",
                        "blocked", "late-change", "rejected", "deferred"],
    "tasks":           ["todo", "in-progress", "review", "done", "blocked"],
    "feedback":        ["triaged", "accepted", "in-progress", "done", "rejected", "deferred", "duplicate"],
    "spec":            ["draft", "approved", "deprecated"],
    "design":          ["draft", "approved", "deprecated"],
    "adrs":            ["proposed", "accepted", "deprecated", "superseded"],
    "decisions":       ["pending", "decided", "superseded"],
    "incidents":       ["open", "mitigated", "resolved", "postmortem-pending", "closed"],
    "change-requests": ["under-review", "approved", "rejected", "deferred"],
    "raw-inputs":      ["unprocessed", "partially-processed", "fully-processed", "superseded"],
}

SKIP_FILES = {
    "_index.md", "_prompts.md",
    "INBOX.md", "backlog.md", "retro.md",
    "README.md", "CHANGELOG.md", "CLAUDE.md", "KICKOFF.md",
    "licenses.md", "feature-flags.md", "secret-rotation-log.md",
    "dashboard.md", "velocity.md", "sprint-board.md", "ops-daily.md",
    "drift-report.md",
    "vision.md", "scope.md", "stakeholders.md", "glossary.md",
    "teams.md", "security.md", "ai-config.md",
}

def classify(file_path):
    for part in file_path.parts:
        if part in REQUIRED_FIELDS:
            return part
    return None

def validate(file_path):
    errors = []
    if file_path.name in SKIP_FILES:
        return []
    content = file_path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return [f"{file_path}: missing frontmatter"]
    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return [f"{file_path}: invalid YAML - {e}"]

    md_type = classify(file_path)
    if not md_type:
        return []

    for field in REQUIRED_FIELDS[md_type]:
        if field not in fm:
            errors.append(f"{file_path}: missing required field '{field}'")

    for field, required_when in CONDITIONAL_REQUIRED.get(md_type, []):
        if required_when(fm) and not fm.get(field):
            errors.append(f"{file_path}: '{field}' required given current status")

    if "status" in fm and fm["status"] not in STATUS_VALUES[md_type]:
        errors.append(f"{file_path}: invalid status '{fm['status']}' for {md_type}")

    return errors

if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    all_errors = []
    for md_file in root.rglob("*.md"):
        all_errors.extend(validate(md_file))
    for err in all_errors:
        print(err)
    sys.exit(1 if all_errors else 0)

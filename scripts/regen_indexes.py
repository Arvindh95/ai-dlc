"""Tier-aware validator + catalog regenerator. See AI-DLC Playbook 3.2.0 + Appendix A.4."""
import sys
import yaml
import re
from pathlib import Path
from datetime import date, datetime

AUTO_MARKER = "<!-- auto-managed below -->"

SKIP_DIRS = {
    ".git", ".obsidian", ".github", "node_modules", "__pycache__",
    "dist", "build", ".venv", "venv", ".pytest_cache", ".mypy_cache",
    "exports", "snapshots", "cache", "_generated", "tmp",
}

TIER_A_PATTERNS = [
    "requirements", "spec", "design", "tasks", "feedback",
    "decisions", "incidents", "prompts", "deliverables",
    "dashboard", "raw-inputs", "signoffs", "change-requests",
    "00-overview", "adrs",
]

TIER_B_PATTERNS = [
    "services", "libs", "infra", "runbooks", "alerts", "tests", "scripts",
]

def folder_tier(folder, repo_root=None):
    parts = set(folder.parts)
    if parts & SKIP_DIRS:
        return "C"
    if any(p in parts for p in TIER_A_PATTERNS):
        return "A"
    if any(p in parts for p in TIER_B_PATTERNS):
        return "B"
    if repo_root is not None and folder.resolve() == repo_root.resolve():
        return "A"
    return "C"

def find_md_folders(root):
    folders = []
    if not any(part in SKIP_DIRS for part in root.resolve().parts):
        folders.append(root)
    for d in root.rglob("*"):
        if not d.is_dir():
            continue
        if any(part in SKIP_DIRS for part in d.parts):
            continue
        folders.append(d)
    return folders

def parse_frontmatter(file_path):
    text = file_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m: return {}
    try: return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError: return {}

def build_catalog(folder):
    rows = []
    for f in sorted(folder.iterdir()):
        if not f.is_file(): continue
        if f.name in ("_index.md", "_prompts.md"): continue
        if f.name.startswith("."): continue
        if f.suffix == ".md":
            fm = parse_frontmatter(f)
            participants = fm.get("participants")
            participant_lead = participants[0] if isinstance(participants, list) and participants else None
            owner = (fm.get("owner") or fm.get("assignee") or fm.get("incident_commander")
                     or participant_lead or fm.get("raised_by") or fm.get("team") or "-")
            updated = fm.get("last_updated") or fm.get("created") or fm.get("date") or "-"
            rows.append({"file": f.name, "id": fm.get("id") or "-",
                         "title": fm.get("title") or f.stem,
                         "status": fm.get("status") or "-",
                         "owner": owner, "updated": updated})
        else:
            mtime = datetime.fromtimestamp(f.stat().st_mtime).date().isoformat()
            rows.append({"file": f.name, "id": "-", "title": f.stem, "status": "-", "owner": "-", "updated": mtime})

    if not rows:
        return "_(empty)_"

    lines = ["| File | ID | Title | Status | Owner | Updated |",
             "|------|----|----|--------|-------|---------|"]
    for r in rows:
        lines.append(f"| [{r['file']}]({r['file']}) | {r['id']} | {r['title']} | {r['status']} | {r['owner']} | {r['updated']} |")
    return "\n".join(lines)

INDEX_REQUIRED_FIELDS = ["folder", "purpose", "owner", "file_naming", "last_updated", "ai_navigation_hint"]
PROMPTS_REQUIRED_FIELDS = ["folder", "purpose_of_this_file", "canonical_prompts_location", "last_updated", "ai_behavior_hint"]
PROMPTS_REQUIRED_SECTIONS = ["## OP-", "## Forbidden", "## Escalate"]

def validate_index_frontmatter(folder):
    index_file = folder / "_index.md"
    if not index_file.exists():
        return True, ""
    fm = parse_frontmatter(index_file)
    missing = [f for f in INDEX_REQUIRED_FIELDS if not fm.get(f)]
    if missing:
        return False, f"INCOMPLETE FRONTMATTER: {index_file} - missing or empty: {missing}"
    return True, f"FRONTMATTER OK: {index_file}"

def bump_frontmatter_last_updated(text):
    today = date.today().isoformat()
    fm_match = re.match(r"^(---\n)(.*?)(\n---)", text, re.DOTALL)
    if not fm_match: return text
    head, body, tail = fm_match.groups()
    if re.search(r"^last_updated:", body, re.MULTILINE):
        new_body = re.sub(r"^last_updated:.*$", f"last_updated: {today}", body, flags=re.MULTILINE)
    else:
        new_body = body.rstrip() + f"\nlast_updated: {today}"
    return text[:fm_match.start()] + head + new_body + tail + text[fm_match.end():]

def regenerate_index(folder, tier="A"):
    index_file = folder / "_index.md"
    if not index_file.exists():
        return False, f"MISSING: {index_file} - Tier {tier} folder requires _index.md"
    content = index_file.read_text(encoding="utf-8")
    if AUTO_MARKER not in content:
        return False, f"NO MARKER: {index_file}"
    before, _ = content.split(AUTO_MARKER, 1)
    catalog = build_catalog(folder)
    new_no_bump = f"{before}{AUTO_MARKER}\n\n## Auto-generated catalog\n\n{catalog}\n"
    if new_no_bump == content:
        return True, f"UP-TO-DATE: {index_file}"
    new_content = bump_frontmatter_last_updated(new_no_bump)
    index_file.write_text(new_content, encoding="utf-8")
    return True, f"REGENERATED: {index_file}"

def validate_prompts(folder, tier="A"):
    prompts_file = folder / "_prompts.md"
    if not prompts_file.exists():
        return False, f"MISSING: {prompts_file} - Tier {tier} folder requires _prompts.md"
    content = prompts_file.read_text(encoding="utf-8")
    fm = parse_frontmatter(prompts_file)
    missing_fields = [f for f in PROMPTS_REQUIRED_FIELDS if not fm.get(f)]
    if missing_fields:
        return False, f"INCOMPLETE: {prompts_file} - missing fields: {missing_fields}"
    missing_sections = [s for s in PROMPTS_REQUIRED_SECTIONS if s not in content]
    if missing_sections:
        return False, f"INCOMPLETE: {prompts_file} - missing sections: {missing_sections}"
    return True, f"OK: {prompts_file}"

if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    folders = find_md_folders(root)
    failed = []
    for folder in folders:
        tier = folder_tier(folder, repo_root=root)
        if tier == "C":
            print(f"SKIP (Tier C): {folder}")
            continue
        ok_idx, msg_idx = regenerate_index(folder, tier=tier)
        print(f"[Tier {tier}] {msg_idx}")
        if not ok_idx: failed.append(msg_idx)
        ok_fm, msg_fm = validate_index_frontmatter(folder)
        if msg_fm: print(f"[Tier {tier}] {msg_fm}")
        if not ok_fm: failed.append(msg_fm)
        if tier == "A":
            ok_prm, msg_prm = validate_prompts(folder, tier=tier)
            print(f"[Tier {tier}] {msg_prm}")
            if not ok_prm: failed.append(msg_prm)
        else:
            prompts_file = folder / "_prompts.md"
            if prompts_file.exists():
                ok_prm, msg_prm = validate_prompts(folder, tier=tier)
                print(f"[Tier {tier}] {msg_prm}")
                if not ok_prm: failed.append(msg_prm)
    if failed:
        print(f"\n{len(failed)} validation failure(s).")
        sys.exit(1)
    print(f"\nAll required folders OK.")

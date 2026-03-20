"""
Persona Parser — loads TeachMeAI Intake_v2 CSV, YAML, or JSON persona data.
"""
import csv
import json
import os

try:
    import yaml
except ImportError:
    yaml = None


JSON_COLUMNS = [
    "Intake State JSON",
    "Deep Research JSON",
    "Learner Profile JSON",
    "IMPACT Strategy JSON",
    "Execution Plan JSON",
    "Final Report JSON",
]

# Keys we want to surface from the parsed JSON blocks
EXTRACT_KEYS = [
    "topPriorities",
    "marketMaturityScore",
    "decisionStyle",
    "uncertaintyHandling",
    "cognitiveLoadTolerance",
    "socialEntanglement",
    "portfolioArtifact",
]


def _safe_json(raw):
    """Parse a JSON string, returning {} on failure."""
    if not raw or not isinstance(raw, str):
        return {}
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {}


def _flatten_blocks(blocks):
    """Merge a list of parsed JSON dicts into a single persona dict, extracting known keys."""
    merged = {}
    for block in blocks:
        if not isinstance(block, dict):
            continue
        for key in EXTRACT_KEYS:
            if key in block and key not in merged:
                merged[key] = block[key]
        # Also recurse one level for nested dicts (e.g. Deep Research has nested fields)
        for v in block.values():
            if isinstance(v, dict):
                for key in EXTRACT_KEYS:
                    if key in v and key not in merged:
                        merged[key] = v[key]
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        for key in EXTRACT_KEYS:
                            if key in item and key not in merged:
                                merged[key] = item[key]
    # Ensure defaults for critical fields
    merged.setdefault("topPriorities", [])
    merged.setdefault("marketMaturityScore", 30)
    merged.setdefault("decisionStyle", "Balanced")
    return merged


def _load_csv(path, row_index=None):
    """Load persona from TeachMeAI CSV. Uses last row by default."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        return _flatten_blocks([])
    row = rows[row_index] if row_index is not None and row_index < len(rows) else rows[-1]
    blocks = [_safe_json(row.get(col, "")) for col in JSON_COLUMNS]
    return _flatten_blocks(blocks)


def _load_yaml_or_json(path):
    """Load persona from YAML or JSON file directly."""
    with open(path, encoding="utf-8") as f:
        if path.endswith((".yaml", ".yml")):
            if yaml is None:
                raise ImportError("PyYAML required to load .yaml persona files")
            data = yaml.safe_load(f)
        else:
            data = json.load(f)
    if isinstance(data, dict):
        # If it already has our keys at top level, just fill defaults
        result = {}
        for key in EXTRACT_KEYS:
            if key in data:
                result[key] = data[key]
        result.setdefault("topPriorities", data.get("topPriorities", []))
        result.setdefault("marketMaturityScore", data.get("marketMaturityScore", 30))
        result.setdefault("decisionStyle", data.get("decisionStyle", "Balanced"))
        return result
    return _flatten_blocks([])


def load_persona(source_path, row_index=None):
    """
    Load persona data from a CSV, YAML, or JSON file.

    Args:
        source_path: Path to the persona source file.
        row_index:   (CSV only) Specific row to extract. Defaults to last row.

    Returns:
        dict with keys like topPriorities, marketMaturityScore, decisionStyle, etc.
    """
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Persona source not found: {source_path}")

    if source_path.endswith(".csv"):
        return _load_csv(source_path, row_index)
    elif source_path.endswith((".yaml", ".yml", ".json")):
        return _load_yaml_or_json(source_path)
    else:
        raise ValueError(f"Unsupported persona file format: {source_path}")

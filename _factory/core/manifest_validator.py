VALID_AUDIENCES = [
    "Executive / C-Suite",
    "Business Analyst",
    "Developer / Engineer",
    "Data Scientist",
    "Product Manager",
]
VALID_TONES = [
    "Strategic & Analytical",
    "Technical & Precise",
    "Practical & Applied",
    "Conversational & Accessible",
]
VALID_COMPLIANCE = ["None", "GDPR", "HIPAA", "SOX", "ISO 27001"]
VALID_REGIONS = ["Global", "EU", "US", "APAC", "Middle East"]


class ManifestValidator:
    DEFAULTS = {
        "tracks": ["base", "integrated", "architect"],
        "audience": "Developer / Engineer",
        "use_cases": [],
        "sessions": list(range(1, 9)),
        "tone": "Practical & Applied",
        "compliance_framework": "None",
        "region": "Global",
        "concurrency": 3,
        "token_budget": {
            "total_tokens": 100000,
            "tokens_per_minute": 1000,
            "defer_after_tokens": 100000
        },
        "data_schema": {
            "columns": ["id", "date", "category", "value", "notes", "status"],
            "dirty_rate": 0.15,
            "row_count": 50
        }
    }

    def __init__(self, manifest_dict):
        self.raw = manifest_dict or {}
        self.errors = []
        self.warnings = []

    def validate(self):
        # industry required
        industry = self.raw.get("industry")
        if not industry or not isinstance(industry, str) or not industry.strip():
            self.errors.append("'industry' field is required and must be a non-empty string.")

        # tracks optional but warn if missing
        tracks = self.raw.get("tracks")
        if tracks is not None:
            valid = {"base", "integrated", "architect"}
            if not isinstance(tracks, list) or not any(t in valid for t in tracks):
                self.warnings.append("'tracks' should be a list containing at least one of: base, integrated, architect.")
        else:
            self.warnings.append("'tracks' not specified, using default: base, integrated, architect.")

        # token_budget optional validation
        tb = self.raw.get("token_budget")
        if tb is not None:
            for key in ("total_tokens", "tokens_per_minute", "defer_after_tokens"):
                val = tb.get(key)
                if val is not None and (not isinstance(val, int) or val <= 0):
                    self.errors.append(f"token_budget.{key} must be a positive integer, got: {val}")
            total = tb.get("total_tokens", self.DEFAULTS["token_budget"]["total_tokens"])
            defer = tb.get("defer_after_tokens", self.DEFAULTS["token_budget"]["defer_after_tokens"])
            if isinstance(total, int) and isinstance(defer, int) and defer > total:
                self.errors.append(f"token_budget.defer_after_tokens ({defer}) must be <= total_tokens ({total}).")

        # data_schema optional validation
        ds = self.raw.get("data_schema")
        if ds is not None:
            cols = ds.get("columns")
            if cols is not None and (not isinstance(cols, list) or len(cols) == 0 or not all(isinstance(c, str) for c in cols)):
                self.errors.append("data_schema.columns must be a non-empty list of strings.")
            dr = ds.get("dirty_rate")
            if dr is not None and (not isinstance(dr, (int, float)) or not (0.0 <= dr <= 1.0)):
                self.errors.append(f"data_schema.dirty_rate must be a float between 0.0 and 1.0, got: {dr}")
            rc = ds.get("row_count")
            if rc is not None and (not isinstance(rc, int) or not (10 <= rc <= 500)):
                self.errors.append(f"data_schema.row_count must be an integer between 10 and 500, got: {rc}")

        # Plan 08 fields — warn on invalid, don't error (they have safe defaults)
        audience = self.raw.get("audience")
        if audience is not None and audience not in VALID_AUDIENCES:
            self.warnings.append(f"Invalid audience '{audience}'. Defaulting to 'Developer / Engineer'.")

        tone = self.raw.get("tone")
        if tone is not None and tone not in VALID_TONES:
            self.warnings.append(f"Invalid tone '{tone}'. Defaulting to 'Practical & Applied'.")

        compliance = self.raw.get("compliance_framework")
        if compliance is not None and compliance not in VALID_COMPLIANCE:
            self.warnings.append(f"Invalid compliance_framework '{compliance}'. Defaulting to 'None'.")

        region = self.raw.get("region")
        if region is not None and region not in VALID_REGIONS:
            self.warnings.append(f"Invalid region '{region}'. Defaulting to 'Global'.")

        sessions = self.raw.get("sessions")
        if sessions is not None and (
            not isinstance(sessions, list) or
            not all(isinstance(s, int) and 1 <= s <= 8 for s in sessions)
        ):
            self.warnings.append(f"Invalid sessions '{sessions}'. Defaulting to all 8 sessions.")

        return len(self.errors) == 0

    def get_merged(self):
        import copy
        merged = copy.deepcopy(self.DEFAULTS)
        for key, value in self.raw.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key].update(value)
            else:
                merged[key] = value
        return merged

    def report(self):
        lines = []
        for e in self.errors:
            lines.append(f"  ERROR: {e}")
        for w in self.warnings:
            lines.append(f"  WARNING: {w}")
        return "\n".join(lines)

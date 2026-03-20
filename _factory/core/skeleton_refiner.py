"""
Skeleton-of-Thought Refiner — structured output generation pattern.
Step 1: Generate section skeleton (headers + 1-line summaries)
Step 2: Expand each section with constrained token budget
Reduces output verbosity, enables parallel generation.
"""


class SkeletonRefiner:
    def __init__(self, max_sections=8, tokens_per_section=300):
        self.max_sections = max_sections
        self.tokens_per_section = tokens_per_section
        self.stats = {"calls": 0, "sections_generated": 0}

    def refine(self, content, industry, llm_caller):
        self.stats["calls"] += 1
        skeleton = self._generate_skeleton(content, industry, llm_caller)
        if not skeleton:
            return content
        expanded = self._expand_skeleton(skeleton, content, industry, llm_caller)
        return expanded if expanded else content

    def _generate_skeleton(self, content, industry, llm_caller):
        prompt = f"""Analyze this {industry} lab guide content and return a JSON array of section skeletons.
Each section: {{"heading": "...", "summary": "one line", "key_points": ["point1", "point2"]}}
Max {self.max_sections} sections. Focus on hands-on steps, not theory.

Content (first 2000 chars):
{content[:2000]}"""
        try:
            result = llm_caller(prompt)
            if isinstance(result, list):
                self.stats["sections_generated"] += len(result)
                return result
        except Exception:
            pass
        return None

    def _expand_skeleton(self, skeleton, original_content, industry, llm_caller):
        sections = []
        for s in skeleton[:self.max_sections]:
            heading = s.get("heading", "Section")
            summary = s.get("summary", "")
            key_points = s.get("key_points", [])
            points_str = "\n".join(f"- {p}" for p in key_points)
            prompt = f"""Expand this section for a {industry} bootcamp lab guide.
Heading: {heading}
Summary: {summary}
Key points:
{points_str}

Rules:
- Max {self.tokens_per_section} tokens
- 80% hands-on steps, 20% explanation
- Include code blocks or CLI commands where relevant
- Use markdown formatting

Write the expanded section content (no heading, just body):"""
            try:
                expanded = llm_caller(prompt)
                if expanded and isinstance(expanded, str):
                    sections.append(f"## {heading}\n\n{expanded}")
            except Exception:
                sections.append(f"## {heading}\n\n{summary}")
        return "\n\n---\n\n".join(sections) if sections else None

    def get_stats(self):
        return self.stats

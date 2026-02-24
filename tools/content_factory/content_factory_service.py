import os
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class DiagramOpportunity(BaseModel):
    title: str
    description: str
    nano_banana_prompt: str

class CourseSection(BaseModel):
    title: str
    integrator_content: str
    architect_content: str
    diagrams: List[DiagramOpportunity] = []

class coursewareDocument(BaseModel):
    title: str
    sections: List[CourseSection]
    summary: str

class ContentFactoryService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be provided or set as an environment variable.")
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-2.5-flash"
        self.system_instruction = """
        You are a professional courseware architect. Your goal is to transform markdown content 
        into a high-grade educational structure using the 'Cyber-Sovereign' theme.
        
        RULES:
        1. Always provide dual perspectives for each section:
           - [INTEGRATOR]: Implementation focus, API-centric, $10k thresholds, Pydantic validation.
           - [ARCHITECT]: Governance, Security, Sovereign Infrastructure, trade-offs.
        2. Identify visual 'Diagram Opportunities' suitable for an AI generator (Nano Banana).
        3. Maintain a professional, enterprise-focused tone.
        """

    def compress_context(self, content: str) -> str:
        """
        Compresses large markdown content into a high-density, context-rich summary
        to reduce token consumption in subsequent multi-agent or iterative calls.
        """
        print("[*] Compressing context for token optimization...")
        prompt = f"""
        Summarize the following markdown content into a high-density technical manifest. 
        Focus on key architectural decisions, implementation requirements, and core concepts. 
        Discard filler text but retain all specific values (thresholds, versions, IDs).
        
        CONTENT:
        {content}
        """
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0, # Deterministic summary
            )
        )
        return response.text

    @property
    def dummy_doc(self) -> coursewareDocument:
        """Returns a mock courseware document for dry-run testing."""
        return coursewareDocument(
            title="[MOCK] Courseware Session",
            summary="A high-density technical session on Sovereign AI and Multi-Agent Orchestration.",
            sections=[
                CourseSection(
                    title="Agentic Orchestration",
                    integrator_content="Implement sequential pipelines using Genkit. Ensure $10k thresholds are enforced via Pydantic shields. use `ai.generate()` with tracing.",
                    architect_content="Evaluate trade-offs between centralized orchestration and decentralized choreography. Focus on sovereign infrastructure to prevent data leakage.",
                    diagrams=[
                        DiagramOpportunity(
                            title="Orchestration Pipeline",
                            description="A logic flow showing a central agent coordinating three sub-agents.",
                            nano_banana_prompt="A sleek enterprise infographic showing a central cyan brain coordinating three purple sub-agents. Cyber-Sovereign theme."
                        )
                    ]
                )
            ]
        )

    def convert_markdown(self, markdown_content: str, compressed_context: Optional[str] = None, dry_run: bool = False) -> coursewareDocument:
        """
        Converts raw markdown into a rich courseware structure using Gemini 1.5 Flash.
        If dry_run is True, returns a mock document.
        """
        if dry_run:
            print("[INFO] Running in DRY-RUN mode. Using mock data.")
            return self.dummy_doc

        context_block = f"CONTEXT MANIFEST:\n{compressed_context}\n\n" if compressed_context else ""
        
        prompt = f"""
        {context_block}
        Transform the following markdown content into its rich courseware representation.
        Follow the system instructions for formatting and theme.

        MARKDOWN CONTENT:
        {markdown_content}
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                response_mime_type="application/json",
                response_schema=coursewareDocument.model_json_schema(),
            ),
        )

        return coursewareDocument.model_validate_json(response.text)

    def save_as_rich_markdown(self, doc: coursewareDocument, output_path: Path):
        """
        Saves the courseware document as a Slidev/MkDocs compatible rich markdown file.
        """
        lines = [f"# {doc.title}\n", f"> {doc.summary}\n\n"]
        
        for section in doc.sections:
            lines.append(f"## {section.title}\n")
            
            lines.append("### [INTEGRATOR] Track\n")
            lines.append(f"{section.integrator_content}\n")
            
            lines.append("### [ARCHITECT] Track\n")
            lines.append(f"{section.architect_content}\n")
            
            if section.diagrams:
                lines.append("### Visual Assets (To be generated by Nano Banana)\n")
                for diag in section.diagrams:
                    lines.append(f"<!-- DIAGRAM_START: {diag.title} -->\n")
                    lines.append(f"> **Prompt**: {diag.nano_banana_prompt}\n")
                    lines.append(f"<!-- DIAGRAM_END -->\n")
            
            lines.append("---\n")
            
        output_path.write_text("\n".join(lines))
        print(f"[OK] Rich courseware saved to {output_path}")

if __name__ == "__main__":
    # Example usage
    sample_md = """
    # Intro to AI Agents
    AI agents are autonomous systems that use LLMs to perform tasks.
    They can be built using Python and frameworks like LangChain or Genkit.
    """
    service = ContentFactoryService()
    doc = service.convert_markdown(sample_md)
    service.save_as_rich_markdown(doc, Path("rich_out.md"))

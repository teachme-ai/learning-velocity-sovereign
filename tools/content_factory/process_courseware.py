import os
import argparse
from pathlib import Path
from content_factory_service import ContentFactoryService
from nano_banana_service import NanoBananaService
from export_service import ExportService

def main():
    parser = argparse.ArgumentParser(description="Process Markdown into Rich Courseware with Nano Banana Diagrams.")
    parser.add_argument("input_file", help="Path to the input markdown file")
    parser.add_argument("--output-dir", "--output_dir", help="Directory to save the rich output", default="output")
    parser.add_argument("--optimize", action="store_true", help="Enable token size optimization (context compression)")
    parser.add_argument("--dry-run", action="store_true", help="Run without an API key using mock data")
    parser.add_argument("--format", choices=["docx", "pdf", "all"], default="all", help="Output format(s)")
    parser.add_argument("--api-key", help="Explicit Gemini API Key")
    args = parser.parse_args()

    # Priority: CLI Argument > Environment Variable
    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")

    input_path = Path(args.input_file)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    rich_md_output = output_dir / f"rich_{input_path.name}"
    assets_dir = output_dir / "assets" / "diagrams"
    assets_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Reading {input_path}...")
    content = input_path.read_text()

    if not args.dry_run:
        factory = ContentFactoryService(api_key=api_key)
    else:
        factory = ContentFactoryService(api_key="DRY_RUN_KEY")
    
    # 1. Token Optimization (Optional)
    compressed_ctx = None
    if args.optimize and not args.dry_run:
        compressed_ctx = factory.compress_context(content)
        print("[OK] Context compressed. Proceeding with transformation...")

    # 2. Transform Content
    print("[*] Transforming content with Gemini 1.5 Flash...")
    doc = factory.convert_markdown(content, compressed_context=compressed_ctx, dry_run=args.dry_run)
    
    # 3. Save Rich Markdown
    factory.save_as_rich_markdown(doc, rich_md_output)

    # 4. Export Service
    exporter = ExportService(output_dir)
    if args.format in ["docx", "all"]:
        exporter.to_docx(doc, f"{input_path.stem}.docx")
    if args.format in ["pdf", "all"]:
        exporter.to_pdf(doc, f"{input_path.stem}.pdf")

    # 5. Generate Diagrams
    if not args.dry_run:
        print("[*] Generating Diagrams with Nano Banana...")
        banana = NanoBananaService(api_key=api_key)
        
        for i, section in enumerate(doc.sections):
            for j, diag in enumerate(section.diagrams):
                diag_filename = f"diag_{i}_{j}.png"
                diag_path = assets_dir / diag_filename
                success = banana.generate_diagram(diag.nano_banana_prompt, diag_path)
                
                if success:
                    md_content = rich_md_output.read_text()
                    marker = f"<!-- DIAGRAM_START: {diag.title} -->"
                    replacement = f"![{diag.title}](assets/diagrams/{diag_filename})\n\n{diag.description}"
                    md_content = md_content.replace(marker, replacement)
                    rich_md_output.write_text(md_content)

    print(f"\n[DONE] Courseware processed! Open: {output_dir}")

if __name__ == "__main__":
    main()

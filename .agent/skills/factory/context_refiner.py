import os
import sys
import ollama
import re

def refine_markdown(file_path, industry_name, industry_slug):
    """Rewrite Introduction and Business Value sections of a markdown manual using industry-specific analogies."""
    print(f"✨ Refining analogies in {os.path.basename(file_path)} for {industry_name}...")
    
    with open(file_path, 'r') as f:
        content = f.read()

    # Define sections to target (Intro and Business Value usually have the analogies)
    # We'll use a prompt that asks to rewrite these specific parts if they exist.
    
    prompt = f"""
    You are a technical curriculum expert. Rewrite the 'Introduction' and 'Business Value' sections of this lab manual for the {industry_name} industry.
    
    Original Content:
    {content[:3000]} # Limit context window
    
    GUIDELINES:
    1. Replace generic analogies (e.g., finance, banks, generic business) with {industry_name} specific ones.
    2. Keep the technical steps, terminal commands, and code blocks IDENTICAL.
    3. Ensure the tone matches the industry ({industry_name}).
    4. Return the ENTIRE rewritten markdown file content.
    5. Start immediately with the markdown content. No conversational filler.
    """
    
    try:
        response = ollama.chat(model='llama3.2:1b', messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        refined_content = response['message']['content'].strip()
        
        # Basic verification to ensure we didn't just get chatter
        if "# " in refined_content or "## " in refined_content:
            with open(file_path, 'w') as f:
                f.write(refined_content)
            print(f"✅ Refined {os.path.basename(file_path)}")
        else:
            print(f"⚠️ LLM output didn't look like markdown for {file_path}, skipping write.")
            
    except Exception as e:
        print(f"❌ Failed to refine {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 context_refiner.py <file_path> <industry_name> <industry_slug>")
        sys.exit(1)
    refine_markdown(sys.argv[1], sys.argv[2], sys.argv[3])

# Skill: No-Guesswork Documentation Standard
**Description**: Ensures all courseware labs are runnable by copy-pasting code blocks with zero external research or configuration required.

## Core Rules

1. **Environment Setup Block**:
   - Provide a single, consolidated `bash` block at the start of every lab.
   - Include `python3 -m venv`, `source activate`, `pip install`, and model pulls (e.g., `ollama pull`).
   - Standardize on `pip install -r requirements.txt` where available.

2. **Step-by-Step Execution**:
   - Every technical phase MUST have a specific terminal command.
   - Example: `python3 logic/cleaner.py` instead of "Run the cleaner script".

3. **Relative Pathing**:
   - All commands must be written as if the user is in the root of the specific session directory (e.g., `01_data_pipeline_automation/`).
   - Clearly state the current working directory at the start of the execution section.

4. **Verification Commands**:
   - Every action must be followed by a verification command.
   - Examples: `ls`, `head`, `cat`, `chroma list`.
   - Provide "Expected Result" comments within the code blocks.

5. **Track Evidence**:
   - **[INTEGRATOR]**: Focus on flow, API connectivity, and successful execution logs.
   - **[ARCHITECT]**: Focus on governance, schema enforcement, and proactive failure logs (e.g., Pydantic rejection).

6. **Persona**:
   - Maintain the **Supportive Facilitator** voice: Empathetic, clear, and enterprise-focused.
7. **File Naming Convention**:
   - Lab notes MUST be named after the session directory (e.g., `01_data_pipeline_automation.md` for the session `01_data_pipeline_automation/`).
   - This ensures easy identification and prevents naming collisions across modules.

#!/usr/bin/env python3
import os
import sys
import subprocess

# Set the root to the build directory
BUILD_DIR = os.path.abspath("builds/sustainability_and_esg")
GUARDIAN_SCRIPT = os.path.abspath(".agent/skills/guardian/scripts/verify_env.py")
GENKIT_PYTHON = "/tmp/genkit_env/bin/python3"

print(f"🛡️ Validating build: {BUILD_DIR}")

# We need to run the guardian script but tell it the ROOT is BUILD_DIR.
# Since verify_env.py calculates ROOT relative to its file path (line 21),
# we might need to patch it or just run it with a modified PYTHONPATH/CWD.
# However, verify_env.py hardcodes paths relative to ROOT.

# Easiest way: copy verify_env.py into the build folder temporarily and run it.
dest_guardian = os.path.join(BUILD_DIR, "verify_env.py")
with open(GUARDIAN_SCRIPT, 'r') as f:
    content = f.read()

# Patch the ROOT calculation in the copied script to be os.getcwd()
content = content.replace(
    'ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))',
    'ROOT = os.getcwd()'
)

with open(dest_guardian, 'w') as f:
    f.write(content)

os.chmod(dest_guardian, 0o755)

try:
    # Run only Set A (Finance) in the build since we haven't refactored the test paths yet
    # but the files exist there.
    subprocess.run([GENKIT_PYTHON, dest_guardian], cwd=BUILD_DIR, check=True)
finally:
    if os.path.exists(dest_guardian):
        os.remove(dest_guardian)

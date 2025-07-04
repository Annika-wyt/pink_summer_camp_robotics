import os
import subprocess
import sys
import shutil

VENV_NAME = "pinkenv"

# Choose best python command for creating venv
python_cmd = shutil.which("python3") or shutil.which("python")
if not python_cmd:
    print("Python is not installed.")
    sys.exit(1)

print(f"Using: {python_cmd}")
print(f"Creating virtual environment: {VENV_NAME}")
subprocess.check_call([python_cmd, "-m", "venv", VENV_NAME])

# Determine correct pip inside venv
if os.name == "nt":
    pip_executable = os.path.join(VENV_NAME, "Scripts", "pip.exe")
else:
    pip_executable = os.path.join(VENV_NAME, "bin", "pip")

print("Installing requirements...")
subprocess.check_call([pip_executable, "install", "-r", "requirements.txt"])

print("\n✅ Done!")
if os.name == "nt":
    print(f"To activate type in the terminal: {VENV_NAME}\\Scripts\\activate.ps1")
else:
    print(f"To activate type in the terminal: source {VENV_NAME}/bin/activate")

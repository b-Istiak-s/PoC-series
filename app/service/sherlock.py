import subprocess
import os
import sys

def run_sherlock(username):
    sherlock_path = os.path.join(os.getcwd(), 'app', 'service', 'sherlock_repo', 'sherlock_project')

    # Use the current Python interpreter
    python_executable = sys.executable

    command = [python_executable, sherlock_path, username]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}"

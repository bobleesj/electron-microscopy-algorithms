#!/usr/bin/env python3
"""
Run all Jupyter notebooks and verify no errors occur.

This script:
1. Clears all outputs from each notebook
2. Executes all cells
3. Checks for any execution errors
4. Saves the notebook with fresh outputs

Usage:
    python check_notebooks.py           # Run all notebooks
    python check_notebooks.py nb.ipynb  # Run specific notebook
    python check_notebooks.py --check   # Check saved outputs only (no execution)
"""

import json
import subprocess
import sys
from pathlib import Path


def run_notebook(path: Path) -> tuple[bool, str]:
    """
    Execute a notebook and return (success, error_message).
    
    Uses nbconvert to execute the notebook in place.
    """
    try:
        result = subprocess.run(
            [
                sys.executable, '-m', 'jupyter', 'nbconvert',
                '--to', 'notebook',
                '--execute',
                '--inplace',
                '--ExecutePreprocessor.timeout=300',
                str(path)
            ],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            # Extract error message
            error_msg = result.stderr.strip()
            # Try to find the actual error
            if 'CellExecutionError' in error_msg:
                lines = error_msg.split('\n')
                for i, line in enumerate(lines):
                    if 'Error' in line or 'Exception' in line:
                        error_msg = '\n'.join(lines[i:i+3])
                        break
            return False, error_msg[:200] if len(error_msg) > 200 else error_msg
        return True, ''
    except FileNotFoundError:
        return False, 'jupyter not found. Install with: pip install jupyter nbconvert'


def check_saved_outputs(path: Path) -> list[dict]:
    """Check notebook's saved outputs for errors (no execution)."""
    errors = []
    with open(path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    for i, cell in enumerate(notebook.get('cells', []), start=1):
        if cell.get('cell_type') != 'code':
            continue
        for output in cell.get('outputs', []):
            if output.get('output_type') == 'error':
                ename = output.get('ename', 'Unknown')
                evalue = output.get('evalue', '')[:100]
                errors.append({'cell': i, 'ename': ename, 'evalue': evalue})
    return errors


def main():
    check_only = '--check' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    
    if args:
        notebooks = [Path(arg) for arg in args]
    else:
        repo_root = Path(__file__).parent
        notebooks = list(repo_root.glob('**/*.ipynb'))
        notebooks = [nb for nb in notebooks if '.ipynb_checkpoints' not in str(nb)]
    
    if not notebooks:
        print("No notebooks found.")
        return 0
    
    mode = "Checking saved outputs" if check_only else "Running"
    print(f"{mode} {len(notebooks)} notebook(s)...\n")
    
    all_passed = True
    
    for nb_path in sorted(notebooks):
        if check_only:
            errors = check_saved_outputs(nb_path)
            if errors:
                all_passed = False
                print(f"❌ {nb_path.name}: {len(errors)} error(s)")
                for err in errors:
                    print(f"   Cell {err['cell']}: {err['ename']}: {err['evalue']}")
            else:
                print(f"✓ {nb_path.name}: OK")
        else:
            print(f"  Running {nb_path.name}...", end=' ', flush=True)
            success, error = run_notebook(nb_path)
            if success:
                print("✓")
            else:
                all_passed = False
                print("❌")
                print(f"    Error: {error}")
    
    print()
    if all_passed:
        print("All notebooks passed! ✓")
        return 0
    else:
        print("Some notebooks have errors.")
        return 1


if __name__ == '__main__':
    sys.exit(main())


if __name__ == '__main__':
    sys.exit(main())

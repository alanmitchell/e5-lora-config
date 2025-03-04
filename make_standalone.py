#!/usr/bin/env python3
"""Makes a standalone executable of the configure.py program, and copies it,
appropriately named for the OS, to the standalone_exec directory.
"""
import subprocess
import sys
import shutil
from pathlib import Path

subprocess.run("uv run pyinstaller -F configure.py", shell=True)

exec_name = {
    'win': 'configure-win',
    'dar': 'configure-mac',
    'lin': 'configure-linux'
}[sys.platform[:3]]

src = Path("dist") / "configure"
dest = Path("standalone-exec") / exec_name

shutil.copy(src, dest)

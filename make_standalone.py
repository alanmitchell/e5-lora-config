#!/usr/bin/env python3
"""Makes a standalone executable of the configure.py program, and copies it,
appropriately named for the OS, to the standalone_exec directory.
"""
import subprocess
import sys
import shutil
from pathlib import Path

subprocess.run("uv run pyinstaller -F configure.py", shell=True)

src_name, dest_name = {
    'win': ('configure.exe', 'configure-win'),
    'dar': ('configure', 'configure-mac'),
    'lin': ('configure', 'configure-linux')
}[sys.platform[:3]]

src = Path("dist") / src_name
dest = Path("standalone-exec") / dest_name

shutil.copy(src, dest)

# e5-lora-config
Utility to configure Seeed Studio Grove Wio E5 LoRaWAN module. Configures it to 
work with the US Things Network. Uses a fixed Data Rate (not ADR), selectable
by the User.

This project uses the `uv` utility to manage the project, including dependencies
and the virtual environment.

The `make_standalone.py` script (run with `uv run make_standalone.py`) will create
a single-file standalone executable for the OS where the script is run.

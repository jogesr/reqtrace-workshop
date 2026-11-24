"""Ermöglicht den Aufruf mit `python -m reqtrace ...`."""

import sys

from reqtrace.cli import main

if __name__ == "__main__":
    sys.exit(main())

#!/bin/bash
set -e

# Use sphinx-build directly if 'make' is not available
if ! command -v make &> /dev/null; then
    echo "Make not found, running Sphinx directly..."
    sphinx-build -b html source _build/html || { echo "Sphinx failed"; exit 1; }
else
    make html || { echo "Make failed"; exit 1; }
fi

# Start the local server
python -m http.server --directory ./_build/html/

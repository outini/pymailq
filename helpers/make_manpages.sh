#! /bin/bash

# You may validate your documentation with:
#   (cd docs && make html && xdg-open _build/html/index.html)

DOCS_DIR="docs"
MAN_DIR="man"

(cd "$DOCS_DIR" && make man)
cp "$DOCS_DIR/_build/man/"* "$MAN_DIR/"

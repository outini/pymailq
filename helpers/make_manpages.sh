#! /bin/bash

DOCS_DIR="docs"
MAN_DIR="man"

(cd "$DOCS_DIR" && make man)
cp "$DOCS_DIR/_build/man/"* "$MAN_DIR/"

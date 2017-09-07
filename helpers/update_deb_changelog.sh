#! /bin/bash

PACKAGING_DIR="packaging"

VERSION=$(cat "VERSION" 2>/dev/null)
CHANGES="CHANGES"
DEB_DISTRO="unstable"

get_changes() {
    sed -n '
        /=== v'$1' /{
            :getchange
            s/.*//;n
            /^\s*$/q
            s/^\s*[*-]\s\+\(.*\)/\1/p
            bgetchange
        }
    ' "$2"
}

[ -z "$VERSION" ] && { echo "Unable to get current version."; exit 2; }
[ -f "$CHANGES" ] || { echo "File $CHANGES not found."; exit 2; }
[ -d "$PACKAGING_DIR" ] || { echo "Packaging directory not found."; exit 2; }
cd "$PACKAGING_DIR"

read -p "Updating changelog with CHANGES content.
Don't forget to export DEB variables:
  DEBEMAIL='${DEBEMAIL}'
  DEBFULLNAME='${DEBFULLNAME}'
proceed ? (^C to abort)"

debchange -D "$DEB_DISTRO" -u low -i "Update to upstream version v$VERSION"
get_changes "$VERSION" "../$CHANGES" | while read changeline; do
    echo "Adding change: $changeline"
    debchange -a "$changeline"
done
debchange -r

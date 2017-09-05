#! /bin/bash

VERSION=$(cat ../VERSION)
CHANGES=../CHANGES
DEB_DISTRO="UNRELEASED"

get_changes() {
    sed -n '
        /=== v'${VERSION}' /{
            :getchange
            s/.*//;n
            /^\s*$/q
            s/^\s*[*-]\s\+\(.*\)/\1/p
            bgetchange
        }
    ' "$CHANGES"
}

read -p "Updating changelog with CHANGES content.
Don't forget to export DEB variables:
  DEBEMAIL='${DEBEMAIL}'
  DEBFULLNAME='${DEBFULLNAME}'
proceed ? (^C to abort)"

get_changes | while read changeline; do
    debchange -a "$changeline"
done

debchange --distribution "$DEB_DISTRO" -r

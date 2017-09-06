#! /bin/bash


LIB_FILE="pymailq/__init__.py"
SETUP_FILE="setup.py"
CHANGES_FILE="CHANGES"


update_lib_version() {
    echo "Updating libraries: $LIB_FILE"
    sed -i "s/^VERSION\s*=\s*.*/VERSION = \"$1\"/" $LIB_FILE
}

update_setup_version() {
    echo "Updating setup: $SETUP_FILE"
    sed -i "s/release\s*=\s*\".*\"/release = \"$1\"/" $SETUP_FILE
}

create_changes_entry() {
    echo "Creating v$1 entry in: $CHANGES_FILE"
    grep -q "=== v$1 " $CHANGES_FILE && {
        echo "Changes have already an entry for version $1"
        return
    }
    today=$(date "+%d/%m/%Y")
    sed -i '
        0,/^=== v/{
            /^=== v/i=== v'$1' '$today' ===\n    * Document your changes\n
        }
    ' $CHANGES_FILE
    echo "Don't forget to fill new entry with changes."
}


# --- Main ---
[ $# -eq 0 ] && { echo "Usage: $0 -v <version>"; exit 1; }
while getopts :v: opt; do
    case "$opt" in
        v) version=$OPTARG ;;
        \?) echo "Unknown option $OPTARG"; exit 2 ;;
        :) echo "Option -$OPTARG requires an argument."; exit 2 ;;
    esac
done

echo "Updating to version $version"
update_lib_version $version
update_setup_version $version
create_changes_entry $version

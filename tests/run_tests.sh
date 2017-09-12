#! /bin/sh

usage() {
    cat <<EOU
Usage: $0 [-hs] [-e ENV]

Options:
    -h      show usage
    -s      generate mail samples
    -e ENV  use ENV as virtualenv (via pew) to run tests
EOU
    exit 1
}

# --- Main ---

gen_samples=false
venv=

while getopts :hse: opt; do
    case "$opt" in
        h) usage ;;
        s) gen_samples=true ;;
        e) venv=$OPTARG ;;
        \?) echo "Unknown option $OPTARG"; exit 2 ;;
        :) echo "Option -$OPTARG requires an argument."; exit 2 ;;
    esac
done

# We're supposed to run in project's root
[ -d tests ] || {
    echo "Run me from project's root, tests directory not found."
    exit 2
}

$gen_sample && {
    echo "Generating samples."
    sudo ./tests/generate_samples.sh
}


if [ pew_env ]; then
    PYTHONPATH=. pew in "$venv" pytest -v ./tests/
else
    PYTHONPATH=. pytest -v ./tests/
fi

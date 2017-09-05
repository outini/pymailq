#!/usr/bin/env bash

requirements="
debhelper
devscripts
build-essential
python-support
python-all
python3-all
"

change_file="pymailq_*.changes"
packages="python-pymailq python3-pymailq"

# Checking requirements
dpkg_output=$(dpkg -l $requirements)
grep -q '^un' <<< "$dpkg_output" && {
    read -p "Missing packages, May I install those? (yes|no) " answer
    [ "$answer" == "yes" ] || {
        echo "Build of debian package aborted."
        exit 1
    }
    sudo apt-get install -qq $requirements
}

# Preparing build directory
[ -d build ] && { echo "Cleaning build directory."; rm -r build; }
echo "Preparing build directory."
mkdir build && cp -a debian build/ &&
[ -d build ] || { echo "Fail to prepare build directory."; exit 2; }

# Building binary package
(cd build && dpkg-buildpackage -us -uc -b) || {
    echo "Failed to build package."
    exit 2
}

# Verify your build
echo "Running lintian and inspecting package content."
lintian -IviE --display-experimental --pedantic -L ">=wishlist" \
        --color auto --show-overrides --checksums $change_file

echo "Showing packages infos and content."
for pkg in $packages; do
    dpkg-deb -I ${pkg}_*.deb
    dpkg-deb -c ${pkg}_*.deb
done

#! /bin/sh

# Call me like:
# PYTHONPATH=. PATH="$PATH:./bin" tests/run_tests.sh

echo "Running python version:"
python --version

echo "# Begin tests suite"
pqshell < tests/commands.txt
echo "# End tests suite"
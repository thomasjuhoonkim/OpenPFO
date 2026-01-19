#!/bin/sh

# Check if python is installed and is version 3.11
PYTHON_VERSION=$(python3 -c "import sys; print(str(sys.version_info.major) + '.' + str(sys.version_info.minor))")
if [ "$PYTHON_VERSION" = "3.11" ]; then
    echo "You are using Python 3.11."
else
    echo "Python version $PYTHON_VERSION detected. OpenPFO requires Python 3.11."
fi

# create virtual environment
echo "Creating virtual environment"
python3 -m venv .venv

# activate virtual environment
echo "Activating virtual environment"
source .venv/bin/activate

# install python dependencies
echo "Installing Python dependencies"
pip install -r requirements-local.txt

# install OpenPFO in editable mode
echo "Installing OpenPFO in editable mode"
pip install -e .

echo 'OpenPFO is initialized!'
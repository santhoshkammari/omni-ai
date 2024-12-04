#!/bin/bash

set -e

# Git operations
# Check if dist directory exists before deleting
if [ -d "dist" ]; then
    echo "Removing existing dist directory..."
    rm -r dist
fi

echo "Uninstalling existing package..."
pip uninstall -y aichatlite

echo "Building package..."
python -m build

echo "Installing wheel file..."
pip install dist/*.whl

echo "Uploading to PyPI..."
#twine upload dist/*

echo "Deployment completed successfully!"
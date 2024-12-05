
echo "Installing wheel file..."
pip install dist/*.whl

echo "Uploading to PyPI..."
twine upload dist/*

echo "Deployment completed successfully!"
# Shell script to publish the project to pypi
# Usage: ./scripts/publish.sh

# Set the API token
poetry config pypi-token.pypi $PYPI_API_TOKEN

# Build and publish the project
poetry publish --build
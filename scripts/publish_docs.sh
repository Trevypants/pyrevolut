# Shell script to publish the docs to github pages
# Usage: ./scripts/publish_docs.sh

# Build and publish the docs
poetry run mkdocs gh-deploy --force
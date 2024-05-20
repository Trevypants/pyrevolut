### Commands to setup all necessary dependencies for running (and developing) the application ###
setup-deps:
	@echo "################################"
	@echo "## Setting up Dependencies... ##"
	@echo "################################"
	@/bin/bash -c "scripts/setup_deps.sh"

setup-dev:
	@echo "#############################"
	@echo "## Setting up Local Env... ##"
	@echo "#############################"
	@/bin/bash -c "scripts/setup_dev.sh"

	@echo "###############################"
	@echo "## Local Env setup complete! ##"
	@echo "###############################"

setup:
	$(MAKE) setup-deps
	$(MAKE) setup-dev

### Commands to format the code ###
format:
	@echo "Formatting code..."
	@poetry run ruff format pyrevolut tests
	@poetry run black pyrevolut tests
	@echo "Code formatted!"

### Commands to run the tests ###
# base64 encode the credentials: base64 -i tests/test_creds.json
test-gen-creds:
	@poetry run pyrevolut auth-manual --credentials-json tests/credentials/test_creds.json

test-lint:
	@echo "Running lint tests..."
	@poetry run python -m black pyrevolut tests
	@poetry run python -m ruff check pyrevolut/ tests/ --fix
	@echo "Lint tests complete!"

test-integration:
	@echo "Running integration tests..."
	@poetry run python -m pytest -n 1 --dist=loadfile --cov-report term-missing --cov-report=xml:coverage.xml --cov=pyrevolut tests
	@echo "Integration tests complete!"

test:
	@echo "Running tests..."
	$(MAKE) test-lint
	$(MAKE) test-integration
	@echo "Tests complete!"

### Commands to git commit ###
stage:
	@echo "Staging changes..."
	@git add .
	@echo "Changes staged!"

commit:
	@echo "Committing changes..."
	@poetry run cz commit
	@echo "Changes committed!"

push: 
	@echo "Pushing changes..."
	@git push
	@echo "Changes pushed!"

### Commands to publish the package ###
publish:
	@echo "Publishing package..."
	@/bin/bash -c "scripts/publish.sh"
	@echo "Package published!"
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

### Commands to run the tests ###
test-lint:
	@echo "Running lint tests..."
	@poetry run ruff check
	@echo "Lint tests complete!"

test-type:
	@echo "Running type tests..."
	@poetry run pyright --warnings --stats
	@echo "Type tests complete!"

test-integration:
	@echo "Running integration tests..."
	@poetry run pytest -n 1
	@echo "Integration tests complete!"

test:
	@echo "Running tests..."
	$(MAKE) test-lint
	# $(MAKE) test-type
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
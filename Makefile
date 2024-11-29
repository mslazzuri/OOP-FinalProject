
PLANTUML = java -jar ~/plantuml.jar
DOCS = docs
UML_DIR = uml
COVERAGE = python -m pytest

.PHONY: all
all: check-style check-type test create-docs clean

.PHONY: check-style
check-style:
	@echo "Checking style with flake8..."
	flake8 calculator.py
	@echo "check-style passed!"

.PHONY: check-type
check-type:
	@echo "Checking types with mypy..."
	mypy --disallow-untyped-defs --strict calculator.py
	@echo "check-type passed!"

.PHONY: test
test:
	@echo "running unittests..."
	@pytest test_calculator.py --verbose
	@echo "all unittests passed!"

.PHONY: create-docs
create-docs:
	@echo "Generating documentation with pdoc..."
	pdoc --output-dir docs calculator.py
	@echo "html docs created and saved in $(DOCS)"

.PHONY: create-uml
create-uml:
	@echo "Checking for Java installation..."
	@if [ -z "$(shell which java)" ]; then \
		echo "Error: Java not found. Install Java to run plantuml."; \
		exit 1; \
	fi
	@echo "Generating UML diagrams..."
	$(PLANTUML) $(UML_DIR)/classes.plantuml
	@echo "UML diagrams created and saved in uml folder"

.PHONY: clean
clean:
	@echo "Cleaning up temporary files..."
ifeq ($(OS),Windows_NT)
	@for /d %%i in (__pycache__) do rmdir /s /q "%%i"
	@for /d %%i in (.pytest_cache) do rmdir /s /q "%%i"
	@for /d %%i in (.mypy_cache) do rmdir /s /q "%%i"
	@for /d %%i in (.hypothesis) do rmdir /s /q "%%i"
	@if exist .coverage del /q .coverage
else
	rm -rf $(shell find . -type d -name __pycache__)
	rm -rf $(shell find . -type d -name .pytest_cache)
	rm -rf $(shell find . -type d -name .mypy_cache)
	rm -rf $(shell find . -type d -name .hypothesis)
	rm -f .coverage
endif
	@echo "Cleanup complete!"
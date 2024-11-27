PLANTUML = java -jar ~/plantuml.jar
DOCS = docs
UML_DIR = uml
COVERAGE = python -m pytest

.PHONY: all
all: check-style check-type fix-style test clean

# use . to do all files ex: flake8 .
.PHONY: check-style
check-style:
	@echo "Checking style with flake8"
	@flake8 design.py
	@echo "check-style passed!"

.PHONY: check-type
check-type:
	@echo "Checking types with mypy"
	@mypy --disallow-untyped-defs --strict design.py
	@echo "check-type passed!"

test:
# unittest methods
	@echo "running unittests ..."
	@pytest tests/test_######.py
	@echo "all unittests passed!"

.PHONY: create-doc-folder
create-doc-folder:
	@mkdir -p $(DOCS) # creates all folder(s) if not exists

.PHONY: create-docs
create-docs: create-doc-folder
	pdoc -o ./docs #########.py # creates .md docs inside docs
	@echo "html docs created and saved in $(DOCS)"

.PHONY: create-uml
create-uml:
# use shell command which to check if java is installed and is in the $PATH
ifeq ($(shell which java), )
	$(error "No java found in $(PATH). Install java to run plantuml")
endif
# use wildcard function to check if file exists
ifeq ($(wildcard ~/plantuml.jar), )
	@echo "Downloading plantuml.jar in home folder..."
	curl -L -o ~/plantuml.jar https://sourceforge.net/projects/plantuml/files/plantuml.jar/download
endif
	$(PLANTUML) $(UML_DIR)/classes.plantuml
	@echo "UML diagrams created and saved in uml folder"

.PHONY: fix-style
fix-style:
	@autopep8 --in-place --recursive --aggressive --aggressive .

.PHONY: run-test-coverage
run-test-coverage:
	@pytest --cov --cov-report=html:./htmlcov
	@coverage run -m unittest discover -s tests ########
	@pytest --cov=######## --cov-report=term-missing

.PHONY: clean
clean:
	# remove all caches recursively
	@rm -rf `find . -type d -name __pycache__` # remove all pycache
	@rm -rf `find . -type d -name .pytest_cache` # remove all pytest cache
	@rm -rf `find . -type d -name .mypy_cache` # remove all mypy cache
	@rm -rf `find . -type d -name .hypothesis` # remove all hypothesis cache
	@rm -rf `find . -name .coverage` # remove all coverage cache 
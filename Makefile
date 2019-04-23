APPLICATION_MODULE=simulator
TEST_MODULE=tests

# @see http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.DEFAULT_GOAL := help
.PHONY: help
help: ## provides cli help for this makefile (default)
	@grep -E '^[a-zA-Z_0-9-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: dist
dist:
	. venv/bin/activate; python setup.py sdist

.PHONY: tests
tests: ## run automatic tests
	. venv/bin/activate; python -m pytest tests/units
	. venv/bin/activate; python -m pytest tests/integrations
	. venv/bin/activate; python -m pytest tests/acceptances


.PHONY: tox
tox: ## run tests described in tox.ini for multi-python environments
	tox

.PHONY: lint
lint: ## run pylint
	. venv/bin/activate; pylint --rcfile=.rcfile $(APPLICATION_MODULE)

.PHONY: clean
clean :
	rm -rf build
	rm -rf dist
	rm -rf venv
	rm -rf .tox
	rm -f .coverage
	rm -rf *.egg-info
	rm -f MANIFEST
	find -name __pycache__ -print0 | xargs -0 rm -rf

.PHONY: freeze_requirements
freeze_requirements: ## update the project dependencies based on setup.py declaration
	rm -rf venv
	$(MAKE) venv
	. venv/bin/activate; pip install --editable .
	. venv/bin/activate; pip freeze --exclude-editable > requirements.txt

.PHONY: install_requirements_dev
install_requirements_dev: venv ## install pip requirements for development
	. venv/bin/activate; pip install -r requirements.txt
	. venv/bin/activate; pip install -e .[dev]

.PHONY: install_requirements
install_requirements: ## install pip requirements based on requirements.txt
	. venv/bin/activate; pip install -r requirements.txt
	. venv/bin/activate; pip install -e .

.PHONY: venv
venv: ## build a virtual env for python 3 in ./venv
	virtualenv venv -p python3
	@echo "\"source venv/bin/activate\" to activate the virtual env"

.PHONY: upload
upload:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	. venv/bin/activate; python setup.py sdist bdist_wheel
	. venv/bin/activate; twine upload dist/*

CODE = .
PACKAGES = conf crud database services utils
# Allow setting run level from cli
RUN_LEVEL = dev
L = RUN_LEVEL=$(RUN_LEVEL)
# Add source dir to pythonpath
PYTHONPATH = PYTHONPATH=./:$(CODE)
# Executables
ALEMBIC = $(L) $(PYTHONPATH) alembic -c $(CODE)/alembic.ini
PYTEST = $(PYTHONPATH) pytest
TEST =  $(PYTEST) --verbosity=2 --showlocals --strict
# Params
DOWNGRADE_DEFAULT = -1

.PHONY: migrations db_upgrade db_downgrade lint format test test-failed test-cov validate

# Actions

migrations:
	$(ALEMBIC) revision --autogenerate -m "$(message)"

db_upgrade:
	$(ALEMBIC) upgrade head

db_downgrade:
	$(ALEMBIC) downgrade $(DOWNGRADE_DEFAULT)

test:
	$(TEST) --cov --cov-fail-under=95

test-failed:
	$(TEST) --last-failed

test-cov:
	$(TEST) --cov --cov-report html

lint:
	pylint --jobs 4 --rcfile=setup.cfg $(PACKAGES)
	black --line-length=100 --skip-string-normalization --check $(CODE)
	mypy $(PACKAGES)

format:
	isort --apply --recursive $(CODE)
	black --line-length=100 --skip-string-normalization $(CODE)
	unify --in-place --recursive $(CODE)

validate: lint test

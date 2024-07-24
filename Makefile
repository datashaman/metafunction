CMD ?= --help

serve:
	hatch run serve

check: lint types cov

test:
	hatch test

lint:
	hatch run lint:style

fix:
	hatch run lint:fix

cov:
	hatch run cov
	open htmlcov/index.html

cli:
	hatch run metafunction $(CMD)

types:
	hatch run lint:types

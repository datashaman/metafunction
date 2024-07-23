CMD ?= --help

serve:
	hatch run serve

test:
	hatch test

cov:
	hatch run cov
	open htmlcov/index.html

cli:
	hatch run metafunction $(CMD)

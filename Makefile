CMD ?= --help

serve:
	hatch run serve

test:
	hatch test

cli:
	hatch run python -m metafunction.cli $(CMD)

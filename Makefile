serve:
	hatch run uvicorn metafunction:app --reload

tox:
	hatch run tox run

venv:
	rm -rf .venv
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

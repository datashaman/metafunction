serve:
	hatch run uvicorn metafunction.app:app --reload

test:
	hatch test

venv:
	rm -rf .venv
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

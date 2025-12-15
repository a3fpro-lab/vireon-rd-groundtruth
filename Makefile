.PHONY: help install lint test smoke bench evidence clean

help:
	@echo "Targets:"
	@echo "  install   - install deps + editable"
	@echo "  lint      - ruff format + ruff check"
	@echo "  test      - pytest"
	@echo "  smoke     - CLI smoke"
	@echo "  bench     - run suites into results/"
	@echo "  evidence  - bench + generate results/EVIDENCE_PACK.md"
	@echo "  clean     - remove results/"

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
	python -m pip install -e .

lint:
	ruff format .
	ruff check .

test:
	pytest -q

smoke:
	vireon-rd smoke

bench:
	python scripts/run_bench.py --out results --seeds "1,2,3,4,5"

evidence: bench
	python scripts/evidence_pack.py --root results --sqk sqk_suite --gs gs_suite --out results/EVIDENCE_PACK.md
	@echo "OK: results/EVIDENCE_PACK.md"

clean:
	rm -rf results

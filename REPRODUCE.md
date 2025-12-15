Step 52 — Step by step (zero ambiguity)
	1.	Open your repo on GitHub (in Safari on your iPhone).
	2.	Go to the repo root (the main page where you see files like README.md, CONTRACT.md, maybe requirements.txt).
	3.	Tap Add file → Create new file.
	4.	In the “Name your file…” box, type exactly:

REPRODUCE.md

	5.	Tap into the big editor box (where you paste text).
	6.	Copy everything in the box below and paste it into the editor:

# Reproduce (VIREON-RD GroundTruth)

1) Install:
```bash
python -m pip install -r requirements.txt
python -m pip install -e .

	2.	Run suites:

vireon-rd suite --spec sqk --seeds 1,2,3,4,5 --out results/sqk_suite
vireon-rd suite --spec gs  --seeds 1,2,3,4,5 --out results/gs_suite

	3.	Generate proof bundle:

python scripts/evidence_pack.py --root results --sqk sqk_suite --gs gs_suite --out results/EVIDENCE_PACK.md

	4.	Open:

	•	results/EVIDENCE_PACK.md
	•	results/*/suite.json
	•	any results/*/seed_*/report.md



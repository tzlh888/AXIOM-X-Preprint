# Reproducibility

Python 3.11+ and the standard library suffice for the included statistics script. No network or credentials are required. The aggregate packet reproduces published arithmetic and sensitivity summaries, not private experiments. The dynamic model alias prevents guaranteed longitudinal response reproduction.

Run `python3 code/rc_stats.py --clusters data/cluster_summary.csv` from the repository root. Verify packet bytes with `shasum -a 256 -c manifest_sha256.txt`. The manifest excludes itself and its receipt to avoid self-reference.

import subprocess
import sys
from pathlib import Path


# ------------------------------------------------
# Project root
# ------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]


# ------------------------------------------------
# Run pipeline step
# ------------------------------------------------

def run_step(script):

    script_path = (
        BASE_DIR / script
    )

    print("\n" + "=" * 70)

    print(
        f"RUNNING: {script}"
    )

    print("=" * 70)

    result = subprocess.run(
        [
            sys.executable,
            str(script_path)
        ],
        cwd=BASE_DIR
    )

    if result.returncode != 0:

        print(
            f"\nERROR: {script} failed."
        )

        sys.exit(
            result.returncode
        )


# =================================================
# 1. FETCH API DATA
# =================================================

run_step(
    "src/api/fetch_trending.py"
)


# =================================================
# 2. STORE HISTORICAL SNAPSHOT
# =================================================

run_step(
    "src/pipeline/store_history.py"
)


# =================================================
# 3. CALCULATE VELOCITY
# =================================================

run_step(
    "src/pipeline/calculate_velocity.py"
)


# =================================================
# 4. CALCULATE TREND SCORE
# =================================================

run_step(
    "src/pipeline/calculate_trend_score.py"
)


# =================================================
# COMPLETE
# =================================================

print("\n" + "=" * 70)

print(
    "TRENDPULSE PIPELINE COMPLETED SUCCESSFULLY"
)

print("=" * 70)
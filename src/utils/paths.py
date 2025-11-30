from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_GENERATORS = ROOT / "data" / "synthetic_generators"
CONFIG_DIR = ROOT / "config"
NOTEBOOKS_DIR = ROOT / "notebooks"


def ensure_dirs():
    for p in [DATA_RAW, DATA_PROCESSED]:
        p.mkdir(parents=True, exist_ok=True)

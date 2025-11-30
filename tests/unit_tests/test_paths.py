from src.utils.paths import ensure_dirs, DATA_RAW, DATA_PROCESSED

def test_ensure_dirs():
    ensure_dirs()
    assert DATA_RAW.exists()
    assert DATA_PROCESSED.exists()

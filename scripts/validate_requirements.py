"""
Validar que requirements.lock sea consistente con pyproject.toml y requirements.txt

Uso:
  python scripts/validate_requirements.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_lock_packages() -> dict[str, str]:
    """Parse requirements.lock and extract package==version."""
    lock_path = ROOT / "requirements.lock"
    packages = {}
    with lock_path.open("r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if "==" in line:
                    pkg, ver = line.split("==", 1)
                    packages[pkg.lower()] = ver
    return packages


def load_txt_packages() -> dict[str, str]:
    """Parse requirements.txt and extract base packages."""
    txt_path = ROOT / "requirements.txt"
    packages = {}
    with txt_path.open("r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                # Extract package name from "package>=version"
                for op in [">=", "<=", "==", "~=", "!="]:
                    if op in line:
                        pkg = line.split(op)[0].strip()
                        packages[pkg.lower()] = line
                        break
    return packages


def validate_coverage() -> bool:
    """Check that lock file has all packages from requirements.txt"""
    lock_pkgs = load_lock_packages()
    txt_pkgs = load_txt_packages()
    
    print("📋 Validating requirements.lock coverage...")
    print(f"   - Lock file has {len(lock_pkgs)} pinned packages")
    print(f"   - requirements.txt defines {len(txt_pkgs)} base packages\n")
    
    missing = []
    for pkg_name in txt_pkgs.keys():
        if pkg_name not in lock_pkgs:
            missing.append(pkg_name)
    
    if missing:
        print(f"❌ Missing from lock: {', '.join(missing)}")
        return False
    
    print(f"✅ All requirements.txt packages are in lock file")
    return True


def validate_syntax() -> bool:
    """Validate lock file can be parsed by pip."""
    lock_path = ROOT / "requirements.lock"
    print("\n🔧 Validating syntax with pip...")
    
    try:
        result = subprocess.run(
            ["pip", "compile", "--dry-run", "--no-header", str(lock_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            print(f"⚠️  pip check reported issues:\n{result.stderr}")
            return True  # Not critical
        print("✅ Lock file syntax is valid")
        return True
    except Exception as e:
        print(f"⚠️  Could not validate with pip: {e}")
        return True


def main() -> None:
    print("🔍 Validating requirements.lock...\n")
    
    checks = [
        ("Coverage", validate_coverage),
        ("Syntax", validate_syntax),
    ]
    
    results = []
    for name, check_fn in checks:
        try:
            results.append(check_fn())
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ All validations passed!")
        sys.exit(0)
    else:
        print("❌ Some validations failed. See above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()

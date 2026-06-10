"""Check and optionally launch local Ansys Fluent 2026 through PyFluent."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ANSYS_ROOT = Path(r"D:\ANSYS2026\ANSYS Inc\v261")
FLUENT_EXE = ANSYS_ROOT / r"fluent\ntbin\win64\fluent.exe"
LMUTIL_EXE = ANSYS_ROOT / r"licensingclient\winx64\lmutil.exe"
LICENSE = "1055@localhost"


def check_path(label: str, path: Path) -> bool:
    exists = path.exists()
    print(f"{label}: {'OK' if exists else 'MISSING'} - {path}")
    return exists


def run_lmstat() -> int:
    if not LMUTIL_EXE.exists():
        print(f"lmutil missing: {LMUTIL_EXE}")
        return 2
    proc = subprocess.run(
        [str(LMUTIL_EXE), "lmstat", "-a", "-c", LICENSE],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = proc.stdout
    print(output)
    for feature in ("cfd_base", "cfd_solve_level1", "cfd_solve_level2", "acfd_fluent"):
        if feature in output:
            print(f"license feature visible: {feature}")
    return proc.returncode


def import_pyfluent() -> bool:
    try:
        import ansys.fluent.core as pyfluent
    except Exception as exc:  # noqa: BLE001
        print(f"PyFluent import: FAILED - {exc}")
        return False
    print(f"PyFluent import: OK - {pyfluent.__version__}")
    return True


def launch_smoke() -> int:
    import ansys.fluent.core as pyfluent

    os.environ["AWP_ROOT261"] = str(ANSYS_ROOT)
    os.environ["ANSYSLMD_LICENSE_FILE"] = LICENSE

    session = pyfluent.launch_fluent(
        product_version="26.1",
        mode="solver",
        precision="double",
        processor_count=1,
        ui_mode="gui",
        fluent_path=str(FLUENT_EXE),
        start_timeout=240,
        cleanup_on_exit=True,
    )
    print("FLUENT_STARTED")
    print(session.get_fluent_version())
    session.exit()
    print("FLUENT_EXITED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", action="store_true", help="launch Fluent through PyFluent")
    parser.add_argument("--lmstat", action="store_true", help="print FlexNet license status")
    args = parser.parse_args()

    ok = True
    ok &= check_path("Ansys root", ANSYS_ROOT)
    ok &= check_path("Fluent exe", FLUENT_EXE)
    ok &= check_path("lmutil", LMUTIL_EXE)
    ok &= import_pyfluent()

    if args.lmstat:
        run_lmstat()

    if args.launch:
        if not ok:
            print("Refusing launch because prerequisite checks failed.")
            return 2
        return launch_smoke()

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Freeze retained attempts and bounded verified checkpoint without overwriting captures."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import verify_native_babality_victims_v728_v1 as verify

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "audit_v733_native_babality_victims_checked_inputs"
OLD_DRIVER = "83BB5285FB6832B52DCEC43B57A6C4879BDC4FAB23A38F367941A65BA1A26492"


def main():
    if OUT.exists():
        raise ValueError("Do not overwrite checkpoint")
    report = verify.verify(ROOT)
    completed = subprocess.run([sys.executable, str(ROOT / "tools/test_native_babality_victims_v728_v1.py")],
                               check=True, capture_output=True, text=True)
    tests = json.loads(completed.stdout)
    inputs = set()
    resolutions = {}
    attempts = []
    retained = [p for p in ROOT.glob("audit_v7*") if p.is_dir() and
                p.name.split("_")[1][1:].isdigit() and 720 <= int(p.name.split("_")[1][1:]) <= 732]
    for directory in retained:
        for file in directory.rglob("*"):
            if file.is_file():
                inputs.add(file.resolve())
        result = directory / "result.json"
        if not result.exists():
            continue
        data = json.loads(result.read_text(encoding="utf-8-sig"))
        for raw_path, wanted in data["input_hashes"].items():
            source = Path(raw_path)
            actual = source
            if source.name == "midtunit_m.cpp" and wanted.upper() == OLD_DRIVER:
                actual = ROOT / "audit_v727_pre_babality_implementation_inputs/midtunit_m.cpp"
                resolutions[str(source)] = str(actual.resolve())
            if verify.sha(actual) != wanted.upper():
                raise ValueError("Retained attempt input changed: " + str(actual))
            inputs.add(actual.resolve())
        attempts.append(dict(case=directory.name, terminal_exit=data["exit_code"],
                             accepted_case=directory.name in [r["case"] for r in report["cases"]] or
                             directory.name.startswith("audit_v732_old_native_baby_stock_liu_")))
    for name in ["diagnostic_v728_native_babality_victims", "audit_v726_original_baby_reference"]:
        for file in (ROOT / name).rglob("*"):
            if file.is_file():
                inputs.add(file.resolve())
    for path in (ROOT / "tools").glob("*babality*v*.py"):
        inputs.add(path.resolve())
    inputs.add((ROOT / "tools/build_original_babality_reference_v1.py").resolve())
    inputs.add((ROOT / "PLAY_LATEST_TEST_BUILD.cmd").resolve())
    inputs.add((ROOT / "STATUS_2026-10-02_NATIVE_BABALITY_VICTIMS.md").resolve())
    prior = ROOT / "audit_v719_current_ending_presentation_checked_inputs/verification.json"
    if prior.exists():
        inputs.add(prior.resolve())
    hashes = {str(p): verify.sha(p) for p in sorted(inputs)}
    report.update(tests=tests, terminal_attempts=attempts, input_hashes=hashes,
                  historical_source_resolutions=resolutions, checked_input_count=len(hashes),
                  boundedVictimAcceptance=True,
                  prior_checkpoint_scope="v719 manifest referenced by hash; prior underlying inputs not all rechecked")
    OUT.mkdir()
    (OUT / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    # Verify the freeze immediately; no reclassification of failures as passes.
    for raw_path, wanted in hashes.items():
        if verify.sha(Path(raw_path)) != wanted:
            raise ValueError("Input changed during freeze")
    print(json.dumps({"checkpoint": str(OUT), "checked_inputs": len(hashes),
                      "retained_terminal_attempts": len(attempts), "tests_passed": tests["tests_passed"],
                      "fullPortAcceptance": False}, indent=2))


if __name__ == "__main__":
    main()

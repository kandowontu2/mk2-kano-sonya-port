"""Successor: real native CMPI.L, preserving the executed ANDI failure source."""
import inspect
from pathlib import Path
import stage_native_shang_drain_tables as prior

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'source_native_shang_drain_compare'
FAILURE = ROOT / 'audit_native_shang_drain_opcode_failure/report.json'


def main():
    template = prior.TEMPLATE
    prior.need(template.count('shang_drain_code({0x0b80,') == 1, 'Exact offending long-compare template boundary')
    template = template.replace('shang_drain_code({0x0b80,', 'shang_drain_code({0x0b60,', 1)
    source = inspect.getsource(prior.main)
    old = 'Path(__file__), ASSETS'
    new = 'Path(__file__), Path(prior.__file__), FAILURE, ASSETS'
    prior.need(source.count(old) == 1, 'Successor preserves/pins original executed template and discovered opcode failure')
    source = source.replace(old, new, 1)
    scope = dict(vars(prior), prior=prior, OUT=OUT, TEMPLATE=template, FAILURE=FAILURE, __file__=__file__)
    exec(compile(source, __file__ + '::same_owned_data_with_real_CMPI_L', 'exec'), scope)
    return scope['main']()


if __name__ == '__main__':
    main()

"""Fresh real-input Baraka proof on the corrected Jax-only data extension."""
import json
import verify_rolling_heads_v1014 as original
import verify_jax_clap_positions_v1030 as jax

OUT=jax.ROOT/'audit_v1034_baraka_after_jax_clap_checked'
CASES=tuple(f'audit_v1034_baraka_{name}_p{side}_jax_clap_grounding_regression' for name in ('kano','sonya') for side in (1,2))

def verify():
    saved=(original.CANDIDATE,original.EXE,original.CASES,original.verify_payload)
    info=json.loads((jax.ROOT/jax.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    original.CANDIDATE=jax.CANDIDATE;original.EXE=info['executable_sha256'];original.CASES=CASES
    guest,assets=jax.expected_guest()
    payload=(jax.ROOT/jax.CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
    def expected(current=None):
        assert current is None or current==payload
        return guest,assets
    original.verify_payload=expected
    try:
        report=original.verify()
        report['scope']='Fresh normal Dead Pool Baraka all owned rolling heads/body poses, both true victims/slots, corrected Jax-table candidate'
        return report
    finally:
        original.CANDIDATE,original.EXE,original.CASES,original.verify_payload=saved

if __name__=='__main__':
    if OUT.exists():raise ValueError('Preserve regression proof')
    report=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('cases','inputHashes')},indent=2))
    raise SystemExit(0 if report['passed'] else 1)

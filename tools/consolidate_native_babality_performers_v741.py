"""Freeze the actual retained attempts and bounded acceptance; never overwrite evidence."""
import json
from pathlib import Path
import subprocess
import sys
import verify_native_babality_performers_v739 as verify

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_v741_native_babality_performers_checked_inputs'

def main():
    if OUT.exists():raise ValueError('Checkpoint already exists')
    report=verify.verify(ROOT)
    completed=subprocess.run([sys.executable,str(ROOT/'tools/test_native_babality_performers_v739.py')],
                             capture_output=True,text=True,check=True)
    report['tests']=json.loads(completed.stdout)
    inputs=set()
    def collect(directory):
        for path in directory.rglob('*'):
            if path.is_file():inputs.add(path.resolve())
    attempts=[]
    accepted={row['case']for row in report['cases']}
    for directory in ROOT.glob('audit_v7*'):
        number=directory.name.split('_')[1][1:]
        if not directory.is_dir() or not number.isdigit() or not 734<=int(number)<=740:continue
        collect(directory)
        path=directory/'result.json'
        if not path.exists():continue
        data=json.loads(path.read_text(encoding='utf-8-sig'))
        for raw,wanted in data['input_hashes'].items():
            source=Path(raw)
            if verify.v.sha(source)!=wanted.upper():raise ValueError('Retained attempt input changed: '+raw)
            inputs.add(source.resolve())
        attempts.append({'case':directory.name,'terminal_exit':data['exit_code'],
                         'accepted_gameplay_case':directory.name in accepted,
                         'original_reference':int(number) in (734,735)})
    collect(ROOT/'diagnostic_v737_native_babality_performers')
    for name in ('PLAY_LATEST_TEST_BUILD.cmd','STATUS_2026-10-02_NATIVE_BABALITY_PERFORMERS.md',
                 'audit_v733_native_babality_victims_checked_inputs/verification.json',
                 'tools/native_babality_runtime_checks_v739.py',
                 'tools/verify_native_babality_performers_v739.py',
                 'tools/test_native_babality_performers_v739.py',
                 'tools/consolidate_native_babality_performers_v741.py',
                 'audit_v732_native_baby_kano_p1/guest_maincpu.bin'):
        inputs.add((ROOT/name).resolve())
    for side in (1,2):
        case=ROOT/f'audit_v732_native_baby_stock_liu_p{side}'
        for name in ('guest_maincpu.bin','run.log','result.json'):inputs.add((case/name).resolve())
        for age in range(0,721,8):inputs.add((case/f'snap/babality_{age}.png').resolve())
    collect(ROOT/'audit_v726_original_baby_reference')
    hashes={str(path):verify.v.sha(path)for path in sorted(inputs)}
    report.update(input_hashes=hashes,checked_input_count=len(hashes),terminal_attempts=attempts,
                  prior_checkpoint_scope='v733 checksum and actual guest/stock baseline frames checked; other prior inputs not all rechecked')
    OUT.mkdir()
    (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    for raw,wanted in hashes.items():
        if verify.v.sha(Path(raw))!=wanted:raise ValueError('Input changed while freezing')
    print(json.dumps({'checkpoint':str(OUT),'checked_inputs':len(hashes),'retained_terminal_attempts':len(attempts),
                      'tests_passed':report['tests']['tests_passed'],'fullPortAcceptance':False},indent=2))

if __name__=='__main__':main()

"""Independent frozen cold comparison cases; no activation is not move acceptance."""
import argparse,json
from pathlib import Path
import verify_current_guard_uppercut_comparison_v2217 as check

def main():
 p=argparse.ArgumentParser();p.add_argument('fighter',choices=('kano','sonya','liu','subzero'));args=p.parse_args()
 for side in (1,2):
  for capture_version,profile,lead in ((2215,'neutral',6),(2215,'guard_release',6),(2219,'guard_release',12),(2219,'guard_release',24)):
   suffix=f'{args.fighter}_p{side}_{profile}_lead{lead}'
   folder=check.ROOT/f'audit_v{capture_version}_current_{suffix}'
   out=check.ROOT/f'audit_v2221_current_{suffix}_checked'
   check.need(not out.exists(),'Immutable native comparison case')
   try:report=check.verify_case(folder)
   except Exception as error:
    import traceback
    report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
   if report['passed']:
    check.current_launch.module_pins(report['inputHashes'])
    report['inputHashes'][str(Path(__file__).resolve())]=check.current_launch.sha(__file__)
   out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
   print(json.dumps(dict(case=suffix,passed=report['passed'],nativeUppercutAccepted=report.get('nativeUppercutAccepted'),nativeContactDamage=report.get('nativeContactDamage'),error=report.get('error'))),flush=True)
   if not report['passed']:raise SystemExit(1)

if __name__=='__main__':main()

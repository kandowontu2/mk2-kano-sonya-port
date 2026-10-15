"""Freeze current repair/runtime proof without promoting unfinished art."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
 if args.output.exists():raise ValueError('Preserve checkpoint')
 gates=('audit_v882_native_death_palette_checked/verification.json',
        'audit_v884_native_death_palette_units/result.json',
        'audit_v890_current_reptile_victims_checked/verification.json',
        'audit_v891_current_reptile_victim_units/result.json')
 reports=[read(ROOT/p)for p in gates]
 if not(all(r['passed']for r in reports)and reports[0]['guestChangedBytes']==119 and
        reports[1]['methods']==14 and reports[3]['methods']==16 and
        reports[2]['nativeVictimTableAndNormalPaletteRuntimeAcceptance']and
        not reports[2]['fullNativeDeathArtAcceptance']and not reports[2]['fullPortAcceptance']):
  raise ValueError('Exact bounded runtime gates required')
 candidate=ROOT/'diagnostic_v873_native_headless_palettes';build=read(candidate/'build-info.json')
 for name,wanted in build['input_hashes'].items():
  if digest(Path(name))!=wanted:raise ValueError('Build source changed: '+name)
 if digest(candidate/'mkport_candidate.exe')!=build['executable_sha256']or digest(candidate/'roms/mk2ks/mk2ks.mdata')!=build['payload_sha256']:
  raise ValueError('Actual current candidate mismatch')
 installed=ROOT/'mame-mkp/mkport.exe'
 if digest(installed)!='413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891':raise ValueError('Installed build changed')
 launchers=[ROOT/p for p in('PLAY_CURRENT_V786_TEST_BUILD.cmd','PLAY_LATEST_TEST_BUILD.cmd','PLAY_MK2_KANO_SONYA.cmd')]
 previous=read(ROOT/'audit_v867_reptile_native_overrun_checkpoint/checkpoint.json')
 for path in launchers:
  if digest(path)!=previous['inputHashes'][str(path)]:raise ValueError('Launcher changed')
 paths=[ROOT/p for p in gates]+launchers+[installed,Path(__file__),candidate/'build-info.json',
  candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',
  ROOT/'STATUS_2026-10-02_CURRENT_DEATH_PALETTE_AND_VICTIMS.md',
  ROOT/'tools/verify_death_palette_v882.py',ROOT/'tools/test_death_palette_v884.py',
  ROOT/'tools/verify_reptile_victims_v889.py',ROOT/'tools/verify_reptile_victims_v890.py',
  ROOT/'tools/test_reptile_victims_v891.py',ROOT/'mk2ks_reptile_victim_v887.lua',
  ROOT/'tools/run_reptile_victim_v887.ps1']
 for r in(reports[0],reports[2]):paths.extend(Path(p)for p in r['inputHashes'])
 directories=('audit_v871_pre_headless_palette_fix','audit_v874_sonya_p2_native_headless_palette',
  'audit_v876_sonya_p2_native_headless_palette','audit_v878_kano_p2_native_headless_palette',
  'audit_v878_sonya_p2_head_bite_scout','audit_v879_sonya_p2_stock_reptile_victim',
  'audit_v880_sonya_p2_stock_reptile_victim','audit_v881_sonya_p2_stock_reptile_victim',
  'audit_v883_sonya_p2_stock_reptile_victim','audit_v885_sonya_p2_stock_reptile_victim',
  'audit_v886_sonya_p2_stock_reptile_victim','audit_v887_sonya_p2_stock_reptile_victim',
  'audit_v888_kano_p1_stock_reptile_victim','audit_v888_kano_p2_stock_reptile_victim',
  'audit_v888_sonya_p1_stock_reptile_victim','audit_v882_native_death_palette_checked',
  'audit_v884_native_death_palette_units','audit_v889_current_reptile_victims_checked',
  'audit_v890_current_reptile_victims_checked','audit_v891_current_reptile_victim_units',
  'art_native_death_drafts_v875')
 for directory in directories:paths.extend(p for p in(ROOT/directory).rglob('*')if p.is_file())
 paths=list(dict.fromkeys(paths));pins={str(p):digest(p)for p in paths}
 args.output.mkdir();archive=args.output/'input_sources';archive.mkdir()
 for path in paths:
  if path.name in('midtunit_m.cpp','verify_death_palette_v882.py','test_death_palette_v884.py',
                   'verify_reptile_victims_v889.py','verify_reptile_victims_v890.py','test_reptile_victims_v891.py',
                   'mk2ks_reptile_victim_v887.lua','run_reptile_victim_v887.ps1',
                   'STATUS_2026-10-02_CURRENT_DEATH_PALETTE_AND_VICTIMS.md')and path.parent!=archive:
   target=archive/path.name
   if not target.exists():shutil.copy2(path,target);pins[str(target)]=digest(target)
 report={'passed':True,'candidate':candidate.name,'nativePaletteTableRepairAcceptance':True,
  'currentBothTrueVictimsBothPhysicalSlotsAcceptance':True,'nativeDeathArtAcceptance':False,
  'fullPortAcceptance':False,'alternatePaletteRuntimeAcceptance':False,'fullTowerClearAcceptance':False,
  'productionAndExistingLaunchersUnchanged':True,'generatedArtInstalled':False,'guestPaletteChangedBytes':119,
  'directCases':4,'realFinisherSnapshots':124,'unitMethods':30,
  'failedGatePreserved':'audit_v889_current_reptile_victims_checked',
  'priorWholePortProofNotPromoted':'audit_v819_current_ui_ground_checkpoint',
  'remaining':['Correct owned main60 headless bodies and main61 detached heads',
               'Remaining native finisher/art/audio/arena/state coverage',
               'Genuine full towers through bosses, continues and endings',
               'Final integrated regressions, actual CMD/release ZIP and obsolete-build cleanup'],
  'pinCount':len(pins),'inputHashes':pins}
 (args.output/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2))
if __name__=='__main__':main()

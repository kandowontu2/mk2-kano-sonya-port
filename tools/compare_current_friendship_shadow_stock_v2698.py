"""Current Friendship shadow-command scheduling and actor teardown match stock.
Preserve failed scanner verifiers and their exact original-ROM corrections.
Current stock/new comparisons cover one arena/cross-character victims in both
slots. No intermediate-row, rendered-shadow/raster, child-object cleanup,
all-arena, all-finisher or full-port acceptance is implied.
"""
import copy,json,subprocess
from pathlib import Path
import verify_current_friendship_shadow_inventory_v2696 as native
ROOT=native.ROOT
OUT=ROOT/'audit_v2699_current_friendship_shadow_stock_comparison_checked'
need=native.need

def same_behavior(cases):
 need(set(cases)==set(native.CASES),'All eight actual stock/new fighter slot contexts')
 for key,case in cases.items():
  phases=case['phases']
  need(phases['startup']['actualShadowAges']==list(range(10))and phases['startup']['slots']==[1,2]and phases['startup']['nativeCopies']>0,'Actual native stock startup shadow schedule '+key)
  need(all(phases[phase]['nativeComponents']==phases[phase]['nativeCopies']==0 and not phases[phase]['actualShadowAges']for phase in ('native_body_scene','handoff_until_retirement','after_retirement')),'Actual scene shadow suppression matches stock '+key)
  need(case['actualPointerRetirement']-case['cleanup']==441,'Native common handoff-to-actor-retirement delay '+key)
  need(case['unresolvedNativeShadowCallbacks']==0 and case['nativeActorRetirementChecked'],'Actual physical native shadow/retirement coverage '+key)
 return True

def verify():
 pins={};cases={};paths={}
 def pin(path,wanted=None):
  path=str(path)
  if path in pins:need(wanted is None or wanted==pins[path],'Consistent actual shadow dependency '+path);return
  actual=native.scene.launch.sha(path);need(wanted is None or wanted==actual,'Immutable actual shadow dependency '+path);pins[path]=actual
 for key,(fighter,side)in native.CASES.items():
  path=ROOT/f'audit_v2697_current_{fighter}_friendship_shadow_p{side}_checked/report.json';pin(path)
  report=json.loads(path.read_text())
  need(report['passed']and report['case']==key and report['wholeActualGuestAndPayloadReconstructed']and report['originalNativeShadowRoutineUnchanged']and
   report['allActualShadowSourceBuffersROMBound']and report['physicalInputAndBuildUnchanged']and report['rejectedSpecificCounterexamples']==7 and report['finalUnmodifiedControlPassed']and
   not report['intermediateShadowRowsAccepted']and not report['fullShadowRowsOrPixelsAccepted']and not report['fullSceneRasterShadowAudioAccepted']and not report['gameChanged']and not report['fullPortAcceptance'],'Exact original-source continuous inventory and teardown, not rendered-scene acceptance')
  for file,wanted in report['inputHashes'].items():pin(file,wanted)
  cases[key]={field:report[field]for field in ('actualTrueID','actualVictimID','action','cleanup','actualPointerRetirement','continuousFields','nativeShadowCopies','nativeShadowComponents','phases','nativeActorRetirementChecked','unresolvedNativeShadowCallbacks')}
  paths[key]=str(path)
 need(same_behavior(cases),'Current native shadow/retirement behavior matches original stock controls')
 outcomes=[]
 for key in cases:
  for label in ('extra_startup_shadow_age','shadow_survives_native_body_scene','wrong_native_retirement_delay'):
   changed=copy.deepcopy(cases)
   if label=='extra_startup_shadow_age':changed[key]['phases']['startup']['actualShadowAges'].append(10);expected='Actual native stock startup shadow schedule'
   elif label=='shadow_survives_native_body_scene':changed[key]['phases']['native_body_scene']['nativeCopies']=1;expected='Actual scene shadow suppression matches stock'
   else:changed[key]['actualPointerRetirement']-=1;expected='Native common handoff-to-actor-retirement delay'
   need(changed!=cases,'Non-vacuous actual stock/new comparison mutation')
   try:same_behavior(changed)
   except ValueError as error:
    need(expected in str(error),'Intended native stock scheduling/retirement rejection');outcomes.append(dict(case=key,name=label,rejectedBy=str(error)))
   else:raise ValueError('Malformed current-vs-stock shadow behavior accepted')
 changed=copy.deepcopy(cases);changed.pop('sonya_p2')
 try:same_behavior(changed)
 except ValueError as error:
  need('All eight actual stock/new fighter slot contexts'in str(error),'Intended missing actual slot rejection');outcomes.append(dict(name='missing_actual_sonya_p2_context',rejectedBy=str(error)))
 else:raise ValueError('Missing actual fighter/slot context accepted')
 need(same_behavior(cases),'Final untouched current/stock behavioral control')
 # Frozen verifier versions are evidence of harness limitations, not game bugs.
 old=ROOT/'tools/verify_current_friendship_shadow_inventory_v2692.py';middle=ROOT/'tools/verify_current_friendship_shadow_inventory_v2694.py';final=ROOT/'tools/verify_current_friendship_shadow_inventory_v2696.py'
 for path,wanted in ((old,'CC82BD3F9E35CE0C1D99D30A018D66323FABE603C3B89A727FAF0502DF442F76'),(middle,'346CE5242E316473225852B819B4F0B4310586A480BD560482F6D74258806719'),(final,'9EDC5281FD220FF69D15A895AB209714C7262037A6DEDA3A469F2BFEEB30DEC0')):pin(path,wanted)
 text=lambda path:path.read_text().rstrip()+'\n'
 original_block="   if command&0x80:\n    need(bit+8<=len(raw)*8,'Complete compressed native header')\n    header=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit%8))&255\n    pre=(header&15)<<((command>>8)&3);post=(header>>4)<<((command>>10)&3)\n    bit+=8+bpp*max(0,w-pre-post)\n   else:bit+=bpp*w\n   need(bit<=len(raw)*8,'Complete native source-row bounds')"
 corrected_block="   # Original FF801680..FF801770 always scans a header byte, including\n   # descriptors without bit 0x80, and advances by signed width-minus-skips.\n   # Do not substitute the body DMA decoder's conditional/zero-clamped path.\n   need(0<=bit and bit+8<=len(raw)*8,'Complete original native scanner header')\n   header=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit%8))&255\n   pre=(header&15)<<((command>>8)&3);post=(header>>4)<<((command>>10)&3)\n   bit+=8+bpp*(w-pre-post)\n   need(0<=bit<=len(raw)*8,'Complete original native scanner source-row bounds')"
 need(text(old).count(original_block)==1,'Exact failed native-scanner interpretation site')
 fixed=text(old).replace(original_block,corrected_block).replace('audit_v2693_current_','audit_v2695_current_').replace('first=(0xff801400-0xff800000)//8;last=(0xff801650-0xff800000)//8','first=(0xff801070-0xff800000)//8;last=(0xff8017a0-0xff800000)//8')
 need(fixed==text(middle),'Only original scanner semantics, stronger original-code range and output leaves changed')
 expanded=text(middle).replace('def inventory(rows,fighter,side,guest):','def inventory(rows,fighter,side,guest,rom_image):')
 expanded=expanded.replace("buffer=gfx[key];raw=bytes.fromhex(buffer['data']);bit=integer(buffer,'offset')%8;origin=bit;starts=[]","buffer=gfx[key];bit=integer(buffer,'offset');origin=bit;starts=[]")
 expanded=expanded.replace("need(0<=bit and bit+8<=len(raw)*8,'Complete original native scanner header')","need(0<=bit and bit+8<=len(rom_image)*8,'Original native scanner header inside complete source ROM region')")
 expanded=expanded.replace("header=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit%8))&255","header=(int.from_bytes(rom_image[bit//8:bit//8+2],'little')>>(bit%8))&255")
 expanded=expanded.replace("need(0<=bit<=len(raw)*8,'Complete original native scanner source-row bounds')","need(0<=bit<=len(rom_image)*8,'Original native scanner source row inside complete source ROM region')")
 expanded=expanded.replace("rows=scene.previous.parse(folder/'run.log');control=inventory(rows,fighter,side,guest)\n image=graphics.graphics(pins)","rows=scene.previous.parse(folder/'run.log');image=graphics.graphics(pins)\n control=inventory(rows,fighter,side,guest,image)")
 expanded=expanded.replace('inventory(changed,fighter,side,guest)','inventory(changed,fighter,side,guest,image)').replace('inventory(rows,fighter,side,guest)==control','inventory(rows,fighter,side,guest,image)==control').replace('audit_v2695_current_','audit_v2697_current_')
 need(expanded==text(final),'Only complete source-ROM scanner addressing replaces cropped body-buffer addressing; all identity/cadence/field/retirement gates retained')
 failures=[]
 for relative,wanted,expected in (
  ('audit_v2693_current_cage_friendship_shadow_p1_checked/report.json','AF4BCB354DCA659417A185D0EB2595C40348F45E4F6B64BF3F545A6ABC5484E8','Native source/cadence/first-last geometry'),
  ('audit_v2695_current_liu_kang_friendship_shadow_p1_checked/report.json','D8BA47CF4BEC962DF3BADC20A771721A57278891A2EA464BFF04EAD5212FB8C3','Complete original native scanner source-row bounds'),
  ('audit_v2695_current_liu_kang_friendship_shadow_p2_checked/report.json','D8BA47CF4BEC962DF3BADC20A771721A57278891A2EA464BFF04EAD5212FB8C3','Complete original native scanner source-row bounds')):
  path=ROOT/relative;pin(path,wanted);failure=json.loads(path.read_text())
  need(not failure['passed']and expected in failure['error'],'Actual failed original scanner evidence retained')
  failures.append(dict(report=str(path),accepted=False,error=failure['error']))
 exe=ROOT/'mame-mkp/unidasm.exe';rom=ROOT/'mk2/mk2-maincpu.bin';pin(exe);pin(rom,'45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23')
 disassembly=subprocess.run([str(exe),str(rom),'-arch','tms34010','-skip','0x2d0','-count','288','-basepc','0xff801680'],capture_output=True,text=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW).stdout
 for required in ('ff801680: 0548','ff801690: 9548','ff801720: 45a8','ff801740: 410a','ff801760: 410a','ff801770: 3df3'):
  need(required in disassembly,'Original unconditional byte-header/signed subtract/two-plus-four bit advance loop')
 pin(Path(__file__).resolve());native.scene.launch.module_pins(pins)
 return dict(passed=True,cases=cases,caseReports=paths,currentStockAndNewCharacterShadowSchedulingMatches=True,
  observedStartupShadowAges=list(range(10)),observedNativeActorRetirementDelayFromCommonHandoff=441,
  actualContinuousFields=sum(case['continuousFields']for case in cases.values()),actualNativeShadowCopies=sum(case['nativeShadowCopies']for case in cases.values()),
  actualNativeShadowComponents=sum(case['nativeShadowComponents']for case in cases.values()),
  actualInventoryCounterexamples=56,stockComparisonCounterexamples=len(outcomes),outcomes=outcomes,
  finalUnmodifiedControlPassed=True,failedOriginalVerifiers=failures,onlyOriginalScannerSemanticsAndSourceAddressingCorrected=True,
  everyFinalInventoryControlFullyRepeated=True,executedSourcesAndCapturedGameplayNeverEdited=True,originalScannerDisassembly=disassembly,
  inputHashes=pins,gameChanged=False,fullShadowRowsOrPixelsAccepted=False,childObjectCleanupAccepted=False,
  completeSceneRasterShadowAudioAccepted=False,fullFinisherAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Immutable original-stock shadow scheduling comparison')
 report=verify();OUT.mkdir()
 (OUT/'native_shadow_scanner_disassembly.txt').write_text(report['originalScannerDisassembly'])
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','cases','caseReports','outcomes','originalScannerDisassembly')},indent=2),flush=True)

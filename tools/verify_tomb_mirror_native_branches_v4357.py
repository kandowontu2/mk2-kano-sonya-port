"""Actual unpressed native mirror Tomb branches; do not infer unexercised ones.

The original full1731 earned/action/801field/retirement contract is retained.
Held branches additionally require original guest code, actual source-entry
PCs, owned Main/actor registers, RNG compare/result and native fixed ceiling.
Drop branches retain the entire3643 original source/phase qualification.
No held outcome is promoted to coverage of the missing drop/button branches.
"""
import hashlib,json,re,subprocess,traceback
from pathlib import Path
import run_tomb_mirror_audio_ram_v4350 as runtime
ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
OUT=ROOT/'audit_v4358_true_mirror_native_tomb_branches'

def branch(log,guest,fighter,side):
    state=runtime.state
    checked=state.check_log(log,fighter,side,1,guest=guest)
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(hashlib.sha256(original).hexdigest().upper()=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23','Original native source unchanged')
    for first,last in ((0xff8eaf00,0xff8eb490),(0xff876650,0xff876b40),(0xff80e980,0xff80ecf0),(0xff82b800,0xff82bca0)):
        lo,hi=(first-0xff800000)//8,(last-0xff800000)//8
        need(guest[lo:hi]==original[lo:hi],'Every original Tomb/RNG/fall/retirement code byte')
    fields=state.native.legacy.rows(log,'FIELD');first=fields[0];own=17 if fighter=='kano'else 18
    actor,main=first['victim'],first['victim_main'];origin=int(first['frame'])
    entries=('FF8EB0D0','FF8EB150','FF80EC20','FF8EB1A0','FF8EB1B0','FF8EB200','FF8EB290','FF876650','FF8EB3C0','FF8EB400')
    branches=[r for r in state.native.records(log,'BRANCH')if int(r['frame'])>=origin and r['entry']in entries]
    need(len(branches)>=4,'Actual original mirror branch entries')
    rng=int(branches[3]['a0'],16);drop=rng<50
    expected=list(entries[:9])if drop else list(entries[:4])+[entries[9]]
    need([r['entry']for r in branches]==expected and branches[2]['a0']=='00000032'and 0<=rng<1000,
         'Actual original unpressed50/1000 RNG compare and selected branch')
    need(all(int(r['pc'],16)==int(r['entry'],16)+16 and r['io0']=='FFFFFFFF'and
      r['a8']==r['actor']==actor and r['a13']==r['main']==main for r in branches),
      'Actual native source-entry PC and owned true victim task, no pressed drop controls')
    retired=next(r for r in fields if r['own']==r['victim']=='00000000')
    need(int(retired['mode'])==3 and int(retired['arena'])==2,'Actual next-screen native retirement of both mirror actors')
    native=state.scope['qualify_drop'](log,fighter,side,1,'positive',guest)if drop else None
    if not drop:
        begin=int(branches[0]['frame'])
        need(all(int(r['frame'])==begin for r in branches),'Exact genuine held branch chronology')
        floor=220-{17:134,18:135}[own];ceiling=floor-259
        held=[r for r in fields if int(r['frame'])>=begin and r['victim']==actor]
        need(held and all(r['victim_main']==main and int(r['victim_id'])==own and int(r['victim_y'])==ceiling for r in held),
             'Every actual held native victim field remains at original character ceiling until retirement')
        motion=[r for r in state.native.records(log,'FIELD')if int(r['frame'])>begin]
        need(len(motion)>400 and [int(r['frame'])for r in motion]==list(range(begin+1,begin+1+len(motion))),
             'Continuous actual arena1 provenance callbacks, not sparse fabricated phases')
        need(all(r['actor']==actor and r['main']==main and int(r['id'])==own and
          (int(r['y']),int(r['vy'],16),int(r['gravity'],16),int(r['action'],16))==(ceiling,0,0,0x503)for r in motion),
          'Actual original held ceiling503 task and zero native velocity/gravity throughout observed callbacks')
        native=dict(floor=floor,ceiling=ceiling,heldNativeFields=len(held),continuousArena1MotionCallbacks=len(motion))
    return dict(passed=True,fighter=fighter,side=side,trueVictim=own,actualNativeRandomValue=rng,nativeDrop=drop,
      branchPCs=[r['pc']for r in branches],nativeMotion=native,earnedContract=checked,retiredFrame=int(retired['frame']))

def faults(log,guest,fighter,side):
    def change(prefix,key,value):
        lines=log.splitlines();index=next(i for i,s in enumerate(lines)if s.startswith(prefix)and key+'='in s)
        lines[index]=re.sub(r'\b'+key+r'=[^\s]+',key+'='+value,lines[index],count=1)
        return '\n'.join(lines)+'\n'
    variants={
      'nonNativePC':change('MK2_STAGE_PROVENANCE_BRANCH ','pc','00000000'),
      'wrongActor':change('MK2_STAGE_PROVENANCE_BRANCH ','a8','00000000'),
      'wrongMain':change('MK2_STAGE_PROVENANCE_BRANCH ','a13','00000000'),
      'pressedControls':change('MK2_STAGE_PROVENANCE_BRANCH ','io0','FFFFFFFE'),
    }
    result={}
    for key,altered in variants.items():
        try:branch(altered,guest,fighter,side)
        except Exception as error:result[key]=str(error)
        else:raise ValueError('Actual native branch fault accepted: '+key)
    need(branch(log,guest,fighter,side)['passed'],'Original actual positive branch restored')
    return result

def main():
    need(not OUT.exists(),'Fresh immutable actual branch proof')
    source=ROOT/'audit_v4354_both_characters_both_slots_tomb_mirrors/report.json'
    matrix=json.loads(source.read_text());need(matrix['passed']and matrix['actualTrueMirrorContexts']==4,'Actual terminal complete mirror matrix')
    pins=dict(matrix['inputHashes']);pins[str(source)]=sha(source);pins[str(Path(__file__).resolve())]=sha(__file__)
    need(all(sha(path)==h for path,h in pins.items()),'Actual executed matrix sources and native records unchanged')
    guest=runtime.old.expected();cases=[]
    for case in matrix['cases']:
        native=[]
        for name in (case['capture'],case['baseline']):
            log=(ROOT/name/'run.log').read_text();checked=branch(log,guest,case['fighter'],case['side'])
            native.append(checked)
        need(native[0]==native[1],'Exact original branch/physics in both actual PCM comparisons')
        native[0]['actualFaultsRejected']=faults((ROOT/case['capture']/'run.log').read_text(),guest,case['fighter'],case['side'])
        cases.append(native[0])
    return dict(passed=True,candidate=runtime.old.NAME,cases=cases,inputHashes=pins,
      actualHeldMirrorContexts=sum(not c['nativeDrop']for c in cases),actualDropMirrorContexts=sum(c['nativeDrop']for c in cases),
      forcedRNGControlsPaletteStageHealthOrCharacterState=False,allMirrorBranchCoverageAccepted=False,
      fullTombRasterAndFloorShadowAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Never overwrite native branch observations');OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before write')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)

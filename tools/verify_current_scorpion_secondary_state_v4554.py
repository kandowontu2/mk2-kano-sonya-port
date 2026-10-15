"""Whole current native secondary-state grammar and actual-row counterexamples.

All six actual captured positive controls remain intact. Faults change or
remove real observed rows only; no guest writes or invented positive events.
No artwork, floor-shadow, alternate/arena, audio or full-port acceptance.
"""
import json,re,subprocess
from pathlib import Path
import run_current_scorpion_secondary_state_v4549 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v4555_current_scorpion_secondary_state_checked'

def main():
    need(not OUT.exists(),'Fresh immutable actual native grammar/fault proof')
    source=native.OUT/'report.json';prior=json.loads(source.read_text())
    need(prior['passed']and prior['actualCurrentNativeContexts']==6 and
      prior['bothTrueAddedVictimsBothSlotsCurrentSecondaryNativeStateAccepted']and
      not prior['fullArtFloorShadowAllArenaAlternateOrAudioAccepted']and not prior['fullPortAcceptance'],
      'All four actual true17/18 contexts and two stock controls qualified first, exclusions intact')
    pins=dict(prior['inputHashes']);pins[str(source)]=sha(source);pins[str(Path(__file__).resolve())]=sha(__file__)
    need(all(sha(p)==h for p,h in pins.items()),'Every actual captured/executed source/current input unchanged')
    cases=[]
    for case in prior['cases']:
        folder=Path(case['capture']);fighter,side=case['fighter'],case['side'];text=(folder/'run.log').read_text()
        meta=json.loads((folder/'result.json').read_text())
        need(meta['exit_code']==0 and meta['guestSHA256']=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'and
          meta['completeGuestBytesComparedInRAM']==1048576 and meta['nativeRGBFramesDigested']==62 and
          meta['rawMediaGuestROMOrBuildFilesWritten']==0 and not meta['cheatsEnabled']and meta['assistance']=='none',
          'Actually terminal current3836 full-guest and complete RAM-scanout transport, not a stock retired capture')
        positive=native.contract(text,fighter,side);need(positive==case['native'],'Same entire actual native positive grammar')
        lines=text.splitlines();find=lambda prefix,predicate=lambda r:True:next(line for line in lines if line.startswith(prefix)and predicate(dict(re.findall(r'(\w+)=([^\s]+)',line))))
        begin=find('MK2_SSECOND_BEGIN ');b=dict(re.findall(r'(\w+)=([^\s]+)',begin))
        complete=find('MK2_SSECOND_COMPLETE ')
        health=find('MK2_STOCK_HEAD_V921_HEALTH ',lambda r:r['pc']=='FF836700')
        win=find('MK2_SSECOND_WIN ')
        ready=find('MK2_STOCK_HEAD_V921_READY ');zero=int(dict(re.findall(r'(\w+)=([^\s]+)',ready))['frame'])
        held=find('MK2_STOCK_HEAD_V921_INPUT ',lambda r:int(r['slot'])==3-side and r['button']=='High_Punch'and int(r['frame'])==zero+5)
        call=find('MK2_SSECOND_CALL ',lambda r:r['entry']=='FF8BC810')
        call_row=dict(re.findall(r'(\w+)=([^\s]+)',call))
        field=find('MK2_SSECOND_FIELD ',lambda r:r['age']=='105')
        after=find('MK2_SSECOND_FIELD ',lambda r:int(r['frame'])==positive['actualNativeRetirement']+1)
        replacements=[
          ('wrong_actual_activation_fetch_PC',begin,begin.replace('pc=FF8BBFF0','pc=FF8BBFE0')),
          ('proxy_actual_victim_ID',begin,begin.replace('victim_id='+b['victim_id'],'victim_id=3')),
          ('wrong_actual_collision_chain',health,health.replace('before=161','before=160')),
          ('wrong_actual_winner_data_PC',win,win.replace('pc=FF8296B0','pc=FF8296C0')),
          ('missing_actual_held_HP_field',held,held.replace('frame='+str(zero+5),'frame='+str(zero+4))),
          ('wrong_actual_victim_callback_Main',call,call.replace('main='+call_row['main'],'main='+b['main'])),
          ('shifted_actual_cooperative_callback_age',call,call.replace('age='+call_row['age'],'age='+str(int(call_row['age'])+1))),
          ('wrong_actual_completion_age',complete,complete.replace('age=96','age=97')),
          ('wrong_actual_dizzy_continuation',ready,ready.replace('continuation=FFA17E10','continuation=FF83C3D0')),
          ('retired_actual_actor_reappears',after,after.replace('actor1=00000000','actor1='+b['victim_actor'])),
        ]
        faults=[]
        for label,old,new in replacements:
            need(old!=new and lines.count(old)==1,'One real, non-vacuous complete actual row fault: '+label)
            altered=text.replace(old,new,1)
            try:native.contract(altered,fighter,side)
            except ValueError as e:faults.append(dict(label=label,rejectedBy=str(e)))
            else:raise ValueError('Accepted actual native metadata fault: '+label)
            need(native.contract(text,fighter,side)==positive,'Whole unchanged positive restored after every actual-row fault')
        need(lines.count(field)==1,'One actual native105 field removal')
        try:native.contract(text.replace(field+'\n','',1),fighter,side)
        except ValueError as e:faults.append(dict(label='missing_actual_consecutive_native_field',rejectedBy=str(e)))
        else:raise ValueError('Accepted omitted actual native field')
        need(native.contract(text,fighter,side)==positive,'Whole unchanged positive restored after actual missing-field fault')
        cases.append(dict(fighter=fighter,physicalVictimSlot=side,identity=positive['identity'],native=positive,
          actualRowFaultsRejected=faults,wholePositiveRestoredAfterEveryFault=True))
    need(len(cases)==6 and all(len(c['actualRowFaultsRejected'])==11 for c in cases),'All six original positives and66 actual-row rejections')
    need(all(sha(p)==h for p,h in pins.items()),'Every actual current/game/input/source/capture byte unchanged')
    report=dict(passed=True,candidate=native.NAME,cases=cases,inputHashes=pins,
      actualCurrentNativeContexts=6,actualQualifiedFaultsRejected=66,completePhysicalStateFields=5760,
      actualCollisionKOs=12,currentBothTrueAddedVictimsBothSlotsScorpionSecondaryNativeStateAccepted=True,
      fullNativeArtFloorShadowAlternateArenasOrAudioAccepted=False,fullPortAcceptance=False,
      gameCodeOrPublicReleaseChanged=False,scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress checked state before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)

if __name__=='__main__':main()

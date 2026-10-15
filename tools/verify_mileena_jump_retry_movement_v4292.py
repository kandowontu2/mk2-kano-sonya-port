"""Native jumps/air-kicks and earned Mileena rounds, not full tower/observer reuse proof."""
import hashlib,json,re,struct,subprocess,traceback
from pathlib import Path
import verify_mileena_jump_retry_prefix_v4286 as physical
ROOT,need,sha=physical.ROOT,physical.need,physical.sha
FOLDER=physical.FOLDER
OUT=ROOT/'audit_v4293_mileena_jump_retry_movement_checked'
off=lambda a:(a-0xff800000)//8

def check(text,guest,native):
    for first,last,words in ((0xff831320,0xff831360,(0x09c0,0x0308,0xb00d,0x01f0)),
                             (0xff871f10,0xff871f50,(0x09c0,0x0200,0xb00d,0x01f0))):
        need(guest[off(first):off(last)]==native[off(first):off(last)]==struct.pack('<4H',*words),
             'Original HUMAN308 jump/HUMAN200 air-kick action store unchanged')
    replay=physical.replay(text);rows=physical.parse(text)
    fields={r['frame']:r for r in rows if r['tag']=='RANGE_FIELD'}
    actions=[r for r in rows if r['tag']=='RANGE_ACTION']
    jumps=[r for r in actions if int(r['after'])==0x308]
    kicks=[r for r in actions if int(r['after'])==0x200]
    need(len(jumps)==len(kicks)==3,'Actual three original native jumps and three air-kick stores, not Up/HK button counts')
    windows=[]
    for jump in jumps:
        same=lambda r:r['actor']==jump['actor'] and r['main']==jump['main']
        following=[f for n,f in fields.items() if jump['frame']<n<=jump['frame']+40 and
                   f['human_actor']==jump['actor'] and f['human_main']==jump['main']]
        need(following and any(int(f['h_floor'])-int(f['h_y'])>8 for f in following),
             'Actual original jump store followed by owned native airborne motion')
        attacks=[r for r in kicks if jump['frame']<r['frame']<=jump['frame']+40 and same(r)]
        need(len(attacks)==1,'Actual own air-kick dispatch follows each distinct native jump')
        windows.append(dict(actualNativeJumpStore=jump,actualNativeAirKickStore=attacks[0],actualFollowingOwnedFields=following))
    wins=[r for r in rows if r['tag']=='WIN' and r['slot']=='2' and r['stage']=='9']
    need(len(wins)==2 and all(r['id']=='18' and int(r['health'].split(',')[0])==0 and
                             0<int(r['health'].split(',')[1])<=161 for r in wins),
         'Both actual native Mileena rounds won by true Sonya18 with genuine winning health')
    stages=[int(r['stage']) for r in rows if r['tag']=='STAGE']
    need(stages==list(range(13)) and not any(r['tag']=='ENDING_COMPLETED' for r in rows),
         'Actual natural progression to12; do not promote it to tower/ending clear')
    need(not any(r['tag']=='LOSS' and r['stage']=='9' for r in rows),'No paid Mileena loss in actual winning branch')
    return dict(actualPhysicalAndNativeReplay=replay,actualNativeMovementWindows=windows,
      actualOwnedMileenaRoundWins=wins,actualNativeProgressionStages=stages,
      nativeHumanJumpStoreNotHurtFlight=True,ownNativeHumanAirKickNotInputAttempt=True,
      actualNativeCpuThrowStoresLogged=replay['actualNativeCpuGroundThrowStores'],
      observerRepairSlotReuseRuntimeProven=False,allMoveRasterAndAudioAccepted=False)

def main():
    need(not OUT.exists(),'Fresh immutable movement proof');physical.capture.source.source_boundary()
    whole_path=ROOT/'audit_v4289_mileena_jump_retry_whole_campaign_checked/report.json'
    whole=json.loads(whole_path.read_text());need(whole['passed'] and whole['case']['actualWholeCampaignGrammarRetained'] and
        not whole['actualNaturalSonyaP2TowerClearAccepted'],'Complete original native campaign gate, not a full clear')
    text=(FOLDER/'run.log').read_text();guest=physical.capture.expected();native=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    proof=json.loads((FOLDER/'guest_memory_proof.json').read_text())
    need(proof['everyActualByteComparedInRAM'] and proof['sha256']==hashlib.sha256(guest).hexdigest().upper(),
         'Whole actual initialized native guest verified in RAM')
    positive=check(text,guest,native);faults=[]
    rows=physical.parse(text)
    for after in (0x308,0x200):
        r=next(r for r in rows if r['tag']=='RANGE_ACTION' and int(r['after'])==after)
        line=next(l for l in text.splitlines() if l.startswith('MK2_NAT_CAMPAIGN_RANGE_ACTION ') and
          dict(re.findall(r'(\w+)=([^\s]+)',l))=={k:str(v) for k,v in r.items() if k!='tag'})
        for key,value in (('pc','FFF00000'),('a0','00000000'),('owner','01000000')):
            damaged,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and damaged!=line,'Actual non-vacuous movement event fault')
            try:check(text.replace(line,damaged,1),guest,native)
            except ValueError as error:faults.append(dict(action=f'{after:04X}',key=key,rejectedBy=str(error)))
            else:raise ValueError('Native movement event fault accepted '+key)
            need(check(text,guest,native)==positive,'Exact actual movement positive restored')
    for label,address in (('original_jump_opcode',0xff831320),('original_air_kick_opcode',0xff871f10)):
        bad=bytearray(guest);bad[off(address)]^=1
        try:check(text,bytes(bad),native)
        except ValueError as error:faults.append(dict(key=label,rejectedBy=str(error)))
        else:raise ValueError('Original movement instruction fault accepted')
        need(check(text,guest,native)==positive,'Exact original dispatch positive restored')
    pins=dict(whole['case']['inputHashes'])
    for p in (Path(__file__),Path(physical.__file__),whole_path,ROOT/'audit_v4291_mileena_jump_retry_observer_runtime_checked/report.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All source/current native proof unchanged')
    return dict(passed=True,actualMovementAndMileenaProgress=positive,actualNativeFaultsRejected=faults,
      inputHashes=pins,naturalTowerClearAccepted=False,nativeObserverSlotReuseRuntimeProven=False,
      completeMoveRasterAndAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh output')
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before writing')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','actualMovementAndMileenaProgress')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)

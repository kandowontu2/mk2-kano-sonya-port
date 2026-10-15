"""Read-only proof of the native ordinary-throw/fatality index collision."""
import hashlib,json,re,struct
from pathlib import Path
import verify_active_launch_timer_v1520 as prior
ROOT=prior.ROOT
OUT=ROOT/'audit_v1594_native_ground_throw_collision'
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as s:
        for b in iter(lambda:s.read(1048576),b''):h.update(b)
    return h.hexdigest().upper()
def inspect():
    guest,_,payload=prior.expected_guest()
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    off=lambda a:(a-0xff800000)//8
    hook=off(0xff8b6e30)
    assert guest[hook:hook+10]==original[hook:hook+10]==struct.pack('<5H',0x0b09,42,0x0d5f,0x2d90,0xff84)
    folder=ROOT/'audit_v1576_native_arenas_kano_p2'
    launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/prior.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    assert launch['exit_code']==0 and launch['candidate']==prior.NAME and launch['assistance']=='none'
    assert launch['executable_sha256']==build['executable_sha256']==prior.EXE_SHA
    assert launch['payload_sha256']==build['payload_sha256']==sha(ROOT/prior.NAME/'roms/mk2ks/mk2ks.mdata')
    log=folder/'run.log';before=sha(log);lives=[];queues=[]
    with log.open(encoding='utf-8-sig') as s:
        for line in s:
            if not line.startswith(('MK2_NAT_CAMPAIGN_LIVE ','MK2_NAT_CAMPAIGN_FLOOR_QUEUE ')):continue
            r=dict(re.findall(r'(\w+)=(\S+)',line))
            if line.startswith('MK2_NAT_CAMPAIGN_LIVE '):
                if r.get('frame') in ('8130','8190','8250','8280','8310'):lives.append(r)
            elif 8255<=int(r['frame'])<=8376 and r.get('slot')=='2' and r.get('pose') in ('FF0137E0','FF013840','FF0138A0','FF013900'):queues.append(r)
    assert sha(log)==before and lives and queues
    assert all(r['human']=='17:17' and r['cpu']=='18:18' and int(r['health'].split(',')[0])>0 and r['actions']=='0,1287' and r['writes']=='0' and r['assistance']=='none' for r in lives)
    assert all(r['id']==r['roster']=='17' and r['owner']==r['actor'] and r['actor']=='01033E10' for r in queues)
    root=struct.unpack_from('<I',guest,0xfc800+17*4)[0];assert root==0xff000000
    sequence=struct.unpack_from('<I',payload,(root-0xfe800000)//8+60*4)[0];assert sequence==0xff00ba30
    phases=struct.unpack_from('<3I',payload,(sequence-0xfe800000)//8);assert phases==(0xff0137e0,0xff013840,0xff0138a0)
    descriptors=[struct.unpack_from('<I',payload,(g-0xfe800000)//8)[0] for g in phases]
    assert descriptors==[0xff800000+(0xfaa00+i*20)*8 for i in range(3)]
    assert all(0x1ec0000*8<=struct.unpack_from('<I',guest,off(d)+8)[0]<0x1ee0000*8 for d in descriptors)
    paths=[Path(__file__),ROOT/'mk2/mk2-maincpu.bin',ROOT/prior.NAME/'roms/mk2ks/mk2ks.mdata',ROOT/prior.NAME/'build-info.json',folder/'result.json',folder/'snap/floor_epoch4_8264.png']
    pins={str(p.resolve()):sha(p) for p in paths};pins[str(log.resolve())]=before
    return dict(defectConfirmed=True,candidate=prior.NAME,nativeThrowAction=0x507,originalUnchangedSelector='42 + actual attacker ID',attackerID=18,victimID=17,selectedMainAnimation=60,expectedSemanticVictimMain=43,deathGroups=[hex(g) for g in phases],livingVictimObservations=lives,actualOwnedDeathArtPublications=len(queues),actualOwnedDeathArtExamples=queues[:4],capturesAndGameUnchanged=True,inputHashes=pins,fullPortAcceptance=False)
if __name__=='__main__':
    assert not OUT.exists(),'Preserve immutable evidence'
    report=inspect();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','livingVictimObservations','actualOwnedDeathArtExamples')},indent=2))

"""Current physical P2 Kano CPU against true P1 Sonya.

Keeps the original v1456 paired-contact/ordinary-follow-up contract unchanged,
adds every native floor anchor and source-bound store opcode. No universal
CPU, renderer, audio or campaign claim.
"""
import json,re,struct
from pathlib import Path
import verify_current_interrupt_v1870 as launch
import verify_physical_p2_cpu_pair_v1456 as original
from verify_human_special_phases_v1767 import sha

ROOT=launch.ROOT;OUT=ROOT/'audit_v1941_current_kano_physical_p2_cpu_checked'
CASES={'sonya':'audit_v1939_current_kano_p2_cpu_human_sonya'}

def verify_log(log,player,guest):
    result=original.verify_log(log,player)
    assert result['passed'],result['errors']
    fields=original.rows(log,'FIELD')
    for r in fields:
        assert r['id']==17 and r['vid']==original.HUMANS[player] and (r['cpu_slot'],r['human_slot'])==(2,1)
        assert r['floor']==r['stage_floor']-134 and r['vfloor']==r['stage_floor']-(134 if player=='kano'else 135),'Every real CPU/human Main floor anchor'
    flags=original.flag_rows(log)
    for r in flags:
        offset=(r['pc']-32-0xff800000)//8
        assert offset>=0 and struct.unpack_from('<HH',guest,offset)==(r['op0'],r['op1']),'Every native store matches current independently reconstructed code'
        actor=r['actor'];main=r['main']
        assert r['at']==(actor+0x160 if r['kind']=='body'else main+(0x1f0 if r['kind']=='action'else 0x210))
    return dict(originalContract=result,allRecordedFields=len(fields),sourceBoundStores=len(flags),floorAnchorsChecked=True)

def matched(folder,pins):
    meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/launch.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    assert meta['exit_code']==0 and meta['candidate']==launch.NAME and meta['assistance']=='none'and not meta['cheats_enabled']
    assert (meta['cpu_slot'],meta['human_slot'])==(2,1) and meta['input_hashes']==before
    assert meta['executable_sha256']==build['executable_sha256'] and meta['payload_sha256']==build['payload_sha256']
    assert all(before.get(file)==value for file,value in build['input_hashes'].items())
    assert 'mk2ks_cpu_recovery_probe_v1438.lua'in {Path(file).name for file in before}
    for file,value in before.items():
        assert sha(file)==value;pins[file]=value
        if Path(file).suffix in('.lua','.ps1','.json'):assert sha(folder/'input_sources'/Path(file).name)==value
        if Path(file).suffix=='.lua':assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',Path(file).read_text())
    for path in folder.rglob('*'):
        if path.is_file():pins[str(path)]=sha(path)
    return meta

def report():
    pins=launch.source_pins();guest,_,_=launch.current.expected();cases={}
    for player,leaf in CASES.items():
        folder=ROOT/leaf;meta=matched(folder,pins);assert meta['player']==player
        cases[player]=verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),player,guest)
    launch.module_pins(pins)
    return dict(passed=True,candidate=launch.NAME,cases=cases,inputHashes=pins,originalTypedContractUnchanged=True,
        gameBytesChanged=False,allCPUAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=report()
    except Exception as error:result=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in('passed','error','cases')if k in result}),flush=True)
    raise SystemExit(0 if result['passed']else 1)

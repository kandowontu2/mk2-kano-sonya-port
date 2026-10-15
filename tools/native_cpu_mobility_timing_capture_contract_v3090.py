"""Whole actual guest/input/state/health proof for normal CPU mobility runs.

Original v2998 metadata/no-injection/full-ledger contract retained. Add the full
source-assembled bicycle and Square continuation windows, not forced actions.
"""
import json,re,struct
from pathlib import Path
import verify_native_cpu_mobility_inventory_v3038 as choice_inventory
import native_cpu_mobility_capture_contract_v3036 as original
assembly=original.assembly;ledgers=original.ledgers;square=original.square
ROOT=assembly.ROOT;need=assembly.need
HEX=original.HEX
TEXT=original.TEXT|{'move'}
def rows(log,tag):
 result=[]
 for line in log.splitlines():
  if not line.startswith(tag+' '):continue
  values=re.findall(r'(\w+)=([^\s]+)',line)
  need(len(values)==len(dict(values)),'Unambiguous actual mobility fields')
  result.append({k:v if k in TEXT else int(v,16 if k in HEX and not(tag.endswith('_HEALTH')and k in('before','after'))else 10)for k,v in values})
 return result

def capture(folder,build,player,approach,policy,pins,boot_frame,confirm_age):
    def pin(path,wanted=None):
        path=Path(path);path=(path if path.is_absolute()else ROOT/path).resolve()
        actual=assembly.sha(path)
        need(wanted is None or actual==wanted,'Unchanged actual input '+str(path))
        need(str(path)not in pins or pins[str(path)]==actual,'Consistent immutable input')
        pins[str(path)]=actual
    candidate=assembly.NAME if build=='new'else assembly.prior.NAME
    guest,old,payload,_,_=assembly.expected();guest=guest if build=='new'else old
    meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    info=json.loads((ROOT/candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    need(meta['exit_code']==0 and meta['candidate']==candidate and meta['player']==player and
         meta['boot_frame']==boot_frame and meta['confirm_age']==confirm_age and
         meta['approach']==approach and meta['policy']==policy and meta['assistance']=='none'and
         not meta['cheats_enabled']and(meta['cpu_slot'],meta['human_slot'])==(2,1)and before==meta['input_hashes'],
         'Terminal normal physical fixture, no native choices prescribed')
    need(meta['executable_sha256']==info['executable_sha256']and meta['payload_sha256']==info['payload_sha256']and
         all(before.get(file)==wanted for file,wanted in info['input_hashes'].items()),'All compiled inputs match captured runtime')
    pin(ROOT/candidate/'build-info.json');pin(ROOT/candidate/'mkport_candidate.exe',info['executable_sha256'])
    pin(ROOT/candidate/'roms/mk2ks/mk2ks.mdata',info['payload_sha256'])
    need((folder/'guest_maincpu.bin').read_bytes()==guest and (ROOT/candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,
         'Whole guest independently reconstructed, not sampled or address-masked')
    for file,wanted in before.items():
        pin(file,wanted)
        if Path(file).suffix in('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)
        if Path(file).suffix=='.lua':
            need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(',Path(file).read_text()),'No guest/register/AI/RNG/HP injection')
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',log,re.I),'No emulator or observer failure')
    cold=ledgers.pair.rows_prefix(log,'MK2_P2CPU_COLD_LIVE ');selection=ledgers.pair.rows_prefix(log,'MK2_P2CPU_SELECT_RESULT ')
    need(len(cold)==len(selection)==1 and cold[0]['human_id']==selection[0]['human_id']==ledgers.pair.HUMANS[player]and
         cold[0]['cpu_id']==selection[0]['initial_cpu']==18 and selection[0]['checks']==50 and selection[0]['errors']==0,
         'Actual natural CPU Sonya and actual human selected through native CSS')
    health,round_by=ledgers.health_ledger(log,guest,player)
    state=ledgers.state_ledgers(log,guest,player,round_by)
    square.source(log,guest)
    windows=rows(log,'MK2_MOBILITY_CODE')
    need({(w['start'],w['stop'])for w in windows}=={(0xfff9a400,0xfff9d000),(0xffffd1c0,0xffffd340),(0xff831a60,0xff831bc0),(0xff876be0,0xff876e00)}and len(windows)==4,
         'Full bicycle and Square native hit continuation windows')
    for w in windows:
        words=[int(x,16)for x in w['words'].split(',')];lo,hi=((w[k]-0xff800000)//8 for k in('start','stop'))
        need(struct.pack('<'+'H'*len(words),*words)==guest[lo:hi],'Every added hit continuation word source-bound')
    for path in folder.rglob('*'):
        if path.is_file():pin(path)
    return log,guest,dict(candidate=candidate,health=health,stateLedger=state,cold=cold[0],selection=selection[0])

def metadata_contract_source():
 import inspect
 original.metadata_contract_source()
 expected=inspect.getsource(original.capture).replace(
  'def capture(folder,build,player,approach,policy,pins):',
  'def capture(folder,build,player,approach,policy,pins,boot_frame,confirm_age):').replace(
  "meta['boot_frame']==(613 if build=='new'else 604)and meta['confirm_age']==264",
  "meta['boot_frame']==boot_frame and meta['confirm_age']==confirm_age")
 need(expected.rstrip()==inspect.getsource(capture).rstrip(),'Entire original guest/input/state/HP/CPU/ownership contract retained; exact requested physical confirmation timing parameterized')


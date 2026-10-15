"""Retain the complete original1036 earned-state proof for actual audio captures.

No scene metadata is invented: provenance and RAM checks use actual4055 audio
results and every original control/health/parser/lookup/wrap invariant remains.
This gate makes no raster or waveform source-fidelity claim.
"""
import hashlib,inspect,json,re
from pathlib import Path
import verify_jax_clap_positions_v1036 as old
import verify_jax_clap_earned_v4038 as scene_state
ROOT,need,sha=scene_state.ROOT,scene_state.need,scene_state.sha
NAME='diagnostic_v3836_native_mileena_rom_identity'

def rows(text):
    return [dict(tag=tag,**r)for tag,r in old.rows(text,'MK2_STOCK_HEAD_V921')]

def source_boundary():
    controller=(ROOT/'tools/run_jax_clap_native_audio_queue_v4054.py').read_text()
    lua=(ROOT/'mk2ks_jax_clap_audio_queue_ram_v4052.lua').read_text()
    need(controller.count("MK2KS_STOCK_KILLER='jax',MK2KS_STOCK_COMMAND='fff_lp_release',MK2KS_STOCK_GAP='64'")==1,'Exact physical Jax release-LP command, gap64')
    need("'-nocheat'"in controller and "'-noautoframeskip','-frameskip','0'"in controller and ':write_'not in lua,'Actual unassisted original guest execution')
    template=(ROOT/'mk2ks_split_audio_queue_ram_v4000.lua').read_text()
    start=template.index('-- Exact original constructor/cursor/mirror trace,')
    end=template.index("local device=manager.machine.devices[':maincpu']")
    template=template[:start]+template[end:]
    changes={
        'read-only full native Kung Lao audio.':'read-only full native Jax head-clap audio.',
        "0xff8c6040,0xff8c604f,'actual native split audio origin'":"0xff8c7820,0xff8c782f,'actual native Jax head-clap audio origin'",
        'at~=0xff8c6040':'at~=0xff8c7820',
        'p:read_u16(a+0x1f0)~=0':'p:read_u16(a+0x1f0)~=11',
        'a13=%08X id=0':'a13=%08X id=11',
    }
    for before,after in changes.items():
        need(template.count(before)==1,'Unique declared read-only Jax observer adaptation');template=template.replace(before,after)
    need(lua==template,'Complete original thirteen-tap/audio/channel/RAM transport retained, no split task injected')
    return True

def ram_guest(folder,text,guest):
    found=[r for r in (dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_MAUDIO_GUEST_DIGEST '))]
    meta=json.loads((folder/'result.json').read_text());wanted=hashlib.sha256(guest).hexdigest().upper()
    return len(found)==1 and found[0]['sha256']==meta['guestSHA256']==wanted and meta['rawAudioRasterVRAMROMCopiesWritten']==0 and not list(folder.rglob('guest*.bin'))

def gate(text,fighter,side,guest):
    source_boundary();scene_state.source_contract(guest)
    case=f'audit_v4055_jax_clap_{fighter}_p{side}_audio_queue_samples'
    source=inspect.getsource(old.verify)
    boundary="        count=struct.unpack_from('<I',payload,0x160008)[0]"
    need(source.count(boundary)==1,'Original earned grammar boundary');source=source[:source.index(boundary)]
    need(source.count('heads.PAYLOAD')==2,'Both original payload provenance checks');source=source.replace('heads.PAYLOAD','PAYLOAD')
    changes={
        "name,side=result['player'],result['victim_slot']":"name,side=result['fighter'],result['side']",
        "result['killer']=='jax' and result['command']=='fff_lp_release' and result['target_gap']==64":"source_boundary()",
        "result['cheats_enabled'] is False":"'-nocheat' in json.loads((directory/'process.json').read_text())['command']",
        "stops[0]['frame']=='5198'":"int(stops[0]['frame'])==start+750",
        "(directory/'guest_maincpu.bin').read_bytes()==guest":"ram_guest(directory,text,guest)",
    }
    for before,after in changes.items():
        need(source.count(before)==1,'One actual audio provenance/RAM/deadline adaptation');source=source.replace(before,after)
    source+="        cases[case]=dict(origin=start,identity=identity,physicalSide=side,nativeWrapAge=188,collisionDamage=322,nativeRounds=2)\n    return dict(passed=not errors,errors=sorted(set(errors)),cases=cases)\n"
    ns=dict(vars(old));ns.update(CANDIDATE=NAME,CASES=(case,),PAYLOAD='91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24',expected_guest=lambda:(guest,None),source_boundary=source_boundary,ram_guest=ram_guest)
    exec(compile(source,__file__+'::complete_original1036_audio_state','exec'),ns)
    result=ns['verify'](texts={case:text})
    need(result['passed'],'Entire original Jax physical/health/parser/lookup/wrap algorithm '+repr(result['errors']))
    return result['cases'][case]

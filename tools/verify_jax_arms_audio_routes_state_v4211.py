"""Full original1074 earned arm state and palette proof for RAM-only audio.

No graphics/pixel metadata is fabricated. All original earned command, health,
true-ID table, palette route and147-field wrap checks are retained. Waveform
fidelity requires separate source qualification, not a matching digest alone.
"""
import hashlib,inspect,json,re
from pathlib import Path
import verify_native_arm_palette_v1074 as old
import verify_jax_arms_earned_v4078 as scene_state
ROOT,need,sha=scene_state.ROOT,scene_state.need,scene_state.sha
NAME='diagnostic_v3836_native_mileena_rom_identity'

def source_boundary():
    runner=(ROOT/'tools/run_jax_arms_native_audio_routes_v4212.py').read_text()
    wrapper=(ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua').read_text()
    need(runner.count("MK2KS_STOCK_KILLER='jax',MK2KS_STOCK_COMMAND='bbbb_lp',MK2KS_STOCK_GAP='96'")==1,'Exact original physical BBBB LP, gap96')
    need("'-nocheat'" in runner and "'-noautoframeskip','-frameskip','0'" in runner,'Unassisted native execution, no skipped fields')
    scene=(ROOT/'mk2ks_jax_arms_native_scene_ram_v4073.lua').read_text()
    first=scene.index('-- Keep only the original three read-only prop-palette taps.')
    last=scene.index('local previous={}',first)
    taps=scene[first:last]
    baseline=(ROOT/'mk2ks_jax_clap_audio_routes_ram_v4057.lua').read_text()
    changes={
      'read-only full native Jax head-clap audio.':'read-only full native Jax arm-rip audio.',
      "dofile('mk2ks_stock_extended_earned_ram_v3958.lua')\n":"dofile('mk2ks_stock_extended_earned_ram_v3958.lua')\n"+taps,
      "0xff8c7820,0xff8c782f,'actual native Jax head-clap audio origin'":"0xff8be240,0xff8be24f,'actual native Jax arm-rip audio origin'",
      'at~=0xff8c7820':'at~=0xff8be240',
    }
    for before,after in changes.items():
        need(baseline.count(before)==1,'Unique declared observer adaptation');baseline=baseline.replace(before,after)
    need(wrapper==baseline,'Whole original PCM/DCS/channel observer retained, only arm origin and exact read-only1073 suffix added')
    palette=(ROOT/'mk2ks_arm_palette_trace_v1073.lua').read_text()
    marker="local p=manager.machine.devices[':maincpu'].spaces.program"
    need(palette.count(marker)==1,'Unique read-only palette suffix')
    need(not re.search(r':write_|set_value|clear_value|\.value\s*=(?!=)|snapshot\(|io\.open|dofile',palette[palette.index(marker):]),'Palette suffix cannot alter gameplay or create media')
    return True

def ram_guest(folder,text,guest):
    found=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_MAUDIO_GUEST_DIGEST ')]
    meta=json.loads((folder/'result.json').read_text());wanted=hashlib.sha256(guest).hexdigest().upper()
    return len(found)==1 and found[0]['sha256']==meta['guestSHA256']==wanted and meta['rawAudioRasterVRAMROMCopiesWritten']==0 and not list(folder.rglob('guest*.bin'))

def make_gate(guest,case):
    source=inspect.getsource(old.verify)
    boundary="        need((directory/'native_arm_rip_gfx.bin').read_bytes()==graphics"
    need(source.count(boundary)==1,'Complete original earned/palette/table boundary');source=source[:source.index(boundary)]
    changes={
      'guest,graphics,assets=reconstruct()':'guest,graphics,assets=actual_guest,None,None',
      "name=result['player'];side=result['victim_slot']":"name=result['fighter'];side=result['side']",
      "not result['cheats_enabled'] and result['killer']=='jax' and result['command']=='bbbb_lp' and result['target_gap']==96":"source_boundary() and '-nocheat' in json.loads((directory/'process.json').read_text())['command']",
      "stops[0]['frame']=='5198'":"int(stops[0]['frame'])==start+750",
      "(directory/'guest_maincpu.bin').read_bytes()==guest":"ram_guest(directory,text,guest)",
    }
    for before,after in changes.items():
        need(source.count(before)==1,'Unique actual provenance/RAM/deadline adaptation');source=source.replace(before,after)
    source+='''        writers={'FF836700','FF825930'if side==1 else'FF825960','FF9DECE0'if side==1 else'FF9DED10','FF9DEF40'if side==1 else'FF9DEF70'}
        need(all(r['pc']in writers for r in items('HEALTH')),'All original native health writers '+case)
        need(len(items('WIN'))==2 and live[0]['own']==action['actor']and action['mode']=='2','Two actual WIN reads, true Jax owner '+case)
        cases[case]=dict(victim=name,side=side,origin=start,nativeWrapAge=147,realCollisionDamage=322,nativeRounds=2,actualPropPaletteConsumers=2,actualOwnedTableConsumers=6)
    return dict(passed=not errors,errors=sorted(set(errors)),cases=cases)
'''
    ns=dict(vars(old));ns.update(CANDIDATE=NAME,CASES=(case,),actual_guest=guest,source_boundary=source_boundary,ram_guest=ram_guest)
    exec(compile(source,__file__+'::original1074_complete_audio_state','exec'),ns)
    return ns['verify']

def gate(text,fighter,side,guest,case):
    source_boundary();scene_state.source_contract(guest)
    result=make_gate(guest,case)(texts={case:text})
    need(result['passed'],'Entire original arm-rip earned state, true tables and palette route '+repr(result['errors']))
    need(result['cases'][case]['victim']==fighter and result['cases'][case]['side']==side,'Actual physical context')
    return result['cases'][case]

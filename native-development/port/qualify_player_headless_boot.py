"""Fresh player patch/stock binary startup; not interactive/gameplay acceptance."""
import json
import csv
import re
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile
from audit_stock_mame_distribution import player_member, file_digest
from inspect_normal_runtime import PORT, BASE
from refresh_special_videos import FLAGS

OBSERVER='''local m=manager.machine
local p=m.devices[':maincpu'].spaces.program
local n=0
local f=assert(io.open('boot.csv','w'))
f:write('field,mode,pc\\n')
emu.register_frame_done(function()
 n=n+1
 if n%20==0 then
  local a=0x010601d0
  f:write(string.format('%d,%d,%x\\n',n,p:read_u8(a)|(p:read_u8(a+8)<<8),m.devices[':maincpu'].state['PC'].value))
  f:flush()
 end
 if n==600 then f:close();m:exit() end
end)
'''


def combat_acceptance(state,mirror=False):
    targets=('18','17') if mirror else ('17','18')
    controlled=[r for r in state if r['mode']=='2' and r['p1state']==r['p2state']=='1' and
        (r['p1char'],r['p2char'])==targets and r['locked']=='1']
    result=dict(controlledHumanFields=len(controlled),targets=targets,
        minimumHP=[min((int(r[k]) for r in controlled),default=161) for k in ('p1hp','p2hp')],
        missingAnimationObserved=any(int(r['missing'])!=0 for r in controlled))
    result['passed']=len(controlled)>=600 and all(hp<161 for hp in result['minimumHP']) and not result['missingAnimationObserved']
    return result


def main():
    assert sys.argv[1:] in ([],['--attract'],['--acknowledge'],['--combat'],['--combat-mirror'])
    combat=bool(sys.argv[1:] and sys.argv[1].startswith('--combat'))
    mirror=sys.argv[1:]==['--combat-mirror']
    acknowledge=sys.argv[1:]==['--acknowledge']
    attract=bool(sys.argv[1:])
    fields=9000 if combat else (3600 if attract else 600)
    observer=OBSERVER.replace('n==600',f'n=={fields}')
    if acknowledge:
        observer=observer.replace('local n=0',"local hp=assert(m.ioport.ports[':IN0'].fields['P1 High Punch'])\nlocal acknowledged=false\nlocal n=0")
        observer=observer.replace(' n=n+1', ''' n=n+1
 local mode=p:read_u8(0x010601d0)|(p:read_u8(0x010601d8)<<8)
 if mode==1 then acknowledged=true end
 hp:set_value(not acknowledged and n>=1000 and n%120<3 and 1 or 0)''')
    if combat:
        observer=(PORT/'diagnostics/normal_probe.lua').read_text()
        assert observer.count('soak and n>=24000')==1
        observer=observer.replace('soak and n>=24000','soak and n>=9000')
    out=PORT/'development_patches'
    proof=json.loads((out/'PLAYER_PLAYTEST_QUALIFICATION.json').read_text())
    package=Path(proof['file']);assert file_digest(package)==proof['SHA256']
    idle=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
        'if (Get-Process mame -ErrorAction SilentlyContinue) { exit 7 }; exit 0'],
        capture_output=True,creationflags=FLAGS)
    assert idle.returncode==0,'Existing emulator'
    with tempfile.TemporaryDirectory(prefix='player-boot-check-',dir=out) as folder:
        work=Path(folder)
        with zipfile.ZipFile(package) as archive:
            pins=json.loads(archive.read('FILES.json'))
            for name in archive.namelist():
                if player_member(name) or name=='uismall.bdf':
                    target=work/name;target.parent.mkdir(parents=True,exist_ok=True)
                    target.write_bytes(archive.read(name));assert file_digest(target)==pins[name]
        root=PORT.parents[1]
        emulator=root.parent/'mame0289/mame.exe'
        assert file_digest(emulator)==pins['mame.exe']==proof['stockEmulatorSHA256']
        os.link(emulator,work/'mame.exe') # No duplicate316MiB executable.
        environment=os.environ.copy();environment.pop('PYTHONPATH',None)
        environment['PYTHONNOUSERSITE']='1';environment['PYTHONDONTWRITEBYTECODE']='1'
        if combat:
            symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',
                (BASE/'mk2-rebuild-main/srcp/MK2P.MAP').read_text())}
            environment.update(KS_NORMAL_SOAK='1',KS_NORMAL_MIRROR='1' if mirror else '0',
                KS_NORMAL_P1_STATE=str(symbols['p1_state']),KS_NORMAL_P2_STATE=str(symbols['p2_state']),
                KS_RECOVERY_PC=str(symbols['illegal_opcode']+0x50),
                KS_MISSING_COUNT=str(symbols['ks_missing_animation_count']))
            for direction in ('UP','DOWN','LEFT','RIGHT'):
                environment['KS_NORMAL_NAV_'+direction]=str(symbols['ks_'+direction.lower()+'_change'])
        subprocess.run([sys.executable,str(work/'patch_native_roms.py'),'--mk2',str(root/'roms/mk2.zip'),
            '--mk3',str(root/'mk3.zip'),'--output',str(work/'roms/mk3.zip')],cwd=work,env=environment,
            check=True,capture_output=True,timeout=60,creationflags=FLAGS)
        assert file_digest(work/'roms/mk3.zip')==file_digest(out/'roundtrip/roms/mk3.zip')
        assert b' -noreadconfig ' in (work/'PLAY.cmd').read_bytes()
        (work/'observe.lua').write_text(observer)
        command=[str(work/'mame.exe'),'mk3','-noreadconfig','-rompath',str(work/'roms'),
            '-cfg_directory',str(work/'config/cfg'),'-nvram_directory',str(work/'config/nvram'),
            '-snapshot_directory',str(work/'config/snap'),'-video','none','-sound','none',
            '-nothrottle','-skip_gameinfo','-autoboot_script',str(work/'observe.lua'),'-seconds_to_run','180' if combat else ('90' if attract else '20')]
        result=subprocess.run(command,cwd=work,env=environment,capture_output=True,text=True,timeout=60,creationflags=FLAGS)
        log=result.stdout+result.stderr
        assert result.returncode==0,log[-2000:]
        assert '[LUA ERROR]' not in log and 'Fatal error:' not in log,log[-2000:]
        rows=(work/('soak_state.csv' if combat else 'boot.csv')).read_text().splitlines()
        if combat:
            state=list(csv.DictReader(rows))
            attract_observed=any(r['mode']=='1' for r in state)
            combat_summary=combat_acceptance(state,mirror)
            assert rows[-1].startswith('9000,'),'Observer ended early'
        else:
            assert len(rows)==fields//20+1 and rows[-1].startswith(f'{fields},'),rows[-3:]
            assert len({r.split(',')[2] for r in rows[1:]})>1,'No observed CPU progression'
            attract_observed=any(r.split(',')[1]=='1' for r in rows[1:])
    assert not work.exists()
    report=dict(scope=(f'{fields} fresh-player fields with finite true-identity human combat; not full gameplay/renderer acceptance' if combat else
        f'{fields} headless startup fields from fresh player patch; not combat/interactive renderer acceptance'),
        packageSHA256=proof['SHA256'],stockEmulatorSHA256=proof['stockEmulatorSHA256'],
        exitCode=result.returncode,observations=rows,temporaryFilesRemoved=True,
        gameMemoryWrites=False,interactiveRendererAcceptance=False,fullPortVerified=False,
        physicalHighPunchAcknowledgment=acknowledge or combat,attractModeObserved=attract_observed,
        observer=observer,log=log)
    if combat:report['combat']=combat_summary
    name=('PLAYER_HEADLESS_COMBAT_MIRROR.json' if mirror else 'PLAYER_HEADLESS_COMBAT.json') if combat else ('PLAYER_HEADLESS_ATTRACT_ACK.json' if acknowledge else ('PLAYER_HEADLESS_ATTRACT_NO_INPUT.json' if attract else 'PLAYER_HEADLESS_BOOT.json'))
    (out/name).write_text(json.dumps(report,indent=2)+'\n')
    if attract:assert attract_observed,'No attract mode observed; failed observations preserved in '+name
    if combat:assert combat_summary['passed'],'Combat gate failed; observations preserved in '+name
    print(f'Verified{fields} headless startup fields; temporary ROM and executable link removed')


if __name__=='__main__':main()

"""Whole genuine pressure snapshot/VRAM/palette/source binding, not DMA proof.

All1800 consecutive current video snapshots are bound to the actual observed
native scanout, including held/nonlive callbacks. Retain original source
equations and all transport bytes. FIFO ownership, complete replay, artistic
review and wider character integration remain separate requirements.
"""
import hashlib
import json
import re
import traceback
from collections import ChainMap
from pathlib import Path
import capture_native_selector_sonya_pressure_snapshot as capture
import qualify_native_selector_sonya_pressure_snapshot_schedule as schedule
import qualify_native_selector_walkin_knife_vram as ram
import qualify_native_selector_walkin_knife_display_face_rows as names
import verify_native_floor_display_v602 as scanout
import read_live_shang_drain_frames as census

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_snapshot_binding_checked'
FRAMES=schedule.FRAMES


def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()
            if line.startswith(tag+' ')]


def schema(text,display):
    snaps=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_SNAP')
    fields=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_DISPLAY')
    state=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_STATE')
    latch=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_LATCH')
    held=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_HELD')
    need([int(r['frame'])for r in snaps]==[int(r['frame'])for r in fields]==FRAMES and
         [int(h['frame'])for h in display['rgbHeaders'].values()]==FRAMES and
         set(display['rgb'])=={'display_%d.png'%f for f in FRAMES},
         'Every actual source-scheduled snapshot, scanout and RGB header exactly once, in order')
    need(all(r['phase']=='frame_done'and r['origin']=='1817'and
             int(r['age'])==int(r['frame'])-1817 for r in snaps),
         'Entire current callback phase and original opening Ring origin, no retiming')
    targets=latch+held
    need(len(targets)==len(FRAMES)and sorted(int(r['snapshot'])for r in targets)==FRAMES,
         'Every actual current snapshot has one genuine flip latch or held native buffer')
    targets={int(r['snapshot']):r for r in targets}
    state={int(r['frame']):r for r in state}
    need(set(state)==set(range(1817,3618)), 'Whole live/nonlive state callback inventory; terminal has no frame_done')
    for snap,field in zip(snaps,fields):
        f=int(snap['frame']);target=targets[f]
        need(snap['file']=='display_%d.png'%f and target['file']=='display_vram_%d.bin'%f and
             field['palette_file']=='display_palette_%d.bin'%f and
             all(field[k]==target[k]for k in ('start','control','tap')),
             'Exact snapshot/VRAM/palette association and current native display registers')
    return snaps,fields,targets,state


def one(snap,field,target,display):
    return scanout.check_latch(display['rgb'][snap['file']],display['buffers'][target['file']],
        display['buffers'][field['palette_file']],*(int(field[k],16)for k in ('start','control','tap')))


def execute(state):
    need(not OUT.exists(),'Fresh immutable whole pressure current scanout qualification')
    parent_path=schedule.OUT/'report.json';parent=json.loads(parent_path.read_text())
    folder,text,_=capture.RAM_CASES[capture.KEY];handle=capture.NATIVE_HANDLES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text())
    need(parent['passed']and meta['passed']and handle['process'].poll()==parent['nativeExit']==meta['nativeExit']==0 and
         handle['identity']==parent['actualNativeIdentity']==meta['nativeTerminal']['actualWindowsIdentity']and
         (handle['identity']['ProcessId'],handle['identity']['ParentProcessId'],handle['identity']['createdUnix'])==
         (47004,38752,1791773031.802763)and not meta['nativeTerminal']['hostDecodeErrors']and
         not capture.reference.base.choices.current.prior.identity.census(),
         'Exact original new47004 terminal Popen/native identity; no timeout substitution')
    host=next(r for r in census.census_hosts()if r['ProcessId']==38752)
    need(host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766,
         'Original retained capture host still live with exact native birth')
    pins=dict(parent['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'All complete preceding sources/evidence unchanged')
    windows={'cold_high':state['WINDOWS']['high'],'cold_owned':state['WINDOWS']['owned'],
             'cold_graphics':state['WINDOWS']['graphics'],'guest':state['guest'],'gfx':state['gfx']}
    need(set(meta['proofs'])==set(windows),'All five complete independent current startup windows')
    for key,raw in windows.items():
        need(meta['proofs'][key]==dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),
             everyActualByteComparedInRAM=True),'Exact entire actual initialized native bytes: '+key)
    display=capture.DISPLAY
    counts=ram.verify_transport(display)
    image=names.runtime_graphics(state,pins);ram.graphics(display,image)
    native_audio=capture.AUDIO[capture.KEY];old_audio=capture.reference.AUDIO[capture.reference.KEY]
    for key in ('pcmChunks','pcmHeaders','dacChunks','dacHeaders','rom','expectedROM','audioGuestObserved'):
        need(native_audio[key]==old_audio[key],'Entire actual original pressure sound history unchanged: '+key)
    snaps,fields,targets,states=schema(text,display)
    records=[]
    for snap,field in zip(snaps,fields):
        f=int(snap['frame']);proof=one(snap,field,targets[f],display)
        records.append(dict(frame=f,file=snap['file'],mode=int(states[f]['mode']),
            health1=int(states[f]['health1']),health2=int(states[f]['health2']),
            held='reason'in targets[f],**proof))
    faults=[]
    def reject(label,action):
        try:action()
        except (ValueError,AssertionError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Effective actual full pressure counterexample accepted: '+label)
    for f in (1818,2324,2611,2942,3039,3107,3176,3599,3617):
        i=f-1818;snap,field=snaps[i],fields[i];target=targets[f]
        changed=dict(display,rgb=ChainMap({snap['file']:display['rgb'][snap['file']].copy()},display['rgb']))
        changed['rgb'][snap['file']][100,100,0]^=1
        reject('actual_current_pixel_%d'%f,lambda:one(snap,field,target,changed))
        one(snap,field,target,display)
    for label,file in (('whole_final_VRAM','display_vram_3617.bin'),
                       ('whole_reset_palette','display_palette_2611.bin'),
                       ('whole_opening_prepass','display_pre_1817.bin')):
        raw=bytearray(display['buffers'][file]);raw[-1]^=1
        changed=dict(display,buffers=ChainMap({file:bytes(raw)},display['buffers']))
        reject(label,lambda:ram.verify_transport(changed))
    bad=dict(display,rgb=ChainMap({},display['rgb']),rgbHeaders=dict(display['rgbHeaders']))
    bad['rgbHeaders'].pop('display_2611.png')
    reject('missing_actual_reset_header',lambda:schema(text,bad))
    first_record=next(iter(display['gfx'].values()));first=int(first_record['first'])
    bad_image=bytearray(image);bad_image[first]^=1
    reject('actual_whole_packed_source_byte',lambda:ram.graphics(display,bad_image))
    ram.verify_transport(display);ram.graphics(display,image);schema(text,display)
    need(all(one(s,f,targets[int(s['frame'])],display)['pixels']==101600 for s,f in zip(snaps,fields)),
         'Every whole untouched actual current native scanout restored after all effective faults')
    for p in (Path(__file__),Path(ram.__file__),Path(names.__file__),Path(names.previous.__file__),
              names.previous.NAME_MODEL,Path(scanout.__file__),Path(schedule.__file__),parent_path,folder/'result.json'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No executed source/evidence changes');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every whole source/native pin intact after restored positives')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=handle['identity'],nativeExit=0,
        completeCurrentSnapshots=len(records),exactCurrentDisplayedPixels=sum(r['pixels']for r in records),
        modeCounts={m:sum(r['mode']==m for r in records)for m in sorted({r['mode']for r in records})},
        heldSnapshotCount=sum(r['held']for r in records),wholeTransportBuffers=counts[0],
        wholeGraphicsSourceStreams=len(display['gfx']),records=records,effectiveFaultsRejected=faults,
        wholeOriginalSoundHistoryUnchanged=True,completeCurrentVRAMPaletteScanoutBindingAccepted=True,
        completeNativeDMAReplayAccepted=False,corpseEffectOwnershipAccepted=False,actualVisualReviewAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,inputHashes=pins,
        requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS all1800 actual current pressure snapshots; whole native VRAM/palette/source binding',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual whole pressure scanout rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise

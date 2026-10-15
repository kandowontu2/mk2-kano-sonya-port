"""Same terminal data, exhaustive original absolute-frame sampling contract.

Keep original106-per-window assumption FAILED. Existing recorder samples every
early100 fields plus actual f%8 tail through150; third start has107, not106.
No callbacks are removed, invented, retimed or replayed.
"""
import hashlib,json,re
from pathlib import Path
import capture_native_selector_cpu_rings_snapshot_ram as capture
import qualify_native_selector_walkin_knife_vram as ram

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_rings_snapshot_transport_checked'


def execute(state):
    need(not OUT.exists(),'Fresh whole same-terminal transport qualification')
    failure=capture.OUT/'failure.json';failed=json.loads(failure.read_text())
    need(not failed['passed']and failed['actualSnapshotCounts']==[106,106,107]and
         failed['error']=="ValueError('All three actually observed full source/VRAM/palette/current RGB windows present')",
         'Keep actual original host cardinality failure unchanged')
    folder,text,_=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text());parent=json.loads(capture.PARENT.read_text())
    need(meta['passed']and held['process'].poll()==meta['nativeExit']==0 and
         held['identity']==meta['nativeTerminal']['actualWindowsIdentity']and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==
         (16764,38752,1791765504.9070606)and not meta['nativeTerminal']['hostDecodeErrors'],
         'Original exact native terminal and whole current cold/state transport genuinely pass')
    pins=dict(meta['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Every complete source/evidence pin intact')
    windows={'cold_high':state['WINDOWS']['high'],'cold_owned':state['WINDOWS']['owned'],
             'cold_graphics':state['WINDOWS']['graphics'],'guest':state['guest'],'gfx':state['gfx']}
    need(set(meta['proofs'])==set(windows),'Exactly all five original complete independent current windows')
    for key,raw in windows.items():
        need(meta['proofs'][key]==dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),
             everyActualByteComparedInRAM=True),'Whole exact independent current cold bytes: '+key)
    original=(ROOT/'mk2ks_human_projectile_full_display_v1289.lua').read_text()
    need('return f-origin<=100 or f%8==0' in original and 'f>origin+960' in original and
         "once('f>origin+960','f>origin+150')" in capture.LUA.read_text(),
         'Actual unchanged whole absolute-frame sample predicate and declared150-field window')
    records=[]
    for n,start in ((1,1817),(2,2175),(3,3027)):
        expected=[f for f in range(start+1,start+151)if f-start<=100 or f%8==0]
        display=capture.DISPLAY[n];actual=[int(h['frame'])for h in display['rgbHeaders'].values()]
        need(actual==expected,'Every actual original source-scheduled callback exactly once; no missing or extra pixel buffer')
        ram.verify_transport(display)
        snaps=[dict(re.findall(r'(\w+)=([^\s]+)',l))for l in text.splitlines()if
               l.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP ')and f'window={n} ' in l]
        need([int(r['frame'])for r in snaps]==expected and all(r['origin']==str(start)and
             r['age']==str(int(r['frame'])-start)and r['phase']=='frame_done'and
             display['rgbHeaders'][r['file']]['window']==str(n) for r in snaps),
             'Every native sampled callback/phase/window/header associated exactly')
        records.append(dict(window=n,start=start,completeSourceScheduledFrames=expected,
            nativeRGBCallbacks=len(actual),buffers=len(display['buffers']),gfxStreams=len(display['gfx'])))
    tags=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_',
          'MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_','MK2_STARTUP_PROJECTILE_')
    old=capture.reference.RAM_CASES[capture.reference.KEY][1]
    need([l for l in text.splitlines()if l.startswith(tags)]==[l for l in old.splitlines()if l.startswith(tags)],
         'Every whole actual physical/HP/identity/projectile/retirement history identical to retained original')
    physical=capture.physical.gate(text,state['guest'])
    for path in (Path(__file__),Path(capture.__file__),Path(ram.__file__),failure,folder/'result.json'):
        key=str(path.resolve());h=sha(path);need(key not in pins or pins[key]==h,'Original source/results immutable');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every full original source/evidence pin after whole transport qualification')
    result=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        originalCardinalityFailurePreserved=True,windows=records,actualRGBFrames=sum(r['nativeRGBCallbacks']for r in records),
        completeOriginalSourceSamplingAccepted=True,wholeNativeStateHealth=physical,inputHashes=pins,
        requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        independentRendererAccepted=False,fullPortAcceptance=False,newNativeGames=0,
        newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,publicPlayableChanged=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS actual source-scheduled Ring frames106/106/107; original16764 retained',flush=True)
    return result

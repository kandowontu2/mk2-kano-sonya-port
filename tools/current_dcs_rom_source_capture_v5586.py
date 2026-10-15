"""Actual complete loaded native DCS ROM source, before/after real finisher.

Independently construct12MiB original sound region from all six original
CRC/SHA1-qualified ROMs, erased odd lanes and mirrors. Compare every actual
byte twice in RAM; retain whole previous physical/art/voice/priority/packet/
port/ADSP/PCM gate. This is necessary firmware/data evidence, NOT an
independent original mixed-waveform oracle or full-port acceptance.
"""
import binascii, hashlib, inspect, json, re, traceback, zipfile
from pathlib import Path
import qualify_current_baraka_direct_packets_v5580 as direct

origin=direct.observed
capture=direct.capture
ROOT,need,sha=direct.ROOT,direct.need,direct.sha
PARENT=ROOT/'audit_v5584_current_baraka_direct_packet_matrix_progress/progress.json'
BASE=ROOT/'audit_v5587_current_dcs_rom_source_ram'
OUT=ROOT/'audit_v5588_current_dcs_rom_source_progress'
LUA=ROOT/'mk2ks_current_dcs_rom_source_v5585.lua'
DRIVER=ROOT/'diagnostic_v5219_current_payload_rom_metadata/input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
ARCHIVE=ROOT/'roms/mk2.zip'
COMPLETED=[]
EXPECTED=None
MANIFEST=((2,'5f23d71d','54c2afef243759e0f3dbe2907edbc4302f5c8bad'),
          (3,'d6d92bf9','397351c6b707f2595e36360471015f9fa494e894'),
          (4,'eebc8e0f','705ab63ff7672a4857d546afda6dca4973cce1ad'),
          (5,'2b0b7961','1cdc64aab74d14afbd8c3531e3d0bd49271a281f'),
          (6,'f694b27f','d43e38a124665f49ebb4ffc5a55e8f19a1a64686'),
          (7,'20387e0a','505d05173b2a1f1ee3ebc2898ccd3a95c98dd04a'))

def expected_region(pins):
    need(sha(DRIVER)=='17FCD9D7C5D862FEB03487828364AC4126D9B0C7AB437DAEBD94F760DA11C0DE',
         'Exact executed candidate driver source, not dirty checkout or invented ROM declaration')
    text=DRIVER.read_text()
    wanted=[]
    for i,(number,crc,s1) in enumerate(MANIFEST):
        wanted.append((f'l1_mortal_kombat_ii_sound_rom_u{number}.u{number}',i*0x200000,0x80000,crc,s1))
    for name in ('mk2','mk2ks'):
        body=text.split(f'ROM_START( {name} )',1)[1].split('ROM_REGION16_LE( 0x100000, "maincpu"',1)[0]
        need('ROM_REGION16_LE( 0xc00000, "dcs", ROMREGION_ERASEFF )' in body,
             'Whole original12MiB little-endian erased sound region declaration')
        loads=[(m[1],int(m[2],16),int(m[3],16),m[4],m[5]) for m in re.finditer(
            r'ROM_LOAD16_BYTE\(\s*"([^"]+)",\s*(0x\w+),\s*(0x\w+),\s*CRC\((\w+)\) SHA1\((\w+)\)',body)]
        reloads=[(int(m[1],16),int(m[2],16)) for m in re.finditer(r'ROM_RELOAD\(\s*(0x\w+),\s*(0x\w+)',body)]
        need(loads==wanted and reloads==[(i*0x200000+0x100000,0x80000)for i in range(6)],
             'All stock and port sound ROM names/lanes/sizes/CRC/SHA1/reload addresses independently exact')
    result=bytearray(b'\xff'*0xc00000);sources=[]
    with zipfile.ZipFile(ARCHIVE) as archive:
        for name,address,size,crc,s1 in wanted:
            raw=archive.read(name)
            need(len(raw)==size and f'{binascii.crc32(raw):08x}'==crc and hashlib.sha1(raw).hexdigest()==s1,
                 'Every complete original sound firmware/data ROM byte bound to original CRC and SHA1')
            for offset in (address,address+0x100000):result[offset:offset+2*size:2]=raw
            sources.append(dict(name=name,bytes=size,address=address,mirrorAddress=address+0x100000,
                                crc32=crc,sha1=s1,sha256=hashlib.sha256(raw).hexdigest().upper()))
    for p in (DRIVER,ARCHIVE,ROOT/'mame-mkp/src/frontend/mame/luaengine_mem.cpp'):
        pins[str(p.resolve())]=sha(p)
    return bytes(result),sources

def region_gate(raw,phase):
    need(phase in ('startup','terminal') and len(raw)==0xc00000 and raw==EXPECTED,
         'Every actual '+phase+' sound ROM byte equals independent stock firmware/data/lane/mirror reconstruction')
    return dict(phase=phase,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),
                everyActualByteComparedInRAM=True,wholeOriginalSoundRegionSourceExact=True)

def region_faults(raw,phase):
    positive=region_gate(raw,phase);faults=[]
    for offset,label in ((0,'actual firmware byte'),(1,'erased odd byte lane'),
                         (0x100000,'actual firmware mirror'),(0xbffffe,'last sound-data mirror byte')):
        bad=bytearray(raw);bad[offset]^=1
        try:region_gate(bytes(bad),phase)
        except ValueError as error:faults.append(dict(phase=phase,label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted real loaded sound ROM corruption')
    need(region_gate(raw,phase)==positive,'Complete actual sound source positive restored after real RAM-byte faults')
    return faults

# Preserve the entire5533 canonical live native capture. Add only ROM-region
# transport; no raw transport hex is ever retained in log files.
source=capture.source
edits={
    '    chunks=[];pcm_headers=[];audio_guest=None':
    '    chunks=[];pcm_headers=[];audio_guest=None\n    dcs={"startup":bytearray(),"terminal":bytearray()};dcs_headers=[]',
    "                if line.startswith(('MK2_BBAUDIO_PCM ','MK2_MAUDIO_GUEST ')):":
    """                if line.startswith('MK2_NATIVE_DCS_ROM '):
                    r=dict(re.findall(r'(\\w+)=([^\\s]+)',line));raw=bytes.fromhex(r.pop('hex'));phase=r['phase']
                    need(phase in dcs and int(r['offset'])==len(dcs[phase]) and len(raw)==int(r['bytes'])==65536
                         and r['size']=='12582912' and r['bytewidth']=='2' and r['bitwidth']=='16'
                         and r['writes']=='0' and r['assistance']=='none','Complete consecutive passive original sound region chunks')
                    need(r['frame']==('1'if phase=='startup'else'5198'),'Real initialized and native terminal sound ROM checkpoints')
                    at=int(r['offset']);need(raw==EXPECTED[at:at+len(raw)],'Every original loaded sound ROM chunk source-exact')
                    dcs[phase].extend(raw);r['sha256']=digest(raw);dcs_headers.append(r)
                    out.write('MK2_NATIVE_DCS_ROM_DIGEST '+' '.join(k+'='+str(v)for k,v in r.items())+'\\n')
                elif line.startswith(('MK2_BBAUDIO_PCM ','MK2_MAUDIO_GUEST ')):""",
    '    pcm=b\'\'.join(chunks)':
    "    dcs_proof=[region_gate(bytes(dcs[phase]),phase)for phase in ('startup','terminal')]\n"
    "    dcs_faults=[f for phase in ('startup','terminal')for f in region_faults(bytes(dcs[phase]),phase)]\n"
    "    need(len(dcs_headers)==384 and len(dcs_faults)==8,'Every complete actual sound ROM region and eight effective byte faults')\n"
    "    final.update(actualOriginalDCSROMProof=dcs_proof,effectiveActualDCSROMByteFaults=dcs_faults,actualDCSROMChunkHeaders=dcs_headers)\n"
    "    pcm=b''.join(chunks)",
}
for before,after in edits.items():
    need(source.count(before)==1,'Entire live native physical/raster/PCM capture only adds read-only original ROM transport')
    source=source.replace(before,after,1)
scope=dict(capture.scope,ROOT=ROOT,BASE=BASE,LUA=LUA,COMPLETED=COMPLETED,EXPECTED=EXPECTED,
           region_gate=region_gate,region_faults=region_faults)
exec(compile(source,__file__+'.entire5533_native_capture_plus_actual_original_DCS_ROM_region','exec'),scope)
native_capture=scope['capture']

# Retain the entire5577 actual-native run audit and source/voice/priority/
# packet/return/fault/PCM nonperturbance/storage gates, adding source semantics
# qualified in5580 and the complete loaded sound ROM region.
source=inspect.getsource(origin.run)
edits={
    '    guest = capture.original.model.current.expected()':
    '    global EXPECTED\n    guest = capture.original.model.current.expected()',
    '    payload = (ROOT/capture.original.model.current.NAME/\'roms/mk2ks/mk2ks.mdata\').read_bytes()':
    "    EXPECTED,rom_sources=expected_region(pins);native_capture.__globals__['EXPECTED']=EXPECTED\n"
    "    payload = (ROOT/capture.original.model.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()",
    "    record = capture.capture(('kano',1),guest,payload,gfx,reference,pins,image,True)":
    "    record = native_capture(('kano',1),guest,payload,gfx,reference,pins,image,True)",
    '    positive = gate(log,guest)':
    '    positive = gate(log,guest)\n    direct_positive=direct.gate(log,guest);direct_faults=direct.faults(log,guest)',
    "    need(len(pngs) == 1 and all(sha(p) == h for p,h in pins.items()), 'One native timed PNG and exact source/current/public/evidence pins')":
    "    need(len(pngs) == 1 and all(sha(p) == h for p,h in pins.items()), 'One native timed PNG and exact source/current/public/evidence pins')\n"
    "    need(len(meta['actualOriginalDCSROMProof'])==2 and len(meta['effectiveActualDCSROMByteFaults'])==8\n"
    "         and len(direct_faults)==12 and 'MK2_NATIVE_DCS_ROM_RESULT frame=5198 checks=2 writes=0 assistance=none' in log,\n"
    "         'Both actual whole sound-ROM checkpoints, complete original direct-source/full-word gate and every new byte fault')",
    "thisGoalTurnClassification='progress: actual original every-packet entry/caller/stack/return independently recorded, complete direct control packets and priority packets high/low/ADSP delivered;10new actual packet-origin faults plus12announcer/22priority faults, original full native physical/art/source voice/timer/RGB/PCM nonperturbance retained; exact direct original callers now available for semantic source decoding'":
    "thisGoalTurnClassification='progress: independently reconstructed complete12MiB stock sound firmware/data region from all six CRC/SHA1 source ROMs including every erased lane and reload mirror; every actual byte compared twice at real startup and native5198 terminal, eight actual RAM byte faults rejected; entire physical/art/voice/announcer/priority/direct-source/full-word/return/ADSP/timer and unchanged125-raster/full-PCM proof retained, no mixed-waveform oracle claim'",
    '        actualPacketOrigins=positive,effectiveActualPacketOriginFaults=rejected,retainedActualAnnouncerFaults=ann_faults,':
    '        actualPacketOrigins=positive,effectiveActualPacketOriginFaults=rejected,retainedActualAnnouncerFaults=ann_faults,\n'
    '        independentOriginalSoundROMs=rom_sources,actualOriginalDCSROMProof=meta["actualOriginalDCSROMProof"],\n'
    '        effectiveActualDCSROMByteFaults=meta["effectiveActualDCSROMByteFaults"],\n'
    '        qualifiedDirectSourceAndFullWordDelivery=direct_positive,effectiveDirectSourceBranchAndPortFaults=direct_faults,',
    "nextAction='Decode actual four original direct packet caller targets and control-word semantics from stock source; qualify source counterexamples without replay, then extend contexts and original waveform/all remaining requirement groups.'":
    "nextAction='Use the actual source-exact original sound firmware/data foundation to qualify independent original DCS mixed-waveform reference; retain all four-context direct-path proof and broaden stage/branch/finisher/move/CPU/campaign/combined-UI/release coverage without narrowing the full original goal.'",
}
for before,after in edits.items():
    need(source.count(before)==1,'Entire5577 native source/return/audio/storage audit with additive loaded sound ROM proof: '+before)
    source=source.replace(before,after,1)
scope=dict(origin.__dict__,ROOT=ROOT,PARENT=PARENT,BASE=BASE,OUT=OUT,LUA=LUA,COMPLETED=COMPLETED,
           direct=direct,native_capture=native_capture,expected_region=expected_region,EXPECTED=EXPECTED,__file__=__file__)
exec(compile(source,__file__+'.entire5577_actual_native_audit_plus_complete_stock_sound_ROM_source','exec'),scope)
run=scope['run']

if __name__=='__main__':
    need(not BASE.exists() and not OUT.exists(),'Fresh immutable actual original sound ROM capture')
    try:report=run()
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedNativeCaptures=COMPLETED,
                    goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in ('remaining','newInputHashes','actualPacketOrigins',
        'effectiveActualPacketOriginFaults','retainedActualAnnouncerFaults','retainedActualPriorityFaults',
        'actualTimerCoverage','actualSourceVoiceEffectRoutes','completedNativeCaptures','qualifiedDirectSourceAndFullWordDelivery',
        'effectiveDirectSourceBranchAndPortFaults')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)

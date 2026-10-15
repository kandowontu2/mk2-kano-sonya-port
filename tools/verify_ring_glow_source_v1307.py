"""Independent whole-guest/source proof for native Sonya ring charge colours."""
import json,re,struct,subprocess
from pathlib import Path
import numpy as np
import verify_native_metadata_build_v1254 as prior
import inspect_secondary_display_v1231 as raster
ROOT=prior.ROOT;CANDIDATE='diagnostic_v1306_native_sonya_ring_glow'
OUT=ROOT/'audit_v1307_native_ring_glow_source_checked'
digest=prior.digest
CHARGE_POSES=(0xfe83dbe0,0xfe83dc40,0xfe83dca0,0xfe83dd00)

def charge_words():
    donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();at=(0xffc96fb0-0xff800000)//8
    assert struct.unpack_from('<H',donor,at)[0]==64
    words=list(struct.unpack_from('<64H',donor,at+2));words[0]=0
    return words

def reconstruct():
    old,gfx,assets,payload=prior.reconstruct();guest=bytearray(old)
    assert guest[0xfc000:0xfc400]==b'\xff'*0x400
    struct.pack_into('<H64H',guest,0xfc000,64,*charge_words())
    words=[]
    address=lambda at:0xff800000+at*8
    cursor=lambda:0xfc100+len(words)*2
    def emit(*w):words.extend(w)
    def mov(reg,value):emit(0x09e0+reg,value&65535,value>>16)
    def jump(op,target):emit(op,target&65535,target>>16)
    def branch(op):at=len(words)+1;jump(op,0);return at
    def patch(at):target=address(cursor());words[at:at+2]=[target&65535,target>>16]
    emit(0x01e0,0x098f,0xf000,0xb502,0x01f0,0x0b42,0xffed)
    not_sonya=branch(0xcb80)
    emit(0x07a1,0x0220,0x0106,0x4901);physical=branch(0xca80)
    emit(0x07a1,0x0df0,0x0106,0x4901);not_physical=branch(0xcb80);patch(physical)
    charged=[]
    for pose in CHARGE_POSES:mov(1,pose);emit(0x4820);charged.append(branch(0xca80))
    emit(0xb501,0x0140,0x2f01,0x24c1,0x0b21,0xbb30,0x0105,0x8621)
    mov(2,address(0xfc000));emit(0x4841);not_charged=branch(0xcb80)
    mov(0,address(0xfdb00));emit(0xb501,0x0160,0x1f21);normal=branch(0xca80)
    mov(0,address(0xf1600));patch(normal);jump(0x0d5f,0xff841090);restored=branch(0xc080)
    for at in charged:patch(at)
    mov(0,address(0xfc000));jump(0x0d5f,0xff841090)
    for at in(not_sonya,not_physical,not_charged,restored):patch(at)
    entry=(0xff838790-0xff800000)//8;original=struct.unpack_from('<4H',old,entry)
    assert original==(0xb208,0x1d0,0xb504,0xf0)
    emit(0x09af,0x000f,0x01c0,*original);jump(0xc080,0xff8387d0)
    assert cursor()<=0xfc400
    struct.pack_into('<'+str(len(words))+'H',guest,0xfc100,*words)
    struct.pack_into('<HI',guest,entry,0xc080,address(0xfc100))
    return bytes(guest),gfx,assets,payload

def check_charge_palette(q,actual):
    assert q['id']==q['roster']==18 and q['pose']in CHARGE_POSES and q['slot']in(1,2)
    expected=np.array([sum(((((c>>s)&31)<<3)|(((c>>s)&31)>>2))<<dest for s,dest in((10,16),(5,8),(0,0)))for c in charge_words()],dtype=np.uint32)
    bank=q['bank']&0x7f00
    assert np.array_equal(actual[bank:bank+64],expected),'Original pink ring-charge palette missing or recoloured'

def verify():
    pins={}
    def pin(path,wanted=None):
        path=Path(path);actual=digest(path);assert wanted is None or actual==wanted,'Changed evidence '+str(path);pins[str(path)]=actual
    metadata_path=prior.OUT/'report.json';metadata=json.loads(metadata_path.read_text());assert metadata['passed'];pin(metadata_path)
    for file,wanted in metadata['inputHashes'].items():pin(file,wanted)
    candidate=ROOT/CANDIDATE;build_path=candidate/'build-info.json';build=json.loads(build_path.read_text(encoding='utf-8-sig'));pin(build_path)
    assert build['name']==CANDIDATE and not build['metadata_only_source_rebuild']and build['game_data_changed']
    for file,wanted in build['input_hashes'].items():pin(file,wanted)
    source=candidate/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
    old_source=ROOT/'audit_v1303_ring_glow_source_transition/midtunit_m.before.cpp';pin(old_source,'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34')
    text=source.read_text();first=text.index("\t// Sonya's first four original ring-release composites")
    last=text.index('\t// The stock fireball impact aligns',first)
    assert text[:first]+text[last:]==old_source.read_text(),'Host-source changes outside isolated native palette/router insertion'
    pin(ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp',digest(old_source))
    driver=candidate/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    assert driver.read_bytes()==(ROOT/prior.CANDIDATE/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp').read_bytes()
    pin(candidate/'mkport_candidate.exe',build['executable_sha256']);pin(candidate/'roms/mk2ks/mk2ks.mdata',build['payload_sha256'])
    expected,_,_,payload=reconstruct();assert payload==(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()
    guest_path=ROOT/'audit_v1308_projectile_ring_p1/guest_maincpu.bin';assert guest_path.read_bytes()==expected,'Whole actual guest must equal independently encoded palette/router patch';pin(guest_path)
    reference=ROOT/'audit_v297_original_ring_release_full';result=json.loads((reference/'result.json').read_text(encoding='utf-8-sig'))
    assert result['exit_code']==0 and result['scope']=='original_MK3_read_only_reference'and result['choreography']
    for file,wanted in result['input_hashes'].items():pin(file,wanted)
    for path in reference.rglob('*'):
        if path.is_file():pin(path)
    # Old mechanical raster tests can be green while using the WRONG colours.
    # Retain actual old files and prove the new colour contract rejects them.
    old_folder=ROOT/'audit_v1291_projectile_ring_p1';groups,*_=raster.data(old_folder);rejected=0
    for display in groups['FLOOR_DISPLAY']:
        actual=np.fromfile(old_folder/display['palette_file'],dtype='<u4')
        for q in groups['FLOOR_QUEUE']:
            if q['frame']==display['frame']-1 and q['slot']==1 and q['pose']in CHARGE_POSES:
                try:check_charge_palette(q,actual)
                except AssertionError:rejected+=1
                else:raise AssertionError('Old incorrect costume palette accepted as pink charge')
    assert rejected>20;pin(old_folder/'run.log')
    pin(Path(__file__))
    return dict(passed=True,candidate=CANDIDATE,wholeGuestIndependentlyReconstructed=True,
        sourceChangesOnlyNativeChargePaletteRouter=True,payloadUnchanged=True,oldWrongChargePaletteSamplesRejected=rejected,
        originalGamePinkChargeReferenceBound=True,nativeROMAuditAccepted=False,inputHashes=pins,
        interruptedReleaseRestorationAccepted=False,allMoveArtAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
    assert not OUT.exists();OUT.mkdir()
    try:
        report=verify();exe=ROOT/CANDIDATE/'mkport_candidate.exe';rompath=str(ROOT/CANDIDATE/'roms')+';'+str(ROOT/'roms')
        audit=subprocess.run([str(exe),'mk2ks','-verifyroms','-rompath',rompath],cwd=ROOT,capture_output=True,text=True)
        (OUT/'verifyroms.log').write_text(audit.stdout+audit.stderr)
        assert audit.returncode==0 and '1 were OK'in audit.stdout and not re.search('WRONG CHECKSUMS|might not run correctly|BAD DUMP|NOT FOUND',audit.stdout+audit.stderr,re.I)
        report['nativeROMAuditAccepted']=True
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Native Sonya charge source/whole guest proof passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
    raise SystemExit(0 if report['passed']else 1)

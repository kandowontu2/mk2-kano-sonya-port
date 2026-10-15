"""Independent native release-origin contact fix, original close reference."""
import json,re,struct,subprocess
from pathlib import Path
import verify_ring_glow_source_v1310 as prior
ROOT=prior.ROOT;CANDIDATE='diagnostic_v1323_native_ring_release_contact'
OUT=ROOT/'audit_v1325_native_ring_close_source_checked'
digest=prior.digest;CHARGE_POSES=prior.CHARGE_POSES
check_charge_palette=prior.check_charge_palette

def reconstruct():
    old,gfx,assets,payload=prior.reconstruct();guest=bytearray(old)
    at=0xf8e00;original=old[at:at+62]
    assert struct.unpack_from('<4H',original)==(0xb701,0x1a0,0x5600,0x8201)
    assert struct.unpack_from('<3H',original,56)==(0xc080,0xfe80,0xff8a)
    assert old[at+62:at+92]==b'\xff'*30
    prefix=struct.pack('<15H',0x09e0,19,0,0x0d5f,0x6a10,0xff8b,
        0x09e0,19,0,0x0d5f,0x6ac0,0xff8b,0xc880,0xffb0,0xff8a)
    guest[at:at+92]=prefix+original
    return bytes(guest),gfx,assets,payload

def original_close(pins):
    folder=ROOT/'audit_v1320_original_ring_close'
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    assert result['exit_code']==0 and result['target']=='sonya'and result['scenario']=='hit'and result['choreography']
    for file,wanted in result['input_hashes'].items():
        assert digest(file)==wanted;pins[file]=wanted
        if Path(file).suffix in('.lua','.ps1'):assert digest(folder/'input_sources'/Path(file).name)==wanted
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    def rows(tag):return[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()if line.startswith(tag+' ')]
    fields=[q for q in rows('MK3_KNIFE_FIELD')if q['frame']=='3900']
    assert len(fields)==2 and abs(int(fields[0]['x'])-int(fields[1]['x']))==63 and fields[0]['id']=='1'
    contacts=[q for q in rows('MK3_KNIFE_HEALTH')if int(q['frame'])<4000]
    assert len(contacts)==1 and contacts[0]['frame']=='3923'and contacts[0]['slot']=='2'and int(contacts[0]['before'])-int(contacts[0]['after'])==19 and contacts[0]['pc']=='FFA5D5A0'
    body=[q for q in rows('MK3_CHOREO_GROUP')if q['body']=='1'and int(q['frame'])<4000]
    child=[q for q in rows('MK3_CHOREO_GROUP')if q['body']=='0'and int(q['frame'])<4000]
    assert len(body)==5 and [q['group']for q in body]==['FF83DBE0','FF83DC40','FF83DCA0','FF83DD00','FF83DEC0']
    assert child[0]['frame']=='3923'and child[0]['group']=='FF83E200'and not any(q['group']in('FF83E100','FF83E140','FF83E180','FF83E1C0')for q in child)
    for path in folder.rglob('*'):
        if path.is_file():pins[str(path)]=digest(path)
    return dict(gap=63,firstRelease=int(body[0]['frame']),firstContact=int(contacts[0]['frame']),firstChildGroup=child[0]['group'],contactBeforeTravel=True)

def verify():
    pins={};previous=json.loads((prior.OUT/'report.json').read_text());assert previous['passed']
    pins[str(prior.OUT/'report.json')]=digest(prior.OUT/'report.json')
    for file,wanted in previous['inputHashes'].items():assert digest(file)==wanted;pins[file]=wanted
    folder=ROOT/CANDIDATE;build=json.loads((folder/'build-info.json').read_text(encoding='utf-8-sig'))
    assert build['name']==CANDIDATE and build['prior_candidate']==prior.CANDIDATE and not build['metadata_only_source_rebuild']and build['game_data_changed']
    for file,wanted in build['input_hashes'].items():assert digest(file)==wanted;pins[file]=wanted
    source=folder/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp';text=source.read_text()
    first=text.index('\t// Original Sonya checks contact at the release origin before any travel.')
    last=text.index('\t// Allocation requires a first group, but Sonya has no held ring intro.',first)
    assert text[:first]+text[last:]==(ROOT/prior.CANDIDATE/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp').read_text()
    for name in('midtunit_m.cpp','midtunit.cpp'):
        a=ROOT/'mame-mkp/src/mame/midway'/name;b=ROOT/'audit_v1321_ring_close_source_transition'/name.replace('.cpp','.before.cpp')
        assert a.read_bytes()==b.read_bytes();pins[str(a)]=digest(a);pins[str(b)]=digest(b)
    guest,_,_,payload=reconstruct()
    for side in(1,2):
        path=ROOT/f'audit_v1324_ring_interrupt_p{side}/guest_maincpu.bin';assert path.read_bytes()==guest;pins[str(path)]=digest(path)
    for path,wanted in((folder/'mkport_candidate.exe',build['executable_sha256']),(folder/'roms/mk2ks/mk2ks.mdata',build['payload_sha256'])):
        assert digest(path)==wanted;pins[str(path)]=wanted
    assert (folder/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload
    reference=original_close(pins)
    pins[str(folder/'build-info.json')]=digest(folder/'build-info.json');pins[str(Path(__file__))]=digest(__file__)
    return dict(passed=True,candidate=CANDIDATE,wholeGuestIndependentlyReconstructed=True,sourceChangesOnlyNativeReleaseContactPrefix=True,
        payloadUnchanged=True,canonicalHistoricalSourceRestored=True,originalCloseReference=reference,inputHashes=pins,nativeROMAuditAccepted=False,
        interruptedReleaseRestorationAccepted=False,allMoveArtAccepted=False,fullPortAccepted=False)

if __name__=='__main__':
    assert not OUT.exists();OUT.mkdir()
    try:
        report=verify();audit=subprocess.run([str(ROOT/CANDIDATE/'mkport_candidate.exe'),'mk2ks','-verifyroms','-rompath',str(ROOT/CANDIDATE/'roms')+';'+str(ROOT/'roms')],cwd=ROOT,capture_output=True,text=True)
        (OUT/'verifyroms.log').write_text(audit.stdout+audit.stderr)
        assert audit.returncode==0 and '1 were OK'in audit.stdout and not re.search('WRONG CHECKSUMS|might not run correctly|BAD DUMP|NOT FOUND',audit.stdout+audit.stderr,re.I)
        report['nativeROMAuditAccepted']=True
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Native release-contact source passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
    raise SystemExit(0 if report['passed']else 1)

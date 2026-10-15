"""Read-only ZIP consistency and explicit outstanding documentation checkpoint."""
import hashlib,json,zipfile
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
path=root/'release_current_native_playtest_20261013_complete_roms/MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013_complete_roms.zip'
def digest(stream):
    h=hashlib.sha256()
    while block:=stream.read(65536):h.update(block)
    return h.hexdigest().upper()
matches=[]
with zipfile.ZipFile(path)as z:
    names=z.namelist()
    for suffix,actual in [('mkport_candidate.exe',sync.BUILD/'mkport_candidate.exe'),('mk2ks.mdata',sync.BUILD/'roms/mk2ks/mk2ks.mdata')]:
        selected=[n for n in names if n.endswith('/'+suffix)or n==suffix];assert len(selected)==1
        with z.open(selected[0])as stream:sha=digest(stream)
        assert sha==sync.sha(actual).upper();matches.append(dict(member=selected[0],SHA256=sha,currentFile=str(actual)))
    wavs=[n for n in names if n.lower().endswith('.wav')];assert len(wavs)==23
    for n in wavs:
        actual=sync.BUILD/'samples/mk2ks'/n.rsplit('/',1)[-1]
        if not actual.is_file():actual=root/'samples/mk2ks'/n.rsplit('/',1)[-1]
        assert actual.is_file()
        with z.open(n)as stream:assert digest(stream)==sync.sha(actual).upper()
    readmes=[n for n in names if n.rsplit('/',1)[-1]=='README.txt'];assert len(readmes)==1
    text=z.read(readmes[0]).decode();assert 'NOT a completed or certified port' in text
    stale='reaches stage5' in text
    launcher=[n for n in names if n.rsplit('/',1)[-1]=='PLAY.cmd'];assert len(launcher)==1
    cmd=z.read(launcher[0]).decode();assert '-nocheat' in cmd and 'check_current_native_playtest.ps1' in cmd
out=root/'audit_current_package_checkpoint_checked';assert not out.exists();out.mkdir()
report=dict(passed=True,zipSHA256=sync.sha(path),zipBytes=path.stat().st_size,currentExecutableAndPayloadExact=matches,all23WaveformAssetsEqualCurrent=True,zipLabelsUnfinishedPlaytest=True,zipReadmeCampaignCheckpointStale=stale,centralStatusTopAlsoSuperseded=True,finalPublicPromotionAuthorized=False,gameSourceChanged=False,scope='Streaming ZIP reads only; no extraction/game launch/new package. Exact EXE/payload/23waveforms and ordinary launcher checked. ROM completeness/nativeaudit retained from root check; final combined acceptance and updated release documentation/package remain required.')
(out/'report.json').write_text(json.dumps(report,indent=2));print(out)

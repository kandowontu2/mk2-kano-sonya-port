"""Correct only new payload ROM identity; preserve strict checksum failure."""
import hashlib,json,subprocess,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'audit_v3834_native_mileena_rom_identity_checked'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def main():
    if OUT.exists():raise ValueError('Immutable new loader proof')
    proof_path=ROOT/'audit_v3820_native_mileena_victim_data_checked/report.json';proof=json.loads(proof_path.read_text())
    assert proof['passed']and proof['requiresCompilationAndNativeRuntimeRegression']and not proof['runtimeAcceptance']
    payload=ROOT/'asset_v3812_native_mileena_victims/roms/mk2ks/mk2ks.mdata';raw=payload.read_bytes()
    driver=ROOT/'source_v3832_native_mileena_rom_identity/midtunit.cpp'
    original=ROOT/'diagnostic_v3680_native_sound_packet_guard/input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    old='CRC(a65205cf) SHA1(b8f9602b0c1a620df3f7e13bd7f659185cc40afa)'
    new=f'CRC({zlib.crc32(raw):08x}) SHA1({hashlib.sha1(raw).hexdigest()})'
    before=original.read_text();after=driver.read_text()
    assert before.count(old)==1 and after==before.replace(old,new) and sha(payload)==proof['payloadSHA256']
    pins=dict(proof['inputHashes'])
    for p in (driver,original,payload,proof_path,Path(__file__),ROOT/'tools/verify_mileena_fixed_runtime_v3829.py',ROOT/'audit_v3827_mileena_kano_p1_fixed/stderr.log'):
        pins[str(p.resolve())]=sha(p)
    for p,h in pins.items():assert sha(p)==h
    assert 'mk2ks.mdata WRONG CHECKSUMS:'in(ROOT/'audit_v3827_mileena_kano_p1_fixed/stderr.log').read_text()
    OUT.mkdir();assert subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0
    value=dict(passed=True,stagedSource=proof['stagedSource'],stagedSourceSHA256=proof['stagedSourceSHA256'],nativeDriverSource=str(driver),nativeDriverSourceSHA256=sha(driver),payloadSHA256=sha(payload),expectedGuestSHA256=proof['expectedGuestSHA256'],requiresCompilationAndNativeRuntimeRegression=True,driverOnlyChecksumDeclarationChanged=True,prior3822StrictRuntimeGateAccepted=False,preservedFailure='3829 rejected actual3822 mk2ks.mdata WRONG CHECKSUMS; no gate relaxation. Native trace evidence retained but not qualified/promoted.',runtimeAcceptance=False,artAcceptance=False,fullPortAcceptance=False,inputHashes=pins)
    (OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n');print(json.dumps({k:value[k]for k in ('passed','nativeDriverSourceSHA256','prior3822StrictRuntimeGateAccepted')}))
if __name__=='__main__':main()

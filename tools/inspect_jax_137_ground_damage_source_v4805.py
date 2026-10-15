"""Original action137 ground-target gate and actual sparse P1/Jax observations.

Source instructions, not sparse samples, establish the ground/velocity test.
No causal attribution from30-field LIVE snapshots, runtime jump success,
complete Jax choreography, campaign clear or finished port is inferred.
"""
import hashlib,json,re,struct,subprocess
from pathlib import Path
import run_sonya_p1_kitana_guard_ram_v4794 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4806_jax_137_ground_damage_source'
FOLDER=ROOT/'audit_v4797_sonya_p1_kitana_guard_ram'

CHECKS={
 0xff86dd90:(0x09c1,0x0137),
 0xff86ddb0:(0x0d3f,0x09dd),
 0xff86dff0:(0x0d5f,0x7bf0,0xff83),
 0xff86e020:(0xc80f,),
 0xff86e030:(0x0d5f,0xd630,0xff83),
 0xff86e060:(0xc80b,),
 0xff86e070:(0x09c0,0x0015),
 0xff86e090:(0x0d5f,0xa7a0,0xff83),
 0xff86e0c0:(0x09e7,0x8ab0,0xff8d),
 0xff86e0f0:(0x0d5f,0x2710,0xff84),
 0xff837bf0:(0xb7a0,0x0140),
 0xff837c10:(0xb7a1,0x0170),
 0xff837c30:(0xb421,0x0200),
 0xff837c50:(0xb603,0x0060),
 0xff837c70:(0xcb06,),
 0xff837c80:(0xb402,0x00b0),
 0xff837ca0:(0x4841,),
 0xff837cb0:(0xcb02,),
 0xff837cc0:(0x0320,0x0960),
 0xff837ce0:(0x0de0,0x0960),
 0xff83d630:(0xb7ae,0x0140),
 0xff83d650:(0xb5ce,0x01f0),
 0xff83d670:(0x0b4e,0xfff2),
 0xff83d690:(0xca05,),
 0xff83d6a0:(0x0b4e,0xfff3),
 0xff83d6c0:(0xca02,),
 0xff83d6d0:(0x0320,0x0960),
 0xff83d6f0:(0x0de0,0x0960),
 0xff83a7a0:(0x098f,0x00a0,0x4c0a,0xb7a8,0x0140,0x5610,0x0d5f,0x7340,0xff83),
}

def qualify(guest,stock):
    for address,words in CHECKS.items():
        offset=(address-0xff800000)//8
        expected=struct.pack('<'+'H'*len(words),*words)
        need(guest[offset:offset+len(expected)]==stock[offset:offset+len(expected)]==expected,
             'Unchanged actual initialized native instruction at '+hex(address))
    for address,opcode,target in ((0xff86e020,0xc80f,0xff86e120),(0xff86e060,0xc80b,0xff86e120),
                                   (0xff837c70,0xcb06,0xff837ce0),(0xff837cb0,0xcb02,0xff837ce0),
                                   (0xff83d690,0xca05,0xff83d6f0),(0xff83d6c0,0xca02,0xff83d6f0)):
        need(address+16+(opcode&255)*16==target,'Actual short conditional branch target')
    # Helper sets Carry for moving or non-floor targets; caller skips damage
    # when Carry is set. Boss-ID12/13 helper also sets Carry; Block is not read.
    return dict(nativeAction=0x137,nativeActionEntry='FF86DD90',nativeGroundHelper='FF837BF0',
        damageSkippedForVerticalVelocityNonzero=True,damageSkippedForYNotEqualActualTargetMainFloor=True,
        damageSkippedForTargetBossID12Or13=True,noBlockInputOrBodyGuardTestInThisGate=True,
        originalDamageOperand=21,originalTargetActorSwapDamageCall='FF83A7A0',
        originalVictimTask='FF8D8AB0',nativeCodeChanged=False)

def main():
    need(not OUT.exists(),'Fresh read-only source diagnosis')
    guest=capture.previous.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    proof=json.loads((FOLDER/'guest_memory_proof.json').read_text())
    need(proof['everyActualByteComparedInRAM'] and proof['bytes']==len(guest)==1048576 and
         proof['sha256']==hashlib.sha256(guest).hexdigest().upper() and proof['guestDumpFilesWritten']==0,
         'Whole actual initialized current guest independently reconstructed and compared in RAM')
    positive=qualify(guest,stock);faults=[]
    for address,label in ((0xff86dd90,'wrong_action_operand'),(0xff86dff0,'wrong_ground_helper'),
                           (0xff86e020,'lost_air_skip'),(0xff86e070,'changed_damage_operand'),
                           (0xff837c50,'wrong_target_vertical_velocity'),(0xff837c30,'wrong_target_floor'),
                           (0xff837cb0,'lost_floor_skip'),(0xff83d670,'wrong_boss_immunity'),
                           (0xff83a7a0,'wrong_native_target_actor_swap')):
        bad=bytearray(guest);bad[(address-0xff800000)//8]^=1
        try:qualify(bad,stock)
        except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Real original instruction corruption admitted '+label)
        need(qualify(guest,stock)==positive,'Actual entire original instruction positive restored')
    # Fixed window from the live file; metadata-only evidence, no live-file hash pin.
    with (FOLDER/'run.log').open('rb') as stream:prefix=stream.read(48*1024*1024)
    prefix=prefix[:prefix.rfind(b'\n')+1];rows=[]
    for line in prefix.decode().splitlines():
        if not line.startswith(('MK2_NAT_CAMPAIGN_LIVE ','MK2_NAT_CAMPAIGN_HEALTH ')):continue
        f=dict(re.findall(r'(\w+)=([^\s]+)',line))
        if 52705<=int(f['frame'])<=52860:rows.append(line)
    lives=[r for r in rows if r.startswith('MK2_NAT_CAMPAIGN_LIVE ')]
    need(lives and all(' human=18:18 cpu=11:11 ' in r and 'human_slot=1' in r
         and 'writes=0 assistance=none' in r for r in lives),
         'Actual true P1 Sonya and scheduled Jax11, not proxy or assigned AI/health')
    paths=[Path(__file__).resolve(),Path(capture.__file__).resolve(),Path(capture.previous.__file__).resolve(),
           FOLDER/'guest_memory_proof.json',FOLDER/'process.json',FOLDER/'input_hashes_before.json',
           ROOT/'audit_v4802_sonya_p1_kitana_progress/progress.json',ROOT/'mk2/mk2-maincpu.bin',
           ROOT/'mame-mkp/src/devices/cpu/tms34010/34010dsm.cpp',ROOT/'mame-mkp/unidasm.exe']
    pins={str(p.resolve()):sha(p) for p in paths}
    result=dict(passed=True,sourceGate=positive,actualInstructionFaultsRejected=faults,
        actualSparseFirstJaxWindow=rows,nativePrefixReadBytes=len(prefix),
        nativePrefixSHA256=hashlib.sha256(prefix).hexdigest().upper(),inputHashes=pins,
        sourceInstructionBoundaryOnly=True,sparseSamplesNotAttackCausality=True,
        actualNativeJaxGroundGateCallbackObserved=False,actualNativeJumpEvadedDamageAccepted=False,
        physicalControlExperimentNeeded='Observe genuine Jax137 entry/floor Carry/damage and Sonya jump handlers while trying ordinary Up edges; keep all native AI/health/identity/RNG/schedule untouched.',
        nativeAndPublicBuildChanged=False,newBuilds=0,rawMediaFilesWritten=0,
        naturalTowerClearAccepted=False,fullPortAcceptance=False,scope=__doc__)
    need(all(sha(p)==h for p,h in pins.items()),'Every immutable source/proof byte unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('inputHashes','actualSparseFirstJaxWindow')},indent=2),flush=True)

if __name__=='__main__':main()

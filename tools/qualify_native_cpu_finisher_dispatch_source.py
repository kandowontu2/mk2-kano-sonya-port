"""Only two initialized nineteen-ID finisher tables and their original operands."""
import hashlib,json,struct,subprocess
from pathlib import Path
import native_ai_response_context as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
STAGE=ROOT/'source_native_cpu_finisher_dispatch'
OUT=ROOT/'audit_native_cpu_finisher_dispatch_source'
TABLES=((0xff8ba210,0xf4320,0xff876b50),(0xff8ba390,0xf436c,0xff876b90))
OWN=(0xff800000+0xf55c0*8,0xff800000+0xf5640*8)
def off(bit):return (bit-0xff800000)//8
def address(byte):return 0xff800000+byte*8
def expected_guest(base=None):
    if base is None:base=prior.expected()
    guest=bytearray(base)
    for source,destination,operand in TABLES:
        need(base[destination:destination+76]==b'\xff'*76,'Entire independent table allocation erased')
        need(struct.unpack_from('<I',base,off(operand))[0]==source,'Exact original native operand')
        guest[destination:destination+68]=base[off(source):off(source)+68]
        struct.pack_into('<2I',guest,destination+68,*OWN)
        struct.pack_into('<I',guest,off(operand),address(destination))
    return bytes(guest)
def source_check():
    names=('midtunit_m.cpp','midtunit.h','midtunit.cpp')
    old={n:(ROOT/'source_native_ai_response'/n).read_text()for n in names}
    staged={n:(STAGE/n).read_text()for n in names}
    marker='\n\n\t// The two shared finisher performer tables have only twelve playable rows.\n'
    start=staged['midtunit_m.cpp'].index(marker)
    end=staged['midtunit_m.cpp'].index('\n}\n\n\nvoid midtunit_state::init_mk2ks_native_selector()',start)
    need(staged['midtunit_m.cpp'][:start]+staged['midtunit_m.cpp'][end:]==old['midtunit_m.cpp'],
         'Whole source delta only initialized finisher data/operands; native gameplay/host/graphics untouched')
    need(all(staged[n]==old[n]for n in names[1:]),'Machine and host audio declarations unchanged')
    addition=staged['midtunit_m.cpp'][start:end]
    for required in ('{0xf4320,0xf436c}','{0xff8ba210,0xff8ba390}','{0xff876b50,0xff876b90}',
        '17*4,rom+table','table+17*4,native_address(kano_finish_action)',
        'table+18*4,native_address(sonya_finish_action)'):
        need(required in addition,'Staged source implements exact independent data correction '+required)
    return {n:sha(STAGE/n)for n in names}
def gate(guest,base):
    need(guest==expected_guest(base),'Entire one-MiB image equals exact two table extensions only')
    for source,destination,operand in TABLES:
        need(guest[destination:destination+68]==base[off(source):off(source)+68],
             'Every original effective0..16 result preserved byte for byte')
        need(struct.unpack_from('<2I',guest,destination+68)==OWN,'Real17/18 select only own existing finisher actions')
    return True
if __name__=='__main__':
    need(not OUT.exists(),'Fresh source-only proof')
    cause=ROOT/'audit_native_cpu_finisher_dispatch_cause_checked/report.json'
    diagnostic=json.loads(cause.read_text())
    need(diagnostic['passed'] and diagnostic['actualFirstCorruptingFrame']==36314 and
         all(sha(p)==h for p,h in diagnostic['inputHashes'].items()),'Entire actual causal replay and sources frozen')
    base=prior.expected();guest=expected_guest(base);sources=source_check();gate(guest,base)
    faults=[]
    for name,at in (
        ('existing_stock_row',TABLES[0][1]),('Kano_proxy_action',TABLES[0][1]+68),
        ('Sonya_proxy_action',TABLES[0][1]+72),('second_Kano_action',TABLES[1][1]+68),
        ('second_Sonya_action',TABLES[1][1]+72),('first_lookup_operand',off(TABLES[0][2])),
        ('second_lookup_operand',off(TABLES[1][2])),('native_ID_lookup',off(0xff83b7f0)),
        ('native_cache_loop',off(0xff838850)),('native_collision',off(0xff836700)),
        ('own_Kano_choreography',0xf55c0),('own_Sonya_choreography',0xf5640)):
        altered=bytearray(guest);altered[at]^=1
        try:gate(altered,base)
        except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
        else:raise ValueError('Source/guest counterexample admitted '+name)
    need(gate(guest,base),'Whole positive restored after twelve faults')
    allowed=set(range(0xf4320,0xf43b8))|set(range(off(0xff876b50),off(0xff876b50)+4))|set(range(off(0xff876b90),off(0xff876b90)+4))
    changed={i for i,(a,b)in enumerate(zip(base,guest))if a!=b}
    need(changed<=allowed and changed,'Every changed byte belongs only to reviewed tables/immediates')
    pins={str(p.resolve()):sha(p)for p in [cause,Path(__file__),*(STAGE/n for n in sources)]}
    report=dict(passed=True,sourceOnlyAccepted=True,compiledFixAccepted=False,nativeRepairAccepted=False,
        proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),initializedGuestByteDelta=len(changed),
        stagedSourceHashes=sources,ownNativeFinishActions=[f'{a:08X}'for a in OWN],
        tables=[dict(original=f'{s:08X}',destination=f'{address(d):08X}',operand=f'{o:08X}')for s,d,o in TABLES],
        allOriginalEffectiveRowsPreserved=True,nativeIDsCacheLoopChoreographyUnchanged=True,
        existingOwnedFinisherActionsOnly=True,noNewSecondFinisherChoreographyClaim=True,
        actualFaultsRejected=faults,inputHashes=pins,goalStatus='active',fullPortAcceptance=False,
        publicBuildPromoted=False,newBuilds=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    for p in [OUT/'report.json',*(STAGE/n for n in sources)]:
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
    print(json.dumps({k:v for k,v in report.items()if k not in('actualFaultsRejected','inputHashes')},indent=2))

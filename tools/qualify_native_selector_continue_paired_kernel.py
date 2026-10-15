"""Same retained P2 run: source-bound Kano paired origin and exact kernel ID.

Preserve original rejected reports. No game replay, controller change, health
write, or waiver for unknown ownership. The fourth distinct physical route
uses kernel creation time rather than a millisecond-rounded CIM timestamp.
"""
import hashlib,json,re
from pathlib import Path
from types import FunctionType,SimpleNamespace
import capture_native_kano_laser_cross_continue as prior
import qualify_native_kano_laser_cross_continue_retained as paired
import native_process_census_v6647 as kernel

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_selector_continue_paired_kernel_source'


def clone(fn,**changes):
    return FunctionType(fn.__code__,dict(fn.__globals__,**changes),fn.__name__,fn.__defaults__,fn.__closure__)


def prepare(state,cases):
    need(not OUT.exists()and not kernel.census(),'Fresh strict analysis; all original native games terminal')
    old=state['contract'];folder,text,images,report=cases['kano_p2_to_sonya']
    need(report['passed']is False and report['nativeExit']==0 and
         all(sha(p)==h for p,h in report['inputHashes'].items()),'Immutable actual original rejected run and source hashes')
    fields={(r['frame'],r['slot']):r for r in old.rows(text,'FIELD')}
    end=int(old.rows(text,'RESULT')[0]['secondKO'])
    added=[]
    for q in old.rows(text,'HEALTH'):
        if q['slot']!='2'or q['pc']!='FF836700'or q['mode']!='2'or int(q['frame'])>end or int(q['before'])<=int(q['after']):continue
        enemy=fields[q['frame'],'1'];victim=fields[q['frame'],'2']
        if old.base_gate.__globals__['origin'](q,enemy):continue
        need(paired.origin(q,enemy)and victim['action']==str(paired.spec.SPECS['kano']['victim_state'])and
             (q['actor'],q['main'],q['id'])==(victim['actor'],victim['main'],victim['id'])and
             int(q['before'])-int(q['after'])==8 and q['after']==victim['hp']and
             q['writes']=='0'and q['assistance']=='none','Actual eight-point paired CPU Kano pulse on owned human victim')
        added.append(q)
    need(len(added)==4,'Exactly four actual initial-loss paired choke pulses, not unrelated post-continue damage')
    guest=state['guest'];original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();at=(0xff836700-48-0xff800000)//8
    need(guest[at:at+6]==original[at:at+6]and hashlib.sha256(guest).hexdigest().upper()==report['guestSHA256'],
         'Actual whole guest and unchanged native health-store instruction')
    base=clone(old.base_gate,origin=paired.origin)
    flow=clone(old._gate,base_gate=base)
    gate=clone(old.gate,_gate=flow)
    positive=gate(text,'kano',2,'sonya');faults=[];q=added[0];enemy=fields[q['frame'],'1']
    for tag,row,key,value in [('HEALTH',q,'ctxOwner','00000000'),('HEALTH',q,'parent',enemy['actor']),
        ('HEALTH',q,'ctxID','18'),('HEALTH',q,'pairActor',q['actor']),('HEALTH',q,'pairMain',q['main']),
        ('HEALTH',q,'pairAction','272'),('HEALTH',q,'caller','FF835D70'),('FIELD',enemy,'action','0'),
        ('FIELD',enemy,'id','18'),('FIELD',enemy,'owner','00000000')]:
        line=next(s for s in text.splitlines()if s.startswith('MK2_SC_'+tag+' ')and dict(re.findall(r'(\w+)=([^\s]+)',s))==row)
        changed=re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(changed!=line,'Effective actual ownership fault')
        try:gate(text.replace(line,changed,1),'kano',2,'sonya')
        except(ValueError,AssertionError)as error:faults.append(dict(tag=tag,field=key,rejectedBy=str(error)))
        else:raise ValueError('False current CPU ownership admitted: '+key)
    need(gate(text,'kano',2,'sonya')==positive,'Whole original positive restored')
    for fighter in ('kano','sonya'):
        target='sonya'if fighter=='kano'else'kano';prior_text=cases[f'{fighter}_p1_to_{target}'][1]
        need(gate(prior_text,fighter,1,target)==old.gate(prior_text,fighter,1,target),'Both previously accepted P1 whole positives unchanged')
    deps=[*old.DEPENDENCIES,Path(__file__),Path(paired.__file__),Path(paired.origins.__file__),Path(paired.spec.__file__),Path(kernel.__file__)]
    OUT.mkdir();proof=dict(passed=True,sourceOnlyAccepted=True,actualAddedPairedKanoHealthStores=added,
        actualAdditionalOwnershipFaultsRejected=faults,wholeOriginalP1PositivesUnchanged=True,
        originalFailurePreserved=True,inputHashes={str(p.resolve()):sha(p)for p in (*deps,folder/'report.json',ROOT/'mk2/mk2-maincpu.bin')},
        newNativeBoots=0,newBuilds=0,newROMCopies=0,newRawMedia=0,fullPortAcceptance=False)
    (OUT/'report.json').write_text(json.dumps(proof,indent=2)+'\n')
    deps.append(OUT/'report.json')
    new=SimpleNamespace(**(vars(old)|dict(gate=gate,base_gate=base,_gate=flow,DEPENDENCIES=deps)))
    state['contract']=new
    state['capture']=clone(state['capture'],contract=new,gate=gate,DEPENDENCIES=deps,census=kernel.census)
    for name in ('qualify','pixel_check','control_check'):state[name]=clone(state[name],contract=new)
    print(json.dumps(dict(passed=True,addedPairedPulses=len(added),actualOwnershipFaults=len(faults),nativeReplay=False)),flush=True)
    return proof


def recover(state,cases,handles,expected):
    key='kano_p2_to_sonya';folder,text,images,old=cases[key];held=handles[key]
    out=ROOT/'audit_native_selector_continue_kano_p2_to_sonya_kernel_birth_recovery'
    identity=json.loads((out/'identity_recovery.json').read_text());terminal=json.loads((out/'native_terminal.json').read_text())
    need(identity['passed']and identity['originalCaptureSHA256']==sha(folder/'report.json')and
         identity['originalTerminalSHA256']==sha(folder/'native_terminal.json')and held['process'].poll()==0 and
         held['process'].pid==identity['originalNativeKernelIdentity']['ProcessId']and not kernel.census()and
         not(out/'report.json').exists()and terminal['exitCode']==0 and not terminal['observationErrors']and
         old['actualGuestGFXProofs']==expected,'Same original retained native terminal and exact kernel identity recovery')
    source=prior.original.source;first=source.index('  result=gate(text,fighter,side,target);');last=source.index('\n except Exception as e:r.update',first)
    body=source[first:last]
    body=prior.replace(body,'except(ValueError,AssertionError,KeyError)as e:','except(ValueError,AssertionError)as e:')
    validate='def validate_original(text,images,r,out,fighter,side,target,pins):\n'+''.join('    '+line[2:]+'\n'for line in body.splitlines())+'    return r\n'
    scope=dict(state['capture'].__globals__)
    exec(compile(validate,__file__+'::whole_original_capture_positive_and_six_faults','exec'),scope)
    recovered=dict(old,nativeIdentity=identity['originalNativeKernelIdentity'],inputHashes=dict(old['inputHashes']),
        originalRejectedCapturePreserved=True,originalRejectedCaptureSHA256=sha(folder/'report.json'),
        actualKernelIdentityRecoverySHA256=sha(out/'identity_recovery.json'))
    for p in (*state['contract'].DEPENDENCIES,out/'identity_recovery.json',out/'native_terminal.json',folder/'report.json',
              folder/'process.json',folder/'live_census.json',folder/'native_terminal.json',folder/'run.log.gz'):
        recovered['inputHashes'][str(p.resolve())]=sha(p)
    scope['validate_original'](text,images,recovered,out,'kano',2,'sonya',recovered['inputHashes'])
    need(recovered['passed']and len(recovered['actualFaultsRejected'])==6 and old['passed']is False,'All original capture gates; failure untouched')
    (out/'report.json').write_text(json.dumps(recovered,indent=2)+'\n')
    held['recoveredIdentity']=recovered['nativeIdentity']
    qualified=state['qualify'](out,text,images,recovered,'kano',2,'sonya')
    pixels=state['pixel_check'](out,text,images,'kano',2,'sonya')
    controls=state['control_check'](out,text,'kano',2,'sonya')
    state['COMPLETED'].append(key)
    print(json.dumps(dict(passed=True,key=key,originalNativeReplayed=False,originalCaptureStillFalse=True,
        stateRasterFaults=len(qualified['actualFaultsRejected']),controlFaults=len(controls['actualControlFaultsRejected']),
        extraPixelFaults=len(pixels['additionalActualImageFaultsRejected']),fullPortAcceptance=False)),flush=True)
    return dict(folder=out,text=text,images=images,report=recovered,qualified=qualified,pixels=pixels,controls=controls)

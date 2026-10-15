"""Six genuine current stock controls: Kitana, LiuKang and Jax in both slots.

Retain entire original stock earned/state/table/panel gate, parameterizing
actual stock ID and its independently stock-qualified row. These six-panel
controls do not prove whole stock scenes or universally accept own placement.
"""
import copy,inspect,json,re,struct
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_jax_arms_stock_corner_v4098 as prior
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6157_current_jax_arms_stock_profiles_checked'

def make_gate():
 source=inspect.getsource(prior.gate)
 def replace(before,after,count=1):
  nonlocal source
  need(source.count(before)==count,'Exact actual stock identity/profile adaptation '+before)
  source=source.replace(before,after)
 replace('def gate(text,frames,image,guest,side):','def gate(text,frames,image,guest,side,identity):')
 replace("live[0]['ids']=='11,4'","live[0]['ids']==f'11,{identity}'")
 replace("'000AFF88'",'f\'{struct.unpack_from("<I",guest,0xfba50+identity*4)[0]:08X}\'',2)
 replace("=='4'","==str(identity)",4)
 replace('guest,at+4*4','guest,at+identity*4')
 replace('dict(identity=4,side=side','dict(identity=identity,side=side')
 scope=dict(vars(prior),__file__=__file__)
 exec(compile(source,__file__+'::whole_original_stock_gate_true_ID_profile','exec'),scope)
 return scope['gate']

def run():
 guest=current.expected();prior.grammar.source_contract(guest);gate=make_gate()
 pins={str(Path(__file__).resolve()):sha(__file__),str(Path(prior.__file__).resolve()):sha(prior.__file__)}
 cases=[]
 for fighter,identity in(('kitana',4),('liu_kang',1),('jax',11)):
  for side in(1,2):
   leaf={'kitana':6147,'liu_kang':6154,'jax':6161}[fighter]
   reportleaf={'kitana':6148,'liu_kang':6155,'jax':6162}[fighter]
   folder=ROOT/f'audit_v{leaf}_current_jax_arms_stock_{fighter}_p{side}_corner_ram'
   rp=ROOT/f'audit_v{reportleaf}_current_jax_arms_stock_{fighter}_p{side}_corner_observed/report.json'
   observed=json.loads(rp.read_text());meta=json.loads((folder/'result.json').read_text());terminal=json.loads((folder/'native_terminal.json').read_text())
   need(observed['passed']and observed['stockReferenceOnly']and observed['actualIdentity']==meta['actualIdentity']==identity and
        observed['fighter']==meta['fighter']==fighter and meta['candidate']==current.NAME and meta['guestSHA256']==current.GUEST_SHA and
        meta['exit_code']==terminal['nativeExit']==0 and meta['guestWrites']==0 and meta['assistance']=='none'and
        meta['actualNativeRGBFrames']==6,'Real current stock native terminal/guest/identity; never a proxy own context')
   process=json.loads((folder/'process.json').read_text());wi=terminal['actualWindowsIdentity']
   need(process['actualWindowsIdentity']==wi and process['pid']==terminal['pid']==wi['ProcessId']and wi['CreationDate']and
        wi['Name']=='mkport_candidate.exe'and Path(wi['ExecutablePath']).resolve()==(ROOT/current.NAME/'mkport_candidate.exe').resolve()and
        str(folder)in wi['CommandLine'],'Actual Windows stock creation/executable/full-command native terminal')
   before=json.loads((folder/'input_hashes_before.json').read_text())
   need(all(meta['inputHashes'][p]==h for p,h in before.items()),'Full actual stock preboot ledger retained')
   for p,h in observed['inputHashes'].items():need(sha(p)==h,'Executed stock inputs/panels unchanged');pins[p]=h
   text=(folder/'run.log').read_text();image=Path(observed['essentialNativeReview']);frames=observed['frames']
   need((folder/'stderr.log').read_text()==''and not list(folder.glob('*.bin'))and not list(folder.glob('*.wav'))and
        not(folder/'input_sources').exists(),'No native fault, raw media or source-directory copies')
   positive=gate(text,frames,image,guest,side,identity);faults=[]
   for tag,key,value,prefix in(('FIRST_LIVE','ids','11,17','MK2_STOCK_HEAD_V921_'),('ACTION','variant','1','MK2_STOCK_HEAD_V921_'),
    ('WRAP','age','146','MK2_STOCK_HEAD_V921_'),('TABLE_RETURN','value','00000000','MK2_STOCK_HEAD_V921_'),
    ('STATE','id','17','MK2_ARM_STOCK_'),('STATE','roster','17','MK2_ARM_STOCK_')):
    line=next(l for l in text.splitlines()if l.startswith(prefix+tag+' '))
    changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and changed!=line,'Non-vacuous actual stock fault')
    try:gate(text.replace(line,changed,1),frames,image,guest,side,identity)
    except(ValueError,KeyError,AssertionError):faults.append(tag+':'+key)
    else:raise ValueError('Actual stock state fault accepted '+key)
   changed=copy.deepcopy(frames);changed[0]['rgbSHA256']='0'*64
   try:gate(text,changed,image,guest,side,identity)
   except(ValueError,KeyError,AssertionError):faults.append('actual_native_panel_digest')
   else:raise ValueError('Actual stock panel corruption accepted')
   need(gate(text,frames,image,guest,side,identity)==positive,'Whole actual stock positive restored')
   pins[str(rp)]=sha(rp)
   cases.append(dict(fighter=fighter,side=side,actualStock=positive,actualSemanticFaultsRejected=faults,
                     actualWindowsTerminal=terminal,essentialNativeReview=str(image)))
 need(all(sha(p)==h for p,h in pins.items()),'Every real executed stock/panel/source file unchanged')
 return dict(passed=True,candidate=current.NAME,actualStockContexts=6,actualAddedCharacterContexts=0,
     actualNativePanels=36,actualNativePanelPixels=3657600,actualSemanticFaultsRejected=42,cases=cases,inputHashes=pins,
     currentNativeStockPositionProfilesAndHeldPageObserved=True,ownCornerArtPositionAccepted=False,
     fullStockSceneReplayAccepted=False,allStockFinisherFidelityAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh six-stock native profile matrix')
 try:report=run()
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)

"""Whole original3747 Kano P2 campaign and fault grammar on actual current3836.

Change build provenance and one initialized guest-file read to RAM-only proof.
Original full campaign/selection/morph/special/health/KO/paid-continue/boss input/
ending/attract contracts remain. No ending-art/full-audio/full-port promotion.
"""
import hashlib,inspect,json,re,subprocess,traceback
from pathlib import Path
import verify_guarded_p2_campaign_v3747 as original
import verify_sonya_zoning700_campaign_v4015 as ram
import run_kano_current_p2_campaign_ram_v4484 as capture
import qualify_kano_current_p2_campaign_source_v4482 as boundary
ROOT,need,sha,NAME=capture.ROOT,capture.need,capture.sha,capture.NAME
FOLDER=capture.FOLDER
OUT=ROOT/'audit_v4488_kano_current_p2_whole_campaign_checked'

def clone(function,changes,scope):
    text=inspect.getsource(function)
    for before,after in changes:
        need(text.count(before)==1,'Unique complete original algorithm adaptation: '+before)
        text=text.replace(before,after,1)
    exec(compile(text,__file__+'::entire_'+function.__name__,'exec'),scope)
    return scope[function.__name__]

matched=clone(ram.matched,
    [('transport_boundary()','boundary.source_boundary()'),
     ("meta['player']=='sonya'and meta['strategy']=='zoning'and meta['boot_frame']==700",
      "meta['player']=='kano'and meta['strategy']=='zoning'and meta['boot_frame']==600")],
    dict(vars(ram),__file__=__file__,NAME=NAME,capture=capture,boundary=boundary))
ram_guest=clone(ram.ram_guest,
    [('mk2ks_guarded_campaign_guest_ram_v4006.lua',capture.LUA)],
    dict(vars(ram),__file__=__file__,capture=capture))

def expected_current():
    previous=ram.data.old.expected_current()
    payload=(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    guest,_=ram.data.check(previous[2],(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),payload,previous[0],
                          json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))
    need(hashlib.sha256(guest).hexdigest().upper()=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821',
         'Exact independently reconstructed whole current initialized guest')
    return (guest,previous[1],payload,previous[3],previous[4])

def ram_guest_checked(folder,pins,wanted,text,errors):
    try:return ram_guest(folder,pins,wanted,text)
    except ValueError as error:
        errors.append(str(error));return wanted

def make_native(expected):
    factory=inspect.getsource(original.knife.make_verifier)
    before='    namespace=dict(vars(old));namespace.update'
    need(factory.count(before)==1,'Whole original Kano native factory and explicit boss input replay')
    factory=factory.replace(before,'    source=ram.adapt_guest_transport(source)\n'+before,1)
    scope=dict(vars(original.knife),ram=ram)
    exec(compile(factory,__file__+'::entire_knife_factory_RAM_guest_read_only','exec'),scope)
    native=scope['make_verifier'](expected)
    native.__globals__.update(NAME=NAME,matched=matched,ram_guest_checked=ram_guest_checked)
    return native

verify_original=clone(original.verify,
    [("folder=ROOT/f'audit_v3745_guarded_{fighter}_natural_p2_campaign'","folder=FOLDER"),
     ('expected=knife.current.expected_current()','expected=expected_current()'),
     ('native=policy.make_verifier(expected)','native=make_native(expected)'),
     ('actual3680P2WholeCampaignAlgorithmRetained','actual3836P2WholeCampaignAlgorithmRetained')],
    dict(vars(original),__file__=__file__,capture=capture,NAME=NAME,FOLDER=FOLDER,
         expected_current=expected_current,make_native=make_native,matched=matched))

def main():
    need(not OUT.exists() and (FOLDER/'result.json').is_file(),'Terminal actual cold capture; unused whole proof leaf')
    observation=json.loads((capture.OUT/'report.json').read_text())
    need(observation['passed'] and observation['capture']==str(FOLDER),'Actual terminal current capture observation')
    positive=verify_original('kano')
    text=(FOLDER/'run.log').read_text();guest=expected_current()[0]
    proof=json.loads((FOLDER/'guest_memory_proof.json').read_text())
    native=make_native(expected_current());base=native(FOLDER)
    need(base['passed'],'Whole original native campaign positive after fault loop')
    faults=[]
    for key,value in (('sha256','0'*64),('bytes',1048575),('everyActualByteComparedInRAM',False),
                      ('captureSourceSHA256','0'*64),('transportSourceSHA256','0'*64),('guestDumpFilesWritten',1)):
        bad=dict(proof);bad[key]=value
        try:ram_guest(FOLDER,{},guest,text,proof_override=bad)
        except ValueError as error:faults.append(dict(key=key,rejectedBy=str(error)))
        else:raise ValueError('Altered actual RAM guest proof accepted '+key)
        need(ram_guest(FOLDER,{},guest,text)==guest,'Exact actual whole guest proof restored')
    header=next(s for s in text.splitlines() if s.startswith('MK2_CAMPAIGN_GUEST_RAM_DIGEST '))
    for label,damaged in (('missing_guest_digest',text.replace(header+'\n','',1)),
                          ('wrong_guest_digest',text.replace(header,header.replace(proof['sha256'],'0'*64),1))):
        result=native(FOLDER,text_override=damaged)
        need(not result['passed'] and any('Exactly one actual digest' in e for e in result['errors']),
             'Same whole original algorithm rejects actual RAM digest fault')
        need(native(FOLDER)==base,'Same full positive restored after every actual RAM fault')
        faults.append(dict(key=label,rejectedBy='Exactly one actual digest'))
    rows=original.knife.old.parse(text,2,'kano')
    deadline=re.findall(r'^MK2_CAMPAIGN_HOST_DEADLINE seconds=([\d.]+) limit=(\d+) assistance=none writes=0$',text,re.M)
    if deadline:
        need(len(deadline)==1 and deadline[0][1]=='5900' and 5900<=float(deadline[0][0])<5900.03,
             'Actual finite host deadline, never a victory marker')
    else:need(positive['unassisted_clear_proven'],'Without host deadline require actual native clear/own ending exit')
    cache=[r for r in text.splitlines() if r.startswith('MK2_MILEENA_CAMPAIGN_RESULT ')]
    need(len(cache)==1 and 'global_cache_stores=0' in cache[0] and
         not any(s.startswith('MK2_MILEENA_CAMPAIGN_OVERRUN ') for s in text.splitlines()),
         'No actual native victim cache overrun through terminal campaign')
    pins=positive['inputHashes']
    for p in (Path(__file__).resolve(),capture.OUT/'report.json',boundary.OUT/'report.json'):
        pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every actual full campaign/source/fault proof byte unchanged')
    positive.update(actualWholeCampaignGrammarRetained=True,actualRAMGuestFaultsRejected=faults,
                    actualNativeInitializedGuestBytesComparedInRAM=1048576,actualGuestDumpFilesWritten=0,
                    originalPhysicalKanoInputsExactlyUnchanged=True,actualFiniteHostDeadlineReached=bool(deadline),
                    globalCacheOverruns=0,endingPixelsAccepted=False,completeCampaignAudioAccepted=False,
                    fullPortAcceptance=False)
    return dict(passed=True,case=positive,current3836KanoP2NaturalTowerOwnEndingAttractAccepted=positive['unassisted_clear_proven'],
                originalComplete3747AlgorithmRetained=True,endingPixelsAccepted=False,
                completeCampaignAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable current whole campaign result');OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
         'Proof compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='case'},indent=2),flush=True)
    if report['passed']:
        print(json.dumps({k:v for k,v in report['case'].items() if k not in ('inputHashes','uppercutAssignmentFrames')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)

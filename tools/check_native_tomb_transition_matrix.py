"""Bind four current opposite-victim Tomb/rejoin cases at their actual scope.

Initial one-base renderer and later source-defined native scanout stay separate.
Every original semantic fault suite, actual visual/RAM retirement, native birth
and frozen input are required. Not wider mirrors, Pit, campaign or port proof.
"""
import gzip
import hashlib
import inspect
import json
from pathlib import Path
import native_process_census_v6647 as census
import run_native_tomb_transition_scanout_checked as exact
import preserve_native_tomb_transition_trial as original_state

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_native_tomb_transition_matrix_checked'


def need(value,message):
    if not value:raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def read(path):
    return json.loads(path.read_text())


def state_gate(ids):
    if ids==[17,18]:return original_state.state_facts
    need(ids==[18,17],'Only actual opposite-character tuple')
    body=inspect.getsource(original_state.state_facts)
    for before,after in (("a[0]['ids']=='17,18'","a[0]['ids']=='18,17'"),
                         ('((1,17),(2,18))','((1,18),(2,17))'),
                         ('(17 if s==1 else 18)','(18 if s==1 else 17)'),
                         ('actualTruePhysicalIDs=[17,18]','actualTruePhysicalIDs=[18,17]')):
        need(body.count(before)==1,'Entire original state gate, only exact IDs change')
        body=body.replace(before,after,1)
    namespace=dict(vars(original_state))
    exec(compile(body,__file__+'::whole_original_reversed_native_state_gate','exec'),namespace)
    return namespace['state_facts']


def run():
    need(not OUT.exists() and not census.census(),'Fresh aggregate only after all real native terminals')
    scope_path=ROOT/'audit_native_paired_stumble_table_bounded_source/report.json'
    scope=read(scope_path)
    need(scope['passed'] and len(scope['originalNaturalIntegrationRequirements'])==14 and
         len(scope['originalRemainingWorkGroups'])==6,'Whole original objective intact')
    pins={}
    def bind(items):
        for p,h in items.items():
            need(sha(p)==h,'Actual unchanged native/source/proof '+p)
            need(p not in pins or pins[p]==h,'Consistent source hashes')
            pins[p]=h
    bind(scope['inputHashes'])
    cases=[]
    for fighter in ('kano','sonya'):
        for side in (1,2):
            folder=ROOT/f'audit_native_tomb_transition_scanout_{fighter}_p{side}_ram'
            output=ROOT/f'audit_native_tomb_transition_scanout_{fighter}_p{side}_checked'
            report_path=output/'report.json';retire_path=output/'native_effective_scanout_visual_review_and_ram_retirement.json'
            meta_path=folder/'result.json';identity_path=folder/'native_identity.json'
            base_path=output.parent/(output.name+'_original_scene_report.json')
            report,retired,meta,identity,base=map(read,(report_path,retire_path,meta_path,identity_path,base_path))
            own=17 if fighter=='kano'else 18;ids=[own if n==side else 35-own for n in (1,2)]
            need(report['passed'] and base['passed'] and retired['passed'] and
                 report['fighter']==meta['fighter']==fighter and report['side']==meta['side']==side and
                 report['candidate']==meta['candidate']=='diagnostic_native_paired_stumble_table_ps7' and
                 report['truePhysicalIDs']==meta['truePhysicalIDs']==ids and
                 meta['ramGuestSHA256']==scope['proposedGuestSHA256'] and
                 meta['executable_sha256']=='E56DD49DB8B918BC1DF806E3C70C34A557716116DCAADB2F683532DBACAFBD3D' and
                 meta['payload_sha256']=='A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3',
                 'Same current compiled whole guest/payload and true physical actors')
            process=read(folder/'process.json');command=process['command']
            need(meta['captureCompleted'] and meta['exit_code']==0 and not meta['modelErrors'] and
                 meta['guest_writes']==0 and meta['assistance']=='none' and not meta['cheats_enabled'] and
                 meta['input_hashes']==read(folder/'input_hashes_before.json') and
                 (folder/'stderr.log').read_text()=='' and identity==retired['exactTerminalNativeIdentity'] and
                 identity['ProcessId']==process['pid'] and identity['ParentProcessId']==process['hostPID'] and
                 identity['createdUnix']>0 and '-samples'in command and '-nocheat'in command and
                 command[command.index('-wavwrite')+1]=='NUL',
                 'Exact original native identity, normal terminal and no assistance')
            branch=report['nativeBranch'];earned=branch['earnedContract']
            need(report['actualCurrentOppositeNativeTombWholeRenderPaletteShadowEraseAccepted'] and
                 report['sampledFrames']==base['sampledFrames']==meta['observedRGBFields']==meta['modelExactFields']==537 and
                 report['exactRGBPixels']==537*101600 and report['oneInitialBaseOnly'] and
                 report['laterTargetsNeverUsedAsAnchors'] and len(report['sourcePreflight']['rejectedProxyTuples'])==5 and
                 len(report['actualPixelFaultsRejected'])==2 and len(report['actualEarnedFaultsRejected'])==12 and
                 len(report['actualOriginalBranchFaultsRejected'])==4 and earned['passed'] and
                 earned['earned_matches']==2 and earned['consecutive_fields']==801 and earned['native_action']=='FF8BDFE0' and
                 branch['passed'] and branch['trueVictim']==35-own,
                 'Whole original independent renderer, earned matches, native branch and actual faults')
            if (fighter,side)==('sonya',1):
                need(branch['nativeDrop'] and branch['actualNativeRandomValue']==20 and
                     len(report['actualDropPhaseFaultsRejected'])==4,'Actual original random drop case, all phase faults')
            else:need(not branch['nativeDrop'],'Actual unpressed held cases remain correctly limited')
            records_path=folder/'post_scene_records.json';states_path=folder/'post_state_records.json'
            records,states=map(read,(records_path,states_path))
            with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
            post=exact.verify_rejoin(text,records,states,ids)
            faults=exact.faults(text,records,states,ids)
            facts=state_gate(ids)(text,states)
            saved=report['laterNativeTransitionAndPhysicalRejoin']
            need(post=={k:v for k,v in saved.items()if k!='actualSemanticFaultsRejected'} and
                 faults==saved['actualSemanticFaultsRejected'] and len(faults)==12 and
                 facts==retired['actualNativeGameplayFacts'] and
                 len(retired['actualStateAndInputFaultsRejected'])==12 and
                 retired['actualVisibleTransitionAndPlayabilityReviewed'] and
                 retired['originalCaptureRAMDictionaryCleared'] and retired['reviewServerClosed'] and
                 retired['originalIndependentSceneFields']==537 and
                 retired['laterSourceDefinedNativeDisplayFields']==len(records) and
                 retired['laterSourceDefinedNativeRGBPixels']==len(records)*101600,
                 'Original complete later rejoin semantics, twelve faults, actual contact and reviewed RAM retirement')
            for s,r in zip(states,records,strict=True):
                t=r['timing'];effective=(t['dpyadr']+(t['vsblnk']-t['veblnk'])*(t['control']&0x03fc))&0xffff
                need(s=={k:r[k]for k in s} and r['passed'] and r['pixels']==101600 and
                     r['nativeDPYADRSourceDefinedAddressOnly'] and r['currentVRAMNeverSelectedAsPassingTarget'] and
                     r['effectiveNativeStart']==effective and r['queuedNativeStart']==s['start'] and
                     t['vcount']==t['vsblnk']-1 and t['vsblnk']-t['veblnk']==254 and
                     t['vtotal']>=t['vsblnk'] and t['control']==s['control'] and t['tap']==s['tap'] and
                     t['control']&0x03fc==16 and t['dpystart']&3==t['dpyadr']&3==0,
                     'Every consecutive actual later raster uses one source-defined completed scanout')
            ledger={r['frame']:r for r in read(folder/'continuous_scene_records.json')}
            need(len(ledger)==537,'All original independent scene fields still present')
            ledger.update({r['frame']:r for r in records})
            views=retired['individuallyReviewedFields']
            need(len(views)==retired['originalNativeRasterBuffersReleased'] and len(views)>=20 and
                 len({v['frame']for v in views})==len(views) and all(v['rgbSHA256']==ledger[v['frame']]['rgbSHA256'] and
                 (v['individuallyViewedNow']or v['exactSamePreviouslyViewedRaster'])for v in views),
                 'All actual held original rasters reviewed and bound to exact original RGB')
            need(not report['fullPortAcceptance'] and not report['allMirrorBranchesAndSlotsAccepted'] and
                 not saved['laterFullIndependentRendererModel'] and not retired['fullPortAcceptance'] and
                 not retired['allStageFinishersAccepted'] and not report['publicPlayableOrReleaseChanged'] and
                 report['rawImageAudioVRAMROMCopiesWritten']==meta['rawImageAudioVRAMROMCopiesWritten']==0 and
                 not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in folder.rglob('*')if p.is_file()),
                 'Finite actual opposite-victim transition scope, no broader claims or raw copies')
            for collection in (report['inputHashes'],report['extensionSourceHashes'],meta['input_hashes'],retired['inputHashes']):bind(collection)
            for p in(report_path,retire_path,meta_path,identity_path,base_path,records_path,states_path):bind({str(p):sha(p)})
            cases.append(dict(fighter=fighter,physicalSlot=side,truePhysicalIDs=ids,initialIndependentFields=537,
                              laterNativeScanoutFields=len(records),laterRGBPixels=len(records)*101600,
                              admitted=facts['admitted'],completed=facts['completed'],resumedFields=181,
                              individuallyReviewedRasters=len(views),nativeRandomDrop=branch['nativeDrop'],
                              actualHealthDecrements=facts['actualHealthDecrements']))
    for p in(Path(__file__).resolve(),Path(exact.__file__),Path(original_state.__file__),scope_path):bind({str(p):sha(p)})
    result=dict(passed=True,cases=cases,finiteBothCharactersBothSlotsOppositeVictimTombTransitionAccepted=True,
                originalIndependentFields=2148,originalIndependentRGBPixels=2148*101600,
                laterNativeScanoutFields=sum(c['laterNativeScanoutFields']for c in cases),
                laterSourceDefinedNativeRGBPixels=sum(c['laterRGBPixels']for c in cases),
                individuallyReviewedNativeRasters=sum(c['individuallyReviewedRasters']for c in cases),
                actualRejoinSemanticFaults=48,actualNativeStateInputHealthFaults=48,
                originalEarnedFaults=48,originalBranchFaults=16,originalDropPhaseFaults=4,
                originalProxyTupleFaults=20,originalPixelFaults=8,laterFullIndependentRendererAccepted=False,
                allStockVictimsAndMirrorsAccepted=False,allStageFinishersAccepted=False,fullPortAcceptance=False,
                originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
                originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],inputHashes=pins,
                newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    result=run()
    print(json.dumps({k:v for k,v in result.items()if k not in
        ('inputHashes','originalNaturalIntegrationRequirements','originalRemainingWorkGroups')},indent=2))

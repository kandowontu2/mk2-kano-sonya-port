"""Complete corrupting-run inventory and bounded original lookup evidence.

The stock lookup candidate is an inference, not an observed caller witness.
Do not patch or label the cause resolved until that native handoff is traced.
"""
import collections
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path
import run_native_sonya_liu_early_leg_campaign as capture
import seal_native_sonya_shang_cache_failure as preserved

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_sonya_shang_cache_failure_diagnosed'


def run():
    need(not OUT.exists() and not capture.core.base.census.census(), 'Fresh read-only diagnosis after exact native retirement')
    paths=[preserved.OUT/'report.json',preserved.RETIRED/'report.json',
           ROOT/'audit_native_liu_early_leg_earned_clear_checked/report.json']
    saved,retired,liu=[json.loads(p.read_text()) for p in paths]
    need(saved['preservationPassed'] and not saved['passed'] and saved['actualGlobalStores']==146 and
         retired['passed'] and liu['passed'] and liu['finiteNativeSonyaLiuClearAccepted'] and
         liu['accepted']['ownSuccessfulRoundFrames']==[392352,393931] and not liu['fullTowerAccepted'],
         'Actual later native corruption and earlier finite earned clear both retained')
    pins={}
    for proof in (saved,retired,liu):
        for p,h in proof['inputHashes'].items():
            need(sha(p)==h and (p not in pins or pins[p]==h),'Every original executed/frozen input remains unchanged');pins[p]=h
    import gzip
    counts=collections.Counter();target_counts=collections.Counter();target_hash=hashlib.sha256()
    late=[];overruns=[];cache=[];rounds=[]
    with gzip.open(capture.OUT/'run.log.gz','rt',encoding='utf-8') as stream:
        for line in stream:
            tag=line.split(' ',1)[0];counts[tag]+=1
            if tag in ('MK2_MILEENA_CAMPAIGN_OVERRUN','MK2_CURRENT_CAMPAIGN_CACHE_FAILURE'):
                q=dict(re.findall(r'(\w+)=([^\s]+)',line))
                (overruns if tag=='MK2_MILEENA_CAMPAIGN_OVERRUN' else cache).append(q)
            if line.startswith('MK2_NAT_CAMPAIGN_'):
                q=dict(re.findall(r'(\w+)=([^\s]+)',line));f=int(q['frame'])
                if f>=394481:
                    target_counts[tag.removeprefix('MK2_NAT_CAMPAIGN_')]+=1;target_hash.update(line.encode())
                if f>=480800 and tag in ('MK2_NAT_CAMPAIGN_LIVE','MK2_NAT_CAMPAIGN_STATE','MK2_NAT_CAMPAIGN_HEALTH'):
                    late.append(dict(category=tag,row=q))
                if tag=='MK2_NAT_CAMPAIGN_WIN' and q['stage']=='14':rounds.append(q)
    need(len(overruns)==len(cache)==146 and all(q['frame']=='480976' and q['pc']=='FF838860' and
         q['a8']=='01034020' and q['a13']=='010757D0' and q['a9']=='FF9D7B70' and q['id']=='18'
         for q in overruns) and all(q['observer_callback']=='480976' and q['pc']=='FF838860' for q in cache),
         'Every actual decoder/global write retained at exact same corrupting native callback')
    need(next(x['row'] for x in late if x['category']=='MK2_NAT_CAMPAIGN_LIVE' and x['row']['frame']=='480960')['poses']=='FF9D7CB0,FF963960' and
         any(x['category']=='MK2_NAT_CAMPAIGN_STATE' and x['row']['frame']=='480977' and
             x['row']['stage']=='65535' and x['row']['schedule']=='FFFFFFFF' for x in late),
         'Actual prior stock-looking victim composite and following corrupted scene, not an invented softlock')
    stock=ROOT/'mk2/mk2-maincpu.bin';disasm=ROOT/'mame-mkp/unidasm.exe';rom=stock.read_bytes()
    need(sha(stock)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23', 'Exact authoritative original program')
    offset=lambda address:(address-0xff800000)//8
    table=0xff9d7770
    lookup=[dict(id=i,address=f'{table+i*32:08X}',value=f'{struct.unpack_from("<I",rom,offset(table)+i*4)[0]:08X}') for i in range(19)]
    need(lookup[18]['value']=='FF9D7B50' and
         struct.unpack_from('<I',rom,offset(0xff9d7b50)+4)[0]==0 and
         struct.unpack_from('<I',rom,offset(0xff9d7b70))[0]==0xffbf18b0,
         'Original true18 index lands in a composite list; subsequent animation token would be raw bitmap descriptor')
    kernels=[]
    for start,end in ((0xff8caf00,0xff8cb490),(0xff842ed0,0xff842f70),(0xff83b7f0,0xff83b870),(0xff838790,0xff838a70)):
        answer=subprocess.run([str(disasm),str(stock),'-arch','tms34010','-basepc',hex(start),
            '-skip',str(offset(start)),'-count',str(end-start),'-norawbytes'],capture_output=True,text=True,check=True)
        need(len(answer.stdout)<20000 and not answer.stderr.strip(),'Bounded original source disassembly, no whole-ROM copy')
        kernels.append(dict(start=f'{start:08X}',endExclusive=f'{end:08X}',bytesSHA256=hashlib.sha256(rom[offset(start):offset(end)]).hexdigest().upper(),instructions=answer.stdout.splitlines()))
    for p in (*paths,Path(__file__).resolve(),Path(capture.__file__),stock,disasm,capture.OUT/'run.log.gz'):
        pins[str(p.resolve())]=sha(p)
    report=dict(passed=False,diagnosisCompleted=True,nativeGameplayAccepted=False,
        completeTransportCategoryCounts=dict(counts),completeLaterTargetCategoryCounts=dict(target_counts),
        completeLaterTargetSHA256=target_hash.hexdigest().upper(),completeCacheWriteRows=cache,
        completeOverrunRows=overruns,allLaterActualRoundWinners=rounds,allFinalSceneHealthRecords=late,
        originalVictimLookupTable=f'{table:08X}',originalLookupRows=lookup,originalSourceKernels=kernels,
        sourceInference='Original FF8CAF00 victim path indexes FF9D7770 via native true victim ID. Index18 is FF9D7B50, a composite rather than an animation stream; its next raw descriptor at FF9D7B70 agrees with the actual overrun A9. Missing extended victim lookup is the leading source candidate.',
        actualLookupCallerWitnessCaptured=False,runtimeRootCauseResolved=False,
        nextRequiredEvidence='Passive native caller/lookup/animation handoff taps on same normal-input campaign. Bind actual true18 victim and actual Shang6 actor/Main, original guest and prior thirteen earned regular opponents. No tactic-only workaround, identity proxy or dropped failure.',
        originalNaturalIntegrationRequirements=saved['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=saved['originalRemainingWorkGroups'],inputHashes=pins,
        fullPortAcceptance=False,newBuilds=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(diagnosisCompleted=True,actualCorruptingNativeFrame=480976,actualGlobalStores=146,
                         runtimeRootCauseResolved=False,sourceCandidateTable='FF9D7770',fullPortAcceptance=False)),flush=True)
    return report


if __name__=='__main__':run()

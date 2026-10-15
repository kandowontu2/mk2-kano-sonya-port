"""Actual ID17 short-table overread, wrong performer grammar and native corruption."""
import copy,gzip,hashlib,json,re,struct,subprocess
from pathlib import Path
import native_ai_response_context as current
import native_process_census_v6647 as census
ROOT,need,sha=current.ROOT,current.need,current.sha
RUN=ROOT/'audit_native_cpu_kano_finish_lookup_cause'
OUT=ROOT/'audit_native_cpu_finisher_dispatch_cause_checked'
def off(bit):return (bit-0xff800000)//8
def parse(text):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines()
            if line.startswith('MK2_KANO_CACHE_CAUSE ')]
def gate(guest,payload,rows):
    u32=lambda bit:struct.unpack_from('<I',guest,off(bit))[0]
    need(guest[off(0xff83b7f0):off(0xff83b860)]==
         (ROOT/'mk2/mk2-maincpu.bin').read_bytes()[off(0xff83b7f0):off(0xff83b860)],
         'Whole original real-ID lookup and return remain native')
    need(u32(0xff876b50)==0xff8ba210 and u32(0xff876b90)==0xff8ba390,
         'Both actual unextended original performer-table operands')
    need(u32(0xff8ba210+17*32)==u32(0xff8ba390+5*32)==0xff8d2410,
         'True Kano first-table overread is exactly adjacent Mileena second finisher')
    lookup=next(r for r in rows if r['kind']=='id_lookup_result' and r['a1']=='FF8BA210')
    wrong=next(r for r in rows if r['kind']=='wrong_Mileena_finish_entry')
    root=next(r for r in rows if r['kind']=='lookup_result' and r['stack0']=='FF8D2490')
    bad=next(r for r in rows if r['kind']=='cache_begin' and r['a0']=='FFB47BC0')
    store=next(r for r in rows if r['kind']=='first_global_write')
    for r in (lookup,wrong,root,bad,store):
        need(r['id']==r['roster']=='17' and r['actor']==r['owner']=='010350A0' and
             r['main']=='010749F0' and r['health']=='0,109' and r['state']=='0' and r['mode']=='2' and
             r['writes']=='0' and r['assistance']=='none','Actual true CPU Kano owns all causal events')
    need(lookup['pc']=='FF83B860' and lookup['a0']=='FF8D2410' and
         wrong['at']=='FF8D2410' and int(lookup['frame'])<=int(wrong['frame'])<=int(root['frame']),
         'Actual real-ID lookup returns wrong routine and original CPU actually enters it')
    need(root['a0']=='FF000840' and root['a9']=='FF00D430' and root['a9_rom']=='FF014340',
         'Wrong original performer consumes actual Kano special4, not stock Mileena animation')
    p32=lambda bit:struct.unpack_from('<I',payload,(bit-0xfe800000)//8)[0]
    need(p32(0xff000840+4*32)==0xff00d430 and p32(0xff00d590)==0 and p32(0xff00d5b0)==0xffb47bc0,
         'Own special4 ends before following unrelated component data')
    need(bad['frame']==store['frame']=='36314' and bad['a9']==store['a9']=='FF00D5D0' and
         bad['a0_rom']=='00200015' and bad['cache']=='0105F230',
         'Actual bad call follows valid cache allocation and interprets frame width/height as list pointer')
    need(store['pc']=='FF838860' and store['at']=='01060050' and store['mask']=='FFFF' and
         store['a0']=='FFB47FE0' and store['a1']=='01060050',
         'Original component-copy loop genuinely reaches physical global-state memory')
    return dict(actualFirstCorruptingFrame=36314,wrongNativeRoutine='FF8D2410',
        realActorID=17,actor='010350A0',main='010749F0',actualShortTable='FF8BA210',
        actualOwnSpecial4='FF00D430',badFrameAsGroup='FFB47BC0',
        cause='Original twelve-row first performer table overreads true ID17 into adjacent Mileena second finisher; that routine walks beyond Kano special4 into frame descriptors.',
        sourceOnlyDiagnosis=True,nativeRepairAccepted=False,fullPortAcceptance=False)
if __name__=='__main__':
    need(not OUT.exists() and not census.census(),'Fresh immutable proof after actual native terminal')
    meta=json.loads((RUN/'result.json').read_text())
    need(meta['nativeExit']==0 and meta['nativeCacheOverrunObserved'] and not meta['fullPortAcceptance'],
         'Actual finite native diagnostic, not a successful campaign')
    pins=json.loads((RUN/'input_hashes_before.json').read_text())
    need(all(sha(p)==h for p,h in pins.items()),'All actually executed sources frozen')
    text=gzip.open(RUN/'run.log.gz','rt',encoding='utf-8').read()
    rows=parse(text);guest=current.expected()
    payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    need(json.loads((RUN/'guest_memory_proof.json').read_text())['sha256']==hashlib.sha256(guest).hexdigest().upper(),
         'Entire actual initialized 1MiB guest matches independent source model')
    need('MK2_KANO_CACHE_CAUSE_STOP frame=36316 first_bad=36314 ' in text,'Native exit after observed corruption')
    prior=gzip.open(ROOT/'audit_native_cpu_kano_cache_cause/run.log.gz','rt',encoding='utf-8').read()
    prefix=lambda value:[line for line in value.splitlines() if line.startswith('MK2_NAT_CAMPAIGN_')]
    need(prefix(prior)==prefix(text),'Entire original physical controller/campaign trajectory reproduced exactly')
    positive=gate(guest,payload,rows);faults=[]
    for name,kind,key,value in (
        ('proxy_id','id_lookup_result','id','1'),('wrong_cpu_owner','wrong_Mileena_finish_entry','owner','01034E90'),
        ('wrong_health','wrong_Mileena_finish_entry','health','161,109'),
        ('different_lookup_result','id_lookup_result','a0','FFFAB000'),
        ('different_animation','lookup_result','a9','FF000920'),
        ('safe_cache_call','cache_begin','a0','FF014540'),
        ('ordinary_health_write','first_global_write','pc','FF836700'),
        ('no_global_write','first_global_write','at','0105F230')):
        changed=copy.deepcopy(rows)
        target=next(r for r in changed if r['kind']==kind and
             (kind!='id_lookup_result' or r['a1']=='FF8BA210') and
             (kind!='lookup_result' or r['stack0']=='FF8D2490') and
             (kind!='cache_begin' or r['a0']=='FFB47BC0'))
        target[key]=value
        try:gate(guest,payload,changed)
        except (ValueError,StopIteration) as error:faults.append(dict(name=name,rejected=str(error)))
        else:raise ValueError('Actual causal fault admitted: '+name)
    need(gate(guest,payload,rows)==positive,'Full original causal positive restored')
    sources={p:dict(sha256=h,text=Path(p).read_text())for p,h in pins.items()
             if Path(p).suffix.lower()in('.py','.lua','.cpp','.h','.cmd')}
    OUT.mkdir()
    with gzip.open(OUT/'exact_executed_sources.json.gz','wt',encoding='utf-8')as stream:json.dump(sources,stream)
    pins[str(Path(__file__).resolve())]=sha(__file__)
    pins.update({str(p):sha(p)for p in RUN.iterdir()if p.is_file()})
    report=dict(passed=True,**positive,actualTraceRows=len(rows),actualFaultsRejected=faults,
        inputHashes=pins,goalStatus='active',publicBuildPromoted=False,newBuilds=0)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    for p in OUT.iterdir():
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
    print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','actualFaultsRejected')},indent=2))

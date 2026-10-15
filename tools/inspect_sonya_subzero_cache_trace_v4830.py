"""Read-only source/native trace inspection; no build or acceptance shortcut."""
import collections,hashlib,json,re,struct
from pathlib import Path
import run_sonya_subzero_cache_trace_ram_v4826 as capture
ROOT=capture.ROOT

def sources():
    guest=capture.previous.expected()
    payload=(ROOT/capture.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    def read(address,fmt='<I'):
        if address>=0xff800000:raw,base=guest,0xff800000
        else:raw,base=payload,0xfe800000
        offset=(address-base)//8;size=struct.calcsize(fmt)
        if address%16 or offset<0 or offset+size>len(raw):raise ValueError('Invalid native ROM read '+hex(address))
        return struct.unpack_from(fmt,raw,offset)[0]
    return guest,payload,stock,read

def inspect():
    guest,payload,stock,read=sources()
    table=read(0xff9060a0);root=read(table+18*32)
    result=dict(guestSHA256=hashlib.sha256(guest).hexdigest().upper(),
        mainTable=f'{table:08X}',sonyaMainRoot=f'{root:08X}',sourceOnly=True,fullPortAcceptance=False,
        selectedMainStreams={})
    for index in (0,15,40,59,60,61,63,64):
        stream=read(root+index*32)
        result['selectedMainStreams'][str(index)]=dict(stream=f'{stream:08X}',
            firstWords=[f'{read(stream+n*32):08X}'for n in range(16)])
    folder=ROOT/'audit_v4828_sonya_subzero_cache_trace_ram'
    if not(folder/'result.json').exists():return result
    meta=json.loads((folder/'result.json').read_text());proof=json.loads((folder/'guest_memory_proof.json').read_text())
    assert meta['exit_code']==0 and proof['everyActualByteComparedInRAM'] and proof['sha256']==result['guestSHA256']
    lines=(folder/'run.log').read_text().splitlines()
    traces=[]
    for line in lines:
        if not line.startswith('MK2_SUBZERO_CACHE_TRACE '):continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        assert row['writes']=='0'and row['assistance']=='none'and row['id']=='18'and row['roster']=='18'
        if row['kind']!='first_global_write':
            assert int(row['pc'],16)==int(row['entry'],16)+16
            assert read(int(row['entry'],16),'<H')==int(row['value'],16)
        for reg in ('a0','a5','a9'):
            addr=int(row[reg],16)
            if 0xfe800000<=addr<=0xffffffc0 and addr%16==0:
                assert read(addr)==int(row[reg+'_rom32'],16),reg+' actual ROM source disagreement'
        traces.append(row)
    result.update(sourceOnly=False,nativeExit=meta['exit_code'],
        nativeRAMGuestCompared=True,traceRows=len(traces),traceCounts=dict(collections.Counter(r['kind']for r in traces)),
        diagnosticStops=[l for l in lines if l.startswith(('MK2_SUBZERO_CACHE_TRACE_STOP ','MK2_SUBZERO_CACHE_TRACE_RESULT '))],
        traceFirst=traces[:2],traceLast=traces[-2:],
        lookups=[r for r in traces if r['kind']in('self_lookup','main_lookup','root_loaded','lookup_cell','lookup_result')][-12:],
        cacheBegins=[r for r in traces if r['kind']=='cache_begin'][-12:],
        firstGroupNext=next((r for r in traces if r['kind']=='group_next'),None),
        actualOverruns=[l for l in lines if l.startswith('MK2_MILEENA_CAMPAIGN_OVERRUN ')])
    return result

if __name__=='__main__':print(json.dumps(inspect(),indent=2))

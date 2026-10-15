"""Read-only inventory of the actual palette-store record, no acceptance claim."""
import collections
import gzip
import re
import capture_native_selector_sonya_pressure_palette as capture

HEX=set('at before data mask after source pc a0 a1 a2 a3 a4 actor main returnPC bank palette_source'.split())


def parse():
    folder=capture.RAM_CASES[capture.KEY][0]
    result=[]
    with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as stream:
        for line in stream:
            if not line.startswith(('MK2_PAL_','MK2_EFFECT_QUEUE ')): continue
            tag=line.split(' ',1)[0]
            pairs=re.findall(r'(\w+)=([^\s]+)',line);r=dict(pairs)
            capture.need(len(r)==len(pairs) and r['writes']=='0' and r['assistance']=='none',
                         'Entire unique passive metadata fields')
            r['tag']=tag
            for key,value in list(r.items()):
                if key in ('phase','assistance','tag'): continue
                if key=='entries':
                    r[key]=[tuple(int(v,16) for v in entry.split(':')) for entry in value.split(',')]
                elif key in HEX: r[key]=int(value,16)
                elif key in ('frame','sequence','index','offset','refs','stamp','writes','terminalFrame'):
                    r[key]=int(value)
            result.append(r)
    return result


def inventory(events):
    writes=[r for r in events if r['tag']=='MK2_PAL_WRITE']
    return dict(tags=dict(collections.Counter(r['tag'] for r in events)),
        storesByNativePCAndOffset={f'{pc:08X}:{off}':count for (pc,off),count in
                                  sorted(collections.Counter((r['pc'],r['offset']) for r in writes).items())},
        ownerStoresByNativePC={f'{pc:08X}':count for pc,count in sorted(collections.Counter(
            r['pc'] for r in events if r['tag']=='MK2_PAL_OWNER').items())},
        fullPortAcceptance=False)

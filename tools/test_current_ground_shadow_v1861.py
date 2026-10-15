"""In-memory counterexamples for actual current source-bound shadow rows."""
import json,re
from pathlib import Path
import verify_current_ground_shadow_v1859 as current
ROOT=current.ROOT;OUT=ROOT/'audit_v1861_current_ground_shadow_counterexamples'

def change(log,tag,key,value):
    lines=log.splitlines(keepends=True)
    for i,line in enumerate(lines):
        if line.startswith('MK2_GROUND_'+tag+' '):
            lines[i],count=re.subn(r'\b'+key+r'=\S+',key+'='+value,line);assert count==1
            return ''.join(lines)
    raise AssertionError('Counterexample must modify actual evidence')

if __name__=='__main__':
    assert not OUT.exists(),'Preserve evidence'
    path=current.OUT/'report.json';proof=json.loads(path.read_text());assert proof['passed']
    for file,wanted in proof['inputHashes'].items():assert current.digest(file)==wanted
    folder=ROOT/'audit_v1858_ground_shadow_sonya_p2';log=(folder/'run.log').read_text(encoding='utf-8-sig')
    pins={};image=current.graphics(pins);current.check_sources(log,image)
    buffers=lambda text:{r['key']:r for r in current.raster.rows(text,'GFX')}
    native=lambda text:current.raster.check_shadow_rows(text,buffers(text))
    baseline=native(log);assert baseline['rowStreamVerified']
    first=current.raster.rows(log,'GFX')[0];altered_data=f'{int(first["data"][:2],16)^1:02X}'+first['data'][2:]
    comp=current.raster.rows(log,'SHADOW_COMPONENT')[0]
    mutations=[('captured_source_byte',change(log,'GFX','data',altered_data),lambda text:current.check_sources(text,image)),
               ('proxy_identity',change(log,'SHADOW_COMPONENT','id','1'),native),
               ('foreign_actor_owner',change(log,'SHADOW_COMPONENT','owner','01000000'),native),
               ('wrong_native_cache_row',change(log,'SHADOW_COMPONENT','row',f'{comp["row"]+16:08X}'),native),
               ('wrong_compressed_component_height',change(log,'SHADOW_COMPONENT','height',str(comp['height']+4)),native)]
    # Modify the actual DMA paired to the first imported shadow row, not an
    # unrelated scenery/body DMA. All changes remain in memory.
    shadow=next(r for r in current.raster.rows(log,'DMA')if r['event']==comp['event'])
    for key,value in (('color','14'),('palette','0200'),('pc','FF8015B0')):
        lines=log.splitlines(keepends=True);changed=False
        for i,line in enumerate(lines):
            if line.startswith('MK2_GROUND_DMA ')and f'event={shadow["event"]}' in line and re.search(r'\bevent='+str(shadow['event'])+r'(?:\s|$)',line):
                lines[i],count=re.subn(r'\b'+key+r'=\S+',key+'='+value,line);assert count==1;changed=True;break
        assert changed;mutations.append(('wrong_shadow_'+key,''.join(lines),native))
    records=[]
    for label,text,checker in mutations:
        try:checker(text)
        except (AssertionError,ValueError,KeyError)as error:records.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise AssertionError('Invalid evidence accepted: '+label)
    for file,wanted in proof['inputHashes'].items():assert current.digest(file)==wanted,'Actual evidence changed'
    pins.update({str(path):current.digest(path),str(Path(__file__)):current.digest(__file__),str(Path(current.__file__)):current.digest(current.__file__)})
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=True,candidate=current.NAME,baseline=baseline['rowStreamVerified'],
        counterexamples=records,count=len(records),actualArtifactsUnchanged=True,inputHashes=pins,fullPortAccepted=False),indent=2)+'\n')
    print('Actual current baseline and8 source/identity/owner/cache/height/colour/palette/caller counterexamples checked',flush=True)

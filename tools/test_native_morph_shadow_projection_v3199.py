"""Actual direct projection and compressed rows: qualified corruptions.

The projection body is extracted verbatim from the accepted full checker, not
a looser reimplementation. Actual defaultdict/schema retained in every case.
No parser/KeyError exceptions count as rejection.
"""
import inspect,json
from collections import defaultdict
from pathlib import Path
from unittest.mock import patch
import verify_native_morph_floor_projection_v3185 as floor
assembly=floor.assembly;ROOT=floor.ROOT;need=floor.need
OUT=ROOT/'audit_v3200_native_morph_shadow_projection_counterexamples'

def projection_function():
    text=inspect.getsource(floor.verify)
    start=text.index("            projections={(p['frame'],p['row'])")
    end=text.index("            print(key+': original morph art",start)
    block=text[start:end]
    need(block.endswith('                geometry+=1\n'),'Entire reached projection contract including final XY criterion')
    prefix="""def check(groups,payload,guest):
    first_by=defaultdict(list)
    for row in groups['SHADOW_COMPONENT']:
        first_by[row['frame'],row['row']].append(row)
    dmas={r['event']:r for r in groups['FLOOR_DMA']}
    geometry=0
"""
    source=prefix+'\n'.join('    '+line[12:]for line in block.rstrip('\n').split('\n'))+'\n    return geometry\n'
    env=dict(defaultdict=defaultdict,ROOT=ROOT,need=need)
    exec(compile(source,'<verbatim3185projection>','exec'),env)
    return env['check'],block

def test():
    need(not OUT.exists(),'Never overwrite evidence')
    floor.source_contract()
    report_path=floor.OUT/'report.json';report=json.loads(report_path.read_text())
    need(report['passed']and report['physicalCases']==4 and report['actualDirectNativeProjectionRegistersAccepted'],
      'Actual four-case full-scene/continuous-clear positive proof')
    guest,*_=assembly.expected()
    payload=(ROOT/floor.human.CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
    check,block=projection_function();rejected=[];pins=dict(report['inputHashes'])
    for target in('kano','sonya'):
        for side in(1,2):
            key=f'{target}_p{side}';folder=ROOT/f'audit_v3184_native_morph_floor_{key}_projection'
            data=floor.raster.data(folder);groups=data[0]
            expected=report['cases'][key]['exactQuarterHeightProjections']
            need(check(groups,payload,guest)==expected,'Exact entire actual projection positive '+key)
            part=next(r for r in groups['SHADOW_COMPONENT']if r['slot']==side and r['first_source']in
              {p['graphic']for parts in floor.morph.references().values()for p in parts})
            proj=next(p for p in groups['FLOOR_SHADOW_PROJECTION']if(p['frame'],p['row'])==(part['frame'],part['row']))
            def changed(tag,row,**fields):
                result=groups.copy()
                result[tag]=[dict(r,**fields)if r is row else r for r in groups[tag]]
                need(result[tag]!=groups[tag],'Actual reached record mutation')
                return result
            def reject(name,mutated,label,fn=check):
                need(isinstance(mutated,defaultdict),'Preserve actual parser defaultdict')
                try:
                    result=fn(mutated,payload,guest)
                except (ValueError,AssertionError)as error:
                    need(str(error)==label,'Only intended reached criterion counts '+name+': '+repr(error))
                else:
                    need(False,'Actual corruption wrongly accepted '+name+' '+str(result))
                rejected.append(dict(case=key,name=name,rejectedBy=label))
            bind='Direct projection snapshot belongs to that exact original owned shadow component'
            algebra='Exact original world-camera subtraction and native B7 ground offset, not a guessed sole offset'
            coordinates='Actual source-derived direct quarter-height world/cache/camera/ground/display projection exact'
            coverage='Every actual original direct shadow call has its own pose/cache/world/camera/ground/display register evidence'
            reject('wrong-real-owner',changed('FLOOR_SHADOW_PROJECTION',proj,owner=proj['owner']+16),bind)
            reject('wrong-direct-caller',changed('FLOOR_SHADOW_PROJECTION',proj,pc=proj['pc']+16),bind)
            reject('wrong-world-coordinate',changed('FLOOR_SHADOW_PROJECTION',proj,world=proj['world']+1),algebra)
            reject('wrong-shadow-camera',changed('FLOOR_SHADOW_PROJECTION',proj,shadow_camera=proj['shadow_camera']+1),algebra)
            reject('wrong-native-ground-offset',changed('FLOOR_SHADOW_PROJECTION',proj,b7=proj['b7']+1),algebra)
            reject('wrong-direct-shadow-body-flag',changed('FLOOR_SHADOW_PROJECTION',proj,body=proj['body']&~16),algebra)
            reject('shifted-native-display-offset',changed('FLOOR_SHADOW_PROJECTION',proj,a5=proj['a5']+1),coordinates)
            missing=groups.copy();missing['FLOOR_SHADOW_PROJECTION']=[p for p in groups['FLOOR_SHADOW_PROJECTION']if p is not proj]
            reject('missing-real-projection',missing,coverage)
            dma=next(d for d in groups['FLOOR_DMA']if d['event']==part['event'])
            reject('shifted-first-native-shadow-DMA',changed('FLOOR_DMA',dma,y=(dma['y']+1)&511),coordinates)
            def rows_check(mutated,*_):
                same=(mutated,)+data[1:]
                with patch.object(floor.shadows,'data',return_value=same):
                    result=floor.shadows.inspect(folder)
                need(result['rowStreamVerified']and not result['failures']and not result['oversized_rows'],
                  'Actual native row source/header/stride/count/coordinate stream exact')
                return result
            with patch.object(floor.shadows,'data',return_value=data):
                positive=floor.shadows.inspect(folder)
            need(positive['rowStreamVerified']and positive['checked_copies']==report['cases'][key]['shadowRows']['checked_copies'],
              'Same mocked row-data path actual positive control')
            reject('backward-row-source',changed('FLOOR_DMA',dma,source=dma['source']-64),
              'Actual native row source/header/stride/count/coordinate stream exact',rows_check)
            reject('wrong-physical-cache',changed('SHADOW_COMPONENT',part,cache=part['cache']+16),
              'Actual component belongs to native actor cache',rows_check)
            missing=groups.copy();missing['SHADOW_COMPONENT']=[r for r in groups['SHADOW_COMPONENT']if r is not part]
            reject('missing-owned-native-copy',missing,
              'Every imported shadow copy has exact owned component evidence',rows_check)
            need(check(groups,payload,guest)==expected,'Original projection unchanged after actual corruptions')
            print(key+':12qualified actual projection/row corruptions rejected',flush=True)
    need(len(rejected)==48,'Four fixtures12specific failures each')
    pins[str(report_path)]=assembly.sha(report_path);pins[str(Path(__file__).resolve())]=assembly.sha(__file__)
    value=dict(passed=True,physicalCases=4,actualCounterexamplesRejected=len(rejected),
      verbatimOriginalProjectionCriteria=True,actualParserDefaultdictPreserved=True,
      sameMockedRowPathPositiveControlsAccepted=True,unrelatedExceptionsNeverAccepted=True,
      projectionSourceSHA256=__import__('hashlib').sha256(block.encode()).hexdigest().upper(),
      counterexamples=rejected,allRasterEraseAudioAndArenaCounterexamplesAccepted=False,
      fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('48qualified original projection/row counterexamples passed',flush=True)
if __name__=='__main__':test()


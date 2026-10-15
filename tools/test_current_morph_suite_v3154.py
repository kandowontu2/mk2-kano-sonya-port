"""Real fresh fixtures, qualified mutations and same-path pixel controls.

Errors must be actual intended criterion failures. Exceptions never count.
"""
import json,re
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
import verify_current_morph_suite_v3150 as suite
human=suite.human
render=suite.render
ROOT=suite.ROOT
OUT=ROOT/'audit_v3155_current_morph_actual_counterexamples'
need=suite.need

def test():
    need(not OUT.exists(),'Never overwrite evidence')
    suite.unchanged_criteria()
    proof=json.loads((suite.OUT/'report.json').read_text())
    need(proof['passed']and proof['physicalCases']==4,'Actual independent full four-fixture positive suite')
    rejected=[];pins=dict(proof['inputHashes'])
    for target in('kano','sonya'):
        for side in(1,2):
            key=f'{target}_p{side}';folder=ROOT/f'audit_v3147_current_morph_{key}'
            log=(folder/'run.log').read_text(encoding='utf-8-sig')
            baseline=render.verify_log(log,folder,target,side)
            need(baseline['passed']and len(baseline['visual'])==80,'Actual unchanged full-pixel positive control')
            def check(name,changed,label):
                need(changed!=log,'Mutation actually changes reached fixture '+key+' '+name)
                value=render.verify_log(changed,folder,target,side,False)
                need(not value['passed']and label in value['errors'],
                  'Only intended native criterion counts, never parser/index exception: '+name)
                rejected.append(dict(case=key,name=name,rejectedBy=label))
            def remove(prefix):
                return re.sub(r'^'+prefix+r'[^\n]*\n','',log,count=1,flags=re.M)
            check('missing-live-field',remove('MK2_HUMAN_SHANG_FIELD '),
              'All 1001 consecutive gameplay fields')
            check('missing-projectile-child',remove('MK2_HUMAN_SHANG_PROJECTILE_CREATE '),
              'Own native projectile action and child creation while morphed')
            check('wrong-forward-native-store',
              log.replace('pc=FF86E670','pc=FF86E680'),
              'Original native forward ID store, not an alias')
            check('wrong-reverse-native-store',
              log.replace('pc=FFA16700','pc=FFA16710'),
              'Original native reverse ID store')
            floor='82'if target=='kano'else'81';identity=17 if target=='kano'else 18
            changed='\n'.join(line.replace('floor='+floor,'floor=86')if line.startswith('MK2_HUMAN_SHANG_FIELD ')and
              f' id={identity} 'in line else line for line in log.split('\n'))
            check('wrong-added-form-floor',changed,'Canonical added-character floor throughout the form')
            group='FF0C4000'if target=='kano'else'FF0C4120'
            check('missing-real-transition-hold',
              re.sub(r'^MK2_MORPH_RENDER_BODY[^\n]*pose='+group+r'[^\n]*\n','',log,count=1,flags=re.M),
              'Every original transition hold in both directions')
            check('missing-native-reverse-window',
              re.sub(r'^MK2_MORPH_RENDER_WINDOW[^\n]*phase=reverse[^\n]*\n','',log,count=1,flags=re.M),
              'Actual forward/reverse capture windows')
            check('wrong-native-copy-writer',log.replace('pc=FF804640','pc=FF804650'),
              'Native full-scale component copy DMA')
            check('wrong-native-scale',log.replace('scale_x=0100','scale_x=0080'),
              'Native full-scale component copy DMA')
            check('wrong-original-morph-palette',
              re.sub(r'(MK2_MORPH_RENDER_PALETTE[^\n]*colors=)[0-9A-F,]+',
                lambda m:m[1]+','.join(['0000']*64),log),
              'All used original morph/body colors reach actual DMA palette')
            check('missing-all-actual-native-DMA',
              re.sub(r'^MK2_MORPH_RENDER_DMA[^\n]*\n','',log,flags=re.M),
              'Actual native DMA/palette evidence')
            changed=re.sub(r'(MK2_MORPH_RENDER_COMPONENT[^\n]*descriptor=)[0-9A-F]+',
              lambda m:m[1]+'00000000',log,count=1)
            check('wrong-native-component-descriptor',changed,
              'Exact native original pixels/descriptor/dimensions/pivots/facing')
            changed=re.sub(r'(MK2_MORPH_RENDER_COMPONENT[^\n]*dx=)(-?\d+)',
              lambda m:m[1]+str(int(m[2])+1),log,count=1)
            check('shifted-original-component-pivot',changed,
              'Exact native original pixels/descriptor/dimensions/pivots/facing')
            actual=Image.open;first=baseline['visual'][0]['bitmap_frame'];calls=[]
            def wrapper(path,*args,**kwargs):
                return actual(path,*args,**kwargs)
            with patch.object(render.Image,'open',side_effect=wrapper):
                positive=render.verify_log(log,folder,target,side)
            need(positive['passed'],'Same mocked image-opening path unchanged positive control')
            def corrupted(path,*args,**kwargs):
                image=actual(path,*args,**kwargs)
                if Path(path).name==f'choreo_{first}.png':
                    calls.append(str(path))
                    return Image.fromarray(np.array(image.convert('RGB'))^255)
                return image
            with patch.object(render.Image,'open',side_effect=corrupted):
                negative=render.verify_log(log,folder,target,side)
            label='Every original opaque component pixel matches at exact two-field native buffer delay'
            need(calls and not negative['passed']and label in negative['errors'],
              'Actual reached fixed-delay pixel corruption rejected by exact raster criterion')
            rejected.append(dict(case=key,name='actual-fixed-delay-bitmap-corruption',rejectedBy=label))
            need(render.verify_log(log,folder,target,side)['passed'],'Final unmodified full-raster replay after all corruptions')
    pins[str(Path(__file__).resolve())]=suite.assembly.sha(__file__)
    report=dict(passed=True,physicalCases=4,actualCounterexamplesRejected=len(rejected),
      sameMockedPathPixelPositiveControlsAccepted=True,unrelatedExceptionsNeverAccepted=True,
      originalNativeAndRasterCriteriaUnchanged=True,counterexamples=rejected,
      fullPortAcceptance=False,inputHashes=pins)
    need(len(rejected)==56,'Four actual fixtures,14 meaningful corruptions each')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','counterexamples')},indent=2),flush=True)

if __name__=='__main__':test()

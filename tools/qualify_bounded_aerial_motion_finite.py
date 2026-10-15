"""Keep occluded stock-body points unresolved rather than claim all body RGB."""
from pathlib import Path
import qualify_bounded_aerial_motion_points as prior

source=Path(prior.__file__).read_text()
source=source.replace('points=[];body=[];fields=[];inputs=[];poses=set();unresolved=[]','points=[];body=[];fields=[];inputs=[];poses=set();unresolved=[];body_unresolved=[]',1)
old="if '_IDLE_SCANPOINT ' in line and r['kind']=='body':check_body(r,id);body.append(r)"
assert source.count(old)==1
source=source.replace(old,"""if '_IDLE_SCANPOINT ' in line and r['kind']=='body':
                if r['match']=='1':check_body(r,id)
                else:
                    assert r['expected']!=r['actual']
                    assert int(r['frame'])==int(r['source_frame'])+1
                    assert r['id']=={'1':str(id),'2':'4'}[r['slot']]
                    assert int(r['display_x'])==int(r['dma_x'])-int(r['column'])
                    assert int(r['display_y'])==int(r['dma_y'])-int(r['row'])
                    body_unresolved.append(r)
                body.append(r)""",1)
source=source.replace('bodyBottomPoints=len(body),unresolvedDMAPredictionPoints=unresolved,','bodyBottomPoints=len(body),unresolvedBodyRGBPoints=body_unresolved,unresolvedDMAPredictionPoints=unresolved,',1)
source=source.replace("bodyPoints=v['bodyBottomPoints'],unresolved=", "bodyPoints=v['bodyBottomPoints'],unresolvedBody=len(v['unresolvedBodyRGBPoints']),unresolved=",1)
scope=dict(prior.__dict__,__name__='finite_aerial_successor',__file__=__file__)
exec(compile(source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()

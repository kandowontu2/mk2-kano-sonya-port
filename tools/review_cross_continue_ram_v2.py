"""Actual rendered airborne screen after the pre-task jump response marker."""
import hashlib,inspect
from pathlib import Path
import review_cross_continue_ram as previous
ROOT,need,sha,contract,server=previous.ROOT,previous.need,previous.sha,previous.contract,previous.server


def select(images,text,report,target,side):
    carrier,choices=previous.select(images,text,report,target,side)
    jump=int(contract.rows(text,'JUMP')[0]['frame'])
    fields={(int(r['frame']),int(r['slot'])):r for r in contract.rows(text,'FIELD')}
    shown=next(q for q in report['actualFullRGBDigests']if q['label'].startswith('ui_')and q['frame']>=jump+3 and
        (q['frame'],side)in fields and int(fields[q['frame'],side]['y'])<int(fields[q['frame'],side]['floor'])and fields[q['frame'],side]['action']!='1283')
    raw=images[shown['frame'],shown['label']];need(hashlib.sha256(raw).hexdigest().upper()==shown['sha256'],'Original complete actual airborne display digest')
    carrier['rgbFrames'][2]=dict(header=dict(shown,width='400',height='254'),pixels=raw);choices[2]=shown
    return carrier,choices


source=inspect.getsource(previous.record_review)
source=source.replace('str(Path(__file__)):sha(__file__)','str(Path(__file__)):sha(__file__),str(Path(previous.__file__)):sha(previous.__file__)')
scope=dict(vars(previous),__file__=__file__,previous=previous)
exec(compile(source,__file__+'::actual_viewed_rendered_airborne_frames','exec'),scope)
record_review=scope['record_review']

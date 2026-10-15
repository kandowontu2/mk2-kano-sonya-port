"""Read-only dynamic-palette diagnostics; not full port or all-arena acceptance."""
import json
from functools import lru_cache
import numpy as np
import inspect_ground_presentation as p
from verify_ko_round_floor_shadows import rgb,need

def data(folder):
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    buffers={r['key']:r for r in p.rows(log,'GFX')}
    palettes={r['bank']:np.array([[int(c[i:i+2],16) for i in (0,2,4)] for c in r['colors'].split(',')],dtype=np.uint8)
              for r in p.rows(log,'RE_PALETTE')}
    draws={}
    for r in p.rows(log,'DMA'):draws.setdefault(r['frame'],[]).append(r)
    caches=p.rows(log,'DMA_CACHE')
    return log,buffers,palettes,draws,caches

def raster(draws,buffers,palettes,caches):
    body=np.zeros((512,512,3),dtype=np.uint8);opaque=np.zeros((512,512),dtype=bool)
    slots={n:np.zeros((512,512),dtype=bool) for n in (1,2)};projected=np.zeros((512,512),dtype=bool)
    for d in draws:
        if d['command']&15!=2 or d['slot']==0:continue
        indices=p.decode(d,buffers);h,w=indices.shape;ys,xs=np.where(indices!=0)
        x=d['x']+(-xs if d['command']&16 else xs);y=(d['y']+(-ys if d['command']&32 else ys))&511
        inside=(x>=0)&(x<512)&(y<254)
        body[y[inside],x[inside]]=palettes[d['palette']][indices[ys[inside],xs[inside]]]
        opaque[y[inside],x[inside]]=True;slots[d['slot']][y[inside],x[inside]]=True
        if not 0x10000000<=d['source']<0x1a000000:continue
        matches=[r for r in caches if r['frame']==d['frame'] and r['slot']==d['slot'] and r['source']==d['source']]
        need(len(matches)==1,'One independently observed actual owning DMA task')
        a=matches[0];need(a['owner']==a['actor'] and a['id'] in (17,18),'Actual imported Main owner')
        signed=lambda value:value-65536 if value>=32768 else value
        ground=a['stageY']+5+signed(a['cameraXY']>>16)-signed(a['worldXY']>>16)
        jump=max(0,min(200,a['floor']-a['y']));sh=min(45,max(12,(h+3)//4+1));top=ground-3-jump*3//10-sh+1
        if d['command']&32:indices=indices[::-1]
        for row in range(sh):
            sy=row*(h-1)//(sh-1);xs=np.flatnonzero(indices[sy]!=0)
            x=d['x']+(-xs if d['command']&16 else xs);y=top+row
            if 0<=y<512:projected[y,x[(x>=0)&(x<512)]]=True
    crop=lambda value:value[:254,56:456]
    return crop(body),crop(opaque),{n:crop(m) for n,m in slots.items()},crop(projected)

def inspect(fighter,side=1):
    old=p.ROOT/f'audit_v472_dynamic_before_{fighter}_p{side}'
    after=p.ROOT/f'audit_v474_dynamic_after_{fighter}_p{side}'
    log,buffers,palettes,draws,caches=data(old);newlog=(after/'run.log').read_text(encoding='utf-8-sig')
    for tag in ('FIELD','PART','INPUT','DMA','DMA_CACHE','GFX','HEALTH','CODE','SELECT','OUTSIDE','SNAP','RESULT','RE_PALETTE'):
        need(p.rows(log,tag)==p.rows(newlog,tag),'Before/after actual '+tag+' records differ')
    ready=p.rows(log,'RE_READY')[0]['frame'];records=[]
    @lru_cache(maxsize=None)
    def model(frame):return raster(draws.get(frame,[]),buffers,palettes,caches)
    for snap in p.rows(log,'SNAP'):
        if snap['frame']<ready:continue
        before=rgb(old/'snap'/snap['file']);new=rgb(after/'snap'/snap['file']);best=None
        for frame in range(snap['frame']-4,snap['frame']+1):
            body,mask,slots,shadow=model(frame)
            if mask.sum()<100:continue
            score=float(np.all(before[mask]==body[mask],axis=1).mean())
            if best is None or score>best[0]:best=(score,frame,body,mask,slots,shadow)
        need(best is not None,'Actual body provenance')
        score,frame,body,mask,slots,shadow=best;expected=shadow&~mask
        missing=int((expected&np.any(new!=0,axis=2)).sum());difference=np.any(new!=before,axis=2)
        records.append(dict(frame=snap['frame'],file=snap['file'],dmaFrame=frame,bodyScoreBefore=score,
                            bodyScoreAfter=float(np.all(new[mask]==body[mask],axis=1).mean()),
                            feet={n:int(np.where(m)[0].max()) for n,m in slots.items()},
                            expectedShadowPixels=int(expected.sum()),missingShadowPixels=missing,
                            changedPixels=int(difference.sum()),changedOutsideShadowAndBodies=int((difference&~(shadow|mask)).sum())))
    return dict(fighter=fighter,side=side,observedFighterPalettes=sorted(palettes),records=records,
                fullPortAcceptance=False,scope='Diagnostic paid cross-reselect and continued-arena dynamic palette silhouette; not complete foreground/all-arenas proof')

if __name__=='__main__':
    for fighter in ('kano','sonya'):
        proof=inspect(fighter)
        print(json.dumps(proof,indent=2))

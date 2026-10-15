"""Original native blood and RNG explain both changed blade recovery scenes.

Classification comes from actual native publication/palette/cache/DMA provenance,
not a red-pixel or rectangle mask. Every pixel operation is still replayed in
full. The original seed/overflow/carry/HCOUNT rotation and stack return are
checked instruction by instruction, without forcing the previous RNG sequence.
This is not universal effects, artwork, audio, campaign or whole-port acceptance.
"""
import argparse,json,struct,sys
from pathlib import Path
from collections import defaultdict
import numpy as np
from PIL import Image
import verify_native_blade_blood_render_v2805 as drawing

ROOT=drawing.ROOT;need=drawing.need;raster=drawing.raster
BLOOD_PALETTE=0xffaf2a40
OUT=ROOT/'audit_v2814_native_blade_blood_cause_checked'

def rng_checked(rows,guest,original):
    addresses=(0xff80e980,0xff80e9c0,0xff80e9d0,0xff80ea10,0xff80ea50,0xff80ea90,0xff80eaa0,0xff80ead0)
    first=(0xff80e980-0xff800000)//8;last=(0xff80eb70-0xff800000)//8
    need(guest[first:last]==original[first:last],'Entire original RNG seed/carry/HCOUNT/return code unchanged')
    need(len(rows)>0 and len(rows)%8==0,'Every observed original RNG call complete')
    calls=[]
    for i in range(0,len(rows),8):
        batch=rows[i:i+8]
        need(tuple(r['at'] for r in batch)==addresses,'Exact ordered original RNG instructions')
        for row in batch:
            op,=struct.unpack_from('<H',original,(row['at']-0xff800000)//8)
            need((row['op'],row['mask'],row['pc'],row['writes'],row['assistance'])==(op,65535,row['at']+16,0,'none'),'Original RNG opcode and read-only provenance')
        start,load,shift,store,carry,rotate,answer,end=batch
        need(all(r['a8']==start['a8'] and r['a13']==start['a13'] for r in batch),'Original caller context maintained')
        need(load['sp']==start['sp']-32 and load['stack']==start['a1'] and load['a1']==start['a1'] and load['a0']==load['seed']==start['seed'],'Actual native seed load and saved A1')
        seed=load['seed'];shifted=(seed<<1)&0xffffffff
        overflow=bool((seed^(seed<<1))&0x80000000);old_carry=bool(seed&0x80000000)
        need(shift['a0']==shifted and bool(shift['status']&0x10000000)==overflow and bool(shift['status']&0x40000000)==old_carry,'Original SLA overflow and carry decision')
        stored=shifted if overflow else shifted|2
        need(store['a0']==stored and store['seed']==seed,'Original JRV/ORI seed branch')
        need(carry['a0']==carry['seed']==stored and carry['a1']==0 and bool(carry['status']&0x40000000)==old_carry,'Original native seed store and preserved carry')
        operand=(stored+int(old_carry))&0xffffffff
        need(rotate['a0']==operand and rotate['seed']==stored and 0<=rotate['a1']<=65535,'Original ADDC and actual HCOUNT operand')
        count=rotate['a1']&31
        expected=((operand<<count)|(operand>>(32-count if count else 32)))&0xffffffff
        need(answer['a0']==end['a0']==expected and answer['a1']==rotate['a1'],'Exact original variable rotate result')
        need(end['a1']==start['a1'] and end['sp']==start['sp'] and end['stack']==start['stack'] and end['seed']==stored,'Original A1/stack/return and seed restoration')
        calls.append(dict(frame=start['frame'],caller=start['stack'],main=start['a13'],actorRegister=start['a8'],
            seed=seed,storedSeed=stored,hcount=rotate['a1'],rotateCount=count,result=expected))
    return dict(passed=True,completeCalls=len(calls),actualInstructionObservations=len(rows),calls=calls,
        originalRNGCodeAndEveryObservedArithmeticResultAccepted=True,actualNativeHCountOperandCaptured=True,
        hardwareReadTapPresent=False,seedOrHardwareCounterWrittenByObserver=False)

def case_checked(version,side,pins):
    folder=ROOT/f'audit_v{version}_native_blade_blood_p{side}'
    candidate=drawing.assembly if version==2802 else drawing.assembly.prior
    def proof(path):
        value=json.loads(path.read_text());need(value['passed'],'Accepted complete render/erase proof '+str(path))
        pins[str(path)]=drawing.phase.sha(path)
        for file,wanted in value['inputHashes'].items():
            need(drawing.phase.sha(file)==wanted,'Unchanged complete scene evidence '+file);pins[file]=wanted
        return value
    rendered=proof(ROOT/f'audit_v2806_native_blade_blood_{version}_p{side}_render_checked/report.json')
    erasure=proof(ROOT/(f'audit_v2809_native_blade_blood_{version}_p{side}_erase_checked/report.json' if version==2802 else f'audit_v2811_native_blade_blood_prior_p{side}_erase_checked/report.json'))
    need(rendered['candidate']==candidate.NAME and rendered['side']==side and rendered['move']=='blade' and
        rendered['exactConsecutiveScanouts']==erasure['continuousExactPreBuffers']==erasure['continuousExactFlips']==(65 if side==1 else 64) and
        erasure['oneInitialBaseOnly'] and not erasure['laterBuffersUsedAsAnchors'],'Complete source-bound drawing plus uninterrupted erasure')
    groups,*_=raster.data(folder)
    guest=(folder/'guest_maincpu.bin').read_bytes();original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(guest==candidate.expected()[0],'Whole actual initialized guest exactly independent source reconstruction')
    random=rng_checked(groups['FLOOR_RNG'],guest,original)
    queues={(r['frame'],r['cursor']):r for r in groups['FLOOR_ALL_QUEUE']}
    palette={(r['frame'],r['cursor']):r for r in groups['FLOOR_ALL_PALETTE']}
    publications={(r['frame'],r['cursor']):r for r in groups['FLOOR_BLOOD_PUBLICATION']}
    need(len(queues)==len(groups['FLOOR_ALL_QUEUE']) and len(palette)==len(groups['FLOOR_ALL_PALETTE']) and queues.keys()==palette.keys(),'Every native publication has independently read allocator source')
    need(len(publications)==len(groups['FLOOR_BLOOD_PUBLICATION'])>100,'Complete original blood publication inventory')
    blood={};by_cursor=defaultdict(list)
    def xy(value):
        def short(n):return (n&65535)-65536 if n&32768 else n&65535
        return short(value),short(value>>16)
    single_first=(0xff804000-0xff800000)//8;single_last=(0xff804420-0xff800000)//8
    need(guest[single_first:single_last]==original[single_first:single_last],'Entire original single/multipart projection/publication code unchanged')
    for key,q in queues.items():
        by_cursor[q['cursor']].append(q);p=palette[key]
        need((p['actor'],p['bank'],p['pc'])==(q['actor'],q['bank']&0x7f00,0xff804420),'Original publication and actual palette source binding')
        if p['palette_source']!=BLOOD_PALETTE:
            need(key not in publications,'No color-based blood ownership substitution');continue
        need(key in publications and q['id']==0 and q['body']&2==0 and p['refs']>0,'Genuine original single-sprite blood with positive native palette reference')
        at=(q['cache']-0xff800000)//8
        need(0<=at<=len(original)-14 and guest[at:at+14]==original[at:at+14],'Entire original blood descriptor unchanged')
        descriptor=struct.unpack_from('<4hIH',original,at)
        width,height,dx,dy,source,format_word=descriptor;r=publications[key]
        need(0<width<=128 and 0<height<=128 and source==q['source']==r['source'],'Original native blood dimensions/source')
        need((r['actor'],r['cache'],r['palette_source'],r['refs'],r['pc'])==(q['actor'],q['cache'],BLOOD_PALETTE,p['refs'],0xff804420),'Actual blood transform uses its original actor/cache/palette')
        command=r['command']>>16
        need(r['size']==width|(height<<16) and command==q['facing']==r['facing'] and command&0x7000==format_word&0x7000 and command&15==2,'Original single-sprite format and actual native pixel command')
        x,y=xy(r['world']);cx,cy=xy(r['camera']);bx,by=xy(r['display'])
        if not r['body']&1:x-=cx;y-=cy
        # Original FF804180 branches directly to FF8042A0 for single sprites.
        # It bypasses multipart cache DX/DY subtraction at FF804290.
        if command&16:x+=width-1
        if command&32:y+=height-1
        need(r['xy']==((x+bx)&65535)|(((y+by)&65535)<<16),'Exact native world/camera/descriptor/flip/display blood projection')
        blood[key]=dict(queue=q,palette=p,descriptor=descriptor,publication=r)
    need(blood.keys()==publications.keys(),'Every original blood publication classified without omissions')
    regs={r['event']:r for r in groups['FLOOR_DMA_REGS']};blood_events={}
    for d in groups['FLOOR_DMA']:
        possible=[q for q in by_cursor[regs[d['event']]['b14']+192] if q['frame']<=d['frame']]
        if not possible or d['command']&15!=2:continue
        q=max(possible,key=lambda q:q['frame']);key=(q['frame'],q['cursor'])
        if q['source']!=d['source'] or key not in blood:continue
        b=blood[key];r=b['publication']
        need((d['slot'],d['palette'],d['width'],d['height'],d['command'])==(0,b['palette']['bank'],b['descriptor'][0],b['descriptor'][1],r['command']>>16),'Actual original blood FIFO reaches unchanged DMA')
        need((d['x'],d['y'])==(r['xy']&1023,(r['xy']>>16)&511),'Actual original blood projection reaches DMA')
        blood_events[d['event']]=b
    need(len(blood_events)>100,'Actual independently owned original blood drawing operations')
    offset=(BLOOD_PALETTE-0xff800000)//8;count,=struct.unpack_from('<H',original,offset)
    need(count==15 and guest[offset:offset+2+count*2]==original[offset:offset+2+count*2],'Complete original fifteen-color blood palette record')
    colors=struct.unpack_from('<15H',original,offset+2)
    expected_palette=np.array([sum(((((c>>s)&31)<<3)|(((c>>s)&31)>>2))<<dest for s,dest in ((10,16),(5,8),(0,0))) for c in colors],dtype=np.uint32)
    by_frame=defaultdict(list);palette_checks=0
    for d in groups['FLOOR_DMA']:by_frame[d['frame']].append(d)
    for display in groups['FLOOR_DISPLAY']:
        actual=np.fromfile(folder/display['palette_file'],dtype='<u4')
        for d in by_frame[display['frame']-1]:
            if d['event'] in blood_events:
                bank=blood_events[d['event']]['palette']['bank']
                need(np.array_equal(actual[bank:bank+15],expected_palette),'Every actually rendered original blood color')
                palette_checks+=1
    target=rendered['state']['recovered']-1;Replay=raster.Replay;mask=[None]
    class BloodReplay(Replay):
        def dma(self,d):super().dma({**d,'slot':4} if d['event'] in blood_events else d)
        def apply(self,kind,d):
            super().apply(kind,d)
            if d['frame']==target-1:mask[0]=(self.body==4).copy()
    raster.Replay=BloodReplay
    try:drawn=raster.inspect(folder)
    finally:raster.Replay=Replay
    need(drawn['frames']==rendered['exactNativeReplayedPasses'] and all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in drawn['records']),'Diagnostic ownership labeling leaves every full pixel operation exact')
    snap=next(r for r in groups['FLOOR_SNAP'] if r['frame']==target)
    latch=next(r for r in groups['FLOOR_LATCH'] if r['snapshot']==target and r['flip_frame']==target)
    flip=next(r for r in groups['FLOOR_FLIP'] if r['event']==latch['event'])
    display=next(r for r in groups['FLOOR_DISPLAY'] if r['frame']==target)
    picture=np.asarray(Image.open(folder/'snap'/snap['file']).convert('RGB'))
    endpoint=np.asarray(Image.open(folder/'snap/special_recovered.png').convert('RGB'))
    need(np.array_equal(picture,endpoint),'Exact recovered callback image belongs to its actual preceding native completed field')
    bound=drawing.check_latch(picture,(folder/latch['file']).read_bytes(),(folder/display['palette_file']).read_bytes(),flip['value'],flip['control'],flip['tap'])
    need(mask[0] is not None,'Actual native recovery ownership mask reconstructed')
    row,col=bound['row'],bound['column'];gore=mask[0][row:row+254,col:col+400]
    need(int(gore.sum())==next(r for r in drawn['records'] if r['frame']==target)['body'][4]['pixels'],'Original blood ownership reaches exact native scanout')
    report=dict(passed=True,candidate=candidate.NAME,side=side,completeScanouts=rendered['exactConsecutiveScanouts'],
        sourceBoundFullDrawingAndContinuousErasureAccepted=True,nativeBloodPublications=len(blood),
        nativeBloodDraws=len(blood_events),fullOriginalBloodPaletteChecks=palette_checks,
        recoveryFrame=target,recoveryBloodPixels=int(gore.sum()),rng=random,
        diagnosticOwnershipLabelOnly=True,pixelsOrDMAOperationsAltered=False,fullPortAccepted=False)
    return report,picture,gore

def verify():
    pins={};cases={}
    for side in (1,2):
        new,picture,mask=case_checked(2802,side,pins)
        prior,old_picture,old_mask=case_checked(2803,side,pins)
        changed=np.any(picture!=old_picture,axis=2)
        need(changed.any() and not np.any(changed&~(mask|old_mask)),'Every differing recovery pixel belongs to source-reconstructed original native blood')
        need(int(changed.sum())==(804 if side==1 else 1068),'Exactly the two previously unresolved endpoint differences')
        first_divergence=None
        for a,b in zip(new['rng']['calls'],prior['rng']['calls']):
            if a['result']==b['result']:continue
            need(all(a[k]==b[k] for k in ('frame','caller','main','actorRegister','seed','storedSeed')) and a['hcount']!=b['hcount'],'First RNG result divergence is the original hardware-count rotate, not a forced seed/caller')
            first_divergence=dict(current=a,prior=b);break
        need(first_divergence is not None,'Actual original hardware-count variation observed')
        cases[f'p{side}']=dict(passed=True,current=new,prior=prior,changedPixels=int(changed.sum()),
            allDifferencesAreOriginalNativeBlood=True,changedPixelsOutsideOriginalBlood=0,
            everyNonBloodRecoveryPixelUnchanged=True,firstObservedNativeRNGDivergence=first_divergence,
            entireParticleSequenceRequiredToMatchOldBuild=False)
        print('p'+str(side)+' every changed pixel source-bound to original native blood; native RNG arithmetic passed',flush=True)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file:
            path=Path(file).absolute()
            if path.is_relative_to(ROOT/'tools') and path.suffix=='.py':pins[str(path)]=drawing.phase.sha(path)
    return dict(passed=True,candidate=drawing.assembly.NAME,cases=cases,
        bothPreviouslyUnresolvedBladeRecoveryScenesAccepted=True,sourceBoundNativeBloodAndRNGAccepted=True,
        completeCurrentAndPriorConsecutiveScanouts=258,currentConsecutiveScanouts=129,
        fullOriginalGoalAcceptance=False,allMoveArtAccepted=False,audioAccepted=False,
        allVictimsArenasAccepted=False,fullPortAccepted=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable native blood cause evidence')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report.get(k) for k in ('passed','error','bothPreviouslyUnresolvedBladeRecoveryScenesAccepted','completeCurrentAndPriorConsecutiveScanouts')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)

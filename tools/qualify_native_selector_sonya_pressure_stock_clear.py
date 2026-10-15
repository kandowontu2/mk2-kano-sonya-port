"""Source-predicted stock shift-register clear, whole actual hide interval.

No new emulator run or guest writes. Keep the failed write-tap-only erase
assertion. Independently predict every word from the preceding actual flip
and stock instruction operands, never the target prepass. This is a finite
source/endpoint proof, not a claim that uncaptured transfer callbacks exist.
"""
import json
import traceback
from pathlib import Path
import numpy as np
import qualify_native_selector_sonya_pressure_hide_source as parent
import inspect_native_smoke_callers as disasm

ROOT,need,sha=parent.ROOT,parent.need,parent.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_stock_clear_checked'


def clear(words,start,source_bit=0x1fe000,pitch_bit=0x2000,height=127,
          transfer_words=1024,opposite=True):
    need(start in (0xeffc,0xfffc), 'Actual stock alternating viewport start')
    # B2 written to105D050 follows the independently decoded flip branch.
    viewport=0x38 if start==0xeffc else 0x01000038
    if not opposite:viewport^=0x01000000
    offset=(viewport>>4)&~15
    result=words.copy().reshape(-1)
    # PIXT loads the two reserved rows; FILL uses dummy_shiftreg_r so its
    # partial-word read does not reload the shift register from destination.
    source=result[source_bit>>3:(source_bit>>3)+transfer_words].copy()
    need(len(source)==transfer_words, 'Complete source-defined shift register')
    for y in range(height):
        at=(offset+y*pitch_bit)>>3
        need(at+transfer_words<=len(result), 'Native transfer within full VRAM')
        result[at:at+transfer_words]=source
    return result.reshape(512,512)


def source_gate(guest):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    lo,hi=0xff816630,0xff8171b0
    need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==
         stock[(lo-0xff800000)//8:(hi-0xff800000)//8],
         'Whole stock flip/conditional clear routine unchanged in actual guest')
    asm={int(s.split(':',1)[0],16):s.split(':',1)[1].strip().upper()
         for s in disasm.disassemble()}
    expected={0xff816740:'MOVI   1000038H,B2',0xff816800:'MOVI   EFFCH,A0',
        0xff816830:'MOVI   38H,B2',0xff8168b0:'MOVE   A0,@C0000090H,0',
        0xff8168e0:'MOVE   B2,@105D050H,1',0xff816940:'MOVE   @10619F0H,A0,0',
        0xff816970:'JREQ   FF816A00H',0xff8169b0:'CALLR  FF816EA0H',
        0xff816f50:'ANDI   FFFF6FFFH,B10',0xff816f80:'ORI    800H,B10',
        0xff816ff0:'MOVE   B10,@C0000080H,0',0xff817020:'MOVI   2000H,B3',
        0xff817050:'MOVI   1FE000H,B2',0xff817080:'PIXT   *B2,B2',
        0xff817090:'MOVE   @105D050H,B4,1',0xff8170c0:'SRL    4H,B4',
        0xff8170f0:'CLR    B2',0xff817100:'MOVI   7F0001H,B7',
        0xff817130:'FILL   XY',0xff817170:'MOVE   A13,@C0000080H,0'}
    need(all(asm.get(at)==v for at,v in expected.items()),
         'Independent exact stock source operands and dispatch, no target fit')
    base=ROOT/'diagnostic_native_selector_layers_long/input_sources/mame-mkp/src'
    files=[base/'mame/midway/midtunit_v.cpp',
           base/'devices/cpu/tms34010/tms34010.cpp',
           base/'devices/cpu/tms34010/34010gfx.hxx',
           base/'devices/cpu/tms34010/34010ops.hxx']
    video,cpu,gfx,ops=(p.read_text()for p in files)
    need('memcpy(shiftreg, &m_local_videoram[address >> 3], 2 * 512 * sizeof(uint16_t));'in video and
         'memcpy(&m_local_videoram[address >> 3], shiftreg, 2 * 512 * sizeof(uint16_t));'in video,
         'Compiled device transfers1024 words with exact bit-address/word indexing')
    fill=gfx[gfx.index('void FUNCTION_NAME(tms340x0_device::fill)'):]
    need('word_read = &tms340x0_device::dummy_shiftreg_r;'in fill and
         'word_write = &tms340x0_device::shiftreg_w;'in fill and
         'daddr += DPTCH();'in fill and 'daddr &= ~(BITS_PER_PIXEL - 1);'in fill and
         'dwordaddr++ << 4, dstword' in fill and
         'm_from_shiftreg_cb(offset, &m_shiftreg[0]);'in gfx and
         '#define DPTCH()        BREG(3)'in cpu and '#define OFFSET()       BREG(4)'in cpu and
         '#define DXYTOL(val)'in ops,
         'Compiled native FILL addressing, dummy read, pitch and unchanged transfer callbacks')
    return expected,files


def execute(state):
    need(not OUT.exists(), 'Fresh immutable source-defined whole clear evidence')
    parent_path=parent.OUT/'report.json';proof=json.loads(parent_path.read_text())
    original=parent.original;capture=original.faults.serialized.body.original.previous.capture
    handle=capture.NATIVE_HANDLES[capture.KEY]
    need(proof['passed']and handle['process'].poll()==0 and
         handle['identity']==proof['actualNativeIdentity'], 'Same original terminal native handle')
    pins=dict(proof['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()), 'Entire existing source/evidence inventory unchanged')
    instructions,source_files=source_gate(state['guest'])
    context=original.faults.scope['CONTEXT'];display=capture.DISPLAY
    rows=[];targets={};seeds={}
    for frame in range(3106,3176):
        before=context['latches'][frame];after=context['pre'][frame]
        need(before['event']+1==after['event'] and before['event']<after['event'],
             'Entire measured hide interval has no intervening tapped write event')
        seed=np.frombuffer(display['buffers'][before['file']],dtype='<u2').reshape(512,512)
        target=np.frombuffer(display['buffers'][after['file']],dtype='<u2').reshape(512,512)
        predicted=clear(seed,before['start'])
        need(np.array_equal(predicted,target),
             'Every whole512x512 native gap endpoint equals source-predicted stock clear')
        changes=seed!=target
        need(changes.any(), 'Actual clear prediction is effective, never a no-op positive')
        rows.append(dict(frame=frame,flipEvent=before['event'],prepassEvent=after['event'],
            displayStart=before['start'],changedWords=int(changes.sum()),
            completeComparedWords=512*512,seedSHA256=__import__('hashlib').sha256(seed.tobytes()).hexdigest().upper(),
            targetSHA256=__import__('hashlib').sha256(target.tobytes()).hexdigest().upper()))
        if frame in (3106,3107,3108):seeds[frame]=seed.copy();targets[frame]=target.copy()
    # Track real sparse physical pixels on their own native pages, not a
    # screen-coordinate mask transplanted into the other alternating page.
    Driver=original.tracked(context,set(proof['actualLatePhysicalSourceFIFOAndDMA']['lastKanoSources']))
    folder=capture.RAM_CASES[capture.KEY][0]
    replay=Driver(folder,context['groups'],context['buffers'],context['owners'])
    erased=[];helper=original.faults.serialized.body.original
    for frame in (3106,3107):
        for kind,d in helper.window(context,frame):
            if kind!='FLOOR_FLIP':replay.apply(kind,d)
        need(replay.words.tobytes()==display['buffers'][context['latches'][frame]['file']],
             'Whole original physical body/shadow pass unchanged')
        mask=(replay.words.labels==1)|(replay.words.labels==3)
        need(mask.any() and np.all(targets[frame+1][mask]==seeds[frame+1][510,0]),
             'Every last physical body/shadow pixel on its actual page erased by next opposite-page clear')
        erased.append(dict(lastVisibleSnapshot=frame,erasedByPrepass=frame+1,
            nativeOwnedPixels=int(mask.sum()),allOwnedPixelsErased=True))
    faults=[]
    # Every effective model alteration must fail against all original words.
    seed,target=seeds[3107],targets[3107];start=context['latches'][3107]['start']
    changes=[('omit_stock_clear',seed),('wrong_page',clear(seed,start,opposite=False)),
        ('one_less_transfer',clear(seed,start,height=126)),
        ('one_less_word',clear(seed,start,transfer_words=1023)),
        ('wrong_source_row',clear(seed,start,source_bit=0x1fd000)),
        ('wrong_pitch',clear(seed,start,pitch_bit=0x1ff0))]
    for label,changed in changes:
        count=int(np.count_nonzero(changed!=target))
        need(count>0, 'Effective complete clear counterexample rejected: '+label)
        faults.append(dict(kind=label,differentWholeWords=count))
    altered=target.copy();altered[0,0]^=1
    need(not np.array_equal(clear(seed,start),altered), 'Complete untouched-page pixel mutation rejected')
    faults.append(dict(kind='actual_unwritten_target_word',differentWholeWords=1))
    need(np.array_equal(clear(seed,start),target), 'Whole original source-derived positive restored')
    for p in [Path(__file__),Path(disasm.__file__),ROOT/'mame-mkp/unidasm.exe',
              ROOT/'mk2/mk2-maincpu.bin',parent_path,*source_files]:
        key=str(p.resolve());h=sha(p)
        need(key not in pins or pins[key]==h,'No executed source or actual rejection changed');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()), 'Whole inventory remains intact')
    result=dict(passed=True,goalStatus='active',actualNativeIdentity=handle['identity'],nativeExit=0,
        stockClearInstructions={f'{k:08X}':v for k,v in instructions.items()},
        wholeActualHideInterval=rows,exactGapWords=len(rows)*512*512,
        actualLastPhysicalPageErasure=erased,effectiveClearFaultsRejected=faults,
        sourcePredictedStockClearEndpointsAccepted=True,
        nativeShiftRegisterCallbacksIndividuallyCaptured=False,
        originalWriteTapOnlyPenEraseFailurePreserved=True,
        allUnsavedInterPassErasureAccepted=False,allFinisherEffectsOwnershipAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],inputHashes=pins,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS whole70 source-predicted stock clears and both actual last physical page masks',flush=True)
    return result


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual stock-clear rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise

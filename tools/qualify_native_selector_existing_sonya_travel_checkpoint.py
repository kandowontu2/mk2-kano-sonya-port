"""Effective native phase/source/raster faults on retained47172, no replay.

Every phase callback and store is checked in its real startup/ordinary followup
context. Existing square visual samples are real; bicycle art and Sonya RNG
choices remain unobserved in this older capture. All14 requirements stay open.
"""
import json
import re
from pathlib import Path
import qualify_native_selector_existing_sonya_travel_phases_live_start as phases
import read_live_shang_drain_frames as census

ROOT,need,sha=phases.ROOT,phases.need,phases.sha
OUT=ROOT/'audit_native_selector_existing_sonya_travel_checkpoint_checked'
VISUAL=ROOT/'audit_native_selector_existing_sonya_travel_actual_views.json'


def execute(state,capture):
    need(not OUT.exists(),'Fresh immutable actual phase fault checkpoint')
    host=next(r for r in census.census_hosts() if r['ProcessId']==38752)
    need(host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766 and
         host['CommandLine']=='"'+host['ExecutablePath']+'" -B tools/capture_native_selector_special_shadow.py',
         'Exact currently live original retained host')
    folder,text,images=capture.RAM_CASES[capture.KEY]
    held=capture.NATIVE_HANDLES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text())
    prior=json.loads((phases.OUT/'report.json').read_text());pins=dict(prior['inputHashes'])
    need(prior['passed'] and held['process'].poll()==meta['nativeExit']==0 and
         held['identity']==prior['actualNativeIdentity'] and held['identity']['ProcessId']==47172 and
         all(sha(p)==h for p,h in pins.items()),'Exact original terminal game and full input provenance')
    positive=phases.gate(text,state['guest'])
    need(positive==prior['qualification'],'Whole original positive phase evidence unchanged')
    raster=phases.original.pixels.rasters(images,meta['actualScenes'])
    def change(tag,key,value,**where):
        line=next(s for s in text.splitlines() if s.startswith(tag+' ') and
                  all(dict(re.findall(r'(\w+)=([^\s]+)',s)).get(k)==str(v) for k,v in where.items()))
        bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and bad!=line,'Effective mutation of one actual captured field')
        return text.replace(line,bad,1)
    rows=phases.original.ledger.rows(text,'MK2_CPU_PAIR_FIELD')
    def shifted(frame,key):
        row=next(r for r in rows if r['frame']==str(frame))
        return change('MK2_CPU_PAIR_FIELD',key,f'{int(row[key],16)^1:08X}',frame=frame)
    trials=[
        ('square_intro_pose',change('MK2_CPU_PAIR_FIELD','pose','00000000',frame=1967)),
        ('square_rise_y',shifted(1968,'yraw')),
        ('square_flight_x',shifted(1976,'xraw')),
        ('square_flight_pose',change('MK2_CPU_PAIR_FIELD','pose','00000000',frame=1980)),
        ('square_drop_gravity',shifted(2001,'gravity')),
        ('square_regain_lock',change('MK2_CPU_OVERLAP_EVENT','flags','0010',frame=2020,kind='regain',a8='010350A0')),
        ('new_ordinary_setup_owner',change('MK2_CPU_PAIR_FLAG','a8','01000000',frame=2026,slot=2,kind='body')),
        ('new_ordinary_cleanup',change('MK2_CPU_PAIR_FLAG','after','0010',frame=2063,slot=2,kind='flags',before='0010')),
        ('new_ordinary_damage',change('MK2_CPU_ROUND_HEALTH','after','103',frame=2035,slot=1)),
        ('bicycle_intro_x',shifted(2767,'xraw')),
        ('bicycle_intro_pose',change('MK2_CPU_PAIR_FIELD','pose','00000000',frame=2769)),
        ('bicycle_launch_velocity',shifted(2773,'vx')),
        ('bicycle_ceiling_gravity',shifted(2786,'gravity')),
        ('bicycle_fall_pose',change('MK2_CPU_PAIR_FIELD','pose','00000000',frame=2787)),
        ('bicycle_landing_fraction',change('MK2_CPU_OVERLAP_EVENT','yraw','00510000',frame=2827,kind='regain',a8='010350A0')),
        ('bicycle_startup_noop',change('MK2_CPU_PAIR_FLAG','before','0001',frame=2766,slot=2,kind='flags',pc='FF9B3B40')),
    ]
    faults=[]
    for label,bad in trials:
        try:phases.gate(bad,state['guest'])
        except (AssertionError,ValueError,KeyError,IndexError) as error:
            faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual phase corruption accepted: '+label)
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(phases.boundary.adjacent_finish_operand(state['guest'],stock), 'Exact source-derived adjacent finisher operand')
    for label,at in [('fall_byte',0xff876660),('finish_low_word',0xff876b50),
                     ('finish_high_word',0xff876b60),('original_finish_row',0xfffa1900)]:
        bad=bytearray(state['guest']);bad[(at-0xff800000)//8]^=1
        try:phases.boundary.adjacent_finish_operand(bad,stock)
        except (AssertionError,ValueError) as error:
            faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Exact neighboring source corruption accepted: '+label)
    first=meta['actualScenes'][0]['imageKey']
    bad=dict(images);bad[first]=images[first].copy();bad[first][0,0,0]^=1
    missing=dict(images);del missing[first]
    extra=dict(images);extra['invented_callback.png']=images[first]
    for label, sample in [('one_pixel',bad),('missing_raster',missing),('extra_raster',extra)]:
        try:phases.original.pixels.rasters(sample,meta['actualScenes'])
        except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Original callback corruption accepted: '+label)
    need(phases.gate(text,state['guest'])==positive and phases.original.pixels.rasters(images,meta['actualScenes'])==raster,
         'Every untouched original positive phase/raster input restored after faults')
    visual=json.loads(VISUAL.read_text())
    need(visual['passed'] and visual['actualNativeIdentity']==held['identity'] and
         [r['index'] for r in visual['actualViewedCallbacks']]==[24,25] and
         not visual['bicycleVisualReviewAccepted'],'Actual square visuals, bicycle gap remains explicit')
    for row in visual['actualViewedCallbacks']:
        actual=raster[row['index']]
        need(row['header']==actual['header'] and row['SHA256']==actual['header']['sha256'] and
             row['nativeRGBSHA256']==actual['nativeRGBSHA256'] and
             row['actualReconstructedAlpha']==actual['actualReconstructedAlpha'],'Every actual viewed pixel/header bound to original capture')
    paths=[Path(__file__),phases.OUT/'report.json',VISUAL,Path(phases.__file__),Path(census.__file__),
           *(ROOT/'tools'/name for name in ('read_native_selector_cpu_projectile_pcm_frames.py',
                'read_native_selector_cpu_projectile_pcm_frames_bound.py','read_native_selector_cpu_projectile_pcm_frames_remote.py',
                'read_native_selector_cpu_projectile_pcm_frames_bound_remote.py'))]
    for path in paths:
        key=str(path.resolve());digest=sha(path)
        need(key not in pins or pins[key]==digest,'No conflicting historical input pin')
        pins[key]=digest
    need(all(sha(p)==h for p,h in pins.items()),'Fresh final complete current source and evidence pin census')
    OUT.mkdir()
    report=dict(passed=True,qualification=positive,actualFaultsRejected=faults,
                actualNativeIdentity=held['identity'],wholeOriginalRasters=raster,actualSquareVisuals=visual,
                inputHashes=pins,requirements=prior['requirements'],remainingGroups=prior['remainingGroups'],goalStatus='active',
                completeActualSquareBicycleMissMotionAccepted=True,bicycleVisualReviewAccepted=False,
                nativeRNGObservationAccepted=False,directNativeFallTapAccepted=False,
                allContactsArenasAccepted=False,fullAudioAcceptance=False,fullPortAcceptance=False,
                publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newRawMedia=0,newZIPs=0)
    phases.original.artifact.save(OUT/'report.json',report)
    print('PASS actual square/bicycle misses and whole native recovery/ordinary follow-up;23 effective faults; no replay',flush=True)
    return report

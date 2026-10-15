"""Whole natural CPU choice / completed leg pair / state-health / RGB evidence.

One original terminal game, no replay. Whole native logic retained, effective
faults must reject through the real gates. Two ring decisions do not prove
square/bicycle choices or complete art/audio integration for all contexts.
"""
import json
import re
from pathlib import Path
import capture_native_selector_sonya_cpu_choices as capture
import qualify_native_selector_natural_state_health_checkpoint as pixels
import capture_current_subzero_audio_v6213 as artifact
import read_live_shang_drain_frames as census

ROOT,need,sha = capture.ROOT,capture.need,capture.sha
OUT = ROOT / 'audit_native_selector_sonya_choices_pair_checked'
VISUAL = ROOT / 'audit_native_selector_sonya_choices_actual_visual_review.json'


def gate(text,guest):
    whole = capture.native_state.gate(text,guest)
    choices = capture.choices_gate(text,guest,whole['schedule'])
    pair = capture.native_state.original.pair
    complete = pair.rows(text,'COMPLETE')
    need(len(complete) == 1, 'One actually completed leg cycle, no activation-only acceptance')
    leg = pair.verify_pair(text,'kano',complete[0]['cycle'],guest)
    need(leg['passed'] and not leg['errors'] and leg['target'] == 'sonya' and
         leg['held_fields'] == 46 and leg['damage'] == 35,
         'Whole unchanged paired phases, physics, damage and both handoffs: ' + repr(leg['errors']))
    return dict(wholeNativeHealthState=whole,nativeChoices=choices,completedLegPair=leg,
                allThreeSonyaChoiceBranchesAccepted=False,fullPortAcceptance=False)


def execute(state):
    need(not OUT.exists(),'Fresh immutable qualification')
    host = next(r for r in census.census_hosts() if r['ProcessId'] == 38752)
    need(host['ParentProcessId'] == 40316 and host['createdUnix'] == 1791734919.6266766 and
         host['CommandLine'] == '"' + host['ExecutablePath'] + '" -B tools/capture_native_selector_special_shadow.py',
         'Same exact currently live original host, not a timeout replay')
    folder,text,images = capture.RAM_CASES[capture.KEY]
    held = capture.NATIVE_HANDLES[capture.KEY]
    meta = json.loads((folder/'result.json').read_text())
    prior = json.loads((capture.OUT/'report.json').read_text())
    need(meta['passed'] and prior['passed'] and held['process'].poll() == meta['nativeExit'] == 0 and
         held['identity'] == prior['actualNativeIdentity'] == meta['nativeTerminal']['actualWindowsIdentity'] and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix']) ==
         (41544,38752,1791751079.5942783), 'Original exact naturally terminal native handle')
    pins = dict(prior['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'Every original capture input unchanged')
    positive = gate(text,state['guest'])
    raster = pixels.rasters(images,meta['actualScenes'])
    visual = json.loads(VISUAL.read_text())
    need(len(raster)==89 and visual['passed'] and visual['actualNativeIdentity']==held['identity'] and
         [r['index'] for r in visual['actualViewedCallbacks']]==[34,40], 'Whole89 callbacks and actual two-view native identity')
    for row in visual['actualViewedCallbacks']:
        actual = raster[row['index']]
        need(row['header']==actual['header'] and row['SHA256']==actual['header']['sha256'] and
             row['nativeRGBSHA256']==actual['nativeRGBSHA256'] and
             row['actualReconstructedAlpha']==actual['actualReconstructedAlpha'],
             'Actually viewed pixels bound to original whole raw callback digest')
    def change(tag,key,value,**where):
        line = next(s for s in text.splitlines() if s.startswith(tag+' ') and
                    all(dict(re.findall(r'(\w+)=([^\s]+)',s)).get(k)==str(v) for k,v in where.items()))
        bad,n = re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and bad!=line,'Effective real observer-field counterexample')
        return text.replace(line,bad,1)
    first = capture.native_state.rows(text,'MK2_SONYA_CHOICE_EVENT')[0]
    first_hp = capture.native_state.rows(text,'MK2_CPU_ROUND_HEALTH')[0]
    complete = positive['completedLegPair']
    trials = [
        ('choice_owner',change('MK2_SONYA_CHOICE_EVENT','owner','01000000',serial=1,kind='entry')),
        ('choice_opcode',change('MK2_SONYA_CHOICE_EVENT','opcode','FFFF',serial=1,kind='entry')),
        ('choice_mask',change('MK2_SONYA_CHOICE_EVENT','mask','FFFE',serial=1,kind='entry')),
        ('choice_threshold',change('MK2_SONYA_CHOICE_EVENT','a0','000000FB',serial=1,kind='first_call')),
        ('choice_return_carry',change('MK2_SONYA_CHOICE_EVENT','carry','1',serial=1,kind='first_result')),
        ('choice_final_branch',change('MK2_SONYA_CHOICE_EVENT','kind','square',serial=1,kind='ring')),
        ('choice_serial_gap',change('MK2_SONYA_CHOICE_EVENT','serial','3',serial=2,kind='entry')),
        ('choice_false_total',change('MK2_SONYA_CHOICE_RESULT','choices','3')),
        ('choice_missing_entry',text.replace(next(s+'\n' for s in text.splitlines()
             if s.startswith('MK2_SONYA_CHOICE_EVENT ') and 'kind=entry' in s),'',1)),
        ('whole_health_store',change('MK2_CPU_ROUND_HEALTH','op0','FFFF',frame=first_hp['frame'],slot=first_hp['slot'])),
        ('whole_health_unexplained',change('MK2_CPU_ROUND_FIELD','hp','160',frame=1818,slot=1)),
        ('pair_held_pose',change('MK2_CPU_PAIR_FIELD','pose','00000000',cycle=complete['cycle'],frame=2603)),
        ('pair_release_damage',change('MK2_CPU_PAIR_EVENT','a10','00000022',cycle=complete['cycle'],kind='damage')),
        ('pair_victim_handoff_lock',change('MK2_CPU_PAIR_VICTIM_REGAIN','vbody','00000004',cycle=complete['cycle'])),
        ('pair_fling_velocity',change('MK2_CPU_PAIR_EVENT','a1','FFFB0000',cycle=complete['cycle'],kind='fling')),
    ]
    faults=[]
    for label,bad in trials:
        need(bad!=text,'Changed actual native evidence')
        try:gate(bad,state['guest'])
        except (ValueError,AssertionError,KeyError,IndexError) as error:
            faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native fault accepted: '+label)
    first_key=meta['actualScenes'][0]['imageKey']
    bad_images=dict(images);bad_images[first_key]=images[first_key].copy();bad_images[first_key][0,0,0]^=1
    try:pixels.rasters(bad_images,meta['actualScenes'])
    except ValueError as error:faults.append(dict(fault='one_original_native_pixel',rejectedBy=str(error)))
    else:raise ValueError('Actual native raster corruption accepted')
    need(gate(text,state['guest'])==positive and pixels.rasters(images,meta['actualScenes'])==raster,
         'Every positive whole native/raster input restored after actual faults')
    paths=[Path(__file__),VISUAL,capture.OUT/'report.json',Path(pixels.__file__),Path(artifact.__file__),
           ROOT/'tools/read_native_selector_sonya_choices_frames.py',ROOT/'tools/read_native_selector_sonya_choices_frames_remote.py',
           *(p for p in folder.rglob('*') if p.is_file())]
    for path in paths:
        key=str(path.resolve());digest=sha(path)
        need(key not in pins or pins[key]==digest,'No historical pin silently replaced')
        pins[key]=digest
    need(all(sha(p)==h for p,h in pins.items()),'Fresh final complete source/candidate/input census')
    OUT.mkdir()
    report=dict(passed=True,qualification=positive,actualNativeIdentity=held['identity'],
                wholeOriginalRasters=raster,actualVisualReview=visual,actualFaultsRejected=faults,inputHashes=pins,
                requirements=prior['requirements'],remainingGroups=prior['remainingGroups'],goalStatus='active',
                completedLegPairAccepted=True,completedAllGrabContexts=False,allThreeSonyaChoiceBranchesAccepted=False,
                fullArtAudioAcceptance=False,fullPortAcceptance=False,publicPlayableChanged=False,
                newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    artifact.save(OUT/'report.json',report)
    print('PASS actual Sonya native ring choices + complete leg pair, whole state/health/89rasters and16faults; wider goal active',flush=True)
    return report

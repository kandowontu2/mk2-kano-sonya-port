"""Negative checks of the accepted consecutive-phase/native-clipping proof."""
import json,re
from pathlib import Path
import verify_human_special_phases_v1767 as checked
ROOT=checked.ROOT;OUT=ROOT/'audit_v1768_human_special_phase_units_checked'

if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite evidence'
    proofpath=ROOT/'audit_v1767_human_special_phases_checked/report.json'
    proof=json.loads(proofpath.read_text());assert proof['passed']and proof['allEightMovesBothSlots']and proof['airborneSquareBothSlots']
    pins={str(proofpath):checked.sha(proofpath)}
    for p,h in proof['inputHashes'].items():assert checked.sha(p)==h;pins[p]=h
    guest,_,payload=checked.current.expected();tests=[]
    def reject(label,folder,text):
        try:checked.verify_case(folder,guest,payload,{},text)
        except (AssertionError,ValueError,IndexError,KeyError)as error:
            tests.append(dict(label=label,rejected=True,error=str(error)))
        else:raise AssertionError('Corruption accepted: '+label)
    leg=ROOT/'audit_v1760_human_leg_p1';ball=ROOT/'audit_v1765_human_ball_p2'
    lt=(leg/'run.log').read_text(encoding='utf-8-sig');bt=(ball/'run.log').read_text(encoding='utf-8-sig')
    for folder,text in((leg,lt),(ball,bt)):checked.verify_case(folder,guest,payload,{},text)
    select=lambda text,tag:next(line for line in text.splitlines(True)if line.startswith('MK2_HPHASE_'+tag+' '))
    snap=select(lt,'SNAP');actor=select(lt,'ACTOR');queue=select(lt,'QUEUE');candidate=select(bt,'CANDIDATE')
    reject('missing_consecutive_scene',leg,lt.replace(snap,'',1))
    reject('duplicated_scene',leg,lt.replace(snap,snap+snap,1))
    reject('wrong_rendered_actor_id',leg,lt.replace(actor,re.sub(r'\bid=\d+','id=1',actor),1))
    reject('wrong_rendered_main_owner',leg,lt.replace(actor,re.sub(r'\bowner=[0-9A-F]+','owner=01000000',actor),1))
    reject('changed_native_sprite_source',leg,lt.replace(queue,re.sub(r'\bsource=[0-9A-F]+','source=00000000',queue),1))
    reject('missing_visible_native_body_component',leg,lt.replace(queue,'',1))
    reject('missing_actor_scene_state',leg,lt.replace(actor,'',1))
    reject('nonzero_observer_write_declaration',leg,lt.replace(snap,snap.replace('writes=0','writes=1'),1))
    reject('wrong_actual_clip_bounds',ball,bt.replace(candidate,re.sub(r'\bclipHigh=[0-9A-F]+','clipHigh=00FE0200',candidate),1))
    bqueue=select(bt,'QUEUE')
    reject('changed_native_flip_display_coordinate',ball,bt.replace(bqueue,re.sub(r'\bxy=[0-9A-F]+','xy=00000000',bqueue),1))
    reject('duplicated_native_clip_candidate',ball,bt.replace(candidate,candidate+candidate,1))
    crows=checked.rows(bt,'CANDIDATE');qkeys={(q['frame'],q['slot'],q['part'])for q in checked.rows(bt,'QUEUE')}
    culled=next(c for c in crows if(c['frame'],c['slot'],c['part'])not in qkeys)
    culled_line=next(line for line in bt.splitlines(True)if line.startswith('MK2_HPHASE_CANDIDATE ')and
                     f'frame={culled["frame"]} 'in line and f'slot={culled["slot"]} 'in line and f'part={culled["part"]} 'in line)
    reject('missing_actually_culled_component',ball,bt.replace(culled_line,'',1))
    reject('wrong_actual_native_clip_pc',ball,bt.replace(candidate,candidate.replace('pc=FF8042B0','pc=FF804420'),1))
    observer=(ROOT/'mk2ks_human_special_phases_v1758.lua').read_text()
    changed=observer.replace('local phase_snaps=0','local phase_snaps=0\nfields[1].Up:set_value(1)',1)
    try:checked.check_observer(changed,1758)
    except AssertionError:tests.append(dict(label='extra_physical_control_in_observer',rejected=True))
    else:raise AssertionError('Additional input code accepted')
    for p in(Path(__file__),ROOT/'tools/verify_human_special_phases_v1767.py'):pins[str(p)]=checked.sha(p)
    report=dict(passed=True,baselines=2,corruptionsRejected=len(tests),tests=tests,inputHashes=pins,
                guestOrGameInputsMutated=False,fullPortAcceptance=False,
                scope='In-memory negative tests of consecutive captures, actual identity/ownership/composites, complete native clipping and unchanged physical controls; no universal raster/art/audio acceptance')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','tests')},indent=2),flush=True)

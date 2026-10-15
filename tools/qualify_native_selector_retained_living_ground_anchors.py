"""Living ordinary stance/walk anchors; preserve distinct native KO reaction."""
import copy
import hashlib
import json
import struct
import traceback
from pathlib import Path
import qualify_native_selector_fresh_lowkick_controls as controls
import verify_native_source_sync as sync

OUT=sync.ROOT/'audit_native_selector_retained_living_ground_anchors_checked'


def gate(fields,guest,stock):
    pointer=struct.unpack_from('<I',guest,(0xff907f70-0xff800000)//8)[0]
    at=(pointer-0xff800000)//8
    table=struct.unpack_from('<19H',guest,at)
    stock_at=(0xff908010-0xff800000)//8
    sync.need(guest[at:at+34]==stock[stock_at:stock_at+34] and table[17:]==(134,135),
              'All original native floor entries unchanged; true added stance anchors')
    low,high=(0xffa0dce0-0xff800000)//8,(0xffa0dd40-0xff800000)//8
    sync.need(guest[low:high]==stock[low:high], 'Whole original eight-pixel reaction adjustment code retained')
    counts={1:0,2:0}; exceptions=[]
    for r in fields:
        sync.need((r['vid'],r['id'])==(17,18),'Actual actors are true Kano/Sonya')
        for slot in (1,2):
            identity=r['vid'] if slot==1 else r['id']
            hp=r['vhp'] if slot==1 else r['hp']
            action=r['vaction'] if slot==1 else r['action']
            body=r['vbody'] if slot==1 else r['body']
            flags=r['vflags'] if slot==1 else r['flags']
            floor=r['vfloor'] if slot==1 else r['floor']
            y=r['vypos'] if slot==1 else r['y']
            vy=r['vvy'] if slot==1 else r['vy']
            gravity=r['vgravity'] if slot==1 else r['gravity']
            trail=r['vtrail'] if slot==1 else r['trail']
            ordinary=hp>0 and action in (0,0x303) and body&12==0 and flags&0x1c==0 and y==floor and vy==gravity==trail==0
            if ordinary:
                counts[slot]+=1
                sync.need(floor+table[identity]==r['stage_floor'],'Every actual living ordinary anchor matches stage baseline')
            if floor+table[identity]!=r['stage_floor']:
                exceptions.append(dict(frame=r['frame'],slot=slot,hp=hp,action=action,floor=floor,stage=r['stage_floor']))
    sync.need(all(counts.values()),'Both physical slots exercise living ordinary grounded states')
    return dict(actualFields=len(fields),ordinaryGroundedFields=counts,
                nonOrdinaryAnchorExceptions=len(exceptions),firstExceptions=exceptions[:2],
                originalNativeFloorEntriesPreserved=17,actualAddedStanceAnchors=[134,135],
                individualReactionFloorWriteTapAccepted=False,graphicalSoleParityAccepted=False,
                allStageAcceptance=False,fullPortAcceptance=False)


def main(lowkick,highkick):
    try:
        sync.need(not OUT.exists(),'Fresh scoped living-ground proof')
        parents=[sync.ROOT/'audit_native_selector_fresh_lowkick_controls_checked/report.json',
                 sync.ROOT/'audit_native_selector_fresh_highkick_controls_checked/report.json']
        proofs=[json.loads(p.read_text()) for p in parents]; pins={}
        for proof in proofs:
            sync.need(proof['passed'],'Actual control-qualified recording')
            for p,h in proof['inputHashes'].items():
                sync.need(p not in pins or pins[p]==h,'Whole shared capture pins agree');pins[p]=h
        sync.need(all(sync.sha(p)==h for p,h in pins.items()),'Whole actual inputs unchanged')
        stock_path=sync.ROOT/'mk2/mk2-maincpu.bin';stock=stock_path.read_bytes(); positives=[];faults=[]
        for n,prepared in enumerate((lowkick,highkick)):
            key=prepared.SCOPE['KEY'];handle=prepared.NATIVE_HANDLES[key]
            sync.need(handle['process'].poll()==0 and handle['identity']==proofs[n]['actualNativeIdentity'],'Same actual terminal, no replay')
            fields=controls.ledger.original.pair.rows(prepared.RAM_CASES[key][1],'FIELD')
            guest=prepared.STATE['guest']
            sync.need(hashlib.sha256(guest).hexdigest().upper()=='45DFC25120FD2A56E895B094AF7DC40AD2DC97E452F742F473BFB43216DCCF0A',
                      'Whole independently cold-qualified current guest')
            positive=gate(fields,guest,stock);positives.append(dict(identity=handle['identity'],**positive))
            for label,slot in (('wrong_Kano_floor',1),('wrong_Sonya_floor',2)):
                bad=copy.deepcopy(fields)
                row=next(r for r in bad if (r['vaction'] if slot==1 else r['action']) in (0,0x303)
                    and (r['vhp'] if slot==1 else r['hp'])>0
                    and (r['vbody'] if slot==1 else r['body'])&12==0
                    and (r['vflags'] if slot==1 else r['flags'])&0x1c==0
                    and (r['vypos'] if slot==1 else r['y'])==(r['vfloor'] if slot==1 else r['floor'])
                    and (r['vvy'] if slot==1 else r['vy'])==(r['vgravity'] if slot==1 else r['gravity'])==(r['vtrail'] if slot==1 else r['trail'])==0)
                floor_key,y_key=('vfloor','vypos') if slot==1 else ('floor','y')
                row[floor_key]+=1; row[y_key]+=1
                try:gate(bad,guest,stock)
                except AssertionError as error:faults.append(dict(recording=n,label=label,rejected=str(error)))
                else:raise AssertionError('Floor fault admitted')
            sync.need(gate(fields,guest,stock)==positive,'Full original field positive restored')
        for p in (Path(__file__),stock_path,*parents):pins[str(p.resolve())]=sync.sha(p)
        sync.need(all(sync.sha(p)==h for p,h in pins.items()),'Whole original/fresh evidence unchanged')
        report=dict(passed=True,actualRecordingPositives=positives,effectiveFaults=faults,inputHashes=pins,
                    livingOrdinaryPhysicalAnchorsAccepted=True,graphicalSoleParityAccepted=False,
                    reactionKOPhysicalAnchorsAccepted=False,fullPortAcceptance=False,newGames=0,newBuilds=0)
        OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report
    except BaseException:
        OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=traceback.format_exc()),indent=2)+'\n');raise

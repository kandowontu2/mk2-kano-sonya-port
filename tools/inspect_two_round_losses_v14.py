"""Limited real loss-flow observations; no complete campaign or pixel acceptance."""
import json
import verify_ko_round_floor_shadows as v
import inspect_ground_presentation as p

def inspect(fighter):
    folder=v.ROOT/f'audit_v466_two_round_loss_{fighter}_p1'
    v.matched(folder);log=v.read(folder);identity={'kano':17,'sonya':18}[fighter]
    fields=p.rows(log,'FIELD');health=p.rows(log,'HEALTH');modes=p.rows(log,'MODE')
    for r in fields:
        v.need(r['id']==r['roster']==(identity if r['slot']==1 else 4) and r['owner']==r['actor'],
               'Correct actual identity and Main owner through both defeats')
        v.need(r['state']==(2 if r['slot']==1 and r['mode']==3 else 1),'Native lost-player controller transition')
    decreases=[r for r in health if r['before']<=161 and r['before']>r['after']]
    v.need([(r['before'],r['after']) for r in decreases]==[(161,121),(121,81),(81,41),(41,1),(1,0)]*2 and
           all(r['slot']==1 and r['pc']==0xff836700 for r in decreases),'Ten real native uppercut health writes')
    v.need(p.rows(log,'SECOND_KO')[0]['frame']==4889,'Actual second KO')
    v.need([(r['frame'],r['mode']) for r in modes]==[(1472,2),(2900,5),(3204,6),(3205,7),(3301,2),(5059,5),(5369,3)],
           'Native round reset, second winner scene and continue state')
    v.need(all(r['hp']==0 for r in fields if r['slot']==1 and r['frame']>=4889),'No post-defeat health assistance')
    v.need(p.rows(log,'RESULT')[0]['frame']==6189 and len(p.rows(log,'SNAP'))==313,'Complete declared diagnostic run')
    out=folder/'observations.json';v.need(not out.exists(),'Do not overwrite diagnostic evidence')
    proof=dict(fighter=fighter,side=1,candidate=v.NAME,executable_sha256=v.EXE,payload_sha256=v.PAYLOAD,
               realUppercuts=10,secondKO=4889,nativeContinueState=5369,participantFields=len(fields),nativeSizeSnapshots=313,
               importedIdentityPreservedThroughNativeDefeat=True,assistance='none',
               continueScreenVisualInspection='Kano ground_5600.png shows 2 KREDITS TO KONTINUE; Sonya pixel/visual acceptance still pending',
               fullPortAcceptance=False,scope='Diagnostic two real human round losses and native continue state; not continue purchase/reselect, finisher, full campaign, all arenas, or independent complete pixel proof',
               nextAction='New input-only continue probe: mode3/state2 at frame5369; coins at ages20 and270, START at310; inspect actual CSS then route/select opposite added fighter and verify actual match/Main/controller/identity and cleared selection art')
    out.write_text(json.dumps(proof,indent=2)+'\n');return proof

if __name__=='__main__':print(json.dumps([inspect(f) for f in ('kano','sonya')],indent=2))

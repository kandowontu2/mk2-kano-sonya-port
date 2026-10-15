"""Finite scalar/image bindings only; manual visual receipt remains separate."""
import hashlib
import json
import re
import struct
import verify_native_source_sync as sync

root=sync.ROOT
case=root/'audit_current_human_laser_four_png_v3_runtime'
prep=root/'audit_current_human_laser_four_png_v3_preparation'
out=root/'audit_current_human_laser_four_png_v3_checked'
def need(v,m):
    if not v: raise ValueError(m)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',x)) for x in text.splitlines() if x.startswith('MK2_LASER_'+tag+' ')]
def contract(text,errors):
    need(not errors.strip() and '[LUA ERROR]' not in text,'No observer errors')
    entries=rows(text,'ENTRY');need(len(entries)==1,'One earned actual entry');e=entries[0]
    need(e['frame']=='3046' and e['hp']=='161,0' and e['gap']=='149','True earned KO admission')
    hp=rows(text,'HEALTH')
    dmg=[x for x in hp if x['slot']=='2' and x['pc']=='FF836700' and int(x['frame'])<3046]
    need(sum(max(0,int(x['before'])-int(x['after'])) for x in dmg)==322 and sum(x['after']=='0' for x in dmg)==2,'Two physically earned KO rounds,322 native damage')
    h=[x for x in rows(text,'HISTORY') if x['frame']=='3046']
    need([x['wanted'] for x in h]==['3','2','2','1'] and all(x['wanted']==x['actual'] for x in h),'Native button command history')
    ready=rows(text,'COMMAND_READY');need(len(ready)==1,'One legal command spacing');start=int(ready[0]['frame'])
    ins=rows(text,'INPUT')
    command=[(int(x['frame']),x['key']) for x in ins if start<=int(x['frame'])<=3046]
    need(command==[(start+a+d,k) for a,k in [(10,'Low_Punch'),(18,'Block'),(26,'Block'),(34,'High_Kick')] for d in range(3)],'Physical command releases')
    phases=rows(text,'PHASE_RAW')
    need([x['cue'] for x in phases]==['6B40','6B41','6B42','6B43','6B44'],'All actual phase markers')
    for x in phases:
        victim=x['cue'] in ('6B42','6B43','6B44')
        need(x['actor']==e['victim' if victim else 'actor'] and x['main']==e['victim_main' if x['cue']=='6B42' else 'main'],'Per-phase actual register ownership')
    need(len(rows(text,'PHASE_OWNED'))==5,'All phases admitted with true body ownership')
    fields=rows(text,'FIELD')
    for slot,ident,actor,main,bank,hpv in [('1','17',e['actor'],e['main'],'0202','161'),('2','18',e['victim'],e['victim_main'],'0303','0')]:
        own=[x for x in fields if x['slot']==slot and int(x['age'])<=450]
        need([int(x['age']) for x in own]==list(range(451)),'Complete body followthrough')
        need(all((x['id'],x['roster'],x['actor'],x['main'],x['bank'],x['hp'])==(ident,ident,actor,main,bank,hpv) for x in own),'No proxy or body replacement')
        if slot=='2': need(all(int(x['body'],16)&0x20 for x in own if int(x['age'])>=164),'Victim hidden after native burst')
        else: need(all(x['child']=='00000000' for x in own if int(x['age'])>=196),'Owned beam attachment cleared')
    win=rows(text,'WINNER');need(len(win)==1 and win[0]['frame']=='3242' and win[0]['main']==e['main'],'On-time owned native winner')
    clean=rows(text,'CLEANUP')
    need(all(any(x['age']=='196' and x['job']==e['main'] and x['kernel']==k for x in clean) for k in ['FF83EFD0','FF840450','FF80E0E0']),'Actual owned native cleanup calls')
    cap=rows(text,'CAPTURE')
    need([(x['label'],x['frame'],x['mode']) for x in cap]==[('charge','3070','2'),('beam','3118','2'),('burst','3222','2'),('next_paid_selection','3849','4')],'Actual phase and nextscene image order')
    modes=rows(text,'MODE');need(any(x['mode']=='3' and x['frame']=='3666' for x in modes) and any(x['mode']=='4' and x['frame']=='3749' for x in modes),'Actual continue to selection')
    paid=[(int(x['frame']),x['slot'],x['key']) for x in ins if int(x['frame'])>3242]
    need(paid==[(f,'2','Coin') for f in list(range(3686,3690))+list(range(3716,3720))]+[(f,'2','Start') for f in range(3746,3749)],'Only physical paid nextscene input')
    need(rows(text,'RESULT')[0]['frame']=='3850','Bounded normal result')
    return dict(entry=e,ownedWinner=win[0],nativeDamage=322,earnedKORounds=2,phaseCues=[x['cue'] for x in phases],captures=cap,stableTrueBodiesThroughAge=450)

def main():
    need(not out.exists(),'Fresh immutable qualifier')
    sync.verify()
    text=(case/'run.log').read_text();errors=(case/'stderr.log').read_text()
    result=contract(text,errors)
    faults=[]
    changes=[('observer_error',text,'[LUA ERROR] synthetic'),('phase_context',text.replace('cue=6B43 pc=FFD87570 actor=010350A0','cue=6B43 pc=FFD87570 actor=01034E90',1),errors),('missing_ko',text.replace('after=0 pc=FF836700','after=1 pc=FF836700',1),errors),('wrong_history',text.replace('wanted=3 actual=3','wanted=3 actual=2',1),errors),('missing_burst',text.replace('MK2_LASER_CAPTURE frame=3222','OMITTED_CAPTURE frame=3222',1),errors),('late_winner',text.replace('MK2_LASER_WINNER frame=3242','MK2_LASER_WINNER frame=3243',1),errors)]
    for label,t,err in changes:
        need(t!=text or err!=errors,'Effective mutation '+label)
        try:contract(t,err)
        except ValueError as exc:faults.append(dict(label=label,rejected=str(exc)))
        else:raise ValueError('Fault admitted '+label)
    terminal=json.loads((case/'terminal.json').read_text())
    need(terminal['limitReason'] is None and terminal['peakWorkingSetBytes']<=320*1024**2 and terminal['elapsedSeconds']<=180 and terminal['logBytes']<=10*1024**2,'Finite resources')
    need(terminal['observerSha256']==sha(prep/'campaign.lua'),'Actual observer hash')
    pngs=sorted(case.glob('*.png'));need(len(pngs)==4 and sum(p.stat().st_size for p in pngs)<=256*1024,'Four bounded PNG')
    for p in pngs:
        b=p.read_bytes();need(b[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',b[16:24])==(400,254),'Native image geometry')
    pins=[case/'run.log',case/'stderr.log',case/'terminal.json',prep/'campaign.lua',prep/'run.ps1',sync.BUILD/'mkport_candidate.exe',*pngs]
    report=dict(passed=True,finiteEarnedHumanLaserSceneBindingAccepted=True,manualVisualReviewRequiredSeparately=True,contract=result,faultsRejected=faults,terminal=terminal,pngBytes=sum(p.stat().st_size for p in pngs),inputHashes={str(p):sha(p) for p in pins},scope='Owned actual native phases, true KO/physical command, hide/beam-child cleanup, native winner and paid nextscene image bindings. Root separately viewed four actual images. No allpool retirement, heardaudio, CPU universality or fullport claim; zero placeholder counters ignored.',allPoolRetirementAccepted=False,heardAudioAccepted=False,fullPortAccepted=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2))
    print(out,len(faults))
if __name__=='__main__':main()

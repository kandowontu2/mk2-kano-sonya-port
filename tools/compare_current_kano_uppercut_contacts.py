"""Existing native health-writer observations following owned uppercut entries."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
proofs=[]
for case in ('close_guard','late_punish'):
    path=sync.ROOT/('audit_current_kano_kitana_'+case+'_runtime/run.log')
    rows=chronology.load(path)
    arrival=int(next(r['frame'] for r in rows['STAGE'] if r['stage']=='3'))
    assert max(int(r['stage']) for r in rows['STAGE'])==3
    entries=rows['KANO_CLOSE_NATIVE_UPPER']
    assert len(entries)==3 and all(r['id']=='17' and r['owner']==r['actor'] for r in entries)
    ledger=[r for r in rows['HEALTH'] if int(r['frame'])>=arrival and r['pc']=='FF836700' and int(r['before'])>int(r['after'])]
    windows=[]
    for entry in entries:
        frame=int(entry['frame'])
        contacts=[r for r in ledger if r['slot']=='2' and 0<=int(r['frame'])-frame<=30 and r['a8']==entry['actor'] and r['a13']==entry['main']]
        windows.append(dict(entryFrame=frame,contacts=contacts,
                            nativeDamage=sum(int(r['before'])-int(r['after']) for r in contacts)))
    proofs.append(dict(case=case,logSHA256=sync.sha(path),nativeUppercutWindows=windows,
                       allIncomingNativeDamage=sum(int(r['before'])-int(r['after']) for r in ledger if r['slot']=='1'),
                       allOutgoingNativeDamage=sum(int(r['before'])-int(r['after']) for r in ledger if r['slot']=='2'),
                       ownKitanaRoundWins=[r for r in rows['WIN'] if r['stage']=='3' and r['slot']=='1']))
out=sync.ROOT/'audit_current_kano_uppercut_contact_comparison'
assert not out.exists();out.mkdir()
report=dict(passedOwnedEntryHealthCorrelation=True,cases=proofs,
            blockingVersusMissProven=False,exactUppercutCallbackAtDamageProven=False,
            scope='Actual FF836700 reductions by same physical actor/Main within30fields of native upper entry. Not a block/miss classifier; absence of health reduction alone cannot distinguish those.',
            fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))

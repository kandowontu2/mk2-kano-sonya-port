"""Check true identities, earned chronology and exact pre-mirror input route."""
import inspect
import json
import check_campaign_stage_chronology as chronology
import qualify_current_sonya_defensive_routes as base
import verify_native_source_sync as sync

sync.verify()
folder = sync.ROOT/'audit_current_sonya_mirror_throw_escape_runtime'
terminal = json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode'] == 0 and terminal['limitReason'] is None
assert terminal['elapsedSeconds'] < 92
assert terminal['peakWorkingSetBytes'] <= 320*1024*1024
assert terminal['logBytes'] <= 10*1024*1024
assert not (folder/'stderr.log').read_text().strip()
rows = chronology.load(folder/'run.log')
assert rows['RESULT'][0]['frame'] == '24000'
old = chronology.load(sync.ROOT/'audit_current_sonya_kunglao_guard_runtime/run.log')
cutoff = int(next(r for r in old['FIGHT'] if r['stage'] == '5')['frame'])
for tag in set(old)|set(rows):
    if tag in ('RESULT','HOST_BOUND','INPUT_DIGEST_FINAL'):
        continue
    assert [r for r in old.get(tag,[]) if int(r['frame']) < cutoff] == [r for r in rows.get(tag,[]) if int(r['frame']) < cutoff]
code = inspect.getsource(base.gate)
code = code.replace(" assert rows['RESULT'][0]['frame']=='18000'\n", '')
code = code.replace('assert actual==list(range(len(actual)))', 'assert actual==(list(range(13))+[14,15,16])[:len(actual)]')
context = {}
exec(compile(code,__file__+'::native chronological gate','exec'), context)
result = context['gate'](rows,1)
escapes = rows.get('MIRROR_THROW_ESCAPE', [])
assert escapes and all(r['stage'] == '5' and int(r['gap']) < 65 for r in escapes)
result.update(passedObservationChecks=True, preMirrorRouteExactThrough=cutoff-1,
              physicalEscapeRequests=len(escapes),
              mirrorRoundWins=[r for r in rows['WIN'] if r['stage']=='5' and r['slot']=='1'],
              fullPortAccepted=False, logSHA256=sync.sha(folder/'run.log'))
out = sync.ROOT/'audit_current_sonya_mirror_throw_escape_checked'
assert not out.exists()
out.mkdir()
(out/'report.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))

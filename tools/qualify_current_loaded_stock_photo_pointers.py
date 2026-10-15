"""Actual loaded stock rows, not transferred whole-route acceptance."""
import json,re
import verify_native_source_sync as sync
sync.verify()
prep=sync.ROOT/'audit_current_loaded_stock_photo_pointers_preparation'
case=sync.ROOT/'audit_current_loaded_stock_photo_pointers_runtime'
out=sync.ROOT/'audit_current_loaded_stock_photo_pointers_checked'
assert not out.exists()
expected=json.loads((prep/'expected.json').read_text())
assert expected['stockSHA256']==sync.sha(sync.ROOT/'mk2/mk2-maincpu.bin')
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (case/'stderr.log').read_text().strip()
text=(case/'run.log').read_text();assert 'LUA ERROR' not in text
rows=[dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in text.splitlines() if s.startswith('MK2_PHOTO_ROW ')]
values=[int(r['value'],16) for r in rows]
assert [int(r['index']) for r in rows]==list(range(41))
assert values==expected['values']
assert 'MK2_PHOTO_OPERAND value=FFFA4800 writes=0 assistance=none' in text
bad=values.copy();bad[40]=0
assert bad!=expected['values']
report=dict(original41StockPhotoPointersExactlyLoaded=True,row40Preserved=True,
    originalLookupRoutedToActualTable=True,row40DeletionFaultRejected=True,
    tableSHA256=sync.sha(prep/'expected.json'),logSHA256=sync.sha(case/'run.log'),
    terminal=terminal,fullSecretRouteAcceptance=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

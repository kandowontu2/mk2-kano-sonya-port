"""Physically earned original Kano finisher at observed native spacing."""
import code
import inspect
import json
import re
import capture_native_secondary_kano_reference as previous

previous.OUT=previous.ROOT/'audit_native_secondary_kano_command_checked'
previous.LUA=previous.ROOT/'mk3_native_secondary_kano_command_checked.lua'

def run():
    root=previous.ROOT
    receipts=[root/name/'report.json'for name in ('audit_native_secondary_kano_reference','audit_native_secondary_kano_raster_checked')]
    for path in receipts:
        report=json.loads(path.read_text())
        previous.need(report['nativeExit']==0 and report['originalWholeGuestMatched'] and
                      all(previous.sha(p)==h for p,h in report['inputHashes'].items()),
                      'Both actually executed prior ordinary-input trials terminal0, full original program and all loaded source frozen')
    import gzip
    with gzip.open(root/'audit_native_secondary_kano_raster_checked/run.log.gz','rt')as stream:text=stream.read()
    rows=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK3_SECONDARY_FINISH_WINDOW ')]
    previous.need(any(row['frame']=='5246'and row['ids']=='0,1'and row['hp']=='166,0'and row['x']=='866,929'and row['finish']=='3'for row in rows),
                  'Actual earned native finish window demonstrates63pixel body separation, not guessed contact geometry')
    replacements=[("local raw,w,h=machine.screens[':screen']:pixels()",
                   "local screen=machine.screens[':screen'];local raw=screen:pixels();local w,h=screen.width,screen.height"),
                  ('if gap>45 then press(forward)','if gap>65 then press(forward)'),
                  ('if gap>20 then press(forward)','if gap>65 then press(forward)')]
    baseline=(root/'mk3_native_secondary_kano_reference.lua').read_text()
    wrapper=previous.LUA.read_text()
    previous.need("local filename='mk3_native_secondary_kano_reference.lua'"in wrapper,'Same frozen original physical controller')
    transformed=baseline
    expression="(ROOT/'mk3_native_secondary_kano_reference.lua').read_text()"
    for old,new in replacements:
        previous.need(transformed.count(old)==1 and old in wrapper and new in wrapper,'Only explicit raster ABI/combat and finish physical spacing replacements')
        transformed=transformed.replace(old,new)
        expression+='.replace('+repr(old)+','+repr(new)+')'
    source=inspect.getsource(previous.run)
    changes=[('source=LUA.read_text()','source='+expression),
             ("ROOT/'audit_native_secondary_finisher_reference/report.json']",
              "ROOT/'audit_native_secondary_finisher_reference/report.json', ROOT/'mk3_native_secondary_kano_reference.lua', ROOT/'tools/capture_native_secondary_kano_reference.py', ROOT/'audit_native_secondary_kano_reference/report.json', ROOT/'audit_native_secondary_kano_raster_checked/report.json']")]
    for old,new in changes:
        previous.need(source.count(old)==1,'Unique explicit controller/provenance specialization')
        source=source.replace(old,new)
    scope=dict(vars(previous),__file__=__file__)
    exec(compile(source,__file__+'::physical_command_checked','exec'),scope)
    return scope['run']()

if __name__=='__main__':
    capture=run()
    code.interact(banner='Original native command attempt terminal; whole actual frames retained in RAM.',local=dict(capture=capture))

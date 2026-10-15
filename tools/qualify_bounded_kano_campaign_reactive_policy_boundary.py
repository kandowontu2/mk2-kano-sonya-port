"""Native stage updates before later LIVE stage marker; bind actual policy edge."""
from pathlib import Path
original=Path(__file__).with_name('qualify_bounded_kano_campaign_reactive.py')
source=original.read_text()
before="cutoff=int(fields(next(line for line in old.splitlines() if line.startswith(prefix+'STAGE') and fields(line)['stage']=='3'))['frame'])"
assert source.count(before)==1
source=source.replace(before,"cutoff=int(fields(next(line for line in text.splitlines() if line.startswith(prefix+'POLICY')))['frame'])")
source=source.replace("'audit_bounded_kano_campaign_reactive_checked'","'audit_bounded_kano_campaign_reactive_policy_boundary_checked'")
source=source.replace('Exact old prefix through stage3 arrival; later controller policy only changes normal inputs','Exact old prefix through native policy boundary; reactive attempt remains bounded, no full clear')
source=source.replace('earlier zoning/gameplay/input digests exactly unchanged','earlier zoning/gameplay/input digests exactly unchanged through actual native policy boundary')
exec(compile(source,str(original),'exec'),{'__name__':'__main__','__file__':str(original)})

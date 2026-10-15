"""Apply original earned campaign gates at actual native physical-policy edge."""
from pathlib import Path
original=Path(__file__).with_name('qualify_bounded_kano_campaign_reactive.py')
source=original.read_text()
source=source.replace('audit_bounded_kano_campaign_reactive_p1_runtime','audit_bounded_kano_campaign_uppercut_p1_runtime')
source=source.replace('audit_bounded_kano_campaign_reactive_checked','audit_bounded_kano_campaign_uppercut_checked')
source=source.replace("policy[0]['physical_policy']=='reactive_jumpkick'","policy[0]['physical_policy']=='grounded_uppercut'")
before="cutoff=int(fields(next(line for line in old.splitlines() if line.startswith(prefix+'STAGE') and fields(line)['stage']=='3'))['frame'])"
assert source.count(before)==1
source=source.replace(before,"cutoff=int(fields(next(line for line in text.splitlines() if line.startswith(prefix+'POLICY')))['frame'])")
source=source.replace('physical reactive policy from natural stage3','physical grounded uppercut policy from native stage3')
source=source.replace('earlier zoning/gameplay/input digests exactly unchanged','earlier zoning/gameplay/input digests unchanged through actual policy boundary')
source=source.replace('Exact old prefix through stage3 arrival; later controller policy only changes normal inputs','Exact old prefix through actual native policy boundary; later inputs use grounded uppercuts')
exec(compile(source,str(original),'exec'),{'__name__':'__main__','__file__':str(original)})

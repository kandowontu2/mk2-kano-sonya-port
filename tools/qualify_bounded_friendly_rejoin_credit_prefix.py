"""Allow separately validated added credits in otherwise exact old prefix."""
from pathlib import Path

original=Path(__file__).with_name('qualify_bounded_friendly_rejoin.py')
source=original.read_text()
source=source.replace("out=sync.ROOT/'audit_bounded_friendly_rejoin_checked'", "out=sync.ROOT/'audit_bounded_friendly_rejoin_credit_prefix_checked'")
marker='assert core(text)==core(baseline),\'Finisher observations changed before baseline stop\''
replacement="""request_line=next(line for line in text.splitlines() if line.startswith(prefix+'REJOIN_REQUEST'))
                request_frame=int(fields(request_line)['frame'])
                actual_core=[line for line in core(text) if not (line.startswith(prefix+'INPUT') and fields(line).get('button')=='Coin' and int(fields(line)['frame'])>=request_frame)]
                assert actual_core==core(baseline),'Non-credit finisher observations changed before baseline stop'"""
assert source.count(marker)==1
source=source.replace(marker,replacement)
exec(compile(source,str(original),'exec'),{'__name__':'__main__','__file__':str(original)})

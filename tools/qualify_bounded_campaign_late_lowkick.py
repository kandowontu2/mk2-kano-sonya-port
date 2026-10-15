"""Keep earned campaign gates and prove prefix unchanged before policy switch."""
from pathlib import Path
import re
import verify_native_source_sync as sync
parent=Path(__file__).with_name('qualify_bounded_sonya_campaign_30000.py')
wrapper=parent.read_text()
marker="exec(compile(source,__file__,'exec'),dict(__file__=__file__,predecessor=predecessor))"
assert wrapper.count(marker)==1
context=dict(__file__=str(parent))
exec(compile(wrapper.split(marker)[0],str(parent),'exec'),context)
def prefix(path):
    answer=[]
    for line in path.read_text().splitlines():
        match=re.search(r'\bframe=(\d+)',line)
        if line.startswith('MK2_NAT_CAMPAIGN_') and match and int(match[1])<12472:
            answer.append(line)
    return answer
baseline=sync.ROOT/'audit_bounded_sonya_campaign_30000_p1_runtime/run.log'
current=sync.ROOT/'audit_bounded_campaign_late_lowkick_p1_runtime/run.log'
assert prefix(baseline)==prefix(current)
source=context['source'].replace('audit_bounded_sonya_campaign_30000_checked','audit_bounded_campaign_late_lowkick_checked')
source=source.replace('audit_bounded_sonya_campaign_30000_p{side}_runtime','audit_bounded_campaign_late_lowkick_p{side}_runtime')
source=source.replace('report=dict(passed=True,results=results,','report=dict(passed=True,results=results,unchangedPrefixFields=12471,baselineLogSHA256=sync.sha(baseline),physicalPolicyChange=\'lowkick from stage4 only\',')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,predecessor=context['predecessor'],baseline=baseline))

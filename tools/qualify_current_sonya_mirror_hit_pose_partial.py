"""Preserve cap failure; qualify only complete fields of saved passive trace."""
from pathlib import Path
code=Path(__file__).with_name('qualify_current_sonya_mirror_hit_pose.py').read_text()
code=code.replace("out=sync.ROOT/'audit_current_sonya_mirror_hit_pose_checked'","out=sync.ROOT/'audit_current_sonya_mirror_hit_pose_partial_checked'")
code=code.replace("assert terminal['exitCode']==0 and terminal['limitReason'] is None","assert terminal['exitCode']==-1 and terminal['limitReason']=='wall_limit'")
code=code.replace("excluded={'HOST_BOUND','MIRROR_CPU_HIT_POSE'}","bound=max(int(r['frame']) for items in rows.values() for r in items)\nexcluded={'HOST_BOUND','MIRROR_CPU_HIT_POSE'}")
code=code.replace("int(r['frame'])<19500","int(r['frame'])<bound")
code=code.replace('maximumFields=19500','completePrefixExclusive=bound, wholeRunPassed=False, terminal=terminal')
exec(compile(code,__file__,'exec'),{'__file__':__file__})

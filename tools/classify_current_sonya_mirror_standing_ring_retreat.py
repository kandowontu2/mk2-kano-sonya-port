from pathlib import Path
code=Path(__file__).with_name('classify_current_sonya_mirror_active_flag_guard.py').read_text().replace('sonya_mirror_active_flag_guard','sonya_mirror_standing_ring_retreat')
code=code.replace("report=dict(observationPassed=True,", "rings=[r for r in rows.get('SPECIAL',[]) if r['move']=='ring' and r['stage']=='5']\nrequests=rows.get('MIRROR_RING_SPACING_ATTEMPT',[])\nreport=dict(nativeOwnedRingStarts=len(rings),ringRequests=len(requests),observationPassed=True,")
exec(compile(code,__file__,'exec'),{'__file__':__file__})

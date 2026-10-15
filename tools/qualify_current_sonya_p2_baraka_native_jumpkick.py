"""Actual airborne/HP outcomes and original handoff evidence, not jump intentions."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_baraka_prethrow_trace.py').read_text().replace('audit_current_sonya_p2_baraka_prethrow_trace','audit_current_sonya_p2_baraka_native_jumpkick')
# Controller changed only at Baraka; preserved-route comparison stops before entry.
source=source.replace("source=source.replace(\"'BARAKA_THROW_START','HOST_BOUND'\",\"'BARAKA_THROW_START','BARAKA_PRETHROW','THROW_HANDOFF_WORD','HOST_BOUND'\")", "source=source.replace(\"'BARAKA_THROW_START','HOST_BOUND'\",\"'BARAKA_THROW_START','BARAKA_PRETHROW','THROW_HANDOFF_WORD','HOST_BOUND'\").replace('60000)','50238)')")
source=source.replace("pre=rows.get('BARAKA_PRETHROW',[]);assert pre","pre=rows.get('BARAKA_PRETHROW',[])")
source=source.replace('audit_current_sonya_p2_baraka_native_jumpkick_preparation/original-words.json','audit_current_sonya_p2_baraka_prethrow_trace_preparation/original-words.json')
source=source.replace("exec(compile(source,__file__+'::native_context','exec'))", "source=source.replace(\"onsets=rows.get('BARAKA_THROW_START',[]);assert onsets\",\"onsets=rows.get('BARAKA_THROW_START',[])\")\nexec(compile(source,__file__+'::native_context','exec'))")
exec(compile(source,__file__+'::native_context','exec'))

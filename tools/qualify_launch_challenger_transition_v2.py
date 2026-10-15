"""Same-terminal correction: inventory selection cues separately from winners.

The first qualifier retained the winner-only marker filter from its parent.
That rejected genuine selection cues even after its count contract was changed.
Keep that executed qualifier intact; retain all original packet/ADSP checks.
"""
import inspect,json
from pathlib import Path
import qualify_launch_challenger_transition as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha

def packet_gate(text):
 native=previous.prior.mirror.qualifier.native_packets
 source=inspect.getsource(native.gate)
 first=source.index(" packets=audio('PACKET');");last=source.index(' return dict(passed=True,',first)
 source=source[first:last]
 before="""need(len(markers)==1 and markers[0]['word']==('FFFE'if identity==17 else'FFFD')and markers[0]['mask']=='FFFF'and
  len(all_sounds)==len(sounds)+1 and packets and len(sounds)==len(delivery)==2*len(packets),
  'Every actual native sound write accounted, with one true winner marker and both port/ADSP bytes per packet')"""
 after="""selection=[r for r in all_sounds if r['pc']=='FFFF3DA0']
 launches=[r for r in all_sounds if r['word']in('6B00','6B01','6B02','6B03')]
 need(not markers and len(selection)==2 and {r['word']for r in selection}=={'FFFB','FFFC'}and
  all(r['mask']=='FFFF'for r in selection)and len(launches)==1 and launches[0]['mask']=='FFFF'and
  len(all_sounds)==len(sounds)+len(selection)+len(launches)and packets and len(sounds)==len(delivery)==2*len(packets),
  'Every actual port write accounted: two selection cues, one startup, no winner, original DCS packet delivery')"""
 need(source.count(before)==1,'Whole original sound packet grammar and separate winner inventory')
 source=source.replace(before,after,1)
 code="def gate(text):\n records=native.inventory(text)\n audio=lambda tag:records.get('MK2_MAUDIO_'+tag,[])\n ends=audio('RESULT');need(len(ends)==1,'One actual terminal');end=ends[0]\n"+source+"\n return dict(passed=True,packets=len(packets),portWrites=len(sounds),nativeDSPReads=len(delivery),ownedStartupWrites=len(launches),selectionWrites=len(selection),winnerWrites=len(markers))\n"
 scope=dict(native.gate.__globals__,native=native)
 exec(compile(code,__file__+'::whole_original_DCS_and_ADSP_chronology','exec'),scope)
 return scope['gate'](text)

def qualify(c):
 failure=ROOT/f"audit_launch_challenger_transition_packet_inventory_rejection_{c['move']}_p{c['side']}"
 need(not failure.exists(),'Fresh retained original qualifier rejection')
 try:previous.packet_gate(c['text'])
 except ValueError as error:
  need(str(error)=='Every actual native port write accounted: complete startup sources, no winner, both actual ADSP bytes per packet','Exact reproduced original winner-only marker inventory rejection')
  failure.mkdir();(failure/'failure.json').write_text(json.dumps(dict(passed=False,nativeTerminal=c['terminal'],error=str(error),executedQualifier=str(Path(previous.__file__).resolve()),executedQualifierSHA256=sha(previous.__file__),rawCaptureReused=True,newNativeBoots=0),indent=2)+'\n')
 else:raise ValueError('Original packet rejection unexpectedly absent')
 source=inspect.getsource(previous.qualify)
 before='for p in(Path(__file__),Path(prior.__file__),'
 need(source.count(before)==1,'Retain full same-terminal qualifier with both executed source pins')
 source=source.replace(before,'for p in(Path(__file__),Path(previous.__file__),Path(prior.__file__),',1)
 scope=dict(vars(previous),__file__=__file__,previous=previous,packet_gate=packet_gate)
 exec(compile(source,__file__+'::whole_same_terminal_qualification','exec'),scope)
 return scope['qualify'](c)

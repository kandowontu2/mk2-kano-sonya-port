"""Direct base-gate successor; retain failed nested-string checker unchanged."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_liu_standing.py').read_text()
source=source.replace('audit_current_kano_p2_liu_standing','audit_current_kano_p2_scorpion_close_air')
source=source.replace('audit_current_kano_p2_subzero_low_knife_runtime','audit_current_kano_p2_campaign_32000_runtime')
source=source.replace("if tag not in ('KANO_P2_LIU_DAMAGE','KANO_P2_LIU_STANDING'):","if tag not in ('HOST_BOUND','RESULT','KANO_P2_SCORPION_DAMAGE','SCORPION_AIR_WRITE'):")
source=source.replace("int(r['frame'])<8510","int(r['frame'])<21977")
source=source.replace("records['RESULT'][0]['frame']=='20000'","records['RESULT'][0]['frame']=='32000'")
source=source.replace('priorEarnedPrefixUnchangedThrough=8509','priorEarnedPrefixUnchangedThrough=21976')
extra="""
assert any(r['stage']=='6' and r['cpu']=='3:3' for r in rows['FIGHT'])
proof['scorpionOwnRoundWins']=[r for r in rows['WIN'] if r['stage']=='6' and r['slot']=='2']
proof['scorpionMatchCleared']=7 in proof['earnedStages']
air=rows.get('SCORPION_AIR_WRITE',[])
for r in air:
    assert r['actor']==r['owner']==r['a8'] and r['main']==r['a13']
    assert int(r['at'],16)==int(r['main'],16)+0x1f0
    assert (r['after'],r['pc']) in [('776','FF831360'),('512','FF871F50')]
proof['kickGeometry']=[dict(frame=int(r['frame']),gap=int(r['gap']),height=int(r['height'])) for r in air if r['after']=='512']
damage=rows.get('KANO_P2_SCORPION_DAMAGE',[])
owned=[r for r in damage if r['victim_slot']=='1' and r['a8']==r['p2_actor'] and r['a13']==r['p2_main'] and r['actions'].split(',')[1]=='512']
proof['ownedAirKickContacts']=len(owned)
proof['ownedAirKickDamage']=sum(int(r['before'])-int(r['after']) for r in owned)
proof['scorpionOutgoing']=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1')
"""
source=source.replace('proof=gate(rows)','proof=gate(rows)'+extra)
exec(compile(source,__file__+'::direct_native_campaign_gate','exec'))

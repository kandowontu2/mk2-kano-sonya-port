"""Same true-ID chronology gate and exact earlier route; native CPU5 combat evidence."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_kitana_counter.py').read_text()
source=source.replace('audit_current_kano_p2_kitana_counter','audit_current_kano_p2_mileena_ball_knife')
source=source.replace('audit_current_kano_p2_early_knife_campaign_40000_runtime','audit_current_kano_p2_campaign_sparse_inputs_runtime')
source=source.replace("int(r['frame'])<34953","int(r['frame'])<41944")
source=source.replace('priorPrefixUnchangedThrough=34952','priorPrefixUnchangedThrough=41943')
source=source.replace("=='40000'","=='60000'").replace('completed40000','completed60000')
source=source.replace('proof=gate(rows)',"""proof=gate(rows)
damage=rows.get('KANO_P2_MILEENA_DAMAGE',[])
assert all(r['ids']=='5,17' and r['p1_actor']!=r['p2_actor'] and r['p1_main']!=r['p2_main'] for r in damage)
balls=[r for r in damage if r['victim_slot']=='1' and r['actions'].split(',')[1]=='523' and r['a8']==r['p2_actor'] and r['a13']==r['p2_main']]
entries=[r for r in rows.get('SPECIAL',[]) if r['stage']=='10']
assert all(r['id']==r['roster']=='17' and r['actor']==r['a8'] and r['main']==r['a13'] for r in entries)
proof['mileenaOwnWins']=[r for r in rows['WIN'] if r['stage']=='10' and r['slot']=='2']
proof['mileenaMatchCleared']=11 in proof['earnedStages']
proof['mileenaOwnedBallContacts']=len(balls)
proof['mileenaOwnedBallDamage']=sum(int(r['before'])-int(r['after']) for r in balls)
proof['mileenaOutgoing']=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1')
proof['mileenaIncoming']=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2')
proof['mileenaNativeSpecialEntries']={move:len([r for r in entries if r['move']==move]) for move in ('ball','knife')}
""")
exec(compile(source,__file__+'::native_mileena_gate','exec'))

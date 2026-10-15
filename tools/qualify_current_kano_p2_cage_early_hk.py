"""Earlier unchanged prefix and real native Cage round evidence."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_baraka_choke_route.py').read_text()
source=source.replace('audit_current_kano_p2_baraka_choke_route','audit_current_kano_p2_cage_early_hk')
source=source.replace('<21977','<8510').replace('priorPrefixUnchangedThrough=21976','priorPrefixUnchangedThrough=8509')
source=source.replace("r['stage']=='6'", "r['stage']=='2'")
source=source.replace('barakaNativeChokeEntries','cageNativeChokeEntries').replace('barakaLPInputFields','cageLPInputFields').replace('barakaOwnWins','cageOwnWins')
exec(compile(source,__file__+'::native_cage_route_gate','exec'))
damage=rows.get('KANO_P2_LIU_DAMAGE',[])  # Preserved legacy tag; actual CPU ID2 is Cage.
assert all(r['ids']=='2,17' and r['p1_actor']!=r['p2_actor'] and r['p1_main']!=r['p2_main'] for r in damage)
kicks=[r for r in damage if r['victim_slot']=='1' and r['actions'].split(',')[1]=='259' and r['a8']==r['p2_actor'] and r['a13']==r['p2_main']]
detail=dict(nativeOpponentID=2,nativeOpponentName='Cage',ownedHKContacts=len(kicks),
            ownedHKDamage=sum(int(r['before'])-int(r['after']) for r in kicks),
            outgoing=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='1'),
            incoming=sum(int(r['before'])-int(r['after']) for r in damage if r['victim_slot']=='2'),
            fullCampaignAccepted=False,fullPortAccepted=False)
(out/'cage-native-hk.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))

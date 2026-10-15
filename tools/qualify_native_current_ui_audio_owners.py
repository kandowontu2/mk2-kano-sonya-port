"""Cold UI is silent; actual combat launches require real physical ownership.

Do not confuse a legitimately active CPU startup in the first match with a
stale selector/ladder audio owner. Preserve every cold field, both participants,
native launch provenance and full source/EOF state, rather than dropping rows.
"""
import re
from decimal import Decimal
import capture_launch_candidate_ui as ui
need=ui.need

def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in text.splitlines() if s.startswith(tag+' ')]

def gate(text,terminal):
    owners=rows(text,'MK2_UA_OWNER');fields=rows(text,'MK2_UI_FIELD');sounds=rows(text,'MK2_UA_SOUND')
    channels=rows(text,'MK2_UA_CHANNEL')
    need(len(owners)==terminal*2 and {(int(r['frame']),int(r['slot'])) for r in owners}==
         {(f,s) for f in range(1,terminal+1) for s in (1,2)},'Every actual owner field, both slots, entire cold-to-combat run')
    need(len(channels)==terminal*14 and {(int(r['frame']),int(r['channel'])) for r in channels}==
         {(f,ch) for f in range(1,terminal+1) for ch in range(14)},'Every actual source channel through cold UI and full first match')
    fieldmap={(int(r['frame']),int(r['slot'])):r for r in fields}
    owner_stamps={(int(r['frame']),int(r['slot'])):Decimal(r['seconds']) for r in owners}
    channelmap={(int(r['frame']),int(r['channel'])):r for r in channels}
    need(fields and len(fieldmap)==len(fields),'Whole unique actual native participant history')
    first=min(int(r['frame']) for r in fields)
    base={s:fieldmap[first,s] for s in (1,2)}
    descriptors={'6B00':('FFFFCAC0',18,519,13,45512), '6B01':('FFF9A4C0',18,516,14,40720),
                 '6B02':('FFF9A520',18,516,15,66523), '6B03':('FFFFDEC0',17,523,16,55465)}
    launches=[]
    for r in sounds:
        if r['word'] not in descriptors:continue
        pc,identity,action,sample,length=descriptors[r['word']]
        need(r['pc']==pc and r['mode']=='2' and r['mask']=='FFFF' and r['writes']=='0' and r['assistance']=='none',
             'Every genuine owned native gameplay startup opcode/port; no selector or stock packet alias')
        slots=[s for s in (1,2) if base[s]['actor']==r['a8'] and base[s]['main']==r['a13']]
        need(len(slots)==1,'Actual actor/Main identifies exactly one physical participant, not an ID-only match')
        slot=slots[0];f=int(r['frame'])
        # A marker can execute after this field's register_frame callbacks.
        # Use the first actual participant publication at/after the marker,
        # never mistake the preceding ordinary action for the launch action.
        published=f if owner_stamps.get((f,slot),Decimal(-1))>=Decimal(r['seconds']) else f+1
        participant=fieldmap.get((published,slot))
        need(participant and int(participant['id'])==int(participant['roster'])==identity and
             int(participant['action'])==action and participant['owner']==r['a8'] and participant['main']==r['a13'] and
             int(participant['hp'])>0,'Actual true-ID participant owns the signature action and positive native health at launch')
        launches.append(dict(r,slot=slot,identity=identity,sample=sample,length=length))
    active_fields=0;cold_fields=0;retired=0;previous={1:False,2:False}
    for r in owners:
        f,s=int(r['frame']),int(r['slot']);stamp=Decimal(r['seconds'])
        need(r['writes']=='0' and r['assistance']=='none','Entire owner observer remains read-only')
        empty=r['actor']==r['main']=='00000000' and r['id']==r['health']=='0'
        emitted=[e for e in launches if e['slot']==s and Decimal(e['seconds'])<=stamp]
        if not emitted:
            need(empty,'All cold/selection/ladder and unlaunched participant owners remain completely clear')
            for ch in (10+(s-1)*2,11+(s-1)*2):
                c=channelmap[f,ch]
                need(c['sample']=='4294967295' and c['length']=='0' and float(c['pos'])==0,'No unowned startup source in any cold or nonlaunching physical slot')
            cold_fields+=1
        elif not empty:
            latest=emitted[-1];participant=fieldmap.get((f,s))
            need(participant and r['actor']==participant['actor']==participant['owner']==latest['a8'] and
                 r['main']==participant['main']==latest['a13'] and int(r['id'])==int(participant['id'])==latest['identity'] and
                 r['health']==participant['hp'] and int(r['health'])>0,'Every active owner is the same currently live actor/Main/health/true identity')
            active_fields+=1
        else:
            if previous[s]:
                used={10+(s-1)*2+(1 if e['word']=='6B02' else 0):e for e in emitted}
                for ch,e in used.items():
                    c=channelmap[f,ch]
                    need(c['sample']=='4294967295' and int(c['length'])==e['length'] and float(c['pos'])>=e['length'],
                         'Observed owner retirement follows complete native source EOF, not stale UI state')
                retired+=1
        previous[s]=not empty
    for c in channels:need(c['loop']==c['paused']==c['writes']=='0','Finite nonlooping actual native sources in every field')
    return dict(passed=True,ownerFields=len(owners),allChannelFields=len(channels),coldOrUnlaunchedOwnerFields=cold_fields,
                actualActiveCombatOwnerFields=active_fields,observedFullEOFRetirements=retired,actualLaunches=launches,
                completeColdOwnershipClear=True,allCombatOwnersSourceBound=True,fullMixedAudioAcceptance=False)

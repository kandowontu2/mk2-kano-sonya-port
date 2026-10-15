"""Actual stock female/male split controls preserve native per-slot schedule."""
import inspect
import qualify_bounded_stock_kiss_timing as previous

def main():
    source=inspect.getsource(previous.main)
    changes={'audit_bounded_stock_kiss_timing_checked':'audit_bounded_stock_split_timing_checked',
        'audit_bounded_kitana_kiss_voice_choice_checked':'audit_bounded_kung_lao_split_voice_packets_checked',
        '_kiss_voice_runtime':'_split_voice_runtime',
        "'kitana','0','none'":"'kung_lao','0','none'",
        "a['address']=='FF8CC650'":"a['address']=='FF8C6040'",
        "x['own'].split(':')[-1]=='4'":"x['own'].split(':')[-1]=='0'",
        "int(w['frame'])-int(a['frame'])==276":"int(w['frame'])-int(a['frame'])==179",
        "age=188 if fighter=='kitana' and side==1 else 179+side":"age=75+side",
        "effect=[r for r in cues if r['cue'] in ('A3','A5','A4')]":"effect=cues",
        "assert [r['cue'] for r in effect]==['A3','A5','A4']":"assert len(effect)==4",
        'offsets==[32,32,172]':'offsets==[0,74,90,132]',
        '(96 if side==1 else 95)':'(103 if side==1 else 102)',
        '_kitana_kiss_voice_priority_runtime':'_kung_lao_split_voice_runtime',
        "['voiceAge']==179+side":"['voiceAge']==75+side",
        'age-(179+side)':'age-(75+side)',
        'finiteStockLiuSlotTimingParityAccepted=True':'finiteStockKitanaAndLiuSlotTimingParityAccepted=True',
        'stockKitanaP1EightFieldVariationObserved=True':'stockTimingVariationObserved=False'}
    for before,after in changes.items():assert source.count(before)==1;source=source.replace(before,after)
    before="            assert len(branches)==1;b=branches[0]"
    assert source.count(before)==1
    source=source.replace(before,"            assert int(w['frame'])-int(a['frame'])==179\n"+before)
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(source,__file__+'::genuine_stock_split_timing','exec'),namespace);namespace['main']()

if __name__=='__main__':main()

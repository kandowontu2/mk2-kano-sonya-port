"""Protect original ending/music packets on the actual earned current route."""
import copy,hashlib,json,re
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_earned_ending_sound_events_runtime'
out=root/'audit_current_earned_ending_dcs_packets_checked';assert not out.exists()
prior=root/'audit_current_kano_earned_ending_sound_events_v2_checked/report.json'
old=json.loads(prior.read_text());assert old['logSHA256']==sync.sha(case/'run.log')
transport=root/'audit_current_stock_stage_dcs_packet_conservation_v2_checked/report.json'
proof=json.loads(transport.read_text());assert proof['currentHostSoundFunctionLogicalSourceExactlyConserved']
current=root/'mame-mkp/src/mame/midway/midtunit_m.cpp'
source=current.read_text();function=source[source.index('void midtunit_state::midtunit_sound_w('):]
assert hashlib.sha256(function.encode()).hexdigest().upper()==proof['soundFunctionSHA256']
assert 'm_maincpu->pc() == 0xffa13c90U' in function and 'm_maincpu->pc() == 0xffa13d60U' in function
rows=[dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in (case/'run.log').read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_ENDING_SOUND_WORD ')]
def gate(rows):
    assert all(r['writes']=='0' and r['assistance']=='none' and r['mute']=='0' for r in rows)
    native=[r for r in rows if r['pc'] in ('FFA13C90','FFA13D60')]
    own=[r for r in rows if r['pc'] not in ('FFA13C90','FFA13D60')]
    assert len(own)==1 and own[0]['pc']=='FFFF3DA0' and own[0]['word']=='FFFC' and own[0]['mode']=='4'
    assert len(native)>100 and len(native)%2==0
    packets=[]
    for h,l in zip(native[::2],native[1::2]):
        assert h['pc']=='FFA13C90' and l['pc']=='FFA13D60' and h['frame']==l['frame']
        assert all(0xff00<=int(r['word'],16)<=0xffff for r in (h,l))
        packets.append(dict(frame=int(h['frame']),mode=int(h['mode']),packet=f"{int(h['word'],16)&255:02X}{int(l['word'],16)&255:02X}"))
    return packets,native
packets,native=gate(rows);faults=[]
for kind in ('missing_low_byte','wrong_native_pc','split_packet_frame','invalid_sign_extension'):
    bad=copy.deepcopy(rows)
    if kind=='missing_low_byte':bad.pop(1)
    elif kind=='wrong_native_pc':bad[0]['pc']='FFFF3DA0'
    elif kind=='split_packet_frame':bad[0]['frame']='0'
    else:bad[0]['word']='1234'
    try:gate(bad)
    except AssertionError:faults.append(kind)
    else:raise AssertionError('Corrupt packet admitted')
report=dict(currentEarnedEndingNativePacketTransportPassed=True,completeNativePairs=len(packets),
    nativeBytes=len(native),nativeMarkerRangeBytes=sum(0xfff7<=int(r['word'],16)<=0xfffe for r in native),
    ownPostEndingSelectionCueSeparate=True,packets=packets,effectiveFaultsRejected=faults,
    hostSoundTransportConserved=True,logSHA256=sync.sha(case/'run.log'),
    inputHashes={str(p):sync.sha(p) for p in (prior,transport,current)},
    fullEndingAudioAccepted=False,heardMixAccepted=False,fullPortAccepted=False,
    scope='Actual native command pairs from final boss through credits and paid restart. No DCS waveform, heard mix or whole audio acceptance inferred.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('packets','inputHashes')}))

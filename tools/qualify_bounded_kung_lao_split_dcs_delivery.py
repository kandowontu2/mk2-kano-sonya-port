"""Every actual split port byte reaches a natural ADSP read before next write."""
import copy,json,re
from decimal import Decimal
from pathlib import Path
import verify_native_source_sync as sync

def load(folder):
    baseline=[];writes=[];reads=[];packets=[]
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            if line.startswith(('MK2_STOCK_HEAD_V921_','MK2_VOICE_','MK2_FINISHER_AUDIO_')):baseline.append(line.strip())
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if line.startswith('MK2_SPLIT_DCS_WRITE '):writes.append(r)
            elif line.startswith('MK2_SPLIT_DCS_READ '):reads.append(r)
            elif line.startswith('MK2_FINISHER_AUDIO_PACKET '):packets.append(r)
    return baseline,writes,reads,packets

def gate(writes,reads,packets):
    assert len(writes)==len(reads)==len(packets)==102
    matched=[]
    for index,(w,packet) in enumerate(zip(writes,packets)):
        assert w['writes']=='0' and w['assistance']=='none'
        assert all(w[k]==packet[k] for k in ('frame','mask','pc','a8','a13')) and w['word']==packet['data']
        assert w['pc']==('FFA13C90' if index%2==0 else 'FFA13D60') and w['mask']=='FFFF'
        first=Decimal(w['seconds']);last=Decimal(writes[index+1]['seconds']) if index+1<len(writes) else first+Decimal('.1')
        candidates=[r for r in reads if first<Decimal(r['seconds'])<last]
        assert len(candidates)==1;r=candidates[0]
        assert r['writes']=='0' and r['assistance']=='none' and r['mask']=='FFFF' and r['at']=='3400'
        assert int(r['word'],16)==(int(w['word'],16)&255) and r['frame']==w['frame']
        assert r['dsp_pc']==('03A1' if index%2==0 else '03A8')
        matched.append(dict(frame=int(w['frame']),byte=f'{int(r["word"],16):02X}',portPC=w['pc'],dspPC=r['dsp_pc'],latencyMicroseconds=float((Decimal(r['seconds'])-first)*1000000)))
    return matched

def main():
    out=sync.ROOT/'audit_bounded_kung_lao_split_dcs_delivery_checked';assert not out.exists()
    proof_path=sync.ROOT/'audit_bounded_kung_lao_split_voice_packets_checked/report.json'
    proof=json.loads(proof_path.read_text());assert proof['passed'];results={}
    for side in (1,2):
        for fighter in ('sonya','kano'):
            key=f'{fighter}P{side}';folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_dcs_delivery_runtime'
            base=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_voice_runtime'
            assert sync.sha(base/'run.log')==proof['results'][key]['logSha256']
            t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip()
            original,writes,reads,packets=load(folder);old,_,_,old_packets=load(base)
            assert original==old and packets==old_packets
            matched=gate(writes,reads,packets);faults=[]
            for label in ('missing_read','wrong_byte','late_read'):
                bad=copy.deepcopy(reads)
                if label=='missing_read':bad.pop(0)
                elif label=='wrong_byte':bad[0]['word']='FFFF'
                else:bad[0]['seconds']=writes[1]['seconds']
                try:gate(writes,bad,packets)
                except AssertionError:faults.append(label)
                else:raise AssertionError('Delivery fault accepted')
            results[key]=dict(nativeBytesConsumed=102,nativeCommandPairs=51,matched=matched,
                originalControlVoiceAndPortRowsUnchanged=True,rejectedFaults=faults,terminal=t,logSha256=sync.sha(folder/'run.log'))
    dcs=sync.ROOT/'mame-mkp/src/mame/shared/dcs.cpp';driver=sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
    dcs_text=dcs.read_text();driver_text=driver.read_text()
    assert 'map(0x3400, 0x37ff).rw(FUNC(dcs_audio_device::input_latch_r)' in dcs_text
    assert 'return m_input_data;' in dcs_text and 'm_dcs->data_w(data & 0xff);' in driver_text
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),voiceProofSha256=sync.sha(proof_path),
        deviceSourcePins={str(dcs):sync.sha(dcs),str(driver):sync.sha(driver)},finiteNativeADSPConsumptionVerified=True,
        nativePCMVerified=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={k:r['nativeBytesConsumed'] for k,r in results.items()})))

if __name__=='__main__':main()

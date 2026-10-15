"""Actual complete ending metadata/callback phase faults; not pixel acceptance."""
import json,re,subprocess
from pathlib import Path
import qualify_ending_display_latch_source_v4647 as source
ROOT,need,sha=source.ROOT,source.need,source.sha
CASE=ROOT/'audit_v4622_kano_p2_ending_display_latch_ram'
OUT=ROOT/'audit_v4656_actual_ending_context_phase_checked'

def main():
    need(not OUT.exists(),'Fresh immutable actual terminal ending phase qualification')
    preflight_path=source.OUT/'report.json';proof=json.loads(preflight_path.read_text())
    need(proof['passed']and not proof['nativeEndingVideoAcceptance']and
         all(sha(p)==h for p,h in proof['inputHashes'].items()),'All actual-schema/source/metadata inputs unchanged, no video claim')
    text=(CASE/'run.log').read_text();positive=source.renderer_window(text,'kano');faults=[]
    lines=text.splitlines();index=next(i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP frame=59335 '))
    missing='\n'.join(lines[:index]+lines[index+1:])+'\n'
    index=next(i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_RESULT frame=59336 '))
    changed=list(lines);changed[index]=changed[index].replace('frame=59336','frame=59335',1)
    early='\n'.join(changed)+'\n'
    index=next(i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_RESULT '))
    changed=list(lines);changed[index]=changed[index].replace('snapshots=3040','snapshots=3039',1)
    count='\n'.join(changed)+'\n'
    fake=text+'MK2_NAT_CAMPAIGN_FLOOR_SNAP frame=59336 human_slot=2 fighter=kano writes=0 assistance=none epoch=1 phase=frame_done file=display_59336.png\n'
    for label,altered in [('missing_actual_last_completed_field',missing),('wrong_actual_terminal_notifier',early),
                          ('wrong_actual_renderer_total',count),('fabricated_post_exit_render_callback',fake)]:
        need(altered!=text,'Actual non-vacuous renderer/terminal phase fault')
        try:source.renderer_window(altered,'kano')
        except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted actual ending callback phase fault: '+label)
        need(source.renderer_window(text,'kano')==positive,'Entire untouched actual renderer/terminal positive restored')
    baseline=ROOT/'audit_v4485_kano_current_p2_campaign_ram/run.log'
    prefixes=('MK2_NAT_CAMPAIGN_','MK2_MILEENA_CAMPAIGN_','MK2_BOSS_KNIFE_','MK2_CAMPAIGN_GUEST_RAM_DIGEST ','MK2_CAMPAIGN_RAM_FRAME_DIGEST ')
    select=lambda t:[line for line in t.splitlines()if line.startswith(prefixes)and not line.startswith(
                    ('MK2_NAT_CAMPAIGN_FLOOR_','MK2_NAT_CAMPAIGN_SHADOW_','MK2_NAT_CAMPAIGN_ENDING_DISPLAY_'))]
    need(select(text)==select(baseline.read_text()),'Every original cold native control/state/health/boss/ending/attract/guest/RGB event exactly unchanged')
    pins=dict(proof['inputHashes'])
    for p in (preflight_path,baseline,Path(__file__).resolve()):pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All original/current input bytes unchanged')
    report=dict(passed=True,actualFirstEndingRendererField=positive[0],actualLastCompletedRendererField=positive[1],
                actualNativeStop=59336,actualAttractRendererFields=300,actualRendererPhaseFaultsRejected=faults,
                everyOriginalColdNativeCampaignEventAndRGBExactlyUnchanged=True,
                completeNativeEndingRendererVideoAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()

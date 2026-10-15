"""Current native CPU evidence: ring/health/flags/body/shadow, real finite visuals.

Keep all14 requirements and six remaining groups. Original standalone failures
remain false; do not promote public CMD/ZIP or substitute finite proofs for goal.
"""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
import capture_native_selector_special_shadow as current
import qualify_native_selector_cpu_ring_trace_ko_origin as ring_source
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_native_selector_cpu_checkpoint_checked'
VIEWED=json.loads(r'''{"kano":[{"index":3,"header":{"stage":"p1_cold_cpu_fight","attempt":1,"frame":1815,"width":400,"height":254,"bytes":406400,"sha256":"45D23C7682E78D17A8A4F7C71D53D3F7EC063EF93B254CE8333F53D591D22187","rawMediaFilesWritten":0},"SHA256":"45D23C7682E78D17A8A4F7C71D53D3F7EC063EF93B254CE8333F53D591D22187","nativeRGBSHA256":"02278554FF8E65CC6EA2D274C27F2BA4D14A489015644294515F2C5C47EBFB78","actualReconstructedAlpha":255},{"index":11,"header":{"stage":"cpu_pair_1_step_8","attempt":1,"frame":2015,"width":400,"height":254,"bytes":406400,"sha256":"830D8D676816AB1EEB52C4A158E745F335E816CB2EA82C625119B2334B43A064","rawMediaFilesWritten":0},"SHA256":"830D8D676816AB1EEB52C4A158E745F335E816CB2EA82C625119B2334B43A064","nativeRGBSHA256":"CE413216842634DCF5CD28800FD873E0BA21D1EE86EFA93FEB858985AE3F5608","actualReconstructedAlpha":255},{"index":19,"header":{"stage":"cpu_pair_1_step_16","attempt":1,"frame":2039,"width":400,"height":254,"bytes":406400,"sha256":"ACA33C7DC0E6377DA96544C025250A6BDB0E281512978531BB963174F98FEDBC","rawMediaFilesWritten":0},"SHA256":"ACA33C7DC0E6377DA96544C025250A6BDB0E281512978531BB963174F98FEDBC","nativeRGBSHA256":"98775F94C2724998CE8EBA9D1565A067811E5E7AF000A67F3027C49F90B08520","actualReconstructedAlpha":255},{"index":25,"header":{"stage":"cpu_pair_1_step_22","attempt":1,"frame":2057,"width":400,"height":254,"bytes":406400,"sha256":"6EB822CE9C93F69C421500BF16986096FBA65DB300EB7D3A82AE70A92B608F94","rawMediaFilesWritten":0},"SHA256":"6EB822CE9C93F69C421500BF16986096FBA65DB300EB7D3A82AE70A92B608F94","nativeRGBSHA256":"DC6A7DF7D89CCF5B376B6909032269E5D32277F5F496AC008ED232A5344353EA","actualReconstructedAlpha":255},{"index":26,"header":{"stage":"cpu_pair_complete","attempt":1,"frame":2105,"width":400,"height":254,"bytes":406400,"sha256":"A48227F5FDC66FA9DCFB9B97DCF81B7372A16C7FDA3D63C3F6AB2DE5A3015FDE","rawMediaFilesWritten":0},"SHA256":"A48227F5FDC66FA9DCFB9B97DCF81B7372A16C7FDA3D63C3F6AB2DE5A3015FDE","nativeRGBSHA256":"B62645790D9747C3D2123BDC5928EDC1E15EDFFA613040E9C9C1F7B943815579","actualReconstructedAlpha":255},{"index":27,"header":{"stage":"cpu_followup_regain","attempt":1,"frame":2140,"width":400,"height":254,"bytes":406400,"sha256":"0513696E819DB5390F58DE2CEC87756C45A44F406921F05854F2EFC3F9CA10F0","rawMediaFilesWritten":0},"SHA256":"0513696E819DB5390F58DE2CEC87756C45A44F406921F05854F2EFC3F9CA10F0","nativeRGBSHA256":"BFE116FDD9569B37F271DB14B871F5DA50B001FDA0933E4CD9328E0D9C44A13D","actualReconstructedAlpha":255}],"sonya":[{"index":0,"header":{"stage":"p1_selection_65","attempt":1,"frame":998,"width":400,"height":254,"bytes":406400,"sha256":"55525A7F6924165400BDB05C332412EACB66F24E846A572A23534E92E86CFA77","rawMediaFilesWritten":0},"SHA256":"55525A7F6924165400BDB05C332412EACB66F24E846A572A23534E92E86CFA77","nativeRGBSHA256":"714CFB13FD08CAE3616A640463A93D050EFBEAFDBE169854094717C2873D8A23","actualReconstructedAlpha":255},{"index":2,"header":{"stage":"p1_selection_exit","attempt":1,"frame":1288,"width":400,"height":254,"bytes":406400,"sha256":"19FC64FC00F4C553A62978DE741B667A750FCED7FD4C4C6E5B5279775952D37C","rawMediaFilesWritten":0},"SHA256":"19FC64FC00F4C553A62978DE741B667A750FCED7FD4C4C6E5B5279775952D37C","nativeRGBSHA256":"38107AC6A77DCA66CF7736E3B13D630C22065F39C0A901ABC44985EE1AE4E67C","actualReconstructedAlpha":255},{"index":3,"header":{"stage":"p1_cold_cpu_fight","attempt":1,"frame":1816,"width":400,"height":254,"bytes":406400,"sha256":"2069EAA829E81A7CB91FA368148EF30127B5B273B581761BED1044C67C52E2AC","rawMediaFilesWritten":0},"SHA256":"2069EAA829E81A7CB91FA368148EF30127B5B273B581761BED1044C67C52E2AC","nativeRGBSHA256":"284ADEBA80E52F4474AA1E762C728704C782C071A5A2039E1A47F6E5E2024596","actualReconstructedAlpha":255},{"index":4,"header":{"stage":"cpu_pair_1_step_1","attempt":1,"frame":2218,"width":400,"height":254,"bytes":406400,"sha256":"19E8398D063C3E7469478A89ABC2E3D9735E7E8C2C1173CEEB63BFB2686BC80F","rawMediaFilesWritten":0},"SHA256":"19E8398D063C3E7469478A89ABC2E3D9735E7E8C2C1173CEEB63BFB2686BC80F","nativeRGBSHA256":"80A81F778D0A293B02D8FCB222670D99E93F7164AC771E60452B3D102649D9AC","actualReconstructedAlpha":255},{"index":5,"header":{"stage":"cpu_pair_1_step_2","attempt":1,"frame":2248,"width":400,"height":254,"bytes":406400,"sha256":"69BFE879F920EFECB26A9F5D8F1A3697C40F7320E12F617AC27346A3493F8671","rawMediaFilesWritten":0},"SHA256":"69BFE879F920EFECB26A9F5D8F1A3697C40F7320E12F617AC27346A3493F8671","nativeRGBSHA256":"2C016611D9DC07462572B1F99703542B4D5F09D69B02EB73A159B1ADCC57DBF8","actualReconstructedAlpha":255},{"index":6,"header":{"stage":"cpu_pair_1_step_3","attempt":1,"frame":2252,"width":400,"height":254,"bytes":406400,"sha256":"FCAF58865ECA42524DD24779B8A7C7377C59EA19C37C350BA093995ABBF39070","rawMediaFilesWritten":0},"SHA256":"FCAF58865ECA42524DD24779B8A7C7377C59EA19C37C350BA093995ABBF39070","nativeRGBSHA256":"219BDAF344A02DE0AA9AA42F8FDC0B649859F428BF0C8EC03CD48ED0B70DDB3A","actualReconstructedAlpha":255},{"index":7,"header":{"stage":"cpu_pair_1_step_4","attempt":1,"frame":2256,"width":400,"height":254,"bytes":406400,"sha256":"3EC4E71C82F769A3CB1FAECAFA6FDA6D2CF5E08DAF2BD86D9FFDB2F972B9A1D6","rawMediaFilesWritten":0},"SHA256":"3EC4E71C82F769A3CB1FAECAFA6FDA6D2CF5E08DAF2BD86D9FFDB2F972B9A1D6","nativeRGBSHA256":"1AF26F7722D31607993B750CEAD68916DB269058CA556C151B0791736BE4C435","actualReconstructedAlpha":255},{"index":8,"header":{"stage":"cpu_pair_1_step_5","attempt":1,"frame":2260,"width":400,"height":254,"bytes":406400,"sha256":"3E32EC0F91024C3D02583C723A707016DE3AB4D4A320FE94EBF94A0CC1A6FA33","rawMediaFilesWritten":0},"SHA256":"3E32EC0F91024C3D02583C723A707016DE3AB4D4A320FE94EBF94A0CC1A6FA33","nativeRGBSHA256":"76D86D2801F24F1F7837EE0832977A91E51AB3573F41BE84E594DD51736FCDA9","actualReconstructedAlpha":255}]}''')


def verify(state,kano,sonya):
    need(not OUT.exists()and not current.prior.identity.census(),'Fresh retained receipt; all actual native jobs terminal')
    ring_path=ring_source.OUT/'report.json';ring=json.loads(ring_path.read_text())
    need(ring['passed']and len(ring['originalRingHealthFlagFaultsRejected'])==30 and
         len(ring['originalBodyShadowFaultsRejected'])==11 and
         ring['originalRepeatedGateStillRejected']and not ring['compoundLegPhaseAcceptance']and
         not ring['fullKOTransitionAccepted']and not ring['fullPortAcceptance']and
         all(sha(p)==h for p,h in ring['inputHashes'].items()),
         'All actual current full ring/health/state/body/shadow gates and41 applicable original faults')
    pins=dict(ring['inputHashes']);records={};reviewed=0
    expected={k:dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),everyActualByteComparedInRAM=True)
              for k,raw in (('guest',state['guest']),('gfx',state['gfx']))}
    expected.update({'cold_'+k:dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),everyActualByteComparedInRAM=True)
                     for k,raw in state['WINDOWS'].items()})
    for name,owner,key in (('kano',kano,'choke_cpu_kano_human_kano'),('sonya',sonya,sonya.KEY)):
        cases=owner.CPU_CASES if name=='kano'else owner.RAM_CASES
        handles=owner.CPU_HANDLES if name=='kano'else owner.NATIVE_HANDLES
        folder,text,images=cases[key];held=handles[key];report=json.loads((folder/'result.json').read_text())
        need(not report['passed']and report['nativeExit']==0 and held['process'].poll()==0 and
             held['identity']==report['nativeTerminal']['actualWindowsIdentity']and
             held['process'].pid==held['identity']['ProcessId']and held['identity']['ParentProcessId']==38752 and
             not report['nativeTerminal']['hostDecodeErrors']and report['proofs']==expected and
             all(sha(p)==h for p,h in report['inputHashes'].items()),
             'Both exact actual current native terminal handles, original rejections, all5 complete/limited proofs')
        pins.update(report['inputHashes'])
        for row in VIEWED[name]:
            scene=report['actualScenes'][row['index']];rgb=images[f"ui_{scene['frame']:04d}.png"]
            need(scene==row['header']and scene['sha256']==row['SHA256']and
                 rgb.shape==(254,400,3)and hashlib.sha256(rgb.tobytes()).hexdigest().upper()==row['nativeRGBSHA256'],
                 'Exactly the actual original reviewed native RGB fields')
            raw=np.empty((254,400,4),np.uint8);raw[:,:,:3]=rgb[:,:,::-1];raw[:,:,3]=row['actualReconstructedAlpha']
            need(row['actualReconstructedAlpha']==255 and hashlib.sha256(raw.tobytes()).hexdigest().upper()==scene['sha256'],
                 'Every original RGB pixel reconstructs the whole actual BGRX capture digest')
            reviewed+=1
        need(all(p.suffix.lower()not in('.png','.wav','.bin','.exe','.zip')for p in folder.rglob('*')if p.is_file()),
             'No raw media/game-build copies in either actual CPU case')
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p.resolve())]=sha(p)
        records[name]=dict(nativeIdentity=held['identity'],originalCapturePassed=False,
                          originalCaptureError=report['error'],memoryProofs=report['proofs'],actuallyViewedFields=VIEWED[name])
        if name=='kano':
            physical=kano.prior.cpu.cpu_body.cpu
            rows=physical.original.rows
            fields=rows(text,'FIELD');stores=rows(text,'HEALTH');by={r['frame']:r for r in fields}
            foreign=[h for h in stores if h['a8']not in(by[h['frame']]['actor'],by[h['frame']]['vactor'])or
                       h['a13']not in(by[h['frame']]['main'],by[h['frame']]['vmain'])]
            need(report['error']=="AssertionError('Only actual executing CPU/human Main, no foreign actor aliases')"and
                 len(foreign)==1 and foreign[0]['frame']==1838 and foreign[0]['before']-foreign[0]['after']==22,
                 'Exact current missing projectile-origin evidence; no unknown owner waiver')
            mechanism=physical.verify_log(text,'kano',state['guest'])
            records[name].update(originalFullPhysicalPairAndOwnFollowup=mechanism,
                                 missingIndependentProjectileOwnershipStores=foreign,wholeTraceAcceptance=False)
    body=ring['case'];flow=body['state'];move=flow['selectedOriginalRing']['acceptedRings']
    need(reviewed==14 and len(move)==1 and move[0]['damage']==22 and not move[0]['blocked']and
         flow['wholeNativeHealthHistory']['nativeHealthStores']==31 and
         flow['wholeNativeHealthHistory']['totalNativeDamageByPhysicalSlot']=={'1':161,'2':0}and
         flow['wholeNativeHealthHistory']['actualOwnedRingDamageStores']==1 and
         not flow['wholeNativeHealthHistory']['unknownActorAliasesAccepted'],
         'Actual current unblocked native ring, every31 native HP context and native owned KO boundary')
    build=ROOT/current.startup.NAME;restore=json.loads((build/'restoration.json').read_text(encoding='utf-8-sig'))
    launcher=ROOT/'PLAY_LATEST_KANO_SONYA.cmd'
    need(sha(build/'mkport_candidate.exe')==state['build']['executable_sha256']and restore['passed']and
         all(sha(p)==h for p,h in restore['restored_actual_preexisting_files'].items())and
         not(ROOT/'mame-mkp/build/mingw-gcc').exists()and
         sha(launcher)=='D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5',
         'Same private executable, preserved dirty canonical files, absent compiler cache/public CMD unchanged')
    for p in(Path(__file__),ring_path,build/'restoration.json',launcher,
             ROOT/'tools/read_native_selector_cpu_frames.py',ROOT/'tools/read_native_selector_cpu_frames_remote.py'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All actual retained evidence/source pins unchanged')
    OUT.mkdir()
    value=dict(passed=True,candidate=current.startup.NAME,goalStatus='active',thisGoalTurnClassification='progress',
        previousGoalTurnClassification='no progress: status-only answer',
        actualCurrentNativeCPUJobs=2,actualReviewedNativeFields=14,records=records,
        actualCurrentCPUSonyaRing=move[0],actualWholeNativeHealth=flow['wholeNativeHealthHistory'],
        actualContiguousActorFields=body['actualContiguousActorFields'],
        actualSourceBoundAddedFighterShadowCopies=body['actualAddedFighterShadowCopies'],
        actualWholeNativeFlagStores=flow['wholeNativeFlagStores'],actualApplicableFaultsRejected=41,
        observations=['Reviewed true Kano choke actions/native shadows/recovery in6 actual fields',
                      'Reviewed true Sonya CSS/cleared exit/ordinary match/all5leg poses in8 actual fields',
                      'Ring ownership/flight/guard/22HP/impact/retirement and every31 HP store pass source contracts, not ring raster or PCM acceptance'],
        requirements=['selection','transition','identity','names','human_moves','cpu_moves','ordinary_combat','ground_shadows',
                      'audio','finishers_victims','stage_finishers','campaign_cinematics','cmd_release','storage'],
        remainingGroups=['Broader startup cue/CPU/overlap/hit/KO/selection/reset/morph ownership cleanup/full UI ground/audio',
            'Broader CPU projectile arena shadow/audio',
            'Later-stage controls/continue audio/post-ending fresh join',
            'Remaining Pit/Tomb/stock victim finishers and sound priority',
            'Secret/morph/cinematics','Final combined visual/audio/gameplay and matching public CMD/finished ZIP'],
        wholeKanoCPUTraceAccepted=False,standaloneRepeatedSonyaLegAccepted=False,compoundLegPhaseAccepted=False,
        fullKOTransitionAccepted=False,allCPUContextsAccepted=False,allArenasAccepted=False,fullRasterAcceptance=False,
        fullAudioAcceptance=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,inputHashes=pins)
    path=OUT/'report.json';current.prior.save(path,value);digest=sha(path)
    need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0and sha(path)==digest,
         'Lossless exact-file receipt compression')
    print(json.dumps(dict(passed=True,actualNativeCPUJobs=2,actualReviewedNativeFields=14,
        applicableFaultsRejected=41,fullPortAcceptance=False)),flush=True)
    return value


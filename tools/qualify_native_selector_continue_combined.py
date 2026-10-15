"""Four original physical CPU-loss/cross-continue routes and 24 reviewed fields.

Finite stage-zero acceptance only. Original failure, actual kernel receipt,
source-bound CPU choke predicate, full windows, all original fault suites and
native callback digests remain required. No full-port/audio/all-stage claim.
"""
import hashlib,json
from pathlib import Path
import qualify_native_selector_continue_paired_kernel as native
ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_native_selector_continue_combined_checked'
VIEWED=json.loads(r'''{"kano_p1_to_sonya":[{"index":7,"header":{"frame":3634,"label":"ui_3634.png","bytes":406400,"sha256":"90062B5D9EB2692485D5C19357574754D915701DF63B8713BC5CECC5CC6C5828"},"SHA256":"90062B5D9EB2692485D5C19357574754D915701DF63B8713BC5CECC5CC6C5828"},{"index":80,"header":{"frame":3922,"label":"ui_3922.png","bytes":406400,"sha256":"42525D5176578503CB4FDC006C1D3B6BDB04E1812BAF4A012D550251A8C0A9D8"},"SHA256":"42525D5176578503CB4FDC006C1D3B6BDB04E1812BAF4A012D550251A8C0A9D8"},{"index":23,"header":{"frame":3672,"label":"ui_3672.png","bytes":406400,"sha256":"A07D07F83958DD8B996AF18A2663F18D700598C71538BFFAE563753EC0FD7090"},"SHA256":"A07D07F83958DD8B996AF18A2663F18D700598C71538BFFAE563753EC0FD7090"},{"index":110,"header":{"frame":3982,"label":"ui_3982.png","bytes":406400,"sha256":"BE3700D96809BAC346B85DBCE2F028B68078907F5147EAEFC89C7A7115353756"},"SHA256":"BE3700D96809BAC346B85DBCE2F028B68078907F5147EAEFC89C7A7115353756"},{"index":134,"header":{"frame":4030,"label":"ui_4030.png","bytes":406400,"sha256":"BE3700D96809BAC346B85DBCE2F028B68078907F5147EAEFC89C7A7115353756"},"SHA256":"BE3700D96809BAC346B85DBCE2F028B68078907F5147EAEFC89C7A7115353756"},{"index":162,"header":{"frame":4278,"label":"ui_4278.png","bytes":406400,"sha256":"967AD20DFE48B4DE227A56B7BBFCECC402544AABABDFB528CA9030A8726B9CD0"},"SHA256":"967AD20DFE48B4DE227A56B7BBFCECC402544AABABDFB528CA9030A8726B9CD0"}],"sonya_p1_to_kano":[{"index":7,"header":{"frame":3498,"label":"ui_3498.png","bytes":406400,"sha256":"C8EBD93BEAB95F329DDF7B5C72138C71C529ADE8C4256FD8AD08C647D117070F"},"SHA256":"C8EBD93BEAB95F329DDF7B5C72138C71C529ADE8C4256FD8AD08C647D117070F"},{"index":23,"header":{"frame":3536,"label":"ui_3536.png","bytes":406400,"sha256":"A9169B5F6878ED99C7940065262562AE018FFCD168EA85F38C1D04CE95C41860"},"SHA256":"A9169B5F6878ED99C7940065262562AE018FFCD168EA85F38C1D04CE95C41860"},{"index":80,"header":{"frame":3786,"label":"ui_3786.png","bytes":406400,"sha256":"8DB90D07B068562BA982D26451BEF6DECC014C2B4450A25BAD9596CC37120ED2"},"SHA256":"8DB90D07B068562BA982D26451BEF6DECC014C2B4450A25BAD9596CC37120ED2"},{"index":110,"header":{"frame":3846,"label":"ui_3846.png","bytes":406400,"sha256":"D6D8BB567F6FA9573053DD0571ED8A882975899425ABAF3A1E7755BE02287BAD"},"SHA256":"D6D8BB567F6FA9573053DD0571ED8A882975899425ABAF3A1E7755BE02287BAD"},{"index":134,"header":{"frame":3894,"label":"ui_3894.png","bytes":406400,"sha256":"D6D8BB567F6FA9573053DD0571ED8A882975899425ABAF3A1E7755BE02287BAD"},"SHA256":"D6D8BB567F6FA9573053DD0571ED8A882975899425ABAF3A1E7755BE02287BAD"},{"index":162,"header":{"frame":4142,"label":"ui_4142.png","bytes":406400,"sha256":"CFE75827F88ABB0D607AFE42B1D1FB672C1982E85DC88689A7FE247BBC193422"},"SHA256":"CFE75827F88ABB0D607AFE42B1D1FB672C1982E85DC88689A7FE247BBC193422"}],"kano_p2_to_sonya":[{"index":7,"header":{"frame":3662,"label":"ui_3662.png","bytes":406400,"sha256":"F1AB669F1405AD17BEDA6FD3C8BF70A071DC33835663B77E1C8ACCBC5AC24C71"},"SHA256":"F1AB669F1405AD17BEDA6FD3C8BF70A071DC33835663B77E1C8ACCBC5AC24C71"},{"index":80,"header":{"frame":3964,"label":"ui_3964.png","bytes":406400,"sha256":"E6419232BBEBB4DAA4CF343EE17DD6B8263DF0D08F19D5C1CA6B1CC19A3A849A"},"SHA256":"E6419232BBEBB4DAA4CF343EE17DD6B8263DF0D08F19D5C1CA6B1CC19A3A849A"},{"index":23,"header":{"frame":3706,"label":"ui_3706.png","bytes":406400,"sha256":"45186197C6E7BBF7706432828BD1EE9B80DA4DC366E509EDB976C276994834B8"},"SHA256":"45186197C6E7BBF7706432828BD1EE9B80DA4DC366E509EDB976C276994834B8"},{"index":30,"header":{"frame":3868,"label":"ui_3868.png","bytes":406400,"sha256":"8526F8DD49FFCB47B20DDC650354529254DCD3F6F1B9F8C4E61B75E00A80C26F"},"SHA256":"8526F8DD49FFCB47B20DDC650354529254DCD3F6F1B9F8C4E61B75E00A80C26F"},{"index":134,"header":{"frame":4118,"label":"ui_4118.png","bytes":406400,"sha256":"DCE8ECBE2D7655BB08BAADE721E50042018C550EF73C294B9CB7C329F35E5568"},"SHA256":"DCE8ECBE2D7655BB08BAADE721E50042018C550EF73C294B9CB7C329F35E5568"},{"index":156,"header":{"frame":4304,"label":"ui_4304.png","bytes":406400,"sha256":"A272F1BE42F32FF1DA7E7C62A4B492E94EE15971B5DC35FAC782E073C896BDFF"},"SHA256":"A272F1BE42F32FF1DA7E7C62A4B492E94EE15971B5DC35FAC782E073C896BDFF"}],"sonya_p2_to_kano":[{"index":7,"header":{"frame":3638,"label":"ui_3638.png","bytes":406400,"sha256":"A8DF67D6BFD6E07347AB1BD27D68A7D493814FA3BEF4C75E8C73194A35D84786"},"SHA256":"A8DF67D6BFD6E07347AB1BD27D68A7D493814FA3BEF4C75E8C73194A35D84786"},{"index":80,"header":{"frame":3940,"label":"ui_3940.png","bytes":406400,"sha256":"566794CF198E2D6E9CBF3631178E29ADFF4C38FC0F03889733627FA9E2C0FF23"},"SHA256":"566794CF198E2D6E9CBF3631178E29ADFF4C38FC0F03889733627FA9E2C0FF23"},{"index":23,"header":{"frame":3682,"label":"ui_3682.png","bytes":406400,"sha256":"042A58DE51B77769855540C113A5077C923514D1E67DA7CB55E6C71B88754BE0"},"SHA256":"042A58DE51B77769855540C113A5077C923514D1E67DA7CB55E6C71B88754BE0"},{"index":30,"header":{"frame":3844,"label":"ui_3844.png","bytes":406400,"sha256":"39B58968B1465BC01E688B91CAFD9EEFF889FE6AC32944197E9D3BC9B1DF1C57"},"SHA256":"39B58968B1465BC01E688B91CAFD9EEFF889FE6AC32944197E9D3BC9B1DF1C57"},{"index":134,"header":{"frame":4094,"label":"ui_4094.png","bytes":406400,"sha256":"DCE8ECBE2D7655BB08BAADE721E50042018C550EF73C294B9CB7C329F35E5568"},"SHA256":"DCE8ECBE2D7655BB08BAADE721E50042018C550EF73C294B9CB7C329F35E5568"},{"index":156,"header":{"frame":4280,"label":"ui_4280.png","bytes":406400,"sha256":"4772C218BD3B49B708C50630B380AEB48433C32DAA6F30D5FA2ACACFB867D8A2"},"SHA256":"4772C218BD3B49B708C50630B380AEB48433C32DAA6F30D5FA2ACACFB867D8A2"}]}''')


def verify(state,cases,handles,expected):
    need(not OUT.exists()and not native.kernel.census(),'All original games actually terminal; fresh combined receipt')
    wanted={'kano_p1_to_sonya','sonya_p1_to_kano','kano_p2_to_sonya','sonya_p2_to_kano'}
    need(set(state['COMPLETED'])==wanted and len(state['COMPLETED'])==4 and set(VIEWED)==wanted,
         'All four distinct physical cross-character continue routes qualified')
    routes={};pins={};total=0;faults=controls=pixel_faults=0
    for key in sorted(wanted):
        fighter,slot,_,target=key.split('_');side=int(slot[1:])
        folder,text,images,captured=cases[key];held=handles[key]
        proof_path=ROOT/f'audit_native_selector_continue_extra_windows_checked_{key}/report.json'
        pixel_path=ROOT/f'audit_native_selector_continue_extra_windows_pixels_{key}/report.json'
        control_path=ROOT/f'audit_native_selector_continue_extra_windows_control_faults_{key}/report.json'
        proof=json.loads(proof_path.read_text());pixels=json.loads(pixel_path.read_text());control=json.loads(control_path.read_text())
        need(held['process'].poll()==0 and captured['nativeExit']==0 and proof['passed']and pixels['passed']and control['passed']and
             proof['actualGuestGFXProofs']==expected and captured['actualGuestGFXProofs']==expected,
             'Each actual native terminal and all five exact whole/limited memory proofs')
        need(len(proof['actualFaultsRejected'])==18 and len(control['actualControlFaultsRejected'])==9 and
             len(pixels['additionalActualImageFaultsRejected'])==(3 if key=='sonya_p2_to_kano'else 2),
             'All original state/raster/ordinary-response/extra-pixel faults retained')
        native_identity=held.get('recoveredIdentity',held.get('identity'))
        need(proof['nativeIdentity']==native_identity and native_identity['ProcessId']==held['process'].pid and
             native_identity['ParentProcessId']==40856,'Exact original native handles, no replay/replacement')
        for report in (proof,pixels,control,captured):
            need(not report['fullPortAcceptance'],'Finite test never substituted for the full objective')
            need(all(sha(p)==h for p,h in report['inputHashes'].items()),'All actual captured source and proof bytes remain unchanged')
            pins.update(report['inputHashes'])
        need(proof['actualSinglePlayerContinue']['trueIdentity']==(17 if target=='kano'else 18)and
             proof['actualSinglePlayerContinue']['actualWalkJumpPunchAccepted'],
             'Actual true continued identity and real walk/jump/punch/recovery')
        if key=='kano_p2_to_sonya':
            recovery=Path(proof['nativeCapture']);identity=json.loads((recovery/'identity_recovery.json').read_text())
            restored=json.loads((recovery/'report.json').read_text())
            need(captured['passed']is False and restored['passed']and identity['passed']and
                 identity['originalCaptureSHA256']==sha(folder/'report.json')and
                 restored['originalRejectedCaptureSHA256']==sha(folder/'report.json')and
                 (recovery/'stderr.log').samefile(folder/'stderr.log'),
                 'Original rejected capture stays FALSE; exact kernel recovery and same original stderr retained')
        else:need(captured['passed'],'Original capture positive on unchanged current guest')
        need(len(VIEWED[key])==6,'Six actually viewed callback fields per route')
        for row in VIEWED[key]:
            actual=captured['actualFullRGBDigests'][row['index']]
            need(actual==row['header']and actual['sha256']==row['SHA256']and
                 hashlib.sha256(images[actual['frame'],actual['label']]).hexdigest().upper()==row['SHA256'],
                 'Actually reviewed raw native raster equals original callback digest')
            total+=1
        for p in (proof_path,pixel_path,control_path,folder/'report.json',folder/'native_terminal.json'):
            pins[str(p.resolve())]=sha(p)
        faults+=len(proof['actualFaultsRejected']);controls+=len(control['actualControlFaultsRejected'])
        pixel_faults+=len(pixels['additionalActualImageFaultsRejected'])
        routes[key]=dict(nativeIdentity=native_identity,nativeExit=0,
            actualSinglePlayerContinue=proof['actualSinglePlayerContinue'],nameShadowChecks=proof['actualUIPixels']['native_name_shadow_checks'],
            selectedPlayerLadderIcon=pixels['selectedPlayerLadderIcon'],viewedActualFields=VIEWED[key],
            fullExactMemoryProofs=expected,originalCapturePassed=captured['passed'],rawPixelsOnlyInOriginalHostRAM=True)
    need(total==24 and faults==72 and controls==36 and pixel_faults==9,'Complete finite four-route totals')
    build=ROOT/state['current'].NAME
    need(sha(build/'mkport_candidate.exe')==state['build']['executable_sha256']and
         sha(ROOT/'PLAY_LATEST_KANO_SONYA.cmd')=='D6BABF8CBC1F4CB020F3D7F3A2C8C5A3A762B946E83D56FC1E5BA3B398129DE5'and
         not(ROOT/'mame-mkp/build/mingw-gcc').exists(),'Exact private build; public launcher unchanged; compiler cache absent')
    restore=json.loads((build/'restoration.json').read_text(encoding='utf-8-sig'))
    need(restore['passed']and all(sha(p)==h for p,h in restore['restored_actual_preexisting_files'].items()),
         'Original dirty canonical files still preserved')
    for p in (Path(__file__),Path(native.__file__),ROOT/'tools/finish_native_selector_continue_kernel_recovery.py',
              ROOT/'tools/read_native_selector_continue.py',ROOT/'tools/read_native_selector_continue_remote.py',
              ROOT/'audit_native_selector_continue_paired_kernel_source/report.json',build/'restoration.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Final authoritative source/proof stability')
    result=dict(passed=True,finiteStageZeroFourPaidCrossCharacterContinueRoutesAccepted=True,
        actualReviewedNativeFields=24,actualStateRasterFaultsRejected=72,actualResponseFaultsRejected=36,
        actualExtraPixelFaultsRejected=9,actualSourceBoundPairedOriginFaultsRejected=10,routes=routes,inputHashes=pins,
        scope='actual physical released-input CPU-earned loss, paid cross-character continue, native CSS/preview/number/border/own ladder icon/teardown/name shadow, true identities and ordinary recovery in stage-zero cases only',
        newNativeBootsDuringQualification=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        fullPortAcceptance=False,allStagesAccepted=False,audioAccepted=False,publicPlayableChanged=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,routes=4,reviewedNativeFields=24,stateRasterFaults=72,actualResponseFaults=36,extraPixelFaults=9,fullPortAcceptance=False)),flush=True)
    return result


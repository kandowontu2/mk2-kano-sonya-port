"""Complete finite Scorpion-secondary renderer matrix, six actual contexts.

Stock Kitana P1/Liu P2 and true Kano/Sonya both victim slots. Preserve full
native earned/state/callback/owned FIFO/source/palette/pixel/retirement gates.
No new game runs, media copies, artistic/all-arena/audio/full-port acceptance.
"""
import copy,json,re,subprocess,traceback
from pathlib import Path
import run_current_scorpion_secondary_state_v4549 as state
import scorpion_secondary_native_scene_model_v4581 as model
import verify_stock_scorpion_secondary_renderer_v4637 as stock
ROOT,need,sha=state.ROOT,state.need,state.sha
OUT=ROOT/'audit_v4652_complete_scorpion_secondary_renderer_matrix_checked'
ROLES={'kitana_p1':('kitana',1,4),'liu_kang_p2':('liu_kang',2,1),
       'kano_p1':('kano',1,17),'kano_p2':('kano',2,17),
       'sonya_p1':('sonya',1,18),'sonya_p2':('sonya',2,18)}

def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]

def contract(cases,graphics):
    need(set(cases)==set(ROLES),'All six actual stock/true-added physical contexts, no missing role or proxy')
    signatures={side:cases[key]['native']['nativeInstructionCallbackSignature']for key,side in [('kitana_p1',1),('liu_kang_p2',2)]}
    result=[]
    for key,(fighter,side,identity)in ROLES.items():
        c=cases[key];native,meta=c['native'],c['meta']
        need(native['identity']==identity and native['victimSlot']==side and
             native['actualNativeCollisionWrites']==10 and native['actualEarnedKOs']==2 and
             native['exactPhysicalStateFields']==960 and native['actualHeldReleaseInputFields']==111 and
             native['nativeInstructionCallbackSignature']==signatures[side],
             'Every true same-slot earned/held-release/cooperative native state matches original stock '+key)
        need(meta['exit_code']==0 and meta['guestSHA256']=='938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'and
             meta['completeGuestBytesComparedInRAM']==1048576 and meta['nativeRGBFramesDigested']==62 and not meta['sceneErrors']and
             meta['rawMediaGuestROMOrBuildFilesWritten']==0 and not meta['cheatsEnabled']and meta['assistance']=='none',
             'Actual native terminal/current guest/full pipeline/no assistance or media writes '+key)
        need(len(meta['nativeRasterFaults'])==2 and {r['kind']for r in meta['nativeRasterFaults']}=={'VRAM target bit','visible RGB bit'},
             'Every original actual native bitmap counterexample retained '+key)
        start=native['actualNativeActivation'];end=c['rendererRetirement']
        need(end+1==native['actualNativeRetirement']and len(c['retired'])==1 and int(c['retired'][0]['frame'])==end and
             c['retired'][0]['p1']==c['retired'][0]['p2']=='00000000',
             'Both original callback phases and genuine both-pointer renderer retirement '+key)
        records,visible,fields=c['records'],c['visible'],c['fields']
        need([r['frame']for r in records]==list(range(start+1,end+31))and len(records)==len(visible)==557==meta['exactNativeSceneFields']and
             [int(r['frame'])for r in fields]==list(range(start,end+31)),
             'Whole actual557 render targets and exactly thirty later renderer fields, no gaps '+key)
        need(all(r['exactVRAMWords']==512*512 and r['exactRGBPixels']==400*254 and
                 v['file']==f"display_{r['frame']}.png"and r['rgbSHA256']==v['rgbSHA256']for r,v in zip(records,visible,strict=True)),
             'Every entire native VRAM/RGB comparison and actual raw-RAM digest binding '+key)
        need(all(r['p1']==r['p2']=='00000000'for r in fields if int(r['frame'])>=end),
             'Retired physical pointers remain cleared throughout native cleanup window '+key)
        queues=c['queues'];need(queues and c['dispatch'],'Actual owned physical FIFO and native palette dispatch '+key)
        need({int(q['id'])for q in queues}=={10,identity}and all(q['owner']==q['actor']and q['id']==q['roster']and
             int(q['id'])==(identity if int(q['slot'])==side else 10)for q in queues),
             'Every actual true physical FIFO owner/id/roster/slot, no proxy or anonymous effects '+key)
        actors={q['actor']for q in queues}
        need(not any(int(q['frame'])>=end and q['actor']in actors for q in c['allQueues']),
             'No retired physical actor republished in actual native FIFO '+key)
        gfx=c['graphics'];need(gfx and len({r['key']for r in gfx})==len(gfx)and all(
             0<=int(r['first'])<int(r['first'])+int(r['bytes'])<=len(graphics)and
             model.digest(graphics[int(r['first']):int(r['first'])+int(r['bytes'])])==r['data_sha256']for r in gfx),
             'Every observed native graphics byte stream equals independent ROM/payload/UI source '+key)
        if identity>=17:
            need(c['ownShadowComponents']and all(int(r['id'])==identity and int(r['slot'])==side and r['owner']==r['actor']
                 for r in c['ownShadowComponents']), 'Actual compressed true added-victim shadow components '+key)
        else:need(c['originalStockShadowRows']>0 and not c['ownShadowComponents'],
                  'Actual independently qualified stock row/font ledger, no manufactured own-art marker '+key)
        result.append(dict(case=key,identity=identity,victimSlot=side,completeFields=557,rendererRetirement=end,
                           actualNativeGraphicsStreams=len(gfx),ownedPaletteDispatches=len(c['dispatch']),
                           actualBitmapFaults=2,postRetirementFields=30))
    return result

def verify():
    need((ROOT/'audit_v4643_scorpion_secondary_liu_kang_p2_native_scene_checked/report.json').exists(),
         'Actual missing Liu stock renderer must reach terminal first')
    cases={};pins={str(Path(__file__).resolve()):sha(__file__)}
    sources={
      'kano_p1':ROOT/'audit_v4593_scorpion_secondary_render_callback_phase_checked/report.json',
      'kitana_p1':ROOT/'audit_v4638_stock_kitana_scorpion_secondary_renderer_checked/report.json',
      'liu_kang_p2':ROOT/'audit_v4643_scorpion_secondary_liu_kang_p2_native_scene_checked/report.json'}
    for key in ('kano_p2','sonya_p1','sonya_p2'):
        sources[key]=ROOT/f'audit_v4598_scorpion_secondary_{key}_native_scene_checked/report.json'
    for key,path in sources.items():
        proof=json.loads(path.read_text());need(proof['passed'],'Every actual individually qualified renderer context '+key)
        for p,h in proof['inputHashes'].items():
            need((p not in pins or pins[p]==h)and sha(p)==h,'Consistent unchanged actual source/capture/native byte pin')
            pins[p]=h
        pins[str(path)]=sha(path);folder=Path(proof['capture']);text=(folder/'run.log').read_text()
        native=state.contract(text,*ROLES[key][:2])
        retired=rows(text,'FLOOR_RETIRED')
        cases[key]=dict(native=native,meta=json.loads((folder/'result.json').read_text()),
          records=json.loads((folder/'native_scene_records.json').read_text()),
          visible=json.loads((folder/'native_scene_visible_digests.json').read_text()),
          rendererRetirement=int(retired[0]['frame']),retired=retired,fields=rows(text,'FLOOR_STATE'),
          queues=rows(text,'FLOOR_QUEUE'),dispatch=rows(text,'FLOOR_QUEUE_DISPATCH'),allQueues=rows(text,'FLOOR_ALL_QUEUE'),
          graphics=rows(text,'FLOOR_GFX'),ownShadowComponents=rows(text,'SHADOW_COMPONENT'),
          originalStockShadowRows=len(stock.stock_shadow_rows(text))if key in ('kitana_p1','liu_kang_p2')else 0)
        baseline=ROOT/f'audit_v4552_scorpion_secondary_{key}_native_state_ram/native_rgb_digests.json'
        need(json.loads(baseline.read_text())==json.loads((folder/'native_rgb_digests.json').read_text()),
             'All original62 same-context native controller RGB digests unchanged '+key)
        pins[str(baseline)]=sha(baseline)
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p)]=sha(p)
    graphic_pins={};graphics=model.sources((ROOT/state.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes(),graphic_pins);pins.update(graphic_pins)
    positive=contract(cases,graphics);faults=[]
    # Mutate actual retained targets/rows only in RAM; never touch frozen logs.
    for key in ROLES:
        original=cases[key]
        mutations=[]
        changed=dict(original,records=original['records'][:10]+original['records'][11:]);mutations.append(('missing_actual_render_field',changed))
        records=copy.deepcopy(original['records']);records[10]['rgbSHA256']='0'*64;mutations.append(('wrong_actual_RGB_digest',dict(original,records=records)))
        native=dict(original['native'],identity=99);mutations.append(('wrong_true_native_identity',dict(original,native=native)))
        meta=dict(original['meta'],guestSHA256='0'*64);mutations.append(('wrong_actual_guest',dict(original,meta=meta)))
        meta=dict(original['meta'],nativeRasterFaults=original['meta']['nativeRasterFaults'][:1]);mutations.append(('missing_actual_bitmap_fault',dict(original,meta=meta)))
        queues=copy.deepcopy(original['queues']);queues[0]['owner']='01000000';mutations.append(('wrong_actual_owned_FIFO_actor',dict(original,queues=queues)))
        gfx=copy.deepcopy(original['graphics']);gfx[0]['data_sha256']='0'*64;mutations.append(('wrong_observed_source_bytes',dict(original,graphics=gfx)))
        for label,changed in mutations:
            altered=dict(cases);altered[key]=changed
            try:contract(altered,graphics)
            except ValueError as error:faults.append(dict(case=key,label=label,rejectedBy=str(error)))
            else:raise ValueError('Accepted actual matrix fault: '+key+' '+label)
            need(contract(cases,graphics)==positive,'Entire unchanged six-context positive restored after every actual fault')
    missing=dict(cases);missing.pop('sonya_p2')
    try:contract(missing,graphics)
    except ValueError as error:faults.append(dict(label='missing_actual_sonya_p2_context',rejectedBy=str(error)))
    else:raise ValueError('Accepted missing actual context')
    need(contract(cases,graphics)==positive,'Final unchanged full six-context matrix positive')
    need(all(sha(p)==h for p,h in pins.items()),'Every actual source/capture/compiled/public input unchanged')
    return dict(passed=True,currentStockAndBothTrueAddedVictimsBothSlotsCompleteNativeRendererWindowsAccepted=True,
      actualContexts=6,contexts=positive,actualConsecutiveNativeRendererFields=3342,exactRGBPixels=3342*400*254,
      exactVRAMWords=3342*512*512,actualMatrixFaultsRejected=faults,actualNativeBitmapFaultsRetained=12,
      everySameSlotOriginalNativeCooperativeCallbackSignatureEqual=True,everyOriginalControllerRGBDigestUnchanged=True,
      wholeFiniteCurrentVsStockRendererMatrixAccepted=True,independentArtAllArenaAlternateGroundAudioAccepted=False,
      fullPortAcceptance=False,rawMediaGuestROMOrBuildCopies=0,publicPlayableOrReleaseChanged=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable entire finite native renderer matrix')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','actualMatrixFaultsRejected')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)

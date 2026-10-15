"""Qualify frozen stock Kitana renderer using actual original shadow row DMA.

No own-art SHADOW_COMPONENT marker is manufactured. All whole557-field
pipeline/physical/callback/graphics/VRAM/RGB and actual bitmap fault evidence
is retained. This is not absolute shadow geometry, all arenas, audio, or a
completed current-vs-stock matrix (stock Liu P2 renderer remains missing).
"""
import copy,inspect,json,re,subprocess,traceback
from pathlib import Path
import verify_scorpion_secondary_render_callback_phase_v4592 as previous
ROOT,need,sha,model,state=previous.ROOT,previous.need,previous.sha,previous.model,previous.state
CASE=ROOT/'audit_v4597_scorpion_secondary_kitana_p1_native_scene_ram'
OUT=ROOT/'audit_v4626_stock_kitana_scorpion_secondary_renderer_checked'
rows=previous.rows

def stock_shadow_rows(text):
    dmas=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_DMA')
    native=[d for d in dmas if int(d['source'],16)<0x10000000 and int(d['command'],16)&15==8]
    regs=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_DMA_REGS')
    need(len({r['event']for r in regs})==len(regs),'Unique actual native DMA register event ledger')
    registers={r['event']:r for r in regs}
    graphics=rows(text,'MK2_NAT_CAMPAIGN_FLOOR_GFX')
    need(len({r['key']for r in graphics})==len(graphics),'Unique observed complete original source streams')
    gfx={r['key']:r for r in graphics}
    need(native,'Actual original stock shadow row draws, not own-art metadata')
    for d in native:
        need(d['pc']in ('FF8015A0','FF801610')and d['palette']=='0000'and d['color']=='15'and
             d['height']=='1'and int(d['width'])>0 and d['scaleX']==d['scaleY']=='256'and d['skip']=='0'and
             ((int(d['command'],16)>>12)&7)==6,
             'Original native six-bit solid-black one-row shadow DMA/caller/unit-scale contract')
        r=registers[d['event']]
        need(r['frame']==d['frame']and r['source']==d['source']and r['command']==d['command']and
             int(r['a0'],16)==int(d['y'])and r['a1']=='00000001',
             'Exact actual native shadow DMA event/source/command/row register provenance')
        key=f"{int(d['source'],16):08X}_{int(d['command'],16):04X}_{d['width']}_1"
        need(key in gfx and int(gfx[key]['bytes'])>0,
             'Every original shadow row has actual independently source-bound graphics bytes')
    return native

text=inspect.getsource(previous.contract)
changes=[
    ("state.contract(text,'kano',1)","state.contract(text,'kitana',1)"),
    ("shadows=rows(text,'MK2_NAT_CAMPAIGN_SHADOW_COMPONENT')","shadows=stock_shadow_rows(text)"),
    ("{'17','10'}","{'4','10'}"),
    ('Actual true Kano17/Scorpion10 owned body FIFO, palette dispatch and compressed floor-shadow components',
     'Actual true Kitana4/Scorpion10 owned FIFO/palette dispatch and original stock shadow row DMA'),
    ('nativeCompressedShadowComponents=len(shadows)','actualOriginalStockShadowRowDMAs=len(shadows)')]
for before,after in changes:
    need(text.count(before)==1,'Only exact stock role/shadow evidence type adaptation: '+before)
    text=text.replace(before,after,1)
scope=dict(vars(previous),stock_shadow_rows=stock_shadow_rows)
exec(compile(text,__file__+'::entire4592_stock_original_shadow_DMA_contract','exec'),scope)
contract=scope['contract']

def verify():
    log=(CASE/'run.log').read_text();meta=json.loads((CASE/'result.json').read_text())
    records=json.loads((CASE/'native_scene_records.json').read_text())
    visible=json.loads((CASE/'native_scene_visible_digests.json').read_text())
    pins=dict(meta['input_hashes'])
    need(all(sha(p)==h for p,h in pins.items()),'Every frozen executed source/build/native input unchanged')
    positive=contract(log,meta,records,visible)
    need(len(records)==557 and not rows(log,'MK2_NAT_CAMPAIGN_SHADOW_COMPONENT'),
         'Real stock557 field window; own-art-only metadata absent, not fabricated')
    baseline=ROOT/'audit_v4552_scorpion_secondary_kitana_p1_native_state_ram/native_rgb_digests.json'
    need(json.loads(baseline.read_text())==json.loads((CASE/'native_rgb_digests.json').read_text()),
         'All62 original stock native physical-controller RGB digests exactly unchanged')
    guest=state.source.current.expected();rom_path=ROOT/'mk2/mk2-maincpu.bin';rom=rom_path.read_bytes()
    first,last=(0xff801070-0xff800000)//8,(0xff8017a0-0xff800000)//8
    need(guest[first:last]==rom[first:last],'Entire actual native shadow scanner/row-copy routine byte-exact stock MK2')
    graphic_pins={};graphics=model.sources((ROOT/state.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes(),graphic_pins)
    gfx=rows(log,'MK2_NAT_CAMPAIGN_FLOOR_GFX')
    need(gfx and all(0<=int(r['first'])<int(r['first'])+int(r['bytes'])<=len(graphics)and
                    model.digest(graphics[int(r['first']):int(r['first'])+int(r['bytes'])])==r['data_sha256']for r in gfx),
         'Every actual native graphics stream, including every stock shadow row, independently byte-exact')
    faults=[];retired=positive['rendererRetirement']
    mutations=[('missing_actual_render_field',log,meta,records[:10]+records[11:],visible),
      ('wrong_retirement_phase',log.replace(f'MK2_NAT_CAMPAIGN_FLOOR_RETIRED frame={retired} ',f'MK2_NAT_CAMPAIGN_FLOOR_RETIRED frame={retired+1} ',1),meta,records,visible),
      ('shortened_post_retirement_window',log,meta,records[:-1],visible[:-1]),
      ('native_guest_mismatch',log,dict(meta,guestSHA256='0'*64),records,visible),
      ('hidden_actual_render_error',log,dict(meta,sceneErrors=[dict(error='actual failure')]),records,visible),
      ('missing_actual_pixel_counterexample',log,dict(meta,nativeRasterFaults=meta['nativeRasterFaults'][:1]),records,visible)]
    native=stock_shadow_rows(log);d=native[0]
    for label,key,value in [('wrong_original_shadow_caller','pc','FF801590'),('wrong_black_pen','color','14'),
                            ('wrong_original_row_height','height','2'),('wrong_original_source','source','00000000')]:
        lines=log.splitlines();index=next(i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_DMA ')and
                                         f"event={d['event']} "in line)
        before=lines[index];lines[index]=re.sub(r'\b'+key+r'=[^\s]+',key+'='+value,before)
        need(lines[index]!=before,'Actual non-vacuous original shadow DMA fault')
        mutations.append((label,'\n'.join(lines)+'\n',meta,records,visible))
    for label,changed,m,r,v in mutations:
        try:contract(changed,m,r,v)
        except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted actual stock pipeline/shadow fault: '+label)
        need(contract(log,meta,records,visible)==positive,'Whole untouched original stock positive restored after each fault')
    phase=ROOT/'audit_v4593_scorpion_secondary_render_callback_phase_checked/report.json'
    phase_report=json.loads(phase.read_text())
    need(phase_report['passed']and all(sha(p)==h for p,h in phase_report['inputHashes'].items()),
         'Original callback source ordering and all current pipeline evidence unchanged')
    pins.update(graphic_pins)
    for p in [baseline,rom_path,phase,Path(__file__).resolve(),Path(previous.__file__),*CASE.rglob('*')]:
        if p.is_file():pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All original source/capture/public/native inputs unchanged after qualification')
    return dict(passed=True,fighter='kitana',physicalVictimSlot=1,identity=4,capture=str(CASE),
      actualNativeCallbackPhase=positive,exactConsecutiveNativeRendererFields=557,
      exactRGBPixels=557*400*254,exactVRAMWords=557*512*512,
      originalStockShadowRowDMAs=len(native),everyObservedGraphicsStreamByteExact=True,exactGraphicsStreams=len(gfx),
      everyOriginalControllerRGBDigestUnchanged=True,actualPipelineAndStockShadowFaultsRejected=faults,
      actualPixelFaultsRejected=meta['nativeRasterFaults'],completeNativeRendererWindowAccepted=True,
      ownArtShadowMetadataFabricated=False,completeCurrentVsStockRendererMatrixAccepted=False,
      absoluteShadowGeometryAllArenasArtAudioAccepted=False,fullPortAcceptance=False,
      priorFrozenCollectorFailure='Required own-art-only SHADOW_COMPONENT marker for stock shadow row DMA, despite all557 real pipeline fields passing.',
      inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable original stock renderer qualification')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)

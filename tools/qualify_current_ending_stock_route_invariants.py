"""Original-ROM caller/command-table/queue ordering gates, artifact-only."""
import copy,gzip,json,re,struct
import verify_native_source_sync as sync
sync.verify();R=sync.ROOT;stock=(R/'mk2/mk2-maincpu.bin').read_bytes()
def off(a):return(a-0xff800000)//8
def words(a,n):return struct.unpack_from('<'+'H'*n,stock,off(a))
def rows(side):
 p=R/f'audit_v5739_sonya_p{side}_ending_audio/run.log.gz'
 d=json.loads((R/f'audit_v5745_sonya_p{side}_ending_audio_window_checked/report.json').read_text())
 groups={t:[] for t in ['ROUTE','QUEUE','PACKET']}
 for l in gzip.open(p,'rt'):
  for t in groups:
   if l.startswith('MK2_EAUDIO_'+t+' '):
    q=dict(re.findall(r'(\w+)=([^\s]+)',l))
    if d['ending']<=int(q['frame'])<d['attract']:groups[t].append(q)
 return groups,p
def gate(g):
 routes=g['ROUTE'];assert routes
 assert all(float(b['seconds'])>float(a['seconds']) for a,b in zip(routes,routes[1:]))
 accepted=[]
 for i,r in enumerate(routes):
  caller=int(r['return_pc'],16);code=int(r['a0'],16);entry=int(r['entry'],16)
  w=words(caller-80,5)
  if w[0]==0x09c0:
   assert code==w[1] and w[2]==0x0d5f and (w[3]|w[4]<<16)==entry
   assert entry in (0xffa12430,0xffa12530)
   mode='fixedMOVI_W'
  else:
   w=words(caller-96,6)
   assert w[0]==0x09e0 and w[3]==0x0d5f and(w[4]|w[5]<<16)==0xffa12180
   assert w[1]<=code<w[1]+w[2] and entry==0xffa12530
   mode='originalRandomRange'
  # Original dispatcher MOVI table,A1, independently decoded from stock.
  tablewords=words(entry+0x80,3);assert tablewords[0]==0x0b20
  table=tablewords[1]|tablewords[2]<<16;header,base=words(table+code*32,2)
  end=float(routes[i+1]['seconds']) if i+1<len(routes) else float('inf')
  q=[q for q in g['QUEUE'] if float(r['seconds'])<=float(q['seconds'])<end and all(q[k]==r[k] for k in ['frame','a8','a13'])]
  assert len(q)==1;q=q[0]
  slot={0xffa12a10:0,0xffa12a80:1,0xffa12b00:2}[int(q['entry'],16)]
  assert int(q['a1'],16)==header>>8 and int(q['a4'],16)==header&255 and int(q['a3'],16)==base
  p=[p for p in g['PACKET'] if float(q['seconds'])<=float(p['seconds'])<end and all(p[k]==r[k] for k in ['frame','a8','a13'])]
  assert len(p)==1 and int(p[0]['a3'],16)==base+slot and p[0]['entry']=='FFA13BA0'
  accepted.append(dict(caller=r['return_pc'],entry=r['entry'],cue=code,sourceMode=mode,table=f'{table:08X}',header=header,base=base,queueSlot=slot,packet=base+slot))
 return accepted
old=(R/'diagnostic_v5219_current_payload_rom_metadata/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp').read_text();new=(R/'mame-mkp/src/mame/midway/midtunit_m.cpp').read_text()
def predicate(s):return s[s.index('unsigned predicate_cursor = predicates;'):s.index('// Canonical roster IDs also select damage scaling.')]
assert predicate(old)==predicate(new)
results=[];pins={};faults=[]
for side in (1,2):
 g,p=rows(side);proof=gate(g);pins[str(p)]=sync.sha(p)
 for kind in ['wrong_cue','wrong_caller','reordered_routes','wrong_queue_base','wrong_packet']:
  b=copy.deepcopy(g)
  if kind=='wrong_cue':b['ROUTE'][0]['a0']='00000042'
  elif kind=='wrong_caller':b['ROUTE'][0]['return_pc']='FF9ED880'
  elif kind=='reordered_routes':b['ROUTE'][0],b['ROUTE'][1]=b['ROUTE'][1],b['ROUTE'][0]
  elif kind=='wrong_queue_base':b['QUEUE'][0]['a3']='00000000'
  else:b['PACKET'][0]['a3']='00000000'
  try:gate(b)
  except (AssertionError,KeyError):faults.append(dict(side=side,kind=kind))
  else:raise AssertionError('Fault admitted:'+kind)
 results.append(dict(side=side,actualOriginalROMBoundRoutes=len(proof),routes=proof))
out=R/'audit_current_ending_stock_route_invariants_checked';assert not out.exists();out.mkdir()
report=dict(originalStockCallerCueAndQueueOrderingInvariantsAccepted=True,actualHistoricalOwnEndingCases=results,effectiveFaultsRejected=faults,currentGenderPatchAllowlistExactlyConserved=True,allowedGenderPatch='FFA122A0 → exact existing Sonya/Jade female predicate trampoline; no arbitrary route substitution',stockROMSHA256=sync.sha(R/'mk2/mk2-maincpu.bin'),currentSourceSHA256=sync.sha(R/'mame-mkp/src/mame/midway/midtunit_m.cpp'),inputHashes=pins,scope='Fixed caller MOVI/CALL and random base/count independently decoded from originalROM; each observed route binds original dispatcher table priority/duration/base, selectedqueue slot and subsequentpacket in chronological owner window. Does not derive entire ending scheduler or prove independent stock waveform parity; historical accepted nativewaveforms retained.',independentStockEndingChoreographyWaveformAccepted=False,heardMixAccepted=False,newEmulatorRuns=0,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(report=str(out/'report.json'),routeCounts=[x['actualOriginalROMBoundRoutes'] for x in results],faults=len(faults))))

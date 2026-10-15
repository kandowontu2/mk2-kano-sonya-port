"""Transfer exact ending components, not whole changed-build gameplay or missing pixel/audio acceptance."""
import difflib,hashlib,json,re
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
oldroot=root/'diagnostic_v5219_current_payload_rom_metadata/input_sources/mame-mkp'
newroot=root/'mame-mkp'
out=root/'audit_current_sonya_ending_component_transfer_checked';assert not out.exists()
oldpath=oldroot/'src/mame/midway/midtunit_m.cpp';newpath=newroot/'src/mame/midway/midtunit_m.cpp'
assert sync.sha(oldpath)=='37E02771B1F20CF17D0D619F83033F5FE37FE5B62DCD9519F60872763BE0E57A'
old=oldpath.read_text();new=newpath.read_text()
def section(text,start,end):return text[text.index(start):text.index(end,text.index(start))]
start='constexpr unsigned ending_text_tables[2]';end='// The two-player BATTLE card'
a=section(old,start,end);b=section(new,start,end)
def normalize(text):
 text=re.sub(r'/\*.*?\*/|//[^\n]*','',text,flags=re.S)
 text=text.replace('0xff8f48f0), 41 * 4, rom + ending_picture_table','0xff8f48f0), 40 * 4, rom + ending_picture_table').replace('unsigned index = 41; index < 50','unsigned index = 40; index < 50')
 return text
def gate(candidate):
 assert normalize(a)==normalize(candidate)
 assert 'write32(ending_picture_table + (50 + fighter * 2 + page) * 4,' in candidate
 assert 'unsigned const original_offset = 0x0c00000 + (fighter ? 0x1000000 : 0x103599a);' in candidate
gate(b);faults=[]
for name,bad in (
 ('Sonya_story_changed',b.replace('SONYA BREAKS FREE','SONYA REMAINS CAPTIVE',1)),
 ('Sonya_picture_index_wrong',b.replace('50 + fighter * 2 + page','49 + fighter * 2 + page',1)),
 ('Sonya_crop_changed',b.replace('(fighter ? 4 : 149)','(fighter ? 5 : 149)',1)),
):
 assert bad!=b
 try:gate(bad)
 except AssertionError:faults.append(name)
 else:raise AssertionError('Ending transfer fault accepted')
equal_files={}
for name in ('src/mame/midway/mk2ks_native_picture.h','src/mame/midway/midtunit_v.cpp','src/mame/midway/midtunit_v.h','src/devices/cpu/tms34010/tms34010.cpp'):
 assert sync.sha(oldroot/name)==sync.sha(newroot/name)
 equal_files[name]=sync.sha(newroot/name)
loaderstart='ROM_START( mk2ks )'
oldloader=section((oldroot/'src/mame/midway/midtunit.cpp').read_text(),loaderstart,'ROM_END')
newloader=section((newroot/'src/mame/midway/midtunit.cpp').read_text(),loaderstart,'ROM_END')
assert oldloader==newloader
patches=['write16(rom_offset(0xff844700), 0x0270);','write16(rom_offset(0xff8448a0), 0x0270);','write16(rom_offset(0xff844720), 0x0170);','write16(rom_offset(0xff844970), 0x0170);','write16(rom_offset(0xff844740), 0x0190);','write16(rom_offset(0xff844ab0), 0x0190);','write16(rom_offset(0xff844760), 0x01b0);','write16(rom_offset(0xff844b40), 0x01b0);']
assert all(p in old and p in new for p in patches)
matrixpath=root/'audit_v5698_current_campaign_four_case_matrix_checked/report.json';matrix=json.loads(matrixpath.read_text())
assert matrix['passed'] and matrix['actualNativeFourCaseBossOwnEndingAttractMatrixAccepted']
historical=[c for c in matrix['cases'] if c['fighter']=='sonya'];assert len(historical)==2
assert all(c['actualOwnEndingCompletions']==1 and c['actualBossRoundWins']>=4 and c['actualNativeExit']==0 for c in historical)
currentcross=root/'audit_current_kano_ending_sonya_crossjoin_v3_checked/report.json';cross=json.loads(currentcross.read_text())
assert cross['currentEarnedKanoEndingThenPaidSonyaP2ControlsAccepted']
report=dict(endingComponentSourceTransferAccepted=True,unchangedOwnStoryPictureGenerationAndNativeDecoder=True,
 exactUnchangedFiles=equal_files,ROMDonorAndPayloadLoaderExactlyUnchanged=True,ROMloaderComponentSHA256=hashlib.sha256(newloader.encode()).hexdigest().upper(),
 ownSonyaPictureRows=[52,53],onlyGeneratorChange='Preserve stock row40: copy41 rows/clear41..49 rather than40. Own50..53 geometry/text/pixelgeneration unchanged.',
 preciseGeneratorDiff=''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True))),
 endingPairedContinuationPatchesExactlyUnchanged=patches,historicalEarnedSonyaCases=historical,
 currentGenericEarnedEndingAndCreditsExercisedByKano=True,currentPostCreditsNativeSonya18ControlExercised=True,
 sourceFaultsRejected=faults,currentWholeSonyaCampaignTransferAccepted=False,
 currentLoadedSonyaEndingTablesAndHeadersAccepted=False,historicalFullEndingPixelsAccepted=False,historicalFullAudioAccepted=False,
 fullPortAccepted=False,nextFiniteVerification='Input-free3fields: loadedSonya table52/53 pictureheaders, five exactstorystrings/nativeheaders/twooperands/eightcontinuationwords. No force-ending/replayedbotladder.',
 historicalMatrixSHA256=sync.sha(matrixpath),currentCrossjoinSHA256=sync.sha(currentcross),oldSourceSHA256=sync.sha(oldpath),currentSourceSHA256=sync.sha(newpath))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(sourceComponentTransferAccepted=True,sourceFaults=faults,unchangedFiles=equal_files,ownRows=[52,53],currentWholeCampaignAccepted=False)))

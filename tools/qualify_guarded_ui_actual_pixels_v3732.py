"""Content-addressed actual3680 RAM pixels plus reported-failure qualification.

Existing3196 PNGs are used only as byte-identical backing storage after every
current raw RGB32 frame digest and whole streamed corpus match. Positive
appearance still uses814's independent source/native-stock pixel contract.
No new emulator, raster files, masked differences or restored retired data.
"""
import hashlib,io,json,re,unittest
from pathlib import Path
import numpy as np
from PIL import Image
import run_guarded_native_ui_ram_v3729 as runtime
import test_current_native_ui_v817 as prior

ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
v=runtime.model
OUT=ROOT/'audit_v3733_guarded_ui_actual_pixel_qualification'
PINS={};EQUIVALENCE=[]

class CurrentRAMUI(prior.NativeUI):
    @classmethod
    def setUpClass(cls):
        accepted_path=runtime.OUT/'report.json';accepted=json.loads(accepted_path.read_text())
        need(accepted['passed']and accepted['candidate']==runtime.NAME and accepted['currentBothSlotSelectionLadderFirstMatchPixelsAccepted'],'Actual current four-context full pixel gate')
        PINS[str(accepted_path)]=sha(accepted_path)
        for file,wanted in accepted['inputHashes'].items():
            need(sha(file)==wanted,'Exact accepted current input/evidence');PINS[file]=wanted
        old_path=ROOT/'audit_v3198_native_morph_shadow_ui_checked/report.json';old=json.loads(old_path.read_text())
        need(old['passed']and old['currentBothSlotSelectionLadderFirstMatchAccepted'],'Retained original independent pixel acceptance')
        PINS[str(old_path)]=sha(old_path)
        cls.logs=[];cls.all_images={};cls.case_folders=[]
        for fighter,side in prior.CASES:
            key=f'{fighter}_p{side}';folder=ROOT/f'audit_v3730_guarded_ui_{key}';log=(folder/'run.log').read_text()
            need(v.verify_log(log,fighter,side)['passed'],'Exact actual native state/controls')
            headers=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()if line.startswith('MK2_UI_RAM_FRAME_DIGEST ')]
            images={};stream=hashlib.sha256();pixels=0
            for h in headers:
                path=ROOT/f'audit_v3196_ui_{key}'/'snap'/h['filename']
                need(sha(path)==old['inputHashes'][str(path)],'Unchanged retained independent original PNG backing')
                image=np.asarray(Image.open(path).convert('RGB'))
                need(image.shape==(254,400,3)and image.dtype==np.uint8,'Unscaled native source RGB frame')
                raw=np.empty((254,400,4),np.uint8);raw[:,:,:3]=image[:,:,::-1];raw[:,:,3]=255
                packed=raw.tobytes();need(hashlib.sha256(packed).hexdigest().upper()==h['sha256'],'Every complete current raw RGB32 frame byte matches retained backing')
                stream.update(packed);pixels+=254*400;images[h['filename']]=image;PINS[str(path)]=sha(path)
            meta=json.loads((folder/'result.json').read_text())
            need(stream.hexdigest().upper()==meta['nativeFrameStreamSHA256']and len(headers)==meta['actualNativeFrameCallbacks']and
              len(images)==meta['actualUniqueNativeFrames'],'Whole actual streamed frame corpus, not sampled-region equivalence')
            rendered=v.render(folder,log,fighter,side,load=lambda name:images[name])
            EQUIVALENCE.append(dict(fighter=fighter,side=side,actualCompleteFrameCallbacks=len(headers),actualCompletePixels=pixels,
              wholeCurrentRGB32StreamSHA256=stream.hexdigest().upper(),rendered=rendered))
            cls.logs.append(log);cls.case_folders.append(folder);cls.all_images[key]=images
        cls.folder=cls.case_folders[0];cls.snapshots=v.records(cls.logs[0],'SNAP');cls.images=cls.all_images['kano_p1']
        cls.ui=(ROOT/'roms/mk2ks/mk2ks.ui').read_bytes()

    def test_four_actual_current_native_cases(self):
        for i,(fighter,side)in enumerate(prior.CASES):
            proof=v.verify_log(self.logs[i],fighter,side)
            rendered=v.render(self.case_folders[i],self.logs[i],fighter,side,load=lambda name:self.all_images[f'{fighter}_p{side}'][name])
            self.assertTrue(proof['passed']);self.assertFalse(proof['whole_character_integration_complete'])
            self.assertEqual(proof['first_match_participant_fields'],362);self.assertGreaterEqual(rendered['native_name_shadow_checks'],4)

    def test_failed_observer_not_accepted(self):
        # Retired old failed captures are not needed. Damage actual current
        # terminal metadata in RAM and retain the original log unchanged.
        last=v.records(self.logs[0],'RESULT')[0]
        changed=prior.change(self.logs[0],'RESULT',int(last['frame']),'live','-1')
        with self.assertRaises(ValueError):v.verify_log(changed,'kano',1)

    def visual_reject(self,altered):
        positive=v.render(self.folder,self.logs[0],'kano',1,load=lambda name:self.images[name])
        self.assertGreaterEqual(positive['native_name_shadow_checks'],4)
        super().visual_reject(altered)
        self.assertEqual(v.render(self.folder,self.logs[0],'kano',1,load=lambda name:self.images[name]),positive)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable actual pixel/state qualification')
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CurrentRAMUI))
    for path in(Path(__file__).resolve(),Path(prior.__file__).resolve(),Path(v.__file__).resolve()):PINS[str(path)]=sha(path)
    need(all(sha(p)==h for p,h in PINS.items()),'Actual backing/source evidence unchanged after all RAM faults')
    OUT.mkdir();(OUT/'unit-tests.log').write_text(stream.getvalue())
    report=dict(passed=result.wasSuccessful(),candidate=runtime.NAME,methods=result.testsRun,cases=EQUIVALENCE,inputHashes=PINS,
      wholeActualCurrentPixelsEquivalentToSHAQualifiedBacking=True if len(EQUIVALENCE)==4 else False,
      actualCompleteFrameCallbacks=sum(c['actualCompleteFrameCallbacks']for c in EQUIVALENCE),
      actualCompletePixels=sum(c['actualCompletePixels']for c in EQUIVALENCE),
      rawRasterFilesWritten=0,newEmulatorRuns=0,retiredReferencesRestored=False,fullPortAcceptance=False,scope=__doc__)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(stream.getvalue(),flush=True)
    print(json.dumps({k:x for k,x in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)

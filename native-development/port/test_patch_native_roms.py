"""Synthetic no-ROM patcher safety, integrity and deterministic-output tests."""
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from ips_codec import create_patch
from patch_native_roms import build,sha

class PatcherTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.package=self.root/'package';(self.package/'patches').mkdir(parents=True)
        self.mk2=self.root/'mk2.zip';self.mk3=self.root/'mk3.zip'
        self.output=self.root/'out/roms/mk3.zip'
        self.records=[]
        with zipfile.ZipFile(self.mk2,'w'),zipfile.ZipFile(self.mk3,'w') as archive:
            for i in range(26):
                name=f'chip{i}.bin';source=bytes([i])*32;archive.writestr(name,source)
                target=(b'new'+source[3:]) if i==0 else source
                record=dict(target=name,sourceArchive='mk3',source=name,sourceBytes=len(source),
                    sourceSHA256=sha(source),targetBytes=len(target),targetSHA256=sha(target),operation='copy')
                if i==0:
                    patch=create_patch(source,target)
                    (self.package/'patches/chip0.ips').write_bytes(patch)
                    record.update(operation='ips',patch='patches/chip0.ips',patchSHA256=sha(patch))
                self.records.append(record)
        self.manifest=dict(format='MK2KS-NATIVE-IPS-1',releaseReady=False,chips=self.records)
        self.save()
    def save(self): (self.package/'PATCH_MANIFEST.json').write_text(json.dumps(self.manifest))
    def run_build(self,output=None,mk3=None):
        return build(self.mk2,mk3 or self.mk3,self.package,output or self.output)
    def test_roundtrip_deterministic_and_inputs_untouched(self):
        before=(sha(self.mk2.read_bytes()),sha(self.mk3.read_bytes()))
        self.run_build();second=self.root/'another.zip';self.run_build(second)
        self.assertEqual(self.output.read_bytes(),second.read_bytes())
        with zipfile.ZipFile(self.output) as archive:
            self.assertEqual(len(archive.namelist()),26)
            self.assertEqual(archive.read('chip0.bin'),b'new'+bytes(29))
        self.assertEqual(before,(sha(self.mk2.read_bytes()),sha(self.mk3.read_bytes())))
    def test_refuse_overwrite(self):
        self.output.parent.mkdir(parents=True);self.output.write_bytes(b'KEEP')
        with self.assertRaises(FileExistsError): self.run_build()
        self.assertEqual(self.output.read_bytes(),b'KEEP')
    def test_release_status_does_not_change_chip_integrity_or_output(self):
        self.run_build()
        self.manifest.update(releaseReady=True,developmentOnly=False,releaseEvidenceSHA256='A'*64)
        self.save()
        other=self.root/'release.zip'
        report=self.run_build(other)
        self.assertEqual(other.read_bytes(),self.output.read_bytes())
        self.assertTrue(report['releaseReady'])
        self.assertFalse(report['developmentOnly'])
        self.assertFalse(report['fullPortVerified'])
    def test_release_status_requires_boolean_pair_and_evidence_binding(self):
        for changes in (dict(releaseReady='true'),dict(releaseReady=True),
                        dict(releaseReady=True,developmentOnly=False),
                        dict(releaseReady=True,developmentOnly=False,releaseEvidenceSHA256='bad'),
                        dict(releaseReady=False,developmentOnly=False)):
            self.manifest=dict(format='MK2KS-NATIVE-IPS-1',releaseReady=False,chips=self.records)
            self.manifest.update(changes);self.save()
            with self.assertRaises(ValueError):self.run_build()
            self.assertFalse(self.output.parent.exists())
    def test_wrong_source_fails_before_output(self):
        self.records[25]['sourceSHA256']='0'*64;self.save()
        with self.assertRaises(ValueError): self.run_build()
        self.assertFalse(self.output.parent.exists())
    def test_corrupt_patch_fails_before_output(self):
        (self.package/'patches/chip0.ips').write_bytes(b'corrupt')
        with self.assertRaises(ValueError): self.run_build()
        self.assertFalse(self.output.parent.exists())
    def test_wrong_result_fails_before_output(self):
        self.records[0]['targetSHA256']='0'*64;self.save()
        with self.assertRaises(ValueError): self.run_build()
        self.assertFalse(self.output.parent.exists())
    def test_unsafe_and_duplicate_targets(self):
        for name in ('../escape.bin','C:\\escape.bin','chip1.bin'):
            self.records[0]['target']=name;self.save()
            with self.assertRaises(ValueError): self.run_build()
            self.assertFalse(self.output.exists())
    def test_unsafe_patch_path(self):
        self.records[0]['patch']='../outside.ips';self.save()
        with self.assertRaises(ValueError): self.run_build()
        self.assertFalse(self.output.parent.exists())
    def test_incomplete_set(self):
        self.manifest['chips']=self.records[:-1];self.save()
        with self.assertRaises(ValueError): self.run_build()
        self.assertFalse(self.output.parent.exists())

if __name__=='__main__': unittest.main()

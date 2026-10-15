"""Baseline/corruption checks for native Friendship audio acceptance."""
import copy,json,struct,unittest
from pathlib import Path
import numpy as np
import verify_native_friendship_audio_v791 as verify

ROOT=Path(__file__).resolve().parent.parent
class AudioChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clips=[verify.audio(ROOT/f'samples/mk2ks/sonya_chicken_{v}.wav')*.7 for v in('a5','aa','af')]
        cls.starts=[1000,6260,11520]
        cls.mix=np.zeros(max(s+len(x)for s,x in zip(cls.starts,cls.clips))+100)
        for s,x in zip(cls.starts,cls.clips):cls.mix[s:s+len(x)]+=x
        cls.old=(ROOT/'audit_v768_kano_friendship_p1/guest_maincpu.bin').read_bytes()
        cls.new=(ROOT/'audit_v790_kano_friendship_p1/guest_maincpu.bin').read_bytes()
    def rows(self,winner='sonya',side=1,case='positive'):
        suffix=f'{winner}_friendship_p{side}'if case=='positive'else f'{winner}_wrong_p1'if case=='wrong_command'else f'{winner}_punch_p2'
        return verify.scene.parse(ROOT/f'audit_v790_{suffix}/run.log')
    def mutant(self,key,value,winner='sonya'):
        rows=copy.deepcopy(self.rows(winner));verify.scene.select(rows,'AUDIO')[0][key]=value
        with self.assertRaises(ValueError):verify.runtime(rows,winner,1,'positive')
    def test_eight_runtime_baselines(self):
        for winner in('kano','sonya'):
            for side,case in((1,'positive'),(2,'positive'),(1,'wrong_command'),(2,'punch_used')):
                with self.subTest(winner=winner,side=side,case=case):verify.runtime(self.rows(winner,side,case),winner,side,case)
    def test_audio_guest_baseline(self):self.assertGreater(verify.guest_audio(self.old,self.new),0)
    def test_audio_guest_corruptions(self):
        for at in(0x14000,0xf98a0,0xfa200,0xfa2e0,0xfa320,0xfa440,0xfa442):
            bad=bytearray(self.new);bad[at]^=1
            with self.subTest(offset=at),self.assertRaises(ValueError):verify.guest_audio(self.old,bad)
    def test_missing_native_rng(self):
        bad=bytearray(self.new);needle=struct.pack('<3H',0x0d5f,0xeae0,0xff80)
        at=bad.index(needle,0xfa580,0xfa700);bad[at]^=1
        with self.assertRaises(ValueError):verify.guest_audio(self.old,bad)
    def test_missing_pop_marker(self):
        bad=bytearray(self.new);needle=struct.pack('<6H',0x09e0,0x6ab4,0,0x0580,0x1030,0x01d0)
        at=bad.index(needle,0xf9a00,0xf9c00);bad[at+2]^=1
        with self.assertRaises(ValueError):verify.guest_audio(self.old,bad)
    def test_bad_identity(self):self.mutant('id','1')
    def test_bad_actor(self):self.mutant('actor','01000000')
    def test_bad_task(self):self.mutant('main','01000000')
    def test_late_cluck(self):self.mutant('frame','3878')
    def test_wrong_cluck_pose(self):self.mutant('pose','FE9D2F70')
    def test_wrong_pop_phase(self):self.mutant('frame','9999','kano')
    def test_sign_extended_command_collision(self):self.mutant('command','FFAA')
    def test_wrong_native_hold_timer(self):self.mutant('timers','19,0,0,0,0')
    def test_single_voice_retrigger(self):
        rows=copy.deepcopy(self.rows());cue=verify.scene.select(rows,'AUDIO')[1]
        command=int(cue['command'],16);cue['command']=f'{command-(command-0x6aa0)%5:04X}'
        with self.assertRaises(ValueError):verify.runtime(rows,'sonya',1,'positive')
    def test_missing_cluck(self):
        rows=self.rows();removed=verify.scene.select(rows,'AUDIO')[1];rows=[(k,r)for k,r in rows if r is not removed]
        with self.assertRaises(ValueError):verify.runtime(rows,'sonya',1,'positive')
    def test_sound_before_action(self):
        rows=self.rows();cue=copy.deepcopy(verify.scene.select(rows,'AUDIO')[0]);cue['frame']='300';rows.insert(0,('AUDIO',cue))
        with self.assertRaises(ValueError):verify.runtime(rows,'sonya',1,'positive')
    def test_rejected_command_has_sound(self):
        rows=self.rows(case='wrong_command');rows.append(('AUDIO',copy.deepcopy(verify.scene.select(self.rows(),'AUDIO')[0])))
        with self.assertRaises(ValueError):verify.runtime(rows,'sonya',1,'wrong_command')
    def test_overlap_waveform_baseline(self):
        fit=verify.fit_overlap(self.mix,self.starts,self.clips)
        self.assertGreater(fit['correlation'],.99999)
    def test_waveform_mutations(self):
        altered=self.mix.copy();altered*=.5
        with self.assertRaises(ValueError):verify.fit_overlap(altered,self.starts,self.clips)
        with self.assertRaises(ValueError):verify.fit_overlap(np.zeros_like(self.mix),self.starts,self.clips)
        with self.assertRaises(ValueError):verify.fit_overlap(self.mix,[s+876 for s in self.starts],self.clips)
        with self.assertRaises(ValueError):verify.fit_overlap(self.mix,self.starts,[self.clips[1],self.clips[0],self.clips[2]])
    def test_audible_single_channel_restart(self):
        restarted=np.zeros_like(self.mix)
        for i,(s,x)in enumerate(zip(self.starts,self.clips)):
            stop=min(s+len(x),self.starts[i+1]if i+1<len(self.starts)else len(restarted))
            restarted[s:stop]=x[:stop-s]
        with self.assertRaises(ValueError):verify.fit_overlap(restarted,self.starts,self.clips)
    def test_lost_original_tail(self):
        missing=self.mix.copy();missing[self.starts[-1]+len(self.clips[-1])//2:]=0
        with self.assertRaises(ValueError):verify.fit_overlap(missing,self.starts,self.clips)
    def test_checkpoint_does_not_claim_release(self):
        proof=json.loads((ROOT/'audit_v791_native_friendship_audio_checked/verification.json').read_text())
        self.assertTrue(proof['boundedHumanFriendshipAudioAcceptance'])
        self.assertFalse(proof['fullPortAcceptance']);self.assertFalse(proof['fullFinisherAcceptance'])

if __name__=='__main__':unittest.main(verbosity=2)

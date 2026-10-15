"""Entire original4448 page verifier for actual current KanoP2 native ending.

Only actual campaign/character/slot references and recorded frame count adapt.
All original photo/font/one-pixel black shadow/common background/RGB/fault
gates and transition/extra-black-pen/audio exclusions are retained.
"""
import hashlib,inspect,json
from pathlib import Path
import verify_sonya_p2_native_ending_pages_v4448 as original
import verify_kano_current_p2_whole_campaign_v4487 as campaign
ROOT,need,sha=campaign.ROOT,campaign.need,campaign.sha
OUT=ROOT/'audit_v4490_kano_current_p2_native_ending_pages_checked'

def main():
    source=inspect.getsource(original.main)
    changes=[('actualNaturalSonyaP2TowerClearAccepted','current3836KanoP2NaturalTowerOwnEndingAttractAccepted'),
             ("starts[0]['roster']=='18'","starts[0]['roster']=='17'"),
             ('True own Sonya18 ending','True own Kano17 ending'),
             ('len(frames)==78',"len(frames)==json.loads((campaign.FOLDER/'result.json').read_text())['actualNativeFrameCallbacks']"),
             ('campaign.capture.expected()','campaign.expected_current()[0]'),
             ("['cases']['sonya']['snapshots']","['cases']['kano']['snapshots']"),
             ('index=52+page-1','index=50+page-1'),
             ("dispatch['roster']=='18'","dispatch['roster']=='17'"),
             ('(18*3+int', '(17*3+int'),
             ("s['roster']=='18'","s['roster']=='17'"),
             ('photos.original.reference(donor,1,page-1)','photos.original.reference(donor,0,page-1)'),
             ('photos.original.reference(donor,0,page-1)','photos.original.reference(donor,1,page-1)'),
             ('text.model(guest,original,graphics,18,page)','text.model(guest,original,graphics,17,page)'),
             ('physicalSlot=2,identity=18','physicalSlot=2,identity=17'),
             ('actualNaturalSonyaP2EndingEarlyLatePhotoTextShadowCommonBackgroundAccepted',
              'actualNaturalKanoP2EndingEarlyLatePhotoTextShadowCommonBackgroundAccepted')]
    # The original own/other donor occurrences swap simultaneously, not twice.
    own='photos.original.reference(donor,1,page-1)';other='photos.original.reference(donor,0,page-1)'
    need(source.count(own)==source.count(other)==1,'Both original character photo references identified')
    source=source.replace(own,'photos.original.reference(donor,OWN,page-1)').replace(other,'photos.original.reference(donor,OTHER,page-1)')
    for before,after in changes:
        if before in (own,other):continue
        need(source.count(before)==1 if before!='physicalSlot=2,identity=18' else source.count(before)==2,
             'Only declared actual native identity/reference/role adaptation: '+before)
        source=source.replace(before,after)
    source=source.replace('photos.original.reference(donor,OWN,page-1)',other).replace('photos.original.reference(donor,OTHER,page-1)',own)
    scope=dict(vars(original),__file__=__file__,campaign=campaign,OUT=OUT)
    exec(compile(source,__file__+'::entire4448_current_KanoP2_only','exec'),scope)
    return scope['main']()

if __name__=='__main__':main()

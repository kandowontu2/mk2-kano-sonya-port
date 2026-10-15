"""Original native Toasty branch, real secret entry and corruption checks."""
import hashlib
import json
import re
from pathlib import Path
import qualify_natural_smoke_lifecycle as life

ROOT, need = life.ROOT, life.need


def gate(c):
    result = life.gate(c)
    records = life.original.inventory(c['text'])
    stock = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo, hi in ((0xff8de9f0,0xff8df2b0),(0xff81e740,0xff81e820),(0xff80e980,0xff80ecf0)):
        a,b = (lo-0xff800000)//8,(hi-0xff800000)//8
        need(c['guest'][a:b] == stock[a:b], 'Whole original uppercut/popup/human-count/RNG code, not a patched shortcut')
    decisions = records['MK2_STAGE_TOASTY_DECISION']
    products = [r for r in decisions if r['entry'] == 'FF8DF120']
    toasts = [r for r in records['MK2_STAGE_TOASTY'] if r['arena'] == '7']
    need(products and toasts, 'Actual native RNG products and original popup are both observed')
    observations = []
    by = {(int(r['frame']),int(r['slot'])):r for r in records['MK2_STAGE_SECRET_FIELD']}
    for product in products:
        f, value = int(product['frame']), int(product['a0'],16)
        args = [r for r in decisions if r['entry'] == 'FF8DF0F0' and r['task'] == product['task'] and r['frame'] == product['frame']]
        need(len(args) == 1 and args[0]['a0'] == '00000028' and product['pc'] == 'FF8DF130' and 0 <= value < 1000,
             'Actual unchanged bounded RNG call uses native 40/1000 Toasty threshold')
        need(product['states'] == '1,1' and product['actor'] == by[f,3-c['side']]['actor'],
             'Native uppercut popup task belongs to the real added victim in the two-human Portal fight')
        popup = [r for r in toasts if int(r['frame']) == f]
        need(bool(popup) == (value < 40), 'Actual native random branch and Toasty popup agree, no forced outcome')
        observations.append(dict(frame=f, nativeRandomValue=value, nativePopup=bool(popup), originalTask=product['task']))
    result['actualNativeToastyDecisions'] = observations
    return result


def faults(c):
    records = life.original.inventory(c['text'])
    original = c['text'].splitlines()
    secret = int(records['MK2_STAGE_SECRET_FIGHT'][0]['frame'])
    side = str(c['side'])
    attempts = [
        ('native acceptance PC', 'MK2_STAGE_SECRET_ACCEPT', lambda r: True, 'pc', 'FF814E90'),
        ('native selected human side', 'MK2_STAGE_SECRET_ACCEPT', lambda r: True, 'taskSide', str(2-c['side'])),
        ('Down not held', 'MK2_STAGE_SECRET_ACCEPT', lambda r: True, 'in0', 'FFFFFFFF'),
        ('cold clock clear substituted for popup', 'MK2_STAGE_TOASTY', lambda r: r['arena']=='7', 'pc', 'FF841C20'),
        ('popup random result outside native threshold', 'MK2_STAGE_TOASTY_DECISION', lambda r: r['entry']=='FF8DF120' and int(r['a0'],16)<40, 'a0', '00000029'),
        ('real human ID replaced by donor', 'MK2_STAGE_SECRET_FIELD', lambda r: int(r['frame'])==secret and r['slot']==side, 'id', '0'),
        ('Smoke ID replaced by Sub-Zero', 'MK2_STAGE_SECRET_FIELD', lambda r: int(r['frame'])==secret and r['slot']!=side, 'id', '7'),
        ('real Main ownership removed', 'MK2_STAGE_SECRET_FIELD', lambda r: int(r['frame'])==secret and r['slot']==side, 'owner', '00000000'),
        ('native lethal collision omitted', 'MK2_SECRET_HEALTH', lambda r: int(r['frame'])>secret and r['slot']==side and r['pc']=='FF836700' and r['after']=='0', None, None),
        ('native KO reset omitted', 'MK2_SECRET_HEALTH', lambda r: int(r['frame'])>secret and r['slot']==side and r['before']=='0' and r['after']=='161', None, None),
        ('actual jump height removed', 'MK2_STAGE_SECRET_FIELD', lambda r: r['slot']==side and int(r['frame'])==int(records['MK2_STAGE_SECRET_JUMP'][0]['frame']), 'y', '131'),
        ('ordinary punch action removed', 'MK2_STAGE_SECRET_FIELD', lambda r: r['slot']==side and int(r['frame'])==int(records['MK2_STAGE_SECRET_PUNCH'][0]['frame']), 'action', '0'),
        ('survival Block pulse omitted', 'MK2_STAGE_INPUT', lambda r: r['slot']==side and r['button']=='Block' and int(r['frame'])>int(records['MK2_STAGE_SECRET_RECOVER'][0]['frame']), None, None),
    ]
    rejected = []
    for label, tag, select, key, value in attempts:
        lines = list(original)
        i = next(i for i,line in enumerate(lines) if line.startswith(tag+' ') and select(dict(re.findall(r'(\w+)=([^\s]+)',line))))
        if key:
            lines[i], count = re.subn(r'\b'+key+r'=[^\s]+',key+'='+value,lines[i])
            need(count==1 and lines[i]!=original[i], 'Non-vacuous actual mutation '+label)
        else:
            lines.pop(i)
        try:
            gate(dict(c,text='\n'.join(lines)+'\n'))
        except ValueError as error:
            rejected.append(dict(fault=label,rejected=str(error)))
            print(json.dumps(rejected[-1]),flush=True)
        else:
            raise ValueError('Actual native record corruption accepted: '+label)
    # All pre-jump actual walking velocities removed, preserving positions and
    # the old delayed recovery marker. It must not count as valid walking.
    end = int(records['MK2_STAGE_SECRET_JUMP'][0]['start'])
    lines = []
    for line in original:
        r = dict(re.findall(r'(\w+)=([^\s]+)',line))
        if line.startswith('MK2_STAGE_SECRET_FIELD ') and r['slot']==side and secret <= int(r['frame']) < end:
            line = re.sub(r'\bvx=[^\s]+','vx=00000000',line)
        lines.append(line)
    try:
        gate(dict(c,text='\n'.join(lines)+'\n'))
    except ValueError as error:
        rejected.append(dict(fault='real source-velocity walking removed',rejected=str(error)))
        print(json.dumps(rejected[-1]),flush=True)
    else:
        raise ValueError('Stationary recovery/knockback accepted as walking')
    return rejected


def seal(c, result, rejected):
    need(len(rejected)==14 and gate(c)==result, 'Whole positive native secret/lifecycle/control/RNG gates rerun and actual faults executed')
    path = c['folder']/'native_secret_decisions_and_faults.json'
    need(not path.exists(), 'Fresh additive original-record proof')
    viewed = [c['rgbFrames'][i]['header'] for i in (16,18,19,20)]
    need([r['stage'] for r in viewed]==['portal_match.png','secret_fight.png','secret_recovered.png','secret_terminal.png'], 'Exact actually viewed native frames')
    for i in (16,18,19,20):
        need(hashlib.sha256(c['rgbFrames'][i]['pixels']).hexdigest().upper()==c['rgbFrames'][i]['header']['sha256'], 'Whole actual viewed native screen bytes')
    report = dict(passed=True, actualNativeSecret=result, actualFaultsRejected=rejected, viewedNativeFrameHeaders=viewed,
                  finiteVisualReview=['Portal shows both real added bodies, matching lifebar names and floor shadows.',
                                      'Secret fight shows actual Kano versus native Smoke with correct names; selector portraits/poses are absent.',
                                      'Post-reset and final survival show the Kano body and normal native Smoke effects, with no lingering selector artwork.'],
                  fullRasterAcceptance=False, fullSecretAudioAccepted=False, fullPortAcceptance=False,
                  capturedNativeBoots=1, replayedNativeBoots=0, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
                  inputHashes={str(Path(p).resolve()):hashlib.sha256(Path(p).read_bytes()).hexdigest().upper() for p in (__file__,life.__file__,life.original.__file__)})
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,actualNativeSecretEntry=True,actualFaultsRejected=14,viewedNativeFrames=4,secretFieldsPerSlot=result['secretFightFieldsPerSlot'])),flush=True)
    return report

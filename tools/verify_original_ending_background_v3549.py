"""Original unmodified MK2 stock ending reference and current frame comparison.

The stock reference has explicit stage14/live-combat health fixtures. All
assistance ends before its native ending; it is never a natural tower clear.
Compare every common visible frame/background pixel, with only independently
decoded photograph and original-font foreground masks excluded. No global
cinematic/audio/P2/hidden-background or whole-port acceptance.
"""
import json
import re
import struct
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image
import verify_current_natural_ending_text_v3542 as text
import decode_native_picture as picture

ROOT, need, sha = text.ROOT, text.need, text.sha
CASE = ROOT / 'audit_v3548_original_mk2_ending_background'
OUT = ROOT / 'audit_v3550_original_native_ending_background_checked'
DRIVER = ROOT / 'mk2ks_original_ending_background_v3546.lua'
BASELINE = ROOT / 'mk2ks_current_ending_presentation_v680_v4.lua'


def source_boundary(actual):
    expected = BASELINE.read_text()
    def replace(before, after, count=1):
        nonlocal expected
        need(expected.count(before) == count, 'Exactly declared original-control adaptation')
        expected = expected.replace(before, after)
    replace('-- Ending-only presentation diagnostic: one preconstruction stage16 fixture,',
            '-- Original MK2 ending/background reference: one preconstruction stage14 fixture,')
    replace("local identity=assert(({liu_kang=1,kano=17,sonya=18})[fighter])\n",
            "local identity=assert(({liu_kang=1,kano=17,sonya=18})[fighter])\nassert(fighter=='liu_kang' and identity==1,'Original stock Liu ending only')\n")
    replace('stage16_combat_health_only', 'stage14_combat_health_only', 2)
    replace('0xff800000+0xf4900*8+(50+(identity-17)*2+page)*32', '0xff8f48f0+(16+identity*2+page)*32')
    replace('~=16', '~=14', 2)
    replace('0xff800000+(page==0 and 0xf4a00 or 0xf4b00)*8', 'page==0 and 0xff8f5550 or 0xff8f59d0')
    start = expected.index('local adjacency={')
    end = expected.index('local function press(button)', start)
    expected = expected[:start] + """local function route(start)
 assert(start==identity,'Original P1 default Liu cursor, no imported adjacency table')
 return {}
end
""" + expected[end:]
    replace('0xfffef800', '0xff822280', 4)
    replace('0xff822280+19*32-1', '0xff822280+17*32-1')
    replace("  log('BOOT','schema=current_ending_presentation_v4 strategy='..strategy..' boot='..boot..' fixtures=stage14_combat_health_only stock_frame_control=true')",
            """  log('BOOT','schema=original_ending_background_v3546 strategy='..strategy..' boot='..boot..' fixtures=stage14_combat_health_only stock_frame_control=true game=mk2')
  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)
  local file=assert(io.open(assert(os.getenv('MK2KS_CAMPAIGN_OUT'))..'/guest_maincpu.bin','wb'));file:write(raw);file:close()""")
    replace('for stage=0,16 do', 'for stage=0,15 do')
    replace('before=%d after=16 mode=', 'before=%d after=14 mode=')
    replace('p:write_u16(0x01061b30,16)', 'p:write_u16(0x01061b30,14)')
    replace('stage==16', 'stage==14', 3)
    replace('stage_wins[16]', 'stage_wins[14]')
    replace('scope=unassisted_campaign_observation_independent_verification_pending',
            'scope=original_stock_ending_background_assisted_diagnostic_not_natural_clear')
    observer = """-- Read-only original scene dispatch, independent from photo/text pointers.
for _,scene in ipairs({18,19})do
 local entry=0xff9f7cf0+scene*32
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'original ending backdrop scene',function(at,data,mask)
  if not first_live or p:read_u16(0x01061b30)~=14 or p:read_u16(slots[side].roster)~=identity or
   p:read_u16(0x01061b00)~=side then return end
  log('SCENE_TABLE',string.format('scene=%d entry=%08X value=%04X mask=%04X pc=%08X',scene,at,data&0xffff,mask,cpu.PC.value))
 end)
end
"""
    replace('emu.register_frame(function()\n', observer + 'emu.register_frame(function()\n')
    need(actual == expected, 'Whole original control/fixture/ending observer preserved except declared stock addresses/read-only evidence')
    writes = re.findall(r'\bp:write_\w+\([^\n]*?\)', actual)
    need(writes == ['p:write_u16(0x01061b30,14)', 'p:write_u16(slots[opponent].hp,1)',
                    'p:write_u16(slots[side].hp,161)'] and
         not re.search(r'\bload\s*\(|\bdofile\s*\(|load_?state|\.value\s*=', actual),
         'Only three explicit pre-ending stage/combat-health fixture sites, no actor/ID/position/ending or dynamic writes')


def stock_text_model(original, graphics, page):
    face, shadow = np.zeros((254, 400), dtype=bool), np.zeros((254, 400), dtype=bool)
    metric = text.u32(original, 0xffa20790 + 0x27 * 32)
    mw, mh = struct.unpack_from('<2H', original, text.off(metric))
    need((mw, mh) == (7, 11), 'Original H-derived stock font metrics')
    scripts = []
    for segment in range(3 if page == 1 else 2):
        table = (0xff8f5550 if page == 1 else 0xff8f59d0) + (3 + segment) * 32
        pointer = text.u32(original, table)
        font, spacing, xy, color, renderer, speed = struct.unpack_from('<6I', original, text.off(pointer))
        need((font, spacing, color, renderer, speed) == (0xffa20790, 2, 0x0e0e0000, 0xffa29920, 0),
             'Untouched original Liu font/style/renderer header')
        story = original[text.off(pointer) + 24:].split(bytes(1), 1)[0].decode('ascii')
        x, y = xy & 65535, xy >> 16; start_x = x
        for char in story.replace('\\n', '\r'):
            if char == '\r':
                x, y = start_x, y + mh + mh // 2
            elif char == ' ':
                x += mw // 2 + spacing
            else:
                pixels, descriptor = text.glyph(original, graphics, char)
                h, w = pixels.shape
                xx, yy = x - descriptor['xOffset'], y - descriptor['yOffset']
                need(0 <= xx and xx + w + 1 <= 400 and 0 <= yy and yy + h + 1 <= 254,
                     'Complete original stock glyph/shadow in native viewport')
                face[yy:yy + h, xx:xx + w] |= pixels
                shadow[yy + 1:yy + 1 + h, xx + 1:xx + 1 + w] |= pixels
                x += w + spacing
        scripts.append(dict(nativeScript=hex(pointer), story=story))
    shadow &= ~face
    return dict(face=face, shadow=shadow, scripts=scripts)


def background_gate(actual, stock, mask):
    need(actual.shape == stock.shape == (254, 400, 3), 'Actual original/current native scanout dimensions')
    need(np.array_equal(actual[mask], stock[mask]), 'Every common visible native original frame/background pixel exact')
    return int(np.count_nonzero(mask))


def main():
    need(not OUT.exists(), 'Immutable fresh original frame/background proof')
    pins = {}
    def pin(path, wanted=None):
        key = str(Path(path).resolve()); digest = sha(path)
        need(wanted is None or digest == wanted, 'Actual original/current accepted input unchanged: ' + key)
        need(key not in pins or pins[key] == digest, 'Consistent original/current byte binding')
        pins[key] = digest
    metadata = json.loads((CASE / 'result.json').read_text(encoding='utf-8-sig'))
    before = json.loads((CASE / 'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    snapshots = json.loads((CASE / 'source_snapshot_paths.json').read_text(encoding='utf-8-sig'))
    need(metadata['exit_code'] == 0 and metadata['game'] == 'mk2' and metadata['player'] == 'liu_kang' and
         metadata['human_slot'] == 1 and metadata['cpu_slot'] == 2 and metadata['assistance'] == 'stage14_combat_health_only' and
         metadata['executable_sha256'] == text.photos.EXE and not metadata['cheats_enabled'] and
         not metadata['unassisted_clear_proven'] and metadata['snapshot_schema'] == 2 and
         metadata['raw_audio_files_written'] == metadata['new_builds_or_rom_copies'] == 0 and
         metadata['input_hashes'] == before, 'Terminal actual original MK2 assisted stock reference, never native campaign acceptance')
    for path, digest in before.items():
        pin(path, digest)
        if Path(path).suffix in ('.lua', '.ps1', '.json'):
            frozen = Path(snapshots[path]).resolve()
            need(frozen.is_relative_to(CASE.resolve()), 'Collision-free frozen original fixture input')
            pin(frozen, digest)
    source = DRIVER.read_text(); source_boundary(source)
    source_faults = []
    for label, a, b in (
        ('wrong_stock_actor_fixture', "p:write_u16(slots[opponent].hp,1)", "p:write_u16(slots[opponent].roster,13)"),
        ('ending_pointer_manipulation', "p:write_u16(0x01061b30,14)", "p:write_u16(0x01061b30,14);p:write_u32(0xff8f4b30,0x07100000)"),
        ('changed_original_physical_control', "if gap>65 then", "if gap>66 then")):
        changed = source.replace(a, b, 1); need(changed != source, 'Non-vacuous actual source fixture fault')
        try:
            source_boundary(changed)
        except ValueError as error:
            need(str(error) == 'Whole original control/fixture/ending observer preserved except declared stock addresses/read-only evidence',
                 'Actual fixture fault rejects whole original source boundary')
            source_faults.append(label)
        else:
            raise ValueError('Accepted fixture source fault: ' + label)
    source_boundary(source)
    runner = (ROOT / 'tools/run_original_ending_background_v3547.ps1').read_text()
    need('& $exe mk2 -rompath "$root/roms"' in runner and '-nocheat' in runner and
         '-nosamples' in runner and '-wavwrite' not in runner and
         '-noautoframeskip -frameskip 0' in runner, 'Actual original game, original parent and complete native scanouts without raw audio')
    original_path = ROOT / 'mk2/mk2-maincpu.bin'; pin(original_path, text.ROM_SHA)
    original = original_path.read_bytes(); pin(CASE / 'guest_maincpu.bin', text.ROM_SHA)
    need((CASE / 'guest_maincpu.bin').read_bytes() == original,
         'Every byte of entire initialized guest equals untouched original MK2, no port patch/selector/ending bytes')
    raw = (CASE / 'run.log').read_text(encoding='utf-8-sig')
    need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation', raw, re.I), 'No original fixture/runtime error')
    rows = text.photos.rows
    start, end, final = rows(raw, 'ENDING_START'), rows(raw, 'ENDING_COMPLETED'), rows(raw, 'ENDING_FIXTURE_RESULT')
    stages, hp, regen = rows(raw, 'ENDING_FIXTURE_STAGE'), rows(raw, 'ENDING_FIXTURE_HEALTH'), rows(raw, 'ENDING_FIXTURE_REGEN')
    need(len(start) == len(end) == len(final) == len(stages) == 1 and len(hp) == 2,
         'One original stage fixture, two live CPU-health fixtures and complete stock ending')
    need(stages[0]['before'] == '0' and stages[0]['after'] == '14' and stages[0]['mode'] == '4' and
         stages[0]['state'] == '4' and stages[0]['own_roster'] == '1' and stages[0]['cpu_roster'] == '65535',
         'Preconstruction original true-Liu stage fixture only')
    for n, item in enumerate(hp, 1):
        need(item['round'] == str(n) and item['slot'] == '2' and item['field'] == '01060EC0' and
             item['before'] == '161' and item['after'] == '1' and item['own_id'] == '1' and item['cpu_id'] == '13' and
             int(item['frame']) < int(start[0]['frame']), 'Actual original true-character live CPU fixture before ending')
    for item in regen:
        need(item['slot'] == '1' and item['field'] == '010602F0' and 0 < int(item['before']) < 161 and
             item['after'] == '161' and item['mode'] == '2' and int(item['cpu_health']) > 0 and
             int(item['frame']) < int(start[0]['frame']), 'Human health fixture confined to alive original combat, never ending')
    need(final[0]['stage_writes'] == '1' and final[0]['cpu_health_writes'] == '2' and
         int(final[0]['own_health_writes']) == len(regen) and final[0]['ending_writes'] == '0' and
         int(final[0]['last_fixture']) == max(int(r['frame']) for r in stages + hp + regen) < int(start[0]['frame']),
         'Every explicit fixture stops before native ending interval')
    live = rows(raw, 'LIVE')
    need(live and all(r['stage'] == '14' and r['human'] == '1:1' and r['cpu'] == '13:13' for r in live),
         'Original live Liu and native Shao, no proxy')
    deaths = [r for r in rows(raw, 'HEALTH') if r['slot'] == '2' and r['before'] == '1' and r['after'] == '0' and r['pc'] == 'FF836700']
    wins = rows(raw, 'WIN')
    need(len(deaths) == 2 and len(wins) == 1 and wins[0]['slot'] == '1' and wins[0]['id'] == '1' and
         wins[0]['entry'] == 'FF8222A0' and wins[0]['pc'] == 'FF8296B0' and
         start[0]['winner'] == '1' and start[0]['roster'] == '1' and start[0]['actors'] == '00000000,00000000',
         'Actual original collision KOs/first winner/boss-death retirement; assisted, not natural clear')
    need(end[0]['pictures'] == '1,1' and end[0]['texts'] == '3,3' and end[0]['roster'] == '3,1' and
         int(end[0]['age']) == int(end[0]['frame']) - int(start[0]['frame']) > 1200,
         'Complete original stock slideshow and return to cast attract')
    pictures, stories, scenes, snaps = [rows(raw, tag) for tag in ('PICTURE', 'TEXT', 'SCENE_TABLE', 'PAGE_SNAP')]
    need(len(pictures) == 2 and len(stories) == 6 and len(scenes) == 2 and len(snaps) == 4,
         'Actual original native picture/story/background dispatch and early/late scanouts')
    for page in (1, 2):
        p = next(r for r in pictures if r['page'] == str(page))
        entry = 0xff8f48f0 + (18 + page - 1) * 32
        need(int(p['entry'], 16) == entry and int(p['value'], 16) == text.u32(original, entry) & 65535 and
             p['pc'] == 'FF8447E0' and p['roster'] == '1', 'Original unmodified stock photo pointer/native renderer')
        for s in [r for r in stories if r['page'] == str(page)]:
            at = (0xff8f5550 if page == 1 else 0xff8f59d0) + (3 + int(s['segment'])) * 32
            need(int(s['entry'], 16) == at and int(s['value'], 16) == text.u32(original, at) & 65535 and
                 s['frame'] == p['frame'] and s['roster'] == '1', 'Original stock story pointers and chronology')
        scene = next(r for r in scenes if r['scene'] == str(20 - page))
        at = 0xff9f7cf0 + (20 - page) * 32
        need(int(scene['entry'], 16) == at and int(scene['value'], 16) == text.u32(original, at) & 65535 and
             scene['pc'] == 'FF844900' and int(p['frame']) < int(scene['frame']) < int(p['frame']) + 60,
             'Actual original scene19/18 dispatch before retained page scanout')

    prior_path = text.OUT / 'report.json'; prior = json.loads(prior_path.read_text()); pin(prior_path)
    need(prior['passed'] and prior['bothNaturalP1StoryGlyphSpacingPunctuationAndBlackShadowsAccepted'], 'Accepted current natural own text captures')
    for path, digest in prior['inputHashes'].items():
        pin(path, digest)
    graphics = bytearray(0x400000)
    for chip in prior['originalFontBankChips']:
        raw_chip = Path(chip['file']).read_bytes(); at = int(chip['regionLane'], 16) - 0x800000
        graphics[at:at + len(raw_chip) * 4:4] = raw_chip
    cases = {}; faults = []; stock_backgrounds = {}
    for page in (1, 2):
        dispatch = next(r for r in pictures if r['page'] == str(page)); frame = int(dispatch['frame'])
        stock_model = stock_text_model(original, graphics, page)
        for late, age in (('', 60), ('_late', 180)):
            filename = f'ending_page{page}{late}_{frame}.png'
            events = [r for r in snaps if r['file'] == filename]
            need(len(events) == 1 and int(events[0]['frame']) == frame + age, 'Real original relative page snapshot chronology')
            path = CASE / 'snap' / filename; pin(path)
            stock = np.asarray(Image.open(path).convert('RGB'))
            need(np.all(stock[stock_model['face']] == (231, 231, 231)) and
                 np.all(stock[stock_model['shadow']] == (0, 0, 0)), 'Original stock complete independently decoded native text face/shadow pixels')
            stock_backgrounds[page, bool(late)] = (stock, stock_model)

    for fighter, (folder_name, _, identity) in text.photos.CASES.items():
        folder = ROOT / folder_name; guest_path = folder / 'guest_maincpu.bin'; pin(guest_path, text.photos.GUEST)
        guest = guest_path.read_bytes(); records = []
        for page in (1, 2):
            own_model = text.model(guest, original, graphics, identity, page)
            for index, capture in enumerate([s for s in prior['cases'][fighter]['snapshots'] if s['page'] == page]):
                path = Path(capture['file']); actual = np.asarray(Image.open(path).convert('RGB'))
                stock, stock_model = stock_backgrounds[page, bool(index)]
                mask = ~(own_model['face'] | own_model['shadow'] | stock_model['face'] | stock_model['shadow'])
                # Only original photograph interiors excluded; native frame
                # overpaint (top row, right/left edge columns) stays compared.
                if page == 1:
                    mask[42:204, 30:153] = False
                else:
                    mask[20:138, 58:336] = False
                count = background_gate(actual, stock, mask)
                corner = np.zeros_like(mask); corner[:10, 340:] = True
                need(np.all(mask[corner]) and np.array_equal(actual[corner], stock[corner]),
                     'Entire page top-right region source-bound original comparison, never hidden behind photo/text masks')
                black = np.all(stock == (0, 0, 0), axis=2) & corner
                if page == 2:
                    need(np.count_nonzero(black) > 100, 'Original MK2 black strip is genuinely present, not a port-only artifact')
                for label, y, x in (('one_actual_frame_or_background_pixel_changed', *np.argwhere(mask & ~corner)[0]),
                                    ('one_original_corner_black_strip_pixel_changed', *np.argwhere(mask & corner)[0])):
                    changed = actual.copy(); changed[y, x, 0] ^= 1
                    need(not np.array_equal(changed, actual), 'Non-vacuous actual frame/background pixel fault')
                    try:
                        background_gate(changed, stock, mask)
                    except ValueError as error:
                        need(str(error) == 'Every common visible native original frame/background pixel exact', 'Intended exact original background rejection')
                        faults.append(dict(fighter=fighter, page=page, capture=index, name=label))
                    else:
                        raise ValueError('Accepted actual background fault')
                background_gate(actual, stock, mask)
                records.append(dict(file=str(path), frame=capture['frame'], page=page,
                    comparedOriginalFrameAndCommonBackgroundPixels=count,
                    sourceDerivedPhotoAndBothTextForegroundPixelsExcluded=int(mask.size - count),
                    exactTopRightRegionPixels=int(np.count_nonzero(corner)),
                    originalTopRightBlackPixels=int(np.count_nonzero(black)),
                    sourceDerivedNativePhotoOverpaintEdgesIncluded=True, samePathOriginalPositiveAccepted=True))
        cases[fighter] = records
    for path in (CASE / 'run.log', CASE / 'result.json', CASE / 'input_hashes_before.json', CASE / 'source_snapshot_paths.json',
                 Path(__file__), Path(text.__file__), Path(picture.__file__)):
        pin(path)
    report = dict(passed=True, currentCandidate=text.photos.CANDIDATE.name, originalReferenceGame='mk2',
        entireOriginalGuestByteExact=True, originalReferenceAssistance='stage14_combat_health_only',
        originalReferenceUnassistedCampaignAccepted=False, originalReferenceFinalFrame=6188,
        actualOriginalNativeSceneIndices=[19, 18], sourceBoundaryQualifiedFaults=source_faults,
        currentNaturalEndingFrameCases=cases,
        exactOriginalFrameAndCommonVisibleBackgroundPixels=sum(r['comparedOriginalFrameAndCommonBackgroundPixels'] for rs in cases.values() for r in rs),
        actualQualifiedFrameBackgroundPixelFaults=faults, originalTopRightPage2BlackStripNotPortSpecificAccepted=True,
        bothNaturalP1NativePhotoFrameOverpaintAndCommonBackgroundAccepted=True,
        foregroundOrHiddenBackgroundAllExtraBlackPensAudioP2OrAllCinematicsAccepted=False,
        newExecutableROMRawAudioOrRecoveredOracleCopies=0, fullPortAcceptance=False, scope=__doc__, inputHashes=pins)
    OUT.mkdir(); path = OUT / 'report.json'; path.write_text(json.dumps(report, indent=2) + '\n'); digest = sha(path)
    compressed = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(path)], capture_output=True, text=True)
    need(compressed.returncode == 0 and sha(path) == digest, 'Lossless compact original frame evidence')
    print(json.dumps({k: v for k, v in report.items() if k not in ('inputHashes', 'currentNaturalEndingFrameCases')}, indent=2))


if __name__ == '__main__':
    main()

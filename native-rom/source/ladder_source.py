"""Native 14-fighter ladder integration; original fighter order/AI preserved."""
import re

SPACING = 51  # Actual native smframe1/smframe2 height, without overlap.
BOTTOM = 0x314  # Original first portrait screen Y preserved after adding rows.
KAHN_INDEX = 16


def selector(text):
    text = text.replace('\r\n', '\n')
    assert 'ks_ladder_roster' not in text
    pattern = r'(?m)^map_([1-6])\t.word[^\n]*(?:\n\t.word[^\n]*)*'
    seen = []

    def extend(match):
        block = match.group(0)
        entries = re.findall(r'\.word\s+([^\s;]+)', block)
        assert len(entries) == 16, entries
        assert entries[11:] == ['ft_smoke', 'ft_st', 'ft_goro', 'ft_final_boss', '-1']
        assert len(set(entries[:11])) == 11
        seen.append(int(match.group(1)))
        marker = '\t.word\tft_smoke'
        assert block.count(marker) == 1
        return block.replace(marker, '\t.word ft_kano\n\t.word ft_sonya\n' + marker)

    text = re.sub(pattern, extend, text)
    assert seen == list(range(1, 7)), seen
    marker = '\nworld_y_spots\n'
    start = text.index(marker)
    end = text.index('\n\ny_spacing', start)
    # Smoke at13 is skipped by MAIN.adv_winner_map; Shang14 keeps the secret
    # camera plateau. Final boss camera/double-step retain native peak framing.
    spots = [BOTTOM, BOTTOM] + [BOTTOM - (i - 1) * SPACING for i in range(2, 14)]
    spots += [spots[-1], BOTTOM - 14 * SPACING, 4]
    assert len(spots) == 17
    table = marker + ''.join(f'\t.word {value}\n' for value in spots)
    text = text[:start] + table + text[end:]
    text, count = re.subn(r'y_spacing\s+\.set\s+03aH',
                         'ks_ladder_roster .set 1\nks_ladder_bottom .set 0314h\ny_spacing .set 033h', text)
    assert count == 1
    for instruction in ('cmpi', 'movi'):
        old = f'\t{instruction}\t0310H,a0'
        assert text.count(old) == 1, instruction
        text = text.replace(old, f'\t{instruction}\tks_ladder_bottom,a0')
    old = '\tcmpi\t00eH,a0\n\tjrne\tbmu0\n\tsll\t1,a1'
    assert text.count(old) == 1
    text = text.replace(old, '\tcmpi\t16,a0\n\tjrne\tbmu0\n\tmovi\t074h,a1')
    marker = '\nbox_coordinate_table\n'
    start = text.index(marker)
    old = re.match(r'\nbox_coordinate_table\n(?:\t.word[^\n]*\n)+', text[start:])
    assert old and old.group(0).count('.word') == 16
    rows = ''.join(f'\t.word 080h+({index}*y_spacing)\n' for index in range(16, -1, -1))
    text = text[:start] + marker + rows + '\t.word -1\n' + text[start + len(old.group(0)):]
    return text


def difficulty(text):
    """Insert two late-regular tiers, retaining every original tier and boss."""
    text = text.replace('\r\n', '\n')
    assert 'ks_ladder_difficulty' not in text
    pattern = r'(?m)^(diff_min_[1-5])\n\t.word\s+([^;\n]+)(;[^\n]*regular characters[^\n]*)'
    seen = []

    def extend(match):
        values = [value.strip() for value in match.group(2).split(',')]
        assert len(values) == 12, values
        seen.append(match.group(1))
        values[11:11] = [values[10], values[10]]
        return match.group(1) + '\n\t.word ' + ','.join(values) + '\t' + match.group(3)

    text = re.sub(pattern, extend, text)
    assert len(seen) == 5
    return '; ks_ladder_difficulty: preserve original tiers around two new fighters\n' + text


def secrets(text):
    text = text.replace('\r\n', '\n')
    assert 'ks_ladder_jade' not in text
    start = text.index('\njade_check\n')
    end = text.index('\njade_no', start)
    block = text[start:end]
    old = '\tcmpi\t10,a0'
    assert block.count(old) == 1
    block = block.replace(old, '\tcmpi\t12,a0')
    old = '\tmovi\t00cH,a0\n\tmove\ta0,@map_position,w'
    assert block.count(old) == 1
    block = block.replace(old, '\tmovi\t14,a0\n\tmove\ta0,@map_position,w')
    return text[:start] + '\n; ks_ladder_jade: last regular rung to Shang after secret challenge\n' + block + text[end:]

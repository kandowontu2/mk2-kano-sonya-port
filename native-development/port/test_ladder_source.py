import re
import unittest
import zipfile
from pathlib import Path
from ladder_source import selector, difficulty, secrets, SPACING, BOTTOM

ZIP = Path('C:/Users/kando/Downloads/mk2-rebuild-main.zip')


class LadderSource(unittest.TestCase):
    def original(self, name):
        with zipfile.ZipFile(ZIP) as archive:
            return archive.read('mk2-rebuild-main/src/' + name).decode('cp437').replace('\r\n', '\n')

    def maps(self, text):
        pattern = r'(?m)^map_([1-6])\t.word[^\n]*(?:\n\t.word[^\n]*)*'
        return {int(m.group(1)): re.findall(r'\.word\s+([^\s;]+)', m.group(0))
                for m in re.finditer(pattern, text)}

    def test_all_maps_add_true_ids_without_replacing_originals(self):
        raw = self.original('MKSEL.ASM')
        result = selector(raw)
        for key, entries in self.maps(result).items():
            self.assertEqual(entries[11:14], ['ft_kano', 'ft_sonya', 'ft_smoke'])
            self.assertEqual(entries[:11] + entries[13:], self.maps(raw)[key])
            self.assertEqual(len(entries), 18)  #17 actual rungs and terminator
            self.assertEqual(entries[14:], ['ft_st', 'ft_goro', 'ft_final_boss', '-1'])
        with self.assertRaises(AssertionError): selector(result)

    def test_geometry_covers_every_rung_without_frame_overlap(self):
        raw = self.original('MKSEL.ASM')
        result = selector(raw)
        self.assertGreaterEqual(SPACING, 51)
        self.assertEqual(128 + 16 * SPACING - BOTTOM, 156)
        spots = result.split('\nworld_y_spots\n')[1].split('\nks_ladder_roster', 1)[0]
        self.assertEqual(len(re.findall(r'\.word', spots)), 17)
        self.assertIn('\tcmpi\t16,a0', result)
        self.assertIn('\tmovi\t074h,a1', result)
        boxes = result.split('\nbox_coordinate_table\n')[1]
        self.assertEqual(len(re.match(r'(?:\t.word[^\n]*\n)+', boxes).group(0).splitlines()), 18)

    def test_original_difficulty_tiers_and_boss_values_preserved(self):
        raw = self.original('MAIN.ASM')
        result = difficulty(raw)
        for index in range(1, 6):
            pattern = rf'diff_min_{index}\n\s*\.word\s+([^;\n]+);[^\n]*\n(\s*\.word[^\n]+)'
            old = re.search(pattern, raw)
            new = re.search(pattern, result)
            a = [v.strip() for v in old.group(1).split(',')]
            b = [v.strip() for v in new.group(1).split(',')]
            self.assertEqual(b[:11] + b[13:], a)
            self.assertEqual(new.group(2), old.group(2))
        with self.assertRaises(AssertionError): difficulty(result)

    def test_jade_remains_last_regular_and_returns_to_shang(self):
        result = secrets(self.original('MKTOAST.ASM'))
        block = result.split('\njade_check\n')[1].split('\njade_no')[0]
        self.assertIn('\tcmpi\t12,a0', block)
        self.assertIn('\tmovi\t14,a0\n\tmove\ta0,@map_position,w', block)
        with self.assertRaises(AssertionError): secrets(result)


if __name__ == '__main__': unittest.main()

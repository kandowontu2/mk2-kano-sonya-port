import unittest
import zipfile
from boss_category_source import integrate,category,HELPER
from prepare_game_candidate import ZIP
from inventory_character_tables import source_tables

class BossCategories(unittest.TestCase):
    def execute_source_helper(self,identity,action):
        lines=[line.split(';',1)[0].strip() for line in HELPER.splitlines()]
        lines=[line for line in lines if line]
        labels={line:index for index,line in enumerate(lines) if ' ' not in line and line!='rets'}
        pc=labels['ks_boss_category'];a0=0xdeadbeef;a1=action;equal=False;stack=[]
        for _ in range(40):
            line=lines[pc];pc+=1
            if line in labels:continue
            op,_,args=line.partition(' ')
            if op=='push':stack.append(a0)
            elif op=='pull':a0=stack.pop()
            elif op=='cmpi':
                value,register=args.split(',')
                value=int(value[:-1],16) if value.endswith('h') else int(value)
                equal=value==(a0 if register=='a0' else a1)
            elif op=='jrne':
                if not equal:pc=labels[args]
            elif op=='jruc':pc=labels[args]
            elif op=='move':
                a0=0x1000 if args.startswith('*a13(') else identity
            elif op=='clr':a1=0
            elif op=='srl':a1>>=8
            elif op=='rets':
                self.assertEqual(a0,0xdeadbeef);self.assertFalse(stack)
                return a1
            else:self.fail('Unhandled helper instruction: '+line)
        self.fail('Nonterminating source helper')

    def test_original_table_bytes_and_routes_preserved(self):
        with zipfile.ZipFile(ZIP) as archive:
            original=archive.read('mk2-rebuild-main/src/MKBOSS.ASM').decode('cp437').replace('\r\n','\n')
        changed=integrate(original)
        before,after=source_tables(original),source_tables(changed)
        for name in before:
            self.assertEqual([(row['type'],row['values']) for row in before[name]['rows']],
                             [(row['type'],row['values']) for row in after[name]['rows']],name)
        self.assertEqual(changed.count('callr ks_boss_category'),2)
        with self.assertRaises(AssertionError):integrate(changed)

    def test_identity_checked_specification(self):
        differences=[]
        for identity in range(19):
            for action in range(0x900):
                actual=self.execute_source_helper(identity,action)
                self.assertEqual(actual,category(identity,action))
                if actual!=action>>8:differences.append((identity,action))
        self.assertEqual(differences,[(17,0x211),(18,0x212)])

if __name__=='__main__':unittest.main()

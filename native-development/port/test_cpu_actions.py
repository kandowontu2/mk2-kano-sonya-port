import unittest
import zipfile
from pathlib import Path
from cpu_action_source import integrate,ROUTES,CODE
from inventory_character_tables import source_tables
from prepare_game_candidate import ZIP
from drone_source import integrate as original_extensions

PORT=Path(__file__).resolve().parent

class CPUActions(unittest.TestCase):
    def execute_lookup(self, identity, action, jade):
        # Execute the source branch/stride logic, not a duplicate dictionary lookup.
        lines=[line.split(';',1)[0].strip() for line in CODE.splitlines()]
        lines=[line for line in lines if line]
        labels={line:i for i,line in enumerate(lines) if ' ' not in line and line not in ('rets','setc','clrc')}
        memory={};tables={};cursor=0x1000
        for who,name in ((17,'kano'),(18,'sonya')):
            tables['ks_'+name+'_counter_rows']=cursor
            for tag,reaction in list(ROUTES[who].items())+[(0,'0')]:
                memory[cursor]=tag;memory[cursor+16]=reaction;cursor+=48
        registers={'a0':0xdeadbeef,'a1':action,'a2':0xfeedface}
        pc=labels['ks_own_counter_lookup'];stack=[];equal=False;carry=None
        for _ in range(180):
            line=lines[pc];pc+=1
            if line in labels:continue
            op,_,args=line.partition(' ')
            if op=='push':stack.append(registers[args])
            elif op=='pull':registers[args]=stack.pop()
            elif op=='move':
                if args=='*a13(p_otherguy),a0,l':registers['a0']=0x2000
                elif args=='*a0(ochar),a0,w':registers['a0']=identity
                elif args=='*a8(ochar),a0,w':registers['a0']=int(jade)
                elif args=='*a2+,a0,w':
                    registers['a0']=memory[registers['a2']];registers['a2']+=16
                elif args=='*a2,a2,l':registers['a2']=memory[registers['a2']]
                else:self.fail('Unhandled move: '+line)
            elif op=='movi':
                value,reg=args.split(',');registers[reg]=tables[value]
            elif op=='cmpi':
                value,reg=args.split(',')
                value=1 if value=='ft_jade' else int(value[:-1],16) if value.endswith('h') else int(value)
                equal=value==registers[reg]
            elif op=='cmp':
                left,right=args.split(',');equal=registers[left]==registers[right]
            elif op=='addi':
                value,reg=args.split(',');registers[reg]+=int(value)
            elif op=='clr':registers[args]='0'
            elif op=='jruc':pc=labels[args]
            elif op=='jreq':
                if equal:pc=labels[args]
            elif op=='jrne':
                if not equal:pc=labels[args]
            elif op=='setc':carry=True
            elif op=='clrc':carry=False
            elif op=='rets':
                self.assertEqual(registers['a0'],0xdeadbeef)
                self.assertEqual(registers['a1'],action)
                self.assertFalse(stack)
                return carry,registers['a2']
            else:self.fail('Unhandled lookup instruction: '+line)
        self.fail('Lookup did not terminate')

    def test_source_lookup_all_identities_and_actions(self):
        for identity in range(19):
            for action in range(0x900):
                for jade in (False,True):
                    handled,reaction=self.execute_lookup(identity,action,jade)
                    expected=ROUTES.get(identity,{}).get(action)
                    self.assertEqual(handled,expected is not None,(identity,action,jade))
                    if handled:
                        if jade and action in (0x211,0x212):expected='0'
                        self.assertEqual(reaction,expected,(identity,action,jade))

    def test_tables_and_history_preserved(self):
        with zipfile.ZipFile(ZIP) as archive:
            original=archive.read('mk2-rebuild-main/src/MKDRONE.ASM').decode('cp437').replace('\r\n','\n')
        original=original_extensions(original)
        changed=integrate(original)
        before,after=source_tables(original),source_tables(changed)
        for name in before:
            self.assertEqual([(row['type'],row['values']) for row in before[name]['rows']],
                             [(row['type'],row['values']) for row in after[name]['rows']],name)
        self.assertIn('move\ta1,*a13(p_otheract),w',changed)
        self.assertEqual(changed.count('callr ks_own_counter_lookup'),1)
        self.assertIn('move *a2+,a0,w\n\tcmpi 0,a0',changed)
        self.assertNotIn('cmpi 0ffffh,a0',changed)
        for name in ('ks_kano_counter_rows','ks_sonya_counter_rows'):
            table=source_tables(changed)[name]
            self.assertEqual(table['rows'][-2]['values'],['0'])
            self.assertEqual(table['rows'][-1]['values'],['0'])
        self.assertIn('callr drone_get_his_action\n\tmovk 3,a7\n\tcallr react_jump_table',changed)
        with self.assertRaises(AssertionError):integrate(changed)

    def test_explicit_own_tags(self):
        self.assertEqual(ROUTES[17][0x211],'ks_counter_projectile')
        self.assertEqual(ROUTES[18][0x212],'ks_counter_projectile')
        for identity in (17,18):
            for action in (0x215,0x218,0x21b):self.assertEqual(ROUTES[identity][action],'0')
            for action in (0x101,0x102,0x103,0x104,0x107):self.assertNotIn(action,ROUTES[identity])

if __name__=='__main__':unittest.main()

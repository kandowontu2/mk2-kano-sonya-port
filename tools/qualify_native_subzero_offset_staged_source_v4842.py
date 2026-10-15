"""Only qualified initialized-ROM table delta against actual compiled3836 source."""
import hashlib,json,re,struct,subprocess
from pathlib import Path
import qualify_native_subzero_victim_offset_v4838 as cause
ROOT,need,sha=cause.ROOT,cause.need,cause.sha
SOURCE=ROOT/'source_v4844_native_subzero_victim_offset/midtunit_m.cpp'
BASE=ROOT/'diagnostic_v3836_native_mileena_rom_identity/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
OUT=ROOT/'audit_v4843_native_subzero_offset_staged_source_checked'

def source_gate(text,old,guest):
    first=text.index("\t// Sub-Zero's original freeze/shatter victim task")
    last=text.index("\t// Reptile's tongue fatality",first)
    block=text[first:last]
    need(text[:first]+text[last:]==old,'Every actual compiled3836 source character outside one added initialization block unchanged')
    need('constexpr unsigned subzero_victim_offsets = 0xfa8a0;'in block and
        'constexpr uint32_t subzero_offset_original = 0xff8c27d0;'in block,'Exact independently free allocation and actual native short table')
    for token in ('read32(rom_offset(0xff8c23a0)) != subzero_offset_original',
        'read16(rom_offset(0xff8c2450)) != 0x24a7','read16(rom_offset(0xff82ede0)) != 0x2481',
        'at<subzero_victim_offsets+0x40','if (rom[at]!=0xff)',
        'std::copy_n(rom+rom_offset(subzero_offset_original),17*2,rom+subzero_victim_offsets);',
        'write16(subzero_victim_offsets+17*2,0);','write16(subzero_victim_offsets+18*2,0);',
        'write32(rom_offset(0xff8c23a0),native_address(subzero_victim_offsets));'):
        need(token in block,'Exact source-bound guarded native offset initialization '+token)
    need(block.count('write16(')==2 and block.count('write32(')==1 and
        not any(t in block for t in ('m_maincpu->','install_','m_regs','TMS34010_W','set_value')),
        'No runtime guest/register/state/identity repair or cache cap')
    repaired=bytearray(guest);destination=int(re.search(r'subzero_victim_offsets = (0x[0-9a-f]+)',block)[1],16)
    table=int(re.search(r'subzero_offset_original = (0x[0-9a-f]+)',block)[1],16)
    need(repaired[destination:destination+64]==b'\xff'*64,'Actual whole initialized RAM guest verifies unused allocation')
    repaired[destination:destination+34]=guest[cause.off(table):cause.off(table)+34]
    for index,value in re.findall(r'write16\(subzero_victim_offsets\+(\d+)\*2,(\d+)\)',block):
        struct.pack_into('<H',repaired,destination+int(index)*2,int(value))
    struct.pack_into('<I',repaired,cause.off(0xff8c23a0),0xff800000+destination*8)
    return hashlib.sha256(repaired).hexdigest().upper()

def main():
    need(not OUT.exists(),'Fresh exact staged source result')
    prior_path=cause.OUT/'report.json';prior=json.loads(prior_path.read_text())
    need(prior['passed']and len(prior['actualFaultsRejected'])==8 and not prior['compiledFixAccepted'],
        'Actual native cause/eight code-context faults retained; no source-only compilation claim')
    need(sha(BASE)=='185291A96BDF9C8B56F71E9B5C92D7A96FD59276F0BF65D7DFE957BDCA4F9D29',
        'Actual compiled machine source, not different dirty checkout or previous incomplete stage')
    need(sha(SOURCE)=='BAF102148E740A1CC96A44320E51051938E3AE4EADE5B716CD6B6D2534B252A6','Exact entire reviewed new native source')
    guest,_,_,_=cause.probe.sources();text,old=SOURCE.read_text(),BASE.read_text()
    positive=source_gate(text,old,guest)
    need(positive==prior['expectedRepairedGuestSHA256'],'Entire independently qualified repaired guest equals source initializer result')
    faults=[]
    for name,bad in (
        ('wrong_original_source',text.replace('init_mk2();','init_mk2ks();',1)),
        ('wrong_allocation',text.replace('= 0xfa8a0;','= 0xfa800;',1)),
        ('wrong_native_operand',text.replace('write32(rom_offset(0xff8c23a0)','write32(rom_offset(0xff8c26b0)',1)),
        ('truncated_stock_rows',text.replace('),17*2,rom+subzero_victim_offsets', '),12*2,rom+subzero_victim_offsets',1)),
        ('proxy_row',text.replace('+18*2,0);','+1*2,0);',1)),
        ('wrong_sonya_offset',text.replace('+18*2,0);','+18*2,1);',1)):
        need(bad!=text,'Actual staged source mutation')
        try:source_gate(bad,old,guest)
        except ValueError as error:faults.append(dict(kind=name,rejectedBy=str(error)))
        else:raise ValueError('Staged source fault admitted '+name)
        need(source_gate(text,old,guest)==positive,'Whole source/initialized guest positive restored')
    wrong=ROOT/'source_v4841_native_subzero_victim_offset/midtunit_m.cpp'
    wrong_text=wrong.read_text();a=wrong_text.index("\t// Sub-Zero's original freeze/shatter victim task");b=wrong_text.index("\t// Reptile's tongue fatality",a)
    need(wrong_text[:a]+wrong_text[b:]!=old,'Earlier dirty-checkout stage explicitly not actual3836 build eligible')
    pins=dict(prior['inputHashes'])
    for p in (prior_path,SOURCE,BASE,Path(__file__).resolve(),wrong,ROOT/'source_v4840_native_subzero_victim_offset/midtunit_m.cpp'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Actual prior native/public/dirty/source evidence unchanged')
    report=dict(passed=True,stagedSource=str(SOURCE),stagedSourceSHA256=sha(SOURCE),baseCompiledSource=str(BASE),
        baseCompiledSourceSHA256=sha(BASE),expectedGuestSHA256=positive,actualNativeCauseReport=str(prior_path),
        originalNativeSourceOutsideOneBlockUnchanged=True,originalNativeCauseFaultsRetained=8,actualSourceFaultsRejected=faults,
        earlierDirtyCheckoutStagesNotBuildEligible=True,currentDirtyCheckoutChanged=False,publicPlayableChanged=False,
        requiresCompilationAndNativeRuntimeRegression=True,compiledFixAccepted=False,fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compression before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
if __name__=='__main__':main()

"""Preserve failed package; successor includes the actual donor ROM dependencies."""
import inspect
import package_current_native_playtest_20261013 as previous

code = inspect.getsource(previous.main)
assert code.count("out = root/'release_current_native_playtest_20261013'") == 1
code = code.replace("out = root/'release_current_native_playtest_20261013'", "out = root/'release_current_native_playtest_20261013_complete_roms'")
code = code.replace('MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013.zip', 'MK2_Kano_Sonya_CURRENT_NATIVE_PLAYTEST_20261013_complete_roms.zip')
needle = '    hashes = {name:sync.sha(path) for name,path in files.items()}\n'
assert code.count(needle) == 1
code = code.replace(needle,
    "    for dependency in sorted((root/'roms/mk2ks').iterdir()):\n"
    "        if dependency.is_file() and dependency.name != 'mk2ks.mdata':\n"
    "            files['roms/mk2ks/'+dependency.name] = dependency\n" + needle)
context = dict(previous.__dict__)
exec(compile(code, __file__+'::complete ROM successor', 'exec'),context)
context['main']()

"""Use retained kernel NT image name; preserve post-exit Win32 query failure."""
import inspect
from types import SimpleNamespace
import recover_native_selector_continue_birth as previous


def recover(state,cases,handles,expected):
    source=inspect.getsource(previous.recover)
    before="    path=c.create_unicode_buffer(32768);length=w.DWORD(len(path))\n    need(kernel.k.QueryFullProcessImageNameW(job._handle,0,path,c.byref(length)), 'Actual original retained native image path after termination')"
    after="""    nt_buffer=c.create_string_buffer(131072);nt_length=w.ULONG()
    status=kernel.nt.NtQueryInformationProcess(job._handle,27,nt_buffer,len(nt_buffer),c.byref(nt_length))
    need(status==0,'Actual original retained kernel NT process-image filename')
    name=kernel.UnicodeString.from_buffer(nt_buffer)
    need(name.Length>0 and name.Length%2==0 and name.MaximumLength>=name.Length and
         c.addressof(nt_buffer)<=name.Buffer<c.addressof(nt_buffer)+len(nt_buffer)and
         name.Buffer+name.Length<=c.addressof(nt_buffer)+len(nt_buffer),'Complete bounded actual native image-name result')
    nt_image=c.wstring_at(name.Buffer,name.Length//2)
    drive=Path(held['command'][0]).drive;device=c.create_unicode_buffer(32768)
    query=kernel.k.QueryDosDeviceW;query.argtypes=[w.LPCWSTR,w.LPWSTR,w.DWORD];query.restype=w.DWORD
    need(query(drive,device,len(device))and nt_image.startswith(device.value+'\\\\'),
         'Actual kernel DOS-drive mapping, no inferred or guessed device path')
    path=SimpleNamespace(value=drive+nt_image[len(device.value):])"""
    changes=((before,after),
        ('actualOriginalHostIdentity=host,originalCIMBornUnix=',
         'actualOriginalHostIdentity=host,actualKernelNTImage=nt_image,actualDOSDrive=drive,actualKernelDOSDevice=device.value,originalPostExitWin32ImageQueryFailurePreserved=True,originalCIMBornUnix='),
        ("Path(__file__),ROOT/'tools/qualify_native_selector_continue_extra_windows.py'",
         "Path(__file__),Path(previous.__file__),ROOT/'tools/qualify_native_selector_continue_extra_windows.py'"))
    for before,after in changes:
        previous.need(source.count(before)==1,'Exact original recovery invariant '+before)
        source=source.replace(before,after,1)
    scope=dict(vars(previous),previous=previous,SimpleNamespace=SimpleNamespace,__file__=__file__)
    exec(compile(source,__file__+'::actual_retained_NT_image_instead_of_unavailable_Win32_getter','exec'),scope)
    return scope['recover'](state,cases,handles,expected)

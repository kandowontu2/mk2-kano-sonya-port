"""Read-only Win32 native process identity without a slow PowerShell subprocess.

Toolhelp supplies actual PID/parent. Kernel queries supply executable path,
creation time and full command line. No emulator, guest or audio state writes.
"""
import ctypes as c
from ctypes import wintypes as w

class ProcessEntry(c.Structure):
 _fields_=[('dwSize',w.DWORD),('cntUsage',w.DWORD),('th32ProcessID',w.DWORD),
           ('th32DefaultHeapID',c.c_size_t),('th32ModuleID',w.DWORD),
           ('cntThreads',w.DWORD),('th32ParentProcessID',w.DWORD),
           ('pcPriClassBase',w.LONG),('dwFlags',w.DWORD),('szExeFile',w.WCHAR*260)]

class UnicodeString(c.Structure):
 _fields_=[('Length',w.USHORT),('MaximumLength',w.USHORT),('Buffer',c.c_void_p)]

k=c.WinDLL('kernel32',use_last_error=True);nt=c.WinDLL('ntdll')
k.CreateToolhelp32Snapshot.argtypes=[w.DWORD,w.DWORD];k.CreateToolhelp32Snapshot.restype=w.HANDLE
k.Process32FirstW.argtypes=[w.HANDLE,c.POINTER(ProcessEntry)];k.Process32FirstW.restype=w.BOOL
k.Process32NextW.argtypes=[w.HANDLE,c.POINTER(ProcessEntry)];k.Process32NextW.restype=w.BOOL
k.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];k.OpenProcess.restype=w.HANDLE
k.CloseHandle.argtypes=[w.HANDLE];k.CloseHandle.restype=w.BOOL
k.QueryFullProcessImageNameW.argtypes=[w.HANDLE,w.DWORD,w.LPWSTR,c.POINTER(w.DWORD)];k.QueryFullProcessImageNameW.restype=w.BOOL
k.GetProcessTimes.argtypes=[w.HANDLE,*([c.POINTER(w.FILETIME)]*4)];k.GetProcessTimes.restype=w.BOOL
nt.NtQueryInformationProcess.argtypes=[w.HANDLE,w.ULONG,c.c_void_p,w.ULONG,c.POINTER(w.ULONG)];nt.NtQueryInformationProcess.restype=w.LONG

def census():
 snapshot=k.CreateToolhelp32Snapshot(2,0)
 if snapshot==c.c_void_p(-1).value:raise c.WinError(c.get_last_error())
 result=[];entry=ProcessEntry();entry.dwSize=c.sizeof(entry)
 try:
  present=k.Process32FirstW(snapshot,c.byref(entry))
  while present:
   if entry.szExeFile.lower()=='mkport_candidate.exe':
    handle=k.OpenProcess(0x1000,False,entry.th32ProcessID)
    if handle:
     try:
      path=c.create_unicode_buffer(32768);length=w.DWORD(len(path))
      creation,exit_time,kernel,user=(w.FILETIME()for _ in range(4))
      buffer=c.create_string_buffer(131072);returned=w.ULONG()
      if (k.QueryFullProcessImageNameW(handle,0,path,c.byref(length))and
          k.GetProcessTimes(handle,c.byref(creation),c.byref(exit_time),c.byref(kernel),c.byref(user))and
          nt.NtQueryInformationProcess(handle,60,buffer,len(buffer),c.byref(returned))==0):
       text=UnicodeString.from_buffer(buffer)
       command=c.wstring_at(text.Buffer,text.Length//2)
       born=((creation.dwHighDateTime<<32)|creation.dwLowDateTime)/10**7-11644473600
       result.append(dict(ProcessId=entry.th32ProcessID,ParentProcessId=entry.th32ParentProcessID,
                          ExecutablePath=path.value,CommandLine=command,createdUnix=born))
      else:raise c.WinError(c.get_last_error())
     finally:k.CloseHandle(handle)
   present=k.Process32NextW(snapshot,c.byref(entry))
  return result
 finally:k.CloseHandle(snapshot)

// Read-only Core Audio ABI from Windows SDK10.0.22621 audiopolicy/mmdeviceapi/endpointvolume.
using System;using System.Collections.Generic;using System.Runtime.InteropServices;
namespace MK2OutputProbe {
[ComImport,Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")]class Enumerator {}
[ComImport,Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]interface Devices {
 void EnumAudioEndpoints(int flow,uint mask,out Collection devices);void GetDefaultAudioEndpoint(int flow,int role,out Device device);
 void GetDevice([MarshalAs(UnmanagedType.LPWStr)]string id,out Device device);void RegisterEndpointNotificationCallback(IntPtr callback);void UnregisterEndpointNotificationCallback(IntPtr callback);
}
[ComImport,Guid("0BD7A1BE-7A1A-44DB-8397-CC5392387B5E"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]interface Collection {void GetCount(out uint n);void Item(uint index,out Device device);}
[ComImport,Guid("D666063F-1587-4E43-81F1-B948E807363F"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]interface Device {
 void Activate(ref Guid iid,uint context,IntPtr parameters,[MarshalAs(UnmanagedType.IUnknown)]out object result);void OpenPropertyStore(uint access,out IntPtr store);void GetId([MarshalAs(UnmanagedType.LPWStr)]out string id);void GetState(out uint state);
}
[ComImport,Guid("77AA99A0-1BD6-484F-8BC7-2C654C9A9B6F"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]interface Manager {
 void GetAudioSessionControl(IntPtr guid,uint flags,out IntPtr control);void GetSimpleAudioVolume(IntPtr guid,uint flags,out IntPtr volume);void GetSessionEnumerator(out Sessions sessions);
}
[ComImport,Guid("E2F5BB11-0570-40CA-ACDD-3AA01277DEE8"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]interface Sessions {void GetCount(out int count);void GetSession(int index,out Control control);}
[ComImport,Guid("F4B1A599-7266-4319-A8CA-E70ACB11E8CD"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]interface Control {void GetState(out int state);}
[ComImport,Guid("BFB7FF88-7239-4FC9-8FA2-07C950BE9C6D"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]interface Control2 {
 void GetState(out int state);void GetDisplayName([MarshalAs(UnmanagedType.LPWStr)]out string name);void SetDisplayName(IntPtr value,IntPtr context);void GetIconPath([MarshalAs(UnmanagedType.LPWStr)]out string path);void SetIconPath(IntPtr path,IntPtr context);void GetGroupingParam(out Guid group);void SetGroupingParam(IntPtr group,IntPtr context);void RegisterAudioSessionNotification(IntPtr events);void UnregisterAudioSessionNotification(IntPtr events);
 void GetSessionIdentifier([MarshalAs(UnmanagedType.LPWStr)]out string id);void GetSessionInstanceIdentifier([MarshalAs(UnmanagedType.LPWStr)]out string id);void GetProcessId(out uint pid);
}
[ComImport,Guid("87CE5498-68D6-44E5-9215-6DA47EF883D8"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]interface SimpleVolume {
 void SetMasterVolume(float volume,IntPtr context);void GetMasterVolume(out float volume);void SetMute([MarshalAs(UnmanagedType.Bool)]bool mute,IntPtr context);void GetMute([MarshalAs(UnmanagedType.Bool)]out bool mute);
}
[ComImport,Guid("C02216F6-8C67-4B5B-9D00-D008E73E0064"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]interface Meter {void GetPeakValue(out float peak);}
[ComImport,Guid("5CDF2C82-841E-4546-9722-0CF74078229A"),InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]interface EndpointVolume {
 void RegisterControlChangeNotify(IntPtr p);void UnregisterControlChangeNotify(IntPtr p);void GetChannelCount(out uint n);void SetMasterVolumeLevel(float v,IntPtr c);void SetMasterVolumeLevelScalar(float v,IntPtr c);void GetMasterVolumeLevel(out float v);void GetMasterVolumeLevelScalar(out float v);void SetChannelVolumeLevel(uint n,float v,IntPtr c);void SetChannelVolumeLevelScalar(uint n,float v,IntPtr c);void GetChannelVolumeLevel(uint n,out float v);void GetChannelVolumeLevelScalar(uint n,out float v);void SetMute([MarshalAs(UnmanagedType.Bool)]bool v,IntPtr c);void GetMute([MarshalAs(UnmanagedType.Bool)]out bool v);
}
public class Reading {public uint Pid;public string Endpoint;public int State;public float Peak,SessionVolume,EndpointVolume;public bool SessionMute,EndpointMute;public string Error;}
public static class ReadOnly {
 static void Free(object value){if(value!=null&&Marshal.IsComObject(value))Marshal.ReleaseComObject(value);}
 public static Reading[] Snapshot(uint target){
  List<Reading> result=new List<Reading>();Devices devices=null;Collection endpoints=null;
  try {devices=(Devices)new Enumerator();devices.EnumAudioEndpoints(0,1,out endpoints);uint n;endpoints.GetCount(out n);if(n>16)throw new Exception("Endpoint bound exceeded");
   for(uint e=0;e<n;e++){Device endpoint=null;object managerObject=null,volumeObject=null;Sessions sessions=null;
    try {endpoints.Item(e,out endpoint);string id;endpoint.GetId(out id);Guid mg=new Guid("77AA99A0-1BD6-484F-8BC7-2C654C9A9B6F");endpoint.Activate(ref mg,23,IntPtr.Zero,out managerObject);((Manager)managerObject).GetSessionEnumerator(out sessions);int count;sessions.GetCount(out count);if(count>128)throw new Exception("Session bound exceeded");
     for(int i=0;i<count;i++){Control control=null;try{sessions.GetSession(i,out control);Control2 typed=(Control2)control;uint pid;typed.GetProcessId(out pid);if(pid!=target)continue;
      Reading r=new Reading();r.Pid=pid;r.Endpoint=id;typed.GetState(out r.State);((Meter)control).GetPeakValue(out r.Peak);((SimpleVolume)control).GetMasterVolume(out r.SessionVolume);((SimpleVolume)control).GetMute(out r.SessionMute);
      Guid vg=new Guid("5CDF2C82-841E-4546-9722-0CF74078229A");endpoint.Activate(ref vg,23,IntPtr.Zero,out volumeObject);((EndpointVolume)volumeObject).GetMasterVolumeLevelScalar(out r.EndpointVolume);((EndpointVolume)volumeObject).GetMute(out r.EndpointMute);Free(volumeObject);volumeObject=null;result.Add(r);
     }catch(Exception ex){result.Add(new Reading{Pid=target,Error=ex.GetType().Name+":"+ex.Message});}finally{Free(control);}}
    }catch(Exception ex){result.Add(new Reading{Pid=target,Error=ex.GetType().Name+":"+ex.Message});}finally{Free(sessions);Free(volumeObject);Free(managerObject);Free(endpoint);}}
  }catch(Exception ex){result.Add(new Reading{Pid=target,Error=ex.GetType().Name+":"+ex.Message});}finally{Free(endpoints);Free(devices);}return result.ToArray();
 }
}
}

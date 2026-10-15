#include <cstdio>
#include <cstdint>
#include <fcntl.h>
#include <io.h>
extern "C" {
#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"
}
int main(int argc,char **argv)
{
    if (argc!=2) return 2;
    lua_State *s=luaL_newstate();if (!s) return 3;luaL_openlibs(s);
    // Parse the entire real outer file, then expand immutable wrappers.
    // Only callback registration is stubbed; no machine or guest exists.
    char const *setup=R"lua(
manager={machine={devices={[':maincpu']={spaces={program={}},state={}}}}}
emu={register_frame=function()end,register_sound_update=function()end,register_stop=function()end}
local native_load=load
load=function(text,name,mode,environment)
 local fn,err=native_load(text,name,mode,environment or _G);assert(fn,err)
 if name and name:find('::allocation_epoch_successor',1,true)then
  assert(not physical_controller);physical_controller=text;return function()end
 elseif name and name:find('::full_native_laser_audio',1,true)then
  assert(not audio_controller);audio_controller=text;return function()end
 end
 return fn
end
)lua";
    if (luaL_dostring(s,setup) || luaL_dofile(s,argv[1])) {
        std::fprintf(stderr,"%s\n",lua_tostring(s,-1));lua_close(s);return 4;
    }
    _setmode(_fileno(stdout),_O_BINARY);
    for (char const *key : {"physical_controller","audio_controller"}) {
        lua_getglobal(s,key);size_t length=0;char const *text=lua_tolstring(s,-1,&length);
        if (!text || !length || length>0xffffffffULL) {lua_close(s);return 5;}
        uint32_t size=static_cast<uint32_t>(length);
        if (std::fwrite(&size,4,1,stdout)!=1 || std::fwrite(text,1,length,stdout)!=length) {lua_close(s);return 6;}
        lua_pop(s,1);
    }
    lua_close(s);return 0;
}

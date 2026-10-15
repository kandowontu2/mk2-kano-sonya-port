#include <cstdio>
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
    lua_State *state=luaL_newstate();
    if (!state) return 3;
    luaL_openlibs(state);
    // Execute only the immutable wrapper expansion. Parse, but never run,
    // the final emulator controller. No machine/guest exists in this probe.
    char const *setup=R"lua(
local original_load=load
load=function(source,name,mode,environment)
 local compiled,error_text=original_load(source,name,mode,environment or _G)
 assert(compiled,error_text)
 if name and name:find('::allocation_epoch_successor',1,true) then
  assert(not captured_controller,'Only one final actual controller')
  captured_controller=source
  return function() end
 end
 return compiled
end
)lua";
    if (luaL_dostring(state,setup) || luaL_dofile(state,argv[1])) {
        std::fprintf(stderr,"%s\n",lua_tostring(state,-1));lua_close(state);return 4;
    }
    lua_getglobal(state,"captured_controller");
    size_t count=0;char const *text=lua_tolstring(state,-1,&count);
    if (!text || !count) {lua_close(state);return 5;}
    _setmode(_fileno(stdout),_O_BINARY);
    bool okay=std::fwrite(text,1,count,stdout)==count;
    lua_close(state);return okay?0:6;
}

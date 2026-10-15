-- Retain the executed6025 spacing failure; adjust only physical stop distance.
local root=assert(os.getenv('MK2KS_BASIC_ROOT'))
local path=root..'/mk2ks_close_contacts_v6025.lua'
local reader=assert(io.open(path,'r'));local source=reader:read('*a');reader:close()
local count;source,count=source:gsub('gap>43','gap>64');assert(count==2)
assert(load(source,'@'..path..'::native_contact_stop_distance_v6029','t',_ENV))()

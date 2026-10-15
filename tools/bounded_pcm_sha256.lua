-- Constant-memory SHA-256 for transient sound-update strings; no files/media.
local pcm_sha_k={
0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2}
local function pcm_ror(x,n)return ((x>>n)|(x<<(32-n)))&0xffffffff end
local function pcm_sha256(raw)
 local size=#raw
 local padded=raw..'\128'..string.rep('\0',(55-size)%64)..string.pack('>I8',size*8)
 local h={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19}
 for offset=1,#padded,64 do
  local w={}
  for i=1,16 do w[i]=string.unpack('>I4',padded,offset+(i-1)*4)end
  for i=17,64 do
   local a,b=w[i-15],w[i-2]
   local s0=pcm_ror(a,7)~pcm_ror(a,18)~(a>>3)
   local s1=pcm_ror(b,17)~pcm_ror(b,19)~(b>>10)
   w[i]=(w[i-16]+s0+w[i-7]+s1)&0xffffffff
  end
  local a,b,c,d,e,f,g,j=table.unpack(h)
  for i=1,64 do
   local s1=pcm_ror(e,6)~pcm_ror(e,11)~pcm_ror(e,25)
   local ch=(e&f)~((~e)&g)
   local t1=(j+s1+ch+pcm_sha_k[i]+w[i])&0xffffffff
   local s0=pcm_ror(a,2)~pcm_ror(a,13)~pcm_ror(a,22)
   local maj=(a&b)~(a&c)~(b&c)
   local t2=(s0+maj)&0xffffffff
   j,g,f,e,d,c,b,a=g,f,e,(d+t1)&0xffffffff,c,b,a,(t1+t2)&0xffffffff
  end
  local v={a,b,c,d,e,f,g,j}
  for i=1,8 do h[i]=(h[i]+v[i])&0xffffffff end
 end
 local hex={};for i=1,8 do hex[i]=string.format('%08X',h[i])end
 return table.concat(hex)
end
assert(pcm_sha256('')=='E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855')
assert(pcm_sha256('abc')=='BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD')
assert(pcm_sha256(string.rep('a',1000000))=='CDC76E5C9914FB9281A1C7E284D73E67F1809A48A497200E046D39CCC7112CD0')

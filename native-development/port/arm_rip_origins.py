"""Native held/throw trajectory geometry, never another fighter's pixels."""

# MKMK3.TBL LKRIPARM1..5 / NJGIRLARM1..5, width,height,xOffset,yOffset.
# Own component sizes differ; preserve each native center and bottom path.
REFERENCE={
    'kano':((57,26,-31,-90),(64,15,6,-113),(46,48,44,-57),(59,23,83,-91),(57,10,97,-135)),
    'sonya':((53,37,-31,-76),(63,21,7,-107),(50,40,50,-53),(58,25,85,-89),(59,7,102,-138)),
}

def origin(actor,phase,width,height):
    old_width,old_height,x,y=REFERENCE[actor][phase]
    return x+round((width-old_width)/2),y+height-old_height

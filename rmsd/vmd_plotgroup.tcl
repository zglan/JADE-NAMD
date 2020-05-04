mol load xyz tmp.xyz
set num [molinfo top get numframes]
mol drawframes top 0 0:$num
color Display Background white
axes location off
rotate x by 90
rotate y by 50
rotate z by 50
render snapshot tmp.bmp
quit

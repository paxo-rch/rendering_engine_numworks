from math import *
from kandinsky import *
from ion import *
from time import *
from random import *
from graphics import *
from os import *
from texture import *

px=0
py=0
pz=0

rx=0
ry=0
rz=0

def rotate(x,y,r):
  r*=-1
  cosR=cos(r)
  sinR=sin(r)
  a2=[0,0]
  a2[0]=x*cosR-y*sinR
  a2[1]=y*cosR+x*sinR
      
  return a2


timer = monotonic()

map=[]

def projection():
  global px,pz
  global rx,rz
  global map
  
  pX=0
  pY=0
  pZ=1
  
  cosX = cos(rx)
  sinX = sin(rx)
  cosY = cos(ry*(-1))
  sinY = sin(ry*(-1))
  
  # rotate Y
  pX2=pX
  pX=cosY*pX2+sinY*pZ
  pZ=-sinY*pX2+cosY*pZ
    
  pY2=pY
  pX2=pX
    
  # rotate X
  pY2=pY
  pY=cosX*pY2-sinX*pZ
  pZ=sinX*pY2+cosX*pZ
  
  vx,vy,vz=pX,pY,pZ
  
  chx, chy, chz = px, py*(-1), pz
  print(vx,vy,vz)

  for i in range(10):
    chx+=vx
    chy+=vy
    chz+=vz
    
    for j in range(len(map)):
      if(map[j][0]<chx and chx<map[j][0]+1):
        if(map[j][1]-1<chy and chy<map[j][1]):
          if(map[j][2]<chz and chz<map[j][2]+1):
            return [map[j][0],map[j][1],map[j][2],map[j][3]]


def keyboard_touch():
  global timer
  if(timer+0.10>monotonic()):
    return False
  if(keydown(KEY_UP) or keydown(KEY_DOWN) or keydown(KEY_RIGHT) or keydown(KEY_LEFT) or keydown(KEY_TWO) or keydown(KEY_FOUR) or keydown(KEY_EIGHT) or keydown(KEY_SIX) or keydown(KEY_PLUS) or keydown(KEY_MINUS) or keydown(KEY_EXE)):
    timer = monotonic()
    return True
  return False
  

def distance3D(x,y,z):
  global px, py, pz

  return sqrt((px-x)**2+(y-py)**2+(pz-z)**2)

def maximum(liste):
    maxi = liste[0]
    for i in liste:
        if i >= maxi:
            maxi = i
    return maxi

def getPoint2D(pointX, pointY, pointZ):
    global px, py, pz, rx, ry, rz
    camX=px
    camY=py
    camZ=pz
    
    camRX=rx
    camRY=ry
    camRZ=rz

    pX = pointX - camX
    pY = pointY - camY
    pZ = pointZ - camZ

    cosX = cos(camRX)
    sinX = sin(camRX)
    cosY = cos(camRY)
    sinY = sin(camRY)
    cosZ = cos(camRZ)
    sinZ = sin(camRZ)

    # rotate Y
    pX2=pX
    pX=cosY*pX2+sinY*pZ
    pZ=-sinY*pX2+cosY*pZ
    
    pY2=pY
    pX2=pX
    
    # rotate X
    pY2=pY
    pY=cosX*pY2-sinX*pZ
    pZ=sinX*pY2+cosX*pZ
    
    if pZ <= 0:
        return None

    """# rotate Z
    pX2 = pX
    pX = cosZ * pX2 - sinZ * pY
    pY = sinZ * pX2 + cosZ * pY"""

    pY2 = pY
    pX2 = pX

    # Perspective projection
    f = 320 / pZ
    pX2 = pX * f
    pY2 = pY * f

    pX2 += 320 / 2
    pY2 += 240 / 2
    return [int(pX2), int(pY2)]

drawed=0
  
class cube:
  def __init__(self,x,y,z,sx,sy,sz):
    self.x=x
    self.y=y
    self.z=z
    self.sx=sx
    self.sy=sy
    self.sz=sz

  def draw(self, index, fill_faces):
    global drawed
    global px, py, pz
    global colors
    self.y*=-1
    if(self.z<=0):
      return
    try:
      co1=getPoint2D(self.x,self.y,self.z)
      co2=getPoint2D(self.x+self.sx,self.y,self.z)
      co3=getPoint2D(self.x+self.sx,self.y+self.sy,self.z)
      co4=getPoint2D(self.x,self.y+self.sy,self.z)
      co5=getPoint2D(self.x,self.y,self.z+self.sz)
      co6=getPoint2D(self.x+self.sx,self.y,self.z+self.sz)
      co7=getPoint2D(self.x+self.sx,self.y+self.sy,self.z+self.sz)
      co8=getPoint2D(self.x,self.y+self.sy,self.z+self.sz)
    except:      
      return

    if(co1==None or co2==None or co3==None or co4==None or co5==None or co6==None or co7==None or co8==None):
      return

    co_=[co1,co2,co3,co4,co5,co6,co7,co8]
    need_return=0
    for i in range(8):
      if(co_[i][0]>0 and co_[i][0]<320 and co_[i][1]>0 and co_[i][1]<220):
        need_return+=1
      
    if(need_return==0):
      return
    
    cote=[[colors[index][0][0],colors[index][0][1],colors[index][0][2]], [colors[index][0][0]/1.2,colors[index][0][1]/1.2,colors[index][0][2]/1.2]]
    color_up=[[colors[index][1][0],colors[index][1][1],colors[index][1][2]], [colors[index][1][0]/1.2,colors[index][1][1]/1.2,colors[index][1][2]/1.2]]

    # calculer le point le plus proche

    listD=[
      distance3D(self.x+0.5,self.y+0.5,self.z),
      distance3D(self.x+0.5+self.sx,self.y+0.5,self.z),
      distance3D(self.x+0.5+self.sx,self.y+0.5+self.sy,self.z),
      distance3D(self.x+0.5,self.y+0.5+self.sy,self.z),      
      distance3D(self.x+0.5,self.y+0.5,self.z+self.sz),
      distance3D(self.x+0.5+self.sx,self.y+0.5,self.z+self.sz),
      distance3D(self.x+0.5+self.sx,self.y+0.5+self.sy,self.z+self.sz),
      distance3D(self.x+0.5,self.y+0.5+self.sy,self.z+self.sz)
    ]

    listT=sorted(listD) # trieÌe
    listC=[0,0,0]
    
    id=listD.index(listT[0])+1

    BLACK=[0,0,0]
    
    if(fill_faces==0):
      draw_line(co5[0],co5[1],co6[0],co6[1],BLACK)
      draw_line(co6[0],co6[1],co7[0],co7[1],BLACK)
      draw_line(co8[0],co8[1],co5[0],co5[1],BLACK)
      draw_line(co1[0],co1[1],co2[0],co2[1],BLACK)
      draw_line(co2[0],co2[1],co3[0],co3[1],BLACK)
      draw_line(co4[0],co4[1],co1[0],co1[1],BLACK)
      draw_line(co3[0],co3[1],co4[0],co4[1],BLACK)
      draw_line(co3[0],co3[1],co7[0],co7[1],BLACK)
      draw_line(co2[0],co2[1],co6[0],co6[1],BLACK)
      draw_line(co1[0],co1[1],co5[0],co5[1],BLACK)
      draw_line(co7[0],co7[1],co8[0],co8[1],BLACK)
      draw_line(co4[0],co4[1],co8[0],co8[1],BLACK)
    
    else:
      if((1 == id) or (2 == id) or (6 == id) or (5 == id)):
        drawFace(co1, co2, co6, co5, [color_up[0], color_up[1]])
        
      if((1 == id) or (3 == id) or (4 == id) or (2 == id)):
        drawFace(co1, co2, co3, co4, [cote[0], cote[1]])
        
      if((2 == id) or (6 == id) or (7 == id) or (3 == id)):
        drawFace(co2, co6, co7, co3, [cote[0], cote[1]])
        
      if((1 == id) or (5 == id) or (4 == id) or (8 == id)):
        drawFace(co1, co5, co8, co4, [cote[0], cote[1]])
        
      if((5 == id) or (6 == id) or (7 == id) or (8 == id)):
        drawFace(co5, co6, co7, co8, [cote[0], cote[1]])

      if((8 == id) or (7 == id) or (3 == id) or (4 == id)):
        drawFace(co8, co7, co3, co4, [cote[0], cote[1]])
          
      drawed+=1

sizeMap=0

def load():
  global map
  global sizeMap
  try:
    o=open("map.py")
  except:
    print("map not found")
  s=o.read()
  sx=0
  
  #try:  
  for y in range(5):
    for z in range(10):
      for x in range(10):
        try:
          if(s[111*y+11*z+x]!="0"):
            map.append([x,y,z+10, int(s[111*y+11*z+x])-1])
            sizeMap+=1
        except:
          pass
  #except:
  #  print("invalid map")

load()

c=cube(0,0,0,0,0,0)

def drawAll():
    global px
    global py 
    global pz
    global drawed
    fill_rect(0,0,320,240,color(194,251,252))
    #draw_string(str(round(px, 1))+";"+str(round(py, 1))+";"+str(round(pz, 1))+"  blocks: " + str(len(map)),0,0)
    drawed=0
    map_=list(map)

    for i in range(len(map)):
      break
      if(keyboard_touch()):
        return True
      c.__init__(map[i][0],map[i][1],map[i][2],1,1,1)
      c.draw(map[i][3], False)
    
    while(len(map_)>0):
      if(keyboard_touch()):
        return True
      sizes=[]
      for i in range(len(map_)):
        sizes.append(distance3D(map_[i][0], -map_[i][1], map_[i][2]))

      index=sizes.index(maximum(sizes))
      c.__init__(map_[index][0],map_[index][1],map_[index][2],1,1,1)
      c.draw(map_[index][3], True)
      del map_[index]
    
    #draw_string("printed: "+str(drawed), 0, 200)
    draw_line(160, 90, 160, 130, color(255,255,255))
    draw_line(140, 110, 180, 110, color(255,255,255))
    return False

reload=1

while(1):
    if(keydown(KEY_UP)):
        mvt=rotate(0.3, 0, ry)
        pz+=mvt[0]
        px+=mvt[1]
        reload=1
    if(keydown(KEY_DOWN)):
        mvt=rotate(-0.3, 0, ry)
        pz+=mvt[0]
        px+=mvt[1]
        reload=1
    if(keydown(KEY_RIGHT)):
        mvt=rotate(0, 0.3, ry)
        pz+=mvt[0]
        px+=mvt[1]
        reload=1
    if(keydown(KEY_LEFT)):
        mvt=rotate(0, -0.3, ry)
        pz+=mvt[0]
        px+=mvt[1]
        reload=1
    if(keydown(KEY_PLUS)):
        py-=0.5
        reload=1
    if(keydown(KEY_MINUS)):
        py+=0.5
        reload=1
    if(keydown(KEY_SIX)):
        ry-=radians(5)
        reload=1
    if(keydown(KEY_FOUR)):
        ry+=radians(5)
        reload=1
    if(keydown(KEY_EIGHT)):
        rx-=radians(5)
        reload=1
    if(keydown(KEY_TWO)):
        rx+=radians(5)
        reload=1
    if(keydown(KEY_EXE)):       
        try:
          del map[map.index(projection())]
        except:
          print(projection()) 
        reload=1
      
    st=False  
    for i in map:
      if(False):
        pass
      
    if st:
      py-=0.5
    
    if(reload==1):
      drawAll()
      reload=0

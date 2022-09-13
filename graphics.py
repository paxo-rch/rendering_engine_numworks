from kandinsky import *
from ion import *
from random import *
from math import *

sp=1

lsts=-1
lstr=0

def fillTriangle(x1, y1, x2, y2, x3, y3, col, st):
    global lstr, lsts
    A=[0,0]
    B=[0,0]
    C=[0,0]
    if (x1>x2):
        if (x2>x3):
            A[0]=x1
            A[1]=y1 
            B[0]=x3
            B[1]=y3 
            C[0]=x2
            C[1]=y2
        else:
            if (x1>x3):
                A[0]=x1
                A[1]=y1
                B[0]=x2
                B[1]=y2
                C[0]=x3
                C[1]=y3
            else :
                A[0]=x3
                A[1]=y3
                B[0]=x2
                B[1]=y2
                C[0]=x1
                C[1]=y1
    else:
        if(x1>x3):
            A[0]=x2
            A[1]=y2 
            B[0]=x3
            B[1]=y3 
            C[0]=x1
            C[1]=y1
        else:
            if (x2<x3):
                A[0]=x3
                A[1]=y3 
                B[0]=x1
                B[1]=y1 
                C[0]=x2
                C[1]=y2
            else:
                A[0]=x2
                A[1]=y2 
                B[0]=x1
                B[1]=y1 
                C[0]=x3
                C[1]=y3

    AB_a = A[1]-B[1] #-x2
    AB_b = B[0]-A[0] #x1
    AB_c = -(AB_a*A[0]+AB_b*A[1]) #c=-(a*xA+b*yA)
    if(AB_b==0):
      AB_a=0
      AB_c=0
    else:
      AB_a /=AB_b 
      AB_c /=AB_b #normalisation pour y
    #equation (AC)
    AC_a = A[1]-C[1] #-x2
    AC_b = C[0]-A[0] #x1
    AC_c = -(AC_a*A[0]+AC_b*A[1]) #c=-(a*xA+b*yA)
    if(AC_b==0):
      AC_a=0
      AC_c=0
    else:
      AC_a /=AC_b 
      AC_c /=AC_b #normalisation pour y
    #equation (BC)
    BC_a = B[1]-C[1] #-x2
    BC_b = C[0]-B[0] #x1
    BC_c = -(BC_a*B[0]+BC_b*B[1]) #c=-(a*xB+b*yB)
    if(BC_b==0):
      BC_a = 0
      BC_c = 0
    else:
      BC_a /=BC_b
      BC_c /=BC_b #normalisation pour y
    i=0
    r=0
    if(st!=lsts):
      r=randint(0,2)
      lstr=r
    else:
      r=lstr
    if(st==0):
      r=0
    else:
      r=1
    lsts=st      
    
    speed=1
    
    x = B[0]
    while (x < C[0]): #partie [BA [BC]
        #draw_line(int(x),int(-(AB_a*x+AB_c)),int(x),int(-(BC_a*x+BC_c)), color(col[0]-i,col[1]-i,col[2]-i))
        fill_rect(int(x),int(-(AB_a*x+AB_c)),speed,int(-(BC_a*x+BC_c))-int(-(AB_a*x+AB_c)),color(col[0]-i,col[1]-i,col[2]-i))
        x+=speed
        i+=r

    x = C[0]
    while (x < A[0]): #parite BA] [AC]
        #draw_line(int(x),int(-(AB_a*x+AB_c)),int(x),int(-(AC_a*x+AC_c)), color(col[0]-i,col[1]-i,col[2]-i))
        fill_rect(int(x),int(-(AB_a*x+AB_c)),speed,int(-(AC_a*x+AC_c))-int(-(AB_a*x+AB_c)),color(col[0]-i,col[1]-i,col[2]-i))
        x+=speed
        i+=r

def circle(x0,y0,r,c,e):
  for i in range(2*e):
    xd=x0-int((r-i*0.5)/sqrt(2))
    xf=x0+int((r-i*0.5)/sqrt(2))
    for x in range(xd,xf+1):
      x1=x
      y1=y0+int(sqrt((r-i*0.5)**2-(x-x0)**2))
      set_pixel(x,y1,c)
      for j in range(3):
        x2=x0+y1-y0
        y2=y0+x0-x1
        set_pixel(x2,y2,c)
        x1,y1=x2,y2

def fillCircle(x0,y0,r,c1,e,c2):
  cercle(x0,y0,r,c1,e)
  cercle(x0,y0,r-e,c2,r-e)
  
def drawFace(co1,co2,co3,co4,texture):
  a=co1
  b=[0,0]
  c=co2
  d=[0,0]
  e=[0,0]
  f=[0,0]
  g=co4
  h=[0,0]
  e=co3
  x=0
  y=1
  
  def di(a,b):
    return sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
  
  def dr(c1, c2):
    draw_line(int(c1[0]),int(c1[1]),int(c2[0]),int(c2[1]),[0,0,0])

  def translation(a,b,c,f):
    sx=c[0]-b[0]
    sy=c[1]-b[1]
    return [b[0]+(sx/f),b[1]+(sy/f)]

  def tmoy(a,b):
    return [(a[0]+b[0])/2,(a[1]+b[1])/2]

  fx=di(g,a)/di(e,c)
  fy=di(c,a)/di(e,g)

  if(fx<0):
      fx=1/fx
  
  dacx=c[x]-a[x]
  dgex=e[x]-g[x]
  dagx=g[x]-a[x]
  dcex=e[x]-c[x]

  dacy=c[y]-a[y]
  dgey=e[y]-g[y]
  dagy=g[y]-a[y]
  dcey=e[y]-c[y]

  print(fx,fy)
  
  b=translation(b,c,a,2)
  f=translation(f,e,g,2)
  h=translation(h,a,g,2)
  d=translation(d,c,e,2)

  i=translation(0,d,h,2)
  
  for i in [a,b,c,d,e,f,g,h,i]:
    i[0]=int(i[0])
    i[1]=int(i[1])

  fill_polygon([a,b,i,h],texture[0])
  fill_polygon([b,c,d,i],texture[1])
  fill_polygon([h,i,f,g],texture[1])
  fill_polygon([i,d,e,f],texture[0])

drawFace([11,12],[101,11],[102,50],[10,110], [color(255, 0, 0), color(0,255,0)])


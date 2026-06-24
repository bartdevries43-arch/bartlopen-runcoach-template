#!/usr/bin/env python3
"""Genereer een social-preview (og-image.png, 1200x630) in de Magma-huisstijl.
Pas TITLE/RUNNER/GOAL/DETAIL/PCT aan per loper en draai: python3 generate_og.py"""
from PIL import Image, ImageDraw, ImageFont
import math

# ---- pas dit aan per loper ----
TITLE  = "Op naar 21,1K"
RUNNER = "Demoloper"
GOAL   = "Halve marathon · richttijd ±2:15"
DETAIL = "16 weken · 3 trainingen per week"
PCT    = 0.62            # decoratieve ring (0..1)
OUT    = "og-image.png"
# --------------------------------

ORANGE=(255,154,61); PINK=(255,45,120); BG0=(11,10,13); BG1=(26,18,30)
WHITE=(245,243,248); MUTED=(150,140,160)
def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def font(paths,size):
    for p in paths:
        try: return ImageFont.truetype(p,size)
        except Exception: pass
    return ImageFont.load_default()
TITLEF=["/System/Library/Fonts/Supplemental/Avenir Next Condensed.ttc","/System/Library/Fonts/Supplemental/Arial Black.ttf"]
BOLD=["/System/Library/Fonts/Supplemental/Arial Bold.ttf"]
REG=["/System/Library/Fonts/Supplemental/Arial.ttf"]

W,H=1200,630
img=Image.new("RGB",(W,H),BG0); px=img.load()
for y in range(H):
    for x in range(0,W,2):
        c=lerp(BG0,BG1,(x/W)*0.5+(y/H)*0.5); px[x,y]=c; px[min(x+1,W-1),y]=c
d=ImageDraw.Draw(img,"RGBA")
for r in range(420,0,-6): d.ellipse([980-r,-120-r,980+r,-120+r],fill=(255,80,120,int(26*(1-r/420))))
for r in range(360,0,-6): d.ellipse([1080-r,120-r,1080+r,120+r],fill=(255,154,61,int(22*(1-r/360))))
cx,cy,R,w=980,330,150,26
d.ellipse([cx-R,cy-R,cx+R,cy+R],outline=(255,255,255,28),width=w)
for i in range(int(360*PCT)):
    ang=math.radians(-90+i); col=lerp(ORANGE,PINK,min(1,(i/360)/max(PCT,0.01)))
    x=cx+R*math.cos(ang); y=cy+R*math.sin(ang); d.ellipse([x-w/2,y-w/2,x+w/2,y+w/2],fill=col)
fp=font(TITLEF,72); s=f"{int(PCT*100)}%"; bb=d.textbbox((0,0),s,font=fp)
d.text((cx-(bb[2]-bb[0])/2,cy-58),s,font=fp,fill=WHITE)
ft2=font(BOLD,26); bb=d.textbbox((0,0),"KLAAR",font=ft2); d.text((cx-(bb[2]-bb[0])/2,cy+24),"KLAAR",font=ft2,fill=MUTED)
d.rounded_rectangle([80,86,134,94],4,fill=ORANGE); d.text((148,78),"BARTLOPEN · RUN COACH",font=font(BOLD,24),fill=MUTED)
ft=font(TITLEF,150); d.text((76,150),TITLE,font=ft,fill=WHITE); bb=d.textbbox((76,150),TITLE,font=ft)
d.rounded_rectangle([80,bb[3]+6,340,bb[3]+16],5,fill=PINK)
d.text((80,bb[3]+44),f"voor {RUNNER}",font=font(BOLD,40),fill=WHITE)
d.text((80,bb[3]+96),GOAL,font=font(REG,34),fill=ORANGE)
d.text((80,H-118),DETAIL,font=font(BOLD,26),fill=MUTED)
d.text((80,H-76),"Zet 'm op, strijder!",font=font(TITLEF,38),fill=WHITE)
img.save(OUT,"PNG"); print("opgeslagen:",OUT)

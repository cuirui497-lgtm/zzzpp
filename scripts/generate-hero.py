"""Generate the original locally encoded hero loop. Requires Pillow, numpy, imageio-ffmpeg."""
import sys
from pathlib import Path
sys.path.insert(0,'/tmp/portfolio-video-deps')
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
W,H=1600,900
root=Path(__file__).resolve().parents[1]/'public/assets'
y,x=np.mgrid[0:H,0:W];glow=np.exp(-((x-1120)**2/(600**2)+(y-450)**2/(470**2)))
bg=np.stack([15+glow*15,17+glow*20,14+glow*10],axis=-1).astype('uint8')
n,m=180,48
u,v=np.meshgrid(np.arange(n)*2*np.pi/n,np.arange(m)*2*np.pi/m,indexing='ij')
u=u.ravel();v=v.ravel()
indices=np.arange(n*m).reshape(n,m)
quads=np.stack([indices,np.roll(indices,-1,axis=0),np.roll(np.roll(indices,-1,axis=0),-1,axis=1),np.roll(indices,-1,axis=1)],axis=-1).reshape(-1,4)
writer=imageio_ffmpeg.write_frames(str(root/'hero.mp4'),(W,H),fps=25,codec='libx264',quality=7,macro_block_size=2,output_params=['-movflags','+faststart','-pix_fmt','yuv420p'])
writer.send(None)
for f in range(150):
 t=f/150*2*np.pi;a=.80+.12*np.sin(t);b=.48+.10*np.cos(t)
 r=2.35+.78*np.cos(v)
 xx=r*np.cos(u); yy=r*np.sin(u);zz=.78*np.sin(v)
 Y=yy*np.cos(a)-zz*np.sin(a);Z=yy*np.sin(a)+zz*np.cos(a)
 X=xx*np.cos(b)+Z*np.sin(b);Z=-xx*np.sin(b)+Z*np.cos(b)
 scale=142*(1+Z*.035)
 coords=np.stack([1120+X*scale,450+Y*scale],axis=-1)
 # A metallic surface with directional reflections and a restrained olive tint.
 light=.08+.24*np.maximum(0,np.cos(v+1.0))+.68*np.maximum(0,.65*np.sin(v+.8)+.35*np.cos(u-1.8))**9
 rim=np.maximum(0,np.cos(v-.5))**18
 colors=np.clip(np.stack([light*.91+rim*.09,light+rim*.12,light*.82],axis=-1)*255,0,255).astype('uint8')
 im=Image.fromarray(bg.copy());d=ImageDraw.Draw(im)
 for q in np.argsort(Z[quads].mean(axis=1)):
  ids=quads[q];d.polygon([tuple(p) for p in coords[ids]],fill=tuple(colors[ids[0]]))
 # Fine ring lines establish a precise, engineered surface.
 for k in range(0,n,12):
  ids=indices[k];visible=Z[ids]>.45
  pts=coords[ids]
  for j in range(m-1):
   if visible[j] and visible[j+1]: d.line([tuple(pts[j]),tuple(pts[j+1])],fill=(95,109,79),width=1)
 if f==0:im.save(root/'hero-poster.jpg',quality=92)
 writer.send(np.asarray(im).tobytes())
writer.close()
print('Created hero.mp4 and hero-poster.jpg')

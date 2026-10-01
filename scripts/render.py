"""Render new sentence images with Pillow's RAQM shaping; not a legacy replica."""
import argparse, json, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, features

p=argparse.ArgumentParser()
p.add_argument('--text',required=True); p.add_argument('--font',type=Path,required=True)
p.add_argument('--output',type=Path,default=Path('generated/sample.png'))
p.add_argument('--size',type=int,default=48); p.add_argument('--seed',type=int,default=0)
p.add_argument('--noise',type=float,default=0)
a=p.parse_args()
if not features.check_feature('raqm'):
    p.error('Pillow with RAQM is required for Persian shaping')
if not 0 <= a.noise <= 1:
    p.error('--noise must be between 0 and 1')
f=ImageFont.truetype(str(a.font),a.size,layout_engine=ImageFont.Layout.RAQM)
b=f.getbbox(a.text,direction='rtl',language='fa'); margin=16
im=Image.new('L',(b[2]-b[0]+2*margin,b[3]-b[1]+2*margin),255)
ImageDraw.Draw(im).text((margin-b[0],margin-b[1]),a.text,font=f,fill=0,direction='rtl',language='fa')
r=random.Random(a.seed)
for _ in range(round(im.width*im.height*a.noise)):
    im.putpixel((r.randrange(im.width),r.randrange(im.height)),r.choice([0,255]))
a.output.parent.mkdir(parents=True,exist_ok=True); im.save(a.output)
a.output.with_suffix('.json').write_text(json.dumps({'text':a.text,'font':a.font.name,'size':a.size,'seed':a.seed,'noise_probability':a.noise,'width':im.width,'height':im.height,'annotation_level':'sentence'},ensure_ascii=False,indent=2)+'\n')

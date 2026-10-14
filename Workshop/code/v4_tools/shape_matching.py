"""Geometric template-matching teaching animation; no learned eye detector.

All templates search the entire Canny edge image. No eye-region restriction,
manual best-match selection, training, or model inference is used.
"""
import json
from pathlib import Path

import cv2
import matplotlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CODE=Path(__file__).resolve().parents[1]
OUT=CODE/'v4_outputs'
ASSETS=CODE/'assets'
FONT_DIR=Path(matplotlib.get_data_path())/'fonts/ttf'
INK='#111111';TEAL='#087D73';ORANGE='#AF5700'


def font(size,bold=False):
    return ImageFont.truetype(str(FONT_DIR/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),size)


def template(name):
    # Equal canvas and stroke width keep the comparison easy to understand.
    # The oval changes aspect ratio, not search resolution or stroke intensity.
    a=np.zeros((76,76),np.uint8)
    if name=='square':cv2.rectangle(a,(11,11),(64,64),255,2)
    elif name=='circle':cv2.circle(a,(38,38),27,255,2)
    elif name=='oval':cv2.ellipse(a,(38,38),(30,21),0,0,360,255,2)
    else:raise ValueError(name)
    return a


def generate():
    OUT.mkdir(exist_ok=True)
    photo=Image.open(ASSETS/'cat_chelsea.png').convert('RGB')
    photo=photo.resize((640,427),Image.Resampling.LANCZOS)
    rgb=np.asarray(photo)
    gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
    edges=cv2.Canny(cv2.GaussianBlur(gray,(3,3),.7),60,140)
    Image.fromarray(edges).save(OUT/'shape_search_edges.png')
    results={};responses={};templates={}
    for name in ('square','circle','oval'):
        t=template(name);templates[name]=t
        r=cv2.matchTemplate(edges,t,cv2.TM_CCOEFF_NORMED)
        _,score,_,loc=cv2.minMaxLoc(r)
        results[name]={'score':float(score),'top_left_xy':list(loc),'canvas_wh':[76,76],
                       'best_box_xyxy':[loc[0],loc[1],loc[0]+76,loc[1]+76]}
        responses[name]=r
        Image.fromarray(t).save(OUT/f'shape_template_{name}.png')
    np.savez_compressed(OUT/'shape_matching_responses.npz',**responses)
    evidence={'source':'assets/cat_chelsea.png','search_image_size':[640,427],
              'method':'cv2.TM_CCOEFF_NORMED on Canny edges','template_canvas':[76,76],
              'edge_preprocessing':{'Gaussian_kernel':[3,3],'sigma':.7,'Canny_thresholds':[60,140]},
              'search_scope':'entire edge image, one fixed scale, no eye-region restriction',
              'templates':results,'interpretation':'Correlation is shape similarity, not probability that a region is an eye.',
              'animation':'Illustrated candidate positions sample the search; the complete response map is computed by matchTemplate.'}
    (OUT/'evidence/shape_matching.json').write_text(json.dumps(evidence,indent=2))

    W,H=1600,800
    PX,PY,PW,PH=245,145,750,500
    HX,HY,HW,HH=1040,200,525,322
    displayed=photo.resize((PW,PH),Image.Resampling.LANCZOS)
    # Show the edge input as an inset, alongside human-readable source photograph.
    edge_preview=Image.fromarray(edges).resize((180,120),Image.Resampling.NEAREST).convert('RGB')

    def frame(name,xy,finished):
        canvas=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(canvas)
        d.text((20,15),'Templates\n(enlarged)',font=font(21,True),fill=INK,spacing=3)
        d.text((PX,20),'Search the photograph’s edge image',font=font(30,True),fill=INK)
        d.text((HX,95),'Similarity at each location',font=font(25,True),fill=INK)
        canvas.paste(displayed,(PX,PY))
        for i,n in enumerate(('square','circle','oval')):
            yy=85+i*190
            d.rounded_rectangle((15,yy-7,220,yy+173),radius=12,
                                fill='#E4F2EF' if n==name else '#F2F4F6')
            thumb=Image.fromarray(templates[n]).resize((118,118),Image.Resampling.NEAREST).convert('RGB')
            canvas.paste(thumb,(55,yy+31))
            d.text((27,yy),n.capitalize(),font=font(23,True),fill=TEAL if n==name else INK)
            d.text((29,yy+147),f"Best score {results[n]['score']:.2f}",font=font(19),fill=INK)
        # Use one common heatmap scale, avoiding misleading per-template rescaling.
        response=responses[name]
        common_max=max(float(v.max()) for v in responses.values())
        heat=np.clip(response,0,common_max)/common_max
        heat=cv2.applyColorMap((heat*255).astype(np.uint8),cv2.COLORMAP_INFERNO)
        heat=cv2.cvtColor(heat,cv2.COLOR_BGR2RGB)
        canvas.paste(Image.fromarray(heat).resize((HW,HH),Image.Resampling.BILINEAR),(HX,HY))
        xx,yy=xy
        col=TEAL if finished else ORANGE
        x1=PX+xx*PW/640;y1=PY+yy*PH/427
        x2=PX+(xx+76)*PW/640;y2=PY+(yy+76)*PH/427
        d.rectangle((x1,y1,x2,y2),outline=col,width=6)
        mx=HX+xx/(response.shape[1]-1)*HW;my=HY+yy/(response.shape[0]-1)*HH
        d.ellipse((mx-7,my-7,mx+7,my+7),outline='white',width=3)
        score=float(response[yy,xx])
        d.text((HX,145),f'{name.capitalize()} template',font=font(28,True),fill=TEAL)
        d.text((HX,540),f"{'Best match' if finished else 'Candidate'}: score {score:.2f}",font=font(27,True),fill=INK)
        d.text((HX,584),'Low ← similarity → high',font=font(21),fill=INK)
        # A compact reference to the processed image prevents confusion about matching RGB pixels.
        canvas.paste(edge_preview,(PX,PH+PY+18))
        d.text((PX+200,PH+PY+30),'Canny edge input',font=font(22),fill=INK)
        d.text((PX+200,PH+PY+70),'A shape match is not proof of an eye.',font=font(23,True),fill=INK)
        return canvas

    frames=[];durations=[]
    # Static export starts with a completed result; slideshow then compares all three.
    frames.append(frame('circle',results['circle']['top_left_xy'],True));durations.append(1700)
    for name in ('square','circle','oval'):
        r=responses[name];rh,rw=r.shape
        candidates=[(int(fx*(rw-1)),int(fy*(rh-1))) for fx,fy in
                    ((.04,.05),(.45,.05),(.90,.05),(.85,.40),(.45,.40),(.05,.70),(.5,.85))]
        for loc in candidates:
            frames.append(frame(name,loc,False));durations.append(420)
        frames.append(frame(name,results[name]['top_left_xy'],True));durations.append(1800)
    frames.append(frame('circle',results['circle']['top_left_xy'],True));durations.append(1800)
    dest=OUT/'shape_matching.gif'
    frames[0].save(dest,save_all=True,append_images=frames[1:],duration=durations,
                   loop=0,optimize=False,disposal=2)
    frames[0].save(OUT/'shape_matching_static.png')
    print('Shape matching:',', '.join(f"{n}={results[n]['score']:.3f} at {tuple(results[n]['top_left_xy'])}" for n in results))
    return evidence


if __name__=='__main__':generate()

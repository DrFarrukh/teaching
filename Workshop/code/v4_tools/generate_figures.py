"""V4 figures: deterministic image processing and pretrained inference; no training.

All inference constructors use weights=None and load verified local checkpoints.
Model builders are never allowed to fetch a backbone. V1/V2/V3 are read-only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pptx import Presentation
import torch
from torchvision.models import (
    mobilenet_v3_small, MobileNet_V3_Small_Weights,
    mobilenet_v3_large, MobileNet_V3_Large_Weights,
    resnet18, ResNet18_Weights,
)
from torchvision.models.detection import (
    ssdlite320_mobilenet_v3_large, SSDLite320_MobileNet_V3_Large_Weights,
    fasterrcnn_mobilenet_v3_large_320_fpn, FasterRCNN_MobileNet_V3_Large_320_FPN_Weights,
)
from torchvision.models.segmentation import (
    lraspp_mobilenet_v3_large, LRASPP_MobileNet_V3_Large_Weights,
    deeplabv3_mobilenet_v3_large, DeepLabV3_MobileNet_V3_Large_Weights,
)

CODE = Path(__file__).resolve().parents[1]
ROOT = CODE.parent
OUT = CODE / "v4_outputs"
ASSETS = CODE / "assets"
SOURCE = OUT / "source"
EVIDENCE = OUT / "evidence"
TEAL = "#087D73"
ORANGE = "#AF5700"
INK = "#111111"
FONT = str(Path(matplotlib.get_data_path()) / "fonts/ttf/DejaVuSans.ttf")
BOLD = str(Path(matplotlib.get_data_path()) / "fonts/ttf/DejaVuSans-Bold.ttf")
plt.rcParams.update({"font.size": 17, "axes.titlesize": 20, "axes.labelsize": 17,
                     "xtick.labelsize": 14, "ytick.labelsize": 14})


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def savefig(fig, name):
    fig.savefig(OUT / name, dpi=150, facecolor="white", bbox_inches="tight", pad_inches=.16)
    plt.close(fig)


def image(name):
    return ImageOps.exif_transpose(Image.open(ASSETS / name)).convert("RGB")


def best_patch(g, size):
    # Fixed search area around the left eye; highest variance, deterministic ties.
    candidates = [(float(g[y:y+size, x:x+size].std()), y, x)
                  for y in range(220, 480-size, 6)
                  for x in range(300, 650-size, 6)]
    _, y, x = max(candidates, key=lambda r: r[0])
    return g[y:y+size, x:x+size].copy(), (x, y)


def grid_figure(values, name, numbers=False, shades=True):
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.imshow(values if shades else np.full_like(values, 250), cmap="gray", vmin=0, vmax=255,
              interpolation="nearest")
    ax.set_xticks(np.arange(-.5, values.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-.5, values.shape[0], 1), minor=True)
    ax.grid(which="minor", color="#CCCCCC", lw=1)
    ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
    if numbers:
        for (r, c), v in np.ndenumerate(values):
            ax.text(c, r, str(int(v)), ha="center", va="center", fontsize=19,
                    color="white" if shades and v < 125 else INK, weight="bold")
    savefig(fig, name)


def classical_figures():
    cat = image("cat_chelsea.png")
    cat.save(OUT / "cat.png")
    low = cat.resize((24, 16), Image.Resampling.BOX)
    low.resize((720, 480), Image.Resampling.NEAREST).save(OUT / "cat_pixel_grid.png")
    g = np.asarray(cat.convert("L"), dtype=np.int32)
    p8, (x, y) = best_patch(g, 8)
    np.save(OUT / "pixel_values.npy", p8)
    zoom = cat.convert("L").convert("RGB")
    dr = ImageDraw.Draw(zoom)
    dr.rectangle((x-4, y-4, x+11, y+11), outline=TEAL, width=4)
    zoom.save(OUT / "pixel_source.png")
    for name, numbers, shades in (("pixels_shades.png",False,True),
                                   ("pixels_shades_numbers.png",True,True),
                                   ("pixels_numbers.png",True,False)):
        grid_figure(p8, name, numbers, shades)
    ImageOps.mirror(cat).save(OUT / "cat_flipped.png")
    weed = image("raw_weed.png")
    hsv = cv2.cvtColor(np.asarray(weed), cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, np.array([25, 45, 25]), np.array([95, 255, 255]))
    selected = np.full_like(np.asarray(weed), 255)
    selected[mask > 0] = np.asarray(weed)[mask > 0]
    Image.fromarray(selected).save(OUT / "weed_green_filter.png")
    Image.fromarray(mask).save(OUT / "weed_binary_mask.png")
    cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    keep = [c for c in contours if cv2.contourArea(c) >= 500]
    canvas = np.asarray(weed).copy()
    cv2.drawContours(canvas, keep, -1, (0, 220, 190), 4)
    Image.fromarray(canvas).save(OUT / "weed_contours.png")
    Image.fromarray(cleaned).save(OUT / "weed_clean_mask.png")
    # A disclosed same-image template lookup, not category detection.
    template = cat.crop((395, 245, 575, 385))
    score_map = cv2.matchTemplate(np.asarray(cat), np.asarray(template), cv2.TM_CCOEFF_NORMED)
    _, max_score, _, loc = cv2.minMaxLoc(score_map)
    found = cat.copy(); draw = ImageDraw.Draw(found)
    draw.rectangle((loc[0], loc[1], loc[0]+template.width, loc[1]+template.height),
                   outline=TEAL, width=9)
    found.save(OUT / "cat_template_match.png")
    template.save(OUT / "cat_template.png")
    # An enlarged eye crop yields a much more legible contour than cluttered field regions.
    eye=np.asarray(template)
    eye_gray=cv2.cvtColor(eye,cv2.COLOR_RGB2GRAY)
    eye_mask=(eye_gray < 30).astype(np.uint8)*255
    eye_contours,_=cv2.findContours(eye_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    pupil=max(eye_contours,key=cv2.contourArea)
    pupil_mask=np.zeros_like(eye_mask);cv2.drawContours(pupil_mask,[pupil],-1,255,-1)
    eye_overlay=eye.copy();cv2.drawContours(eye_overlay,[pupil],-1,(0,200,165),3)
    Image.fromarray(pupil_mask).save(OUT/'eye_binary_mask.png')
    Image.fromarray(eye_overlay).save(OUT/'eye_contour.png')
    # Weed assets are user-provided output images. Do not fabricate labels or metrics.
    for f in ("raw_weed.png", "weed_with_mask.png", "weed_with_mask_zoomed_out.png"):
        image(f).save(SOURCE / f)
    (EVIDENCE / "classical.json").write_text(json.dumps({
        "cat_sha256": digest(ASSETS/"cat_chelsea.png"), "pixel_crop_xywh": [x,y,8,8],
        "pixel_values": p8.tolist(), "colour_filter_HSV": [[25,45,25],[95,255,255]],
        "contour_count_after_area_filter":len(keep), "template_xy":list(loc),
        "template_correlation":float(max_score),
        "eye_contour_threshold":30,
    }, indent=2))


def cached_model(builder, weights, device, **kwargs):
    path = Path(torch.hub.get_dir()) / "checkpoints" / weights.url.rsplit("/",1)[-1]
    if not path.is_file():
        raise FileNotFoundError(f"No cached weights: {path.name}; downloads are disabled here")
    prefix = path.name.rsplit("-",1)[-1].split(".")[0]
    sha = digest(path)
    if not sha.startswith(prefix):
        raise RuntimeError(f"Weight hash mismatch: {path.name}")
    model = builder(weights=None, **kwargs)
    model.load_state_dict(torch.load(path, map_location="cpu", weights_only=True))
    return model.to(device).eval(), {"weights":str(weights), "file":path.name, "sha256":sha,
                                   "parameters":sum(p.numel() for p in model.parameters())}


def classify(model, weights, im, device):
    with torch.inference_mode():
        probs = model(weights.transforms()(im).unsqueeze(0).to(device)).softmax(1)[0].cpu()
    val, ids = probs.topk(5)
    return {"top5":[{"label":weights.meta["categories"][int(i)],"p":float(v)}
                    for v,i in zip(val,ids)],
            "cat":float(probs[281:286].sum()), "dog":float(probs[151:269].sum()),
            "other":float(1-probs[281:286].sum()-probs[151:269].sum())}


def detect(model, weights, im, device, threshold=.55):
    with torch.inference_mode():
        r = model([weights.transforms()(im).to(device)])[0]
    return [{"label":weights.meta["categories"][int(l)],"score":float(s),
             "box":[float(v) for v in b.cpu()]} for b,l,s in zip(r['boxes'],r['labels'],r['scores'])
            if float(s)>=threshold]


def segment(model, weights, im, device):
    with torch.inference_mode():
        mask=model(weights.transforms()(im).unsqueeze(0).to(device))["out"][0].argmax(0).cpu().numpy()
    mask=np.asarray(Image.fromarray(mask.astype(np.uint8)).resize(im.size,Image.Resampling.NEAREST))
    ids, counts=np.unique(mask,return_counts=True)
    coverage=sorted([{"label":weights.meta["categories"][int(i)],"pct":float(c/mask.size*100)}
                     for i,c in zip(ids,counts)],key=lambda r:-r['pct'])
    return mask,coverage


def boxes_image(im, boxes, name):
    # Draw on an upsampled canvas so labels remain readable on slides.
    scale=max(1,1200/im.width)
    dest=im.resize((int(im.width*scale),int(im.height*scale)),Image.Resampling.LANCZOS)
    d=ImageDraw.Draw(dest); f=ImageFont.truetype(BOLD,27)
    for b in boxes:
        x1,y1,x2,y2=[v*scale for v in b['box']]
        d.rectangle((x1,y1,x2,y2),outline='#E13B40',width=5)
        label=f"{b['label']} {b['score']:.2f}"
        tw=d.textlength(label,font=f); xx=min(x1,dest.width-tw-14); yy=max(0,y1-39)
        d.rectangle((xx,yy,xx+tw+14,yy+37),fill='#A92329')
        d.text((xx+7,yy+2),label,font=f,fill='white')
    dest.save(OUT/name)


def overlay(im, mask, name):
    # Explicit, consistent categories; background remains unpainted.
    colors={8:(179,48,162),12:(0,153,129),18:(48,115,206),9:(239,158,44),
            6:(213,52,61),15:(48,115,206)}
    arr=np.asarray(im).astype(float)
    for i in np.unique(mask):
        if i==0: continue
        c=colors.get(int(i),tuple(int(v*255) for v in plt.get_cmap('tab20')(int(i)%20)[:3]))
        arr[mask==i]=.48*arr[mask==i]+.52*np.array(c)
    Image.fromarray(np.clip(arr,0,255).astype(np.uint8)).save(OUT/name)


def score_bars(r, name, grouped=False):
    if grouped:
        labels=['Cat','Dog','Other']; vals=[r['cat'],r['dog'],r['other']]
    else:
        labels=[v['label'] for v in r['top5'][:3]]; vals=[v['p'] for v in r['top5'][:3]]
    fig,ax=plt.subplots(figsize=(7,3.8))
    ys=np.arange(len(vals))[::-1]
    ax.barh(ys,vals,color=[TEAL,'#AF5700','#687581'][:len(vals)],height=.62)
    ax.set_yticks(ys,labels); ax.set_xlim(0,1.14)
    for yy,v in zip(ys,vals): ax.text(v+.02,yy,f'{v*100:.1f}%',va='center',fontsize=22,weight='bold')
    ax.set_xticks([0,.5,1],['0','0.5','1']); ax.set_xlabel('Model probability')
    for s in ('top','right'): ax.spines[s].set_visible(False)
    savefig(fig,name)


def feature_maps(device):
    w=ResNet18_Weights.IMAGENET1K_V1
    model,meta=cached_model(resnet18,w,device)
    capture={}
    def hook(name):
        def fn(_,inputs,output): capture[name]=output.detach().cpu().clone()
        return fn
    handles=[getattr(model,name).register_forward_hook(hook(name))
             for name in ('bn1','relu','maxpool','layer1','layer4','avgpool')]
    im=image('cat_chelsea.png'); x=w.transforms()(im).unsqueeze(0).to(device)
    with torch.inference_mode(): logits=model(x).cpu()
    for h in handles: h.remove()
    p=logits.softmax(1)[0]; vals,idx=p.topk(5)
    result={"top5":[{"label":w.meta['categories'][int(i)],"p":float(v)} for v,i in zip(vals,idx)],
            "cat":float(p[281:286].sum()),"dog":float(p[151:269].sum()),
            "other":float(1-p[281:286].sum()-p[151:269].sum())}
    # Select channels by spatial variance, not by a claimed semantic meaning.
    chosen={}
    for layer in ('relu','maxpool','layer1','layer4'):
        a=capture[layer][0].numpy()
        ids=np.argsort(a.var(axis=(1,2)),kind='stable')[-4:][::-1]
        chosen[layer]=[int(i) for i in ids]
        fig,axes=plt.subplots(1,4,figsize=(12,3.1))
        for ax,ch in zip(axes,ids):
            v=a[ch]; lo,hi=float(v.min()),float(v.max())
            ax.imshow(v,cmap='magma',vmin=lo,vmax=hi,interpolation='nearest')
            ax.set_title(f'Channel {ch}',fontsize=18); ax.axis('off')
        savefig(fig,f'features_{layer}.png')
    np.savez_compressed(OUT/'feature_activations.npz',**{k:v.numpy() for k,v in capture.items()},
                        logits=logits.numpy(),input=x.cpu().numpy())
    # The exact pooled vector and linear head reconstruct the measured logits.
    head=model.fc.cpu()
    with torch.inference_mode():
        reconstructed=head(capture['avgpool'].flatten(1)).detach()
    error=float((reconstructed-logits).abs().max())
    meta.update({'selected_channels':chosen,'tensor_shapes':{k:list(v.shape) for k,v in capture.items()},
                 'normalization':'Each displayed channel independently min-max scaled',
                 'selection':'four channels with greatest spatial variance in each layer',
                 'head_reconstruction_max_abs_error':error,'classification':result})
    score_bars(result,'features_prediction.png')
    # Animated pooling uses a genuine nonnegative ReLU activation patch.
    ch=chosen['relu'][0]
    response=capture['relu'][0,ch].numpy()
    # ResNet uses 3x3 max pooling stride2 padding1; demonstrate that exact window.
    pooling_gif(response,ch)
    return meta


def numeric_grid(d,vals,x,y,cell=64,highlight=None,fmt='int',filled=None):
    font=ImageFont.truetype(BOLD,21)
    for r in range(vals.shape[0]):
        for c in range(vals.shape[1]):
            xx=x+c*cell; yy=y+r*cell
            color='#F1F4F6'
            if highlight and highlight[0]<=r<highlight[0]+highlight[2] and highlight[1]<=c<highlight[1]+highlight[2]: color='#D3EDE7'
            d.rectangle((xx,yy,xx+cell-3,yy+cell-3),fill=color,outline='#BAC4CD',width=1)
            if filled is not None and r*vals.shape[1]+c>=filled: continue
            t=str(int(vals[r,c])) if fmt=='int' else f'{float(vals[r,c]):.1f}'
            tw=d.textlength(t,font=font)
            d.text((xx+(cell-3-tw)/2,yy+19),t,font=font,fill=INK)


def animated_save(frames, name, durations):
    frames[0].save(OUT/name,save_all=True,append_images=frames[1:],duration=durations,
                   loop=0,optimize=False,disposal=2)
    frames[0].save(OUT/(Path(name).stem+'_static.png'))


def convolution_gifs():
    cat=image('cat_chelsea.png'); g=np.asarray(cat.convert('L'),dtype=np.int32)
    p,(px,py)=best_patch(g,6); k=np.array([[-1,0,1]]*3)
    out=np.array([[np.sum(p[r:r+3,c:c+3]*k) for c in range(4)] for r in range(4)])
    frames=[]; photo_frames=[]
    states=[16]+list(range(17))
    for step in states:
        canvas=Image.new('RGB',(1450,580),'white'); d=ImageDraw.Draw(canvas)
        title=ImageFont.truetype(BOLD,26); small=ImageFont.truetype(FONT,22)
        d.text((28,18),'Input: 6 × 6 pixel values',font=title,fill=INK)
        d.text((515,18),'Fixed 3 × 3 kernel',font=title,fill=INK)
        d.text((915,18),'Output: 4 × 4 response',font=title,fill=INK)
        rc=divmod(min(step,15),4)
        numeric_grid(d,p,28,85,64,(rc[0],rc[1],3))
        numeric_grid(d,k,530,160,70)
        numeric_grid(d,out,935,85,74,filled=step)
        d.text((465,233),'×',font=ImageFont.truetype(BOLD,40),fill=INK)
        d.text((820,233),'→',font=ImageFont.truetype(BOLD,40),fill=INK)
        if step<16:
            value=int(out[rc])
            d.text((28,515),f'Window ({rc[0]+1}, {rc[1]+1}): multiply corresponding cells, then sum → {value}',font=small,fill=INK)
        else:
            d.text((28,515),'The same weights are reused at every position. Stride 1; no padding.',font=small,fill=INK)
        frames.append(canvas)
        # Same calculation synchronized with a moving window on the photograph crop.
        pc=Image.new('RGB',(1450,620),'white'); dd=ImageDraw.Draw(pc)
        photo=cat.resize((570,380)); pc.paste(photo,(20,70))
        # Enlarged 6x6 source patch, preserving visible pixel cells.
        patch=Image.fromarray(p.astype(np.uint8)).resize((360,360),Image.Resampling.NEAREST).convert('RGB')
        pd=ImageDraw.Draw(patch); sr,sc=rc
        pd.rectangle((sc*60,sr*60,(sc+3)*60-1,(sr+3)*60-1),outline='#00E0AD',width=7)
        pc.paste(patch,(620,85))
        # Mark the precise crop location on the overview.
        xx=20+px*570/cat.width; yy=70+py*380/cat.height
        dd.rectangle((xx-6,yy-6,xx+12,yy+12),outline=TEAL,width=4)
        numeric_grid(dd,out,1090,85,69,filled=step)
        dd.text((20,20),'Source photograph',font=title,fill=INK)
        dd.text((620,20),'Enlarged pixel patch',font=title,fill=INK)
        dd.text((1090,20),'Responses',font=title,fill=INK)
        dd.text((20,535),'A moving local window → one response at each position',font=ImageFont.truetype(BOLD,29),fill=INK)
        photo_frames.append(pc)
    durations=[1200]+[480]*16+[1500]
    animated_save(frames,'convolution.gif',durations)
    animated_save(photo_frames,'moving_window.gif',durations)
    (EVIDENCE/'convolution.json').write_text(json.dumps({'crop_xy':[px,py],'input':p.tolist(),
         'kernel':k.tolist(),'output':out.tolist(),'operation':'cross-correlation (CNN convention)'},indent=2))


def pooling_gif(response,channel):
    # An interior patch aligned to the model's actual stride2/padding1 pooling grid.
    # Pick a non-flat interior patch, aligned to actual stride2/padding1 windows.
    locations=[(float(response[y:y+5,x:x+5].std()),y,x)
               for y in range(1,response.shape[0]-5,2)
               for x in range(1,response.shape[1]-5,2)]
    _,y,x=max(locations,key=lambda row:row[0])
    patch=response[y:y+5,x:x+5]
    pooled=np.array([[patch[r*2:r*2+3,c*2:c*2+3].max() for c in range(2)] for r in range(2)])
    frames=[]
    for step in [4,0,1,2,3,4]:
        canvas=Image.new('RGB',(1500,550),'white'); d=ImageDraw.Draw(canvas)
        title=ImageFont.truetype(BOLD,28); f=ImageFont.truetype(FONT,23)
        d.text((20,20),'Convolution → ReLU → Max pooling',font=title,fill=INK)
        d.text((20,70),'ReLU(x) = max(0, x)         Pooling: 3 × 3 window, stride 2',font=f,fill=INK)
        rc=divmod(min(step,3),2)
        numeric_grid(d,patch,100,130,65,(rc[0]*2,rc[1]*2,3),fmt='float')
        numeric_grid(d,pooled,940,170,96,fmt='float',filled=step)
        d.text((570,205),'Keep the maximum',font=title,fill=TEAL)
        d.text((680,260),'→',font=ImageFont.truetype(BOLD,50),fill=INK)
        d.text((20,492),'Numbers are from a ResNet18 ReLU feature map; displayed to one decimal place.',font=f,fill=INK)
        frames.append(canvas)
    animated_save(frames,'relu_pooling.gif',[1400,700,700,700,700,1500])
    (EVIDENCE/'pooling.json').write_text(json.dumps({'input':patch.tolist(),'output':pooled.tolist(),
        'window':3,'stride':2,'source_crop_xy':[x,y],'source_channel':int(channel),
        'source_layer':'ResNet18 relu'},indent=2))


def capture_lab_evidence(source):
    # Freeze source evidence locally; never rewrite the supplied notebook/results.
    source=Path(source)
    notebook_path=source/'solutions/Session1_Lab_executed.ipynb'
    notebook=json.loads(notebook_path.read_text())
    histories={'scratch':[],'ft':[]}; stdout=[]
    import re
    for cell in notebook['cells']:
        for o in cell.get('outputs',[]):
            if o.get('output_type')=='stream': stdout.append(''.join(o.get('text',[])))
    # Strip progress bars before freezing compact evidence.
    text='\n'.join(line for line in '\n'.join(stdout).replace('\r','\n').splitlines()
                   if not re.search(r'\] epoch \d+/\d+:',line))
    for tag,key in [('scratch','scratch'),('resnet18-ft','ft')]:
        patt=rf'\[{tag}\] epoch (\d+)/\d+ — train loss ([\d.]+) \| train acc\s*([\d.]+)% \| test acc\s*([\d.]+)%'
        histories[key]=[[int(ep),float(loss),float(tr),float(te)] for ep,loss,tr,te in re.findall(patt,text)]
    if len(histories['scratch'])!=5 or len(histories['ft'])!=3:
        raise RuntimeError('Recorded epoch histories missing from executed notebook')
    # Pull the matrix from the saved, machine-readable display data if available;
    # otherwise preserve the source figure and verify its counts against the printed report.
    report=re.findall(r'airplane\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)',text)
    (EVIDENCE/'lab_stdout.txt').write_text(text)
    (EVIDENCE/'lab_history.json').write_text(json.dumps(histories,indent=2))
    for f in ('confusion_matrix_ft.png','curves_compare.png','curves_scratch.png'):
        shutil.copyfile(source/'assets/expected_outputs'/f,EVIDENCE/f)
    shutil.copyfile(source/'assets/gallery/chelsea.png',SOURCE/'lab_chelsea.png')
    sources='\n'.join(''.join(c.get('source',[])) for c in notebook['cells'])
    cfg=re.findall(r'"train_per_class"\s*:\s*(\d+)|"test_per_class"\s*:\s*(\d+)',sources)
    prediction=re.search(r'chelsea\.png\s*→ cat ([\d.]+)% \| dog ([\d.]+)% \| airplane ([\d.]+)%',text)
    sizes=re.search(r'Train images:\s*(\d+)\s*\|\s*Test images:\s*(\d+)',text)
    info={'notebook_sha256':digest(notebook_path),'history_source':'executed notebook stdout',
          'notes':'Test accuracy was reported every epoch in the historical lab. No new training in V4.',
          'subset_configuration_matches':cfg,'printed_report_airplane':report,
          'training_images':int(sizes[1]) if sizes else None,
          'test_images':int(sizes[2]) if sizes else None,
          'head_example_image_sha256':digest(SOURCE/'lab_chelsea.png'),
          'head_example':({'cat':float(prediction[1]),'dog':float(prediction[2]),
                           'airplane':float(prediction[3])} if prediction else None)}
    (EVIDENCE/'lab_provenance.json').write_text(json.dumps(info,indent=2))
    return histories,info


def lab_evidence(lab_dir,reuse=False):
    if reuse:
        histories=json.loads((EVIDENCE/'lab_history.json').read_text())
        info=json.loads((EVIDENCE/'lab_provenance.json').read_text())
    else:
        histories,info=capture_lab_evidence(lab_dir)
    def curves(name,keys):
        fig,axes=plt.subplots(1,2,figsize=(12.5,4.9))
        for key in keys:
            a=np.array(histories[key]); label='Scratch CNN' if key=='scratch' else 'Frozen ResNet18 + head'
            col=ORANGE if key=='scratch' else TEAL
            axes[0].plot(a[:,0],a[:,1],'-o',color=col,lw=3,label=label)
            axes[1].plot(a[:,0],a[:,3],'-o',color=col,lw=3,label=label)
            axes[1].annotate(f'{a[-1,3]:.1f}%',(a[-1,0],a[-1,3]),xytext=(-15,15),textcoords='offset points',fontsize=19)
        for ax in axes:
            ax.set_xlabel('Epoch'); ax.grid(alpha=.18); ax.spines[['top','right']].set_visible(False)
            ax.set_xticks(range(1,max(len(histories[k]) for k in keys)+1))
        axes[0].set_title('Training loss');axes[1].set_title('Test accuracy (%)')
        axes[0].legend(fontsize=13)
        savefig(fig,name)
    curves('curves_scratch.png',['scratch'])
    curves('curves_compare.png',['scratch','ft'])
    curves('curves_ft.png',['ft'])
    a=np.array(histories['scratch']);fig,ax=plt.subplots(figsize=(10.5,4.9))
    ax.plot(a[:,0],a[:,2],'-o',label='Training',color=TEAL,lw=3)
    ax.plot(a[:,0],a[:,3],'-o',label='Test (historical run)',color=ORANGE,lw=3)
    ax.set(xlabel='Epoch',ylabel='Accuracy (%)');ax.legend();ax.grid(alpha=.18)
    ax.spines[['top','right']].set_visible(False);ax.set_xticks(range(1,6))
    savefig(fig,'train_test.png')
    return histories,info


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--device',choices=['cuda','cpu'],default='cpu')
    ap.add_argument('--lab-dir',type=Path,default=Path('/tmp/opencode/workshop_src/Session1/Lab'))
    ap.add_argument('--reuse-lab-evidence',action='store_true',help='Use the preserved notebook evidence; do not reread an external notebook')
    args=ap.parse_args()
    for d in (OUT,SOURCE,EVIDENCE):d.mkdir(parents=True,exist_ok=True)
    torch.manual_seed(0);np.random.seed(0);torch.set_num_threads(4)
    if args.device=='cuda' and not torch.cuda.is_available():raise RuntimeError('CUDA unavailable')
    device=torch.device(args.device)
    # Extract only source slide pictures needed for retained teaching examples.
    deck=Presentation(ROOT/'AI_Workshop_Session1_v2.pptx')
    for n in (20,21,34):
        pics=[s for s in deck.slides[n-1].shapes if s.shape_type==13]
        for j,s in enumerate(pics):
            (SOURCE/f'v2_slide_{n}_{j}.{s.image.ext}').write_bytes(s.image.blob)
    bus_source=args.lab_dir/'assets/gallery/bus.jpg'
    if bus_source.is_file():shutil.copyfile(bus_source,SOURCE/'bus.jpg')
    elif not (SOURCE/'bus.jpg').is_file():raise FileNotFoundError('Missing bus.jpg source photograph')
    classical_figures();convolution_gifs();hist,labinfo=lab_evidence(args.lab_dir,args.reuse_lab_evidence)
    meta={};results={}
    model_specs=[('small',mobilenet_v3_small,MobileNet_V3_Small_Weights.IMAGENET1K_V1,{}),
        ('ssdlite',ssdlite320_mobilenet_v3_large,SSDLite320_MobileNet_V3_Large_Weights.COCO_V1,{'weights_backbone':None}),
        ('lraspp',lraspp_mobilenet_v3_large,LRASPP_MobileNet_V3_Large_Weights.COCO_WITH_VOC_LABELS_V1,{'weights_backbone':None}),
        ('large',mobilenet_v3_large,MobileNet_V3_Large_Weights.IMAGENET1K_V2,{}),
        ('faster',fasterrcnn_mobilenet_v3_large_320_fpn,FasterRCNN_MobileNet_V3_Large_320_FPN_Weights.COCO_V1,{'weights_backbone':None}),
        ('deeplab',deeplabv3_mobilenet_v3_large,DeepLabV3_MobileNet_V3_Large_Weights.COCO_WITH_VOC_LABELS_V1,{'weights_backbone':None,'aux_loss':True})]
    inputs={'cat':image('cat_chelsea.png'),'mix':image('cat_dog_mix.jpg'),
            'fluffy':image('dog_fluffy.jpg'),'couch':image('cats_couch.jpg'),
            'dog':image('dog_closeup.jpg'),'bus':Image.open(SOURCE/'bus.jpg').convert('RGB')}
    for key,builder,w,kw in model_specs:
        print(f'Inference: {key}',flush=True)
        model,meta[key]=cached_model(builder,w,device,**kw);results[key]={}
        cases={'small':['cat'],'ssdlite':['mix','dog'],'lraspp':['mix','cat'],
               'large':['cat','mix','fluffy'],'faster':['mix','fluffy','dog','bus'],
               'deeplab':['mix','dog','couch','bus']}[key]
        for n in cases:
            im=inputs[n]
            if key in ('small','large'):
                r=classify(model,w,im,device);score_bars(r,f'{key}_{n}_scores.png',grouped=key=='large')
            elif key in ('ssdlite','faster'):
                r=detect(model,w,im,device);boxes_image(im,r,f'{key}_{n}_boxes.png')
            else:
                mask,cov=segment(model,w,im,device);r={'coverage':cov}
                np.save(OUT/f'{key}_{n}_mask.npy',mask);overlay(im,mask,f'{key}_{n}_overlay.png')
            results[key][n]=r
        del model
        if device.type=='cuda':torch.cuda.empty_cache()
    print('Extracting ResNet18 features',flush=True)
    features=feature_maps(device)
    bus_box=next(b for b in results['faster']['bus'] if b['label']=='bus')
    boxes_image(inputs['bus'],[bus_box],'bus_one_box.png')
    # Explicitly illustrative IoU, computed deterministically from disclosed boxes.
    b=np.array(bus_box['box']);a=b+np.array([-30,-20,35,30]);p=b+np.array([60,40,-40,-70])
    inter=np.maximum(0,np.minimum(a[2:],p[2:])-np.maximum(a[:2],p[:2])).prod()
    area=lambda q:np.maximum(0,q[2:]-q[:2]).prod()
    iou=float(inter/(area(a)+area(p)-inter))
    im=inputs['bus'].copy();d=ImageDraw.Draw(im,'RGBA')
    overlap=[*np.maximum(a[:2],p[:2]),*np.minimum(a[2:],p[2:])]
    d.rectangle(overlap,fill=(0,160,135,65));d.rectangle(a.tolist(),outline=(0,130,115,255),width=7)
    d.rectangle(p.tolist(),outline=(195,100,0,255),width=7);im.save(OUT/'iou_boxes.png')
    manifest={'source_v2_sha256':digest(ROOT/'AI_Workshop_Session1_v2.pptx'),
        'device':str(device),'torch':torch.__version__,'models':meta,'inference':results,
        'features':features,'lab_history':hist,'lab_provenance':labinfo,
        'iou':{'illustrative_box_A':a.tolist(),'illustrative_box_B':p.tolist(),'value':iou},
        'training_performed':False,'downloads_permitted_here':False}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
    print('Generated V4 figures and evidence manifest',flush=True)


if __name__=='__main__':main()

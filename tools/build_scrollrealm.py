import os, json, math, shutil, textwrap, zipfile, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path('/mnt/data/scrollrealm-github-pages')
if ROOT.exists():
    shutil.rmtree(ROOT)
(ROOT/'assets'/'css').mkdir(parents=True)
(ROOT/'assets'/'js').mkdir(parents=True)
(ROOT/'assets'/'images').mkdir(parents=True)
(ROOT/'assets'/'icons').mkdir(parents=True)
(ROOT/'data').mkdir(parents=True)
(ROOT/'tools').mkdir(parents=True)

DATE = '2026-05-28'
DOMAIN = 'https://scrollrealm.com'

# ---------- Asset generation ----------
def font(size, bold=False):
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()

def save_webp(img, name, quality=82):
    img.save(ROOT/'assets'/'images'/name, 'WEBP', quality=quality, method=6)

def draw_stars(draw, w, h, count=180, seed=1):
    rnd = random.Random(seed)
    for _ in range(count):
        x = rnd.randrange(w); y = rnd.randrange(h)
        a = rnd.randrange(30, 150)
        r = rnd.choice([1,1,1,2])
        draw.ellipse((x-r,y-r,x+r,y+r), fill=(235,210,140,a))

def gradient_bg(w, h, top, bottom):
    img = Image.new('RGB', (w,h), top)
    px = img.load()
    for y in range(h):
        t = y/(h-1)
        col = tuple(int(top[i]*(1-t)+bottom[i]*t) for i in range(3))
        for x in range(w):
            px[x,y] = col
    return img

def draw_mountains(draw, w, h, base_y, color, layers=1, seed=0):
    rnd = random.Random(seed)
    step = w//8
    pts = [(0,h)]
    x=0
    while x <= w:
        peak_y = base_y - rnd.randint(40, 160)
        pts.append((x+rnd.randint(-20,20), peak_y))
        x += step
        pts.append((min(x,w), base_y + rnd.randint(-20, 40)))
    pts += [(w,h)]
    draw.polygon(pts, fill=color)

def add_noise(img, opacity=18, seed=0):
    rnd = random.Random(seed)
    noise = Image.new('RGBA', img.size, (0,0,0,0))
    d = ImageDraw.Draw(noise)
    w,h = img.size
    for _ in range((w*h)//900):
        x = rnd.randrange(w); y = rnd.randrange(h); v = rnd.randrange(255)
        d.point((x,y), fill=(v,v,v,opacity))
    return Image.alpha_composite(img.convert('RGBA'), noise).convert('RGB')

def hero_bg():
    w,h = 1800,900
    img = gradient_bg(w,h,(10,16,23),(4,8,12)).convert('RGBA')
    d = ImageDraw.Draw(img, 'RGBA')
    draw_stars(d,w,h,250,seed=3)
    # aurora glows
    for cx,cy,col in [(1350,240,(110,70,180,55)),(400,220,(190,120,45,38)),(900,190,(60,120,140,32))]:
        for r in range(380,0,-8):
            a = max(0, col[3]*(r/380)**2)
            d.ellipse((cx-r,cy-r,cx+r,cy+r), fill=(col[0],col[1],col[2],int(a)))
    # map lines
    rnd=random.Random(6)
    for _ in range(42):
        pts=[]
        x=rnd.randrange(w); y=rnd.randrange(120,h-80)
        for i in range(rnd.randint(3,7)):
            pts.append((x,y)); x+=rnd.randint(-90,120); y+=rnd.randint(-45,45)
        d.line(pts, fill=(175,128,55,28), width=2)
    # distant mountains/layers
    draw_mountains(d,w,h,650,(22,34,44,190),seed=1)
    draw_mountains(d,w,h,710,(13,23,32,230),seed=4)
    draw_mountains(d,w,h,780,(8,14,20,255),seed=7)
    # skyline/castles
    for x in [720,760,810,860,915,980,1040]:
        height=random.Random(x).randint(100,230)
        d.rectangle((x,650-height,x+random.Random(x+1).randint(18,42),790), fill=(18,24,28,220))
        d.polygon([(x-8,650-height),(x+18,610-height),(x+42,650-height)], fill=(24,28,32,230))
    # arcane circle right
    cx,cy=1440,310
    for r,a in [(230,52),(165,38),(95,30)]:
        d.ellipse((cx-r,cy-r,cx+r,cy+r), outline=(125,80,205,a), width=4)
    for ang in range(0,360,24):
        x1=cx+math.cos(math.radians(ang))*95; y1=cy+math.sin(math.radians(ang))*95
        x2=cx+math.cos(math.radians(ang))*230; y2=cy+math.sin(math.radians(ang))*230
        d.line((x1,y1,x2,y2), fill=(125,80,205,34), width=2)
    # vignette
    vignette = Image.new('L',(w,h),0)
    vd=ImageDraw.Draw(vignette)
    for r in range(max(w,h),0,-25):
        shade=int(255*(1-r/max(w,h))**2)
        vd.ellipse((w/2-r,h/2-r,w/2+r,h/2+r), fill=shade)
    img = Image.composite(Image.new('RGBA',(w,h),(0,0,0,150)), img, vignette)
    img = add_noise(img.convert('RGB'),18,9)
    save_webp(img,'hero-bg.webp',86)

def draw_card(draw, xy, title, colors, rot=0, seed=0):
    x,y,w,h = xy
    card = Image.new('RGBA',(w,h),(0,0,0,0))
    cd=ImageDraw.Draw(card,'RGBA')
    cd.rounded_rectangle((0,0,w-1,h-1), radius=22, fill=(18,16,13,255), outline=(180,126,49,255), width=5)
    cd.rounded_rectangle((14,14,w-15,h-15), radius=14, fill=(8,10,13,255), outline=(87,63,32,255), width=2)
    # art box
    for yy in range(26,int(h*.62)):
        t=(yy-26)/(h*.62-26)
        col=tuple(int(colors[0][i]*(1-t)+colors[1][i]*t) for i in range(3))+(255,)
        cd.line((24,yy,w-24,yy), fill=col)
    rnd=random.Random(seed)
    for _ in range(28):
        xx=rnd.randint(30,w-30); yy=rnd.randint(35,int(h*.58)); rr=rnd.randint(2,6)
        cd.ellipse((xx-rr,yy-rr,xx+rr,yy+rr), fill=(240,210,140,rnd.randint(30,120)))
    # silhouette/mountain
    pts=[(24,int(h*.62))]
    for i in range(9):
        xx=24+i*(w-48)//8
        yy=int(h*.52)-rnd.randint(0,70)
        pts.append((xx,yy))
    pts += [(w-24,int(h*.62))]
    cd.polygon(pts, fill=(6,8,12,190))
    cd.rectangle((24,int(h*.66),w-24,h-60), fill=(238,222,181,215), outline=(120,80,30,255))
    cd.text((w//2, h-44), title.upper(), anchor='mm', fill=(245,210,135,255), font=font(24, True))
    cd.ellipse((16,16,58,58), fill=(25,20,12,255), outline=(201,153,72,255), width=3)
    cd.text((37,37), str((seed%7)+1), anchor='mm', fill=(240,220,160,255), font=font(26, True))
    if rot != 0:
        card = card.rotate(rot, expand=True, resample=Image.Resampling.BICUBIC)
    return card

def card_stack():
    w,h=850,640
    img=Image.new('RGBA',(w,h),(0,0,0,0))
    cards=[('Draconic Revenant',((130,30,18),(255,140,34)),-10,1),('Lumina Starseer',((20,80,120),(150,220,255)),2,2),('Ironclad Sentinel',((42,45,55),(165,125,75)),12,3)]
    positions=[(40,84,238,350),(275,50,238,350),(500,98,238,350)]
    for xy,(title,cols,rot,seed) in zip(positions,cards):
        c=draw_card(ImageDraw.Draw(Image.new('RGBA',(1,1))),(0,0,xy[2],xy[3]),title,cols,rot,seed)
        img.alpha_composite(c,(xy[0],xy[1]))
    # glow
    glow=Image.new('RGBA',(w,h),(0,0,0,0)); gd=ImageDraw.Draw(glow,'RGBA')
    gd.ellipse((60,130,790,620), fill=(190,125,50,42))
    glow=glow.filter(ImageFilter.GaussianBlur(34))
    out=Image.alpha_composite(glow,img)
    save_webp(out.convert('RGB'),'card-stack.webp',84)

def silhouettes():
    w,h=760,650
    img=Image.new('RGBA',(w,h),(0,0,0,0))
    d=ImageDraw.Draw(img,'RGBA')
    # mage glow circle
    cx,cy=585,250
    for r,a in [(210,50),(150,40),(85,30)]:
        d.ellipse((cx-r,cy-r,cx+r,cy+r), outline=(140,85,220,a), width=5)
    for ang in range(0,360,30):
        d.line((cx,cy,cx+math.cos(math.radians(ang))*210,cy+math.sin(math.radians(ang))*210), fill=(140,85,220,22), width=2)
    # warrior silhouette
    d.ellipse((165,115,255,210), fill=(42,33,28,255), outline=(186,140,78,180), width=2)
    d.polygon([(210,205),(105,520),(335,520)], fill=(36,31,29,255), outline=(186,140,78,160))
    d.polygon([(130,260),(35,505),(120,510)], fill=(25,23,24,255))
    d.polygon([(285,250),(410,520),(315,520)], fill=(25,23,24,255))
    d.line((270,240,500,545), fill=(210,205,190,200), width=8)
    d.line((280,230,510,535), fill=(90,120,145,200), width=3)
    # mage silhouette
    d.ellipse((560,120,635,200), fill=(38,28,45,255), outline=(175,115,235,190), width=2)
    d.polygon([(600,190),(485,540),(720,540)], fill=(28,22,38,255), outline=(140,85,220,160))
    d.ellipse((690,245,730,285), fill=(185,95,255,200))
    for r in range(90,0,-5):
        d.ellipse((710-r,265-r,710+r,265+r), outline=(180,85,255,max(0,int(70*r/90))), width=2)
    save_webp(img.convert('RGB'),'hero-figures.webp',86)

def lore_image(name, title, palette, seed):
    w,h=720,420
    img=gradient_bg(w,h,palette[0],palette[1]).convert('RGBA')
    d=ImageDraw.Draw(img,'RGBA')
    rnd=random.Random(seed)
    draw_stars(d,w,h,60,seed=seed)
    # terrain
    for layer in range(3):
        base=290+layer*40
        pts=[(0,h)]
        for x in range(0,w+120,90):
            pts.append((x,base-rnd.randint(30,120)))
        pts += [(w,h)]
        d.polygon(pts, fill=(8+layer*8,13+layer*8,15+layer*7,150+layer*30))
    # theme motifs
    if 'aurelian' in name:
        for x in [260,320,380,435]:
            d.rectangle((x,150-rnd.randint(0,50),x+28,330), fill=(86,70,52,210))
            d.polygon([(x-10,150),(x+14,105-rnd.randint(0,30)),(x+38,150)], fill=(153,116,55,180))
    elif 'shadow' in name:
        for x in [210,300,400,500]:
            d.polygon([(x,330),(x+35,80-rnd.randint(0,30)),(x+70,330)], fill=(10,15,29,230))
    elif 'verdant' in name:
        d.rectangle((350,170,382,340), fill=(57,78,43,220))
        for r in [150,110,75,45]:
            d.ellipse((366-r,190-r,366+r,190+r), fill=(56,100,58,120))
    else:
        for r,c in [(180,(180,59,35,110)),(110,(255,132,45,140)),(55,(255,204,98,160))]:
            d.ellipse((360-r,255-r,360+r,255+r), fill=c)
        d.polygon([(140,350),(360,100),(580,350)], fill=(55,25,20,210))
    # overlay title faint
    d.rectangle((0,h-82,w,h), fill=(0,0,0,105))
    d.text((w//2,h-52), title.upper(), anchor='mm', fill=(246,219,162,255), font=font(32, True))
    img=add_noise(img.convert('RGB'),16,seed+12)
    save_webp(img,f'{name}.webp',84)

def product_image(name, title, kind, seed):
    w,h=600,600
    img=gradient_bg(w,h,(10,15,19),(2,4,7)).convert('RGBA')
    d=ImageDraw.Draw(img,'RGBA')
    draw_stars(d,w,h,60,seed=seed)
    # tabletop shadow
    d.ellipse((85,450,515,545), fill=(0,0,0,130))
    if kind=='box':
        # 3D box
        d.polygon([(170,160),(410,118),(480,182),(238,228)], fill=(73,54,33,255), outline=(206,156,72,255))
        d.polygon([(238,228),(480,182),(480,430),(238,480)], fill=(22,28,34,255), outline=(206,156,72,255))
        d.polygon([(170,160),(238,228),(238,480),(170,400)], fill=(13,19,27,255), outline=(126,91,47,255))
        cover=(252,240,470,435)
    elif kind=='packs':
        for i,dx in enumerate([-70,0,70]):
            poly=[(210+dx,140+i*8),(365+dx,118+i*8),(400+dx,430),(235+dx,460)]
            d.polygon(poly, fill=(18+i*8,28+i*3,42+i*8,255), outline=(206,156,72,255))
        cover=(230,150,386,430)
    else:
        d.polygon([(185,120),(410,160),(380,500),(150,460)], fill=(73,53,33,255), outline=(206,156,72,255))
        d.polygon([(205,145),(386,178),(360,465),(176,433)], fill=(24,20,18,255), outline=(145,100,45,255))
        cover=(205,145,386,465)
    # emblem
    cx=(cover[0]+cover[2])//2; cy=(cover[1]+cover[3])//2
    for r in [95,60,28]:
        d.ellipse((cx-r,cy-r,cx+r,cy+r), outline=(196,143,70,170), width=3)
    for ang in range(0,360,45):
        d.line((cx,cy,cx+math.cos(math.radians(ang))*105,cy+math.sin(math.radians(ang))*105), fill=(196,143,70,100), width=2)
    d.text((cx,cy-120),'CAELTERRA',anchor='mm', fill=(242,208,130,255), font=font(32,True))
    d.text((cx,cy+132),title.upper(),anchor='mm', fill=(242,208,130,255), font=font(24,True))
    img=add_noise(img.convert('RGB'),18,seed)
    save_webp(img,f'{name}.webp',84)

def news_image(name, palette, title, seed):
    w,h=720,380
    img=gradient_bg(w,h,palette[0],palette[1]).convert('RGBA')
    d=ImageDraw.Draw(img,'RGBA')
    draw_stars(d,w,h,80,seed)
    draw_mountains(d,w,h,300,(10,16,22,230),seed=seed+10)
    # foreground card/people/table shapes
    rnd=random.Random(seed)
    for i in range(7):
        x=rnd.randint(70,650); y=rnd.randint(170,330)
        d.rectangle((x,y,x+30,y+70), fill=(23,20,18,180), outline=(180,125,60,120))
    d.rectangle((0,h-72,w,h), fill=(0,0,0,110))
    d.text((32,h-47),title, fill=(245,220,165,255), font=font(28,True))
    img=add_noise(img.convert('RGB'),16,seed+30)
    save_webp(img,f'{name}.webp',84)

def og_image():
    w,h=1200,630
    img=gradient_bg(w,h,(8,12,17),(3,6,9)).convert('RGBA')
    d=ImageDraw.Draw(img,'RGBA')
    draw_stars(d,w,h,200,seed=22)
    draw_mountains(d,w,h,500,(11,20,28,210),seed=8)
    # compass
    cx,cy=600,230
    for r in [150,95,42]:
        d.ellipse((cx-r,cy-r,cx+r,cy+r), outline=(203,153,72,165), width=4)
    for ang in range(0,360,30):
        d.line((cx,cy,cx+math.cos(math.radians(ang))*160,cy+math.sin(math.radians(ang))*160), fill=(203,153,72,90), width=2)
    d.text((600,250),'CAELTERRA',anchor='mm',fill=(242,207,132,255),font=font(98,True))
    d.text((600,360),'One world. Two ways to play.',anchor='mm',fill=(245,239,220,255),font=font(46,False))
    d.text((600,425),'A fantasy TCG & TRPG universe by Scrollrealm.',anchor='mm',fill=(207,190,154,255),font=font(28,False))
    save_webp(add_noise(img.convert('RGB'),14,2),'og-caelterra.webp',88)

hero_bg(); card_stack(); silhouettes(); og_image()
lore_image('realm-aurelian','The Aurelian Empire',((64,45,27),(167,126,63)),11)
lore_image('realm-shadow','The Shadow Courts',((9,14,28),(38,52,96)),12)
lore_image('realm-verdant','The Verdant Wilds',((10,31,26),(68,105,57)),13)
lore_image('realm-ashen','The Ashen Wastes',((35,17,15),(145,53,27)),14)
product_image('product-starter-set','Starter Set','box',21)
product_image('product-booster-packs','Booster Packs','packs',22)
product_image('product-core-rulebook','Core Rulebook','book',23)
news_image('news-lore',((20,31,42),(74,60,42)),'World Lore Deep Dive',31)
news_image('news-cards',((16,24,41),(45,65,105)),'Card Preview',32)
news_image('news-quickstart',((23,20,18),(79,45,31)),'TRPG Quickstart',33)

# SVG icons/logo
logo_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" role="img" aria-labelledby="title"><title>Scrollrealm crest</title><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f4d98c"/><stop offset="1" stop-color="#9e6b2e"/></linearGradient></defs><rect width="128" height="128" fill="none"/><circle cx="64" cy="64" r="45" fill="none" stroke="url(#g)" stroke-width="5"/><circle cx="64" cy="64" r="22" fill="none" stroke="url(#g)" stroke-width="3"/><path d="M64 7l12 45 45 12-45 12-12 45-12-45L7 64l45-12z" fill="none" stroke="url(#g)" stroke-width="5" stroke-linejoin="round"/><path d="M64 21v86M21 64h86M34 34l60 60M94 34L34 94" stroke="#c99a50" stroke-width="2" opacity=".55"/></svg>'''
(ROOT/'assets'/'icons'/'scrollrealm-crest.svg').write_text(logo_svg,encoding='utf-8')

# Copy design preview if exists
preview = Path('/mnt/data/판타지_tcg_trpg_홈페이지_디자인.png')
if preview.exists():
    (ROOT/'assets'/'images'/'design-concept-preview.png').write_bytes(preview.read_bytes())

# ---------- Data ----------
products = [
    {'name':'Caelterra Starter Set','slug':'starter-set','image':'product-starter-set.webp','summary':'A complete entry point into Caelterra TCG, designed for first battles and faction discovery.','cta':'Learn More','type':'Starter box','status':'Coming soon'},
    {'name':'Caelterra Booster Packs','slug':'booster-packs','image':'product-booster-packs.webp','summary':'Expand your collection with new allies, relics, tactics, and faction-defining cards.','cta':'View Details','type':'Card booster','status':'Coming soon'},
    {'name':'Caelterra Core Rulebook','slug':'core-rulebook','image':'product-core-rulebook.webp','summary':'The complete TRPG guide for game masters, adventurers, campaigns, and realm exploration.','cta':'Read More','type':'TRPG rulebook','status':'In development'},
]
releases = [
    {'title':'Alpha Preview','period':'Q3 2026','desc':'Early access to Caelterra TCG previews and TRPG quickstart material.'},
    {'title':'Starter Set Launch','period':'Q4 2026','desc':'Starter Set release window for introductory TCG play.'},
    {'title':'Booster Wave I','period':'Q1 2027','desc':'The first booster wave expands deck-building and faction strategy.'},
    {'title':'TRPG Core Rulebook','period':'Q2 2027','desc':'Full core rulebook release for campaign-ready play.'},
]
news = [
    {'title':'Building Caelterra: World Lore Deep Dive','slug':'building-caelterra-world-lore-deep-dive','tag':'Dev Update','date':'2026-05-28','image':'news-lore.webp','summary':'Explore the ancient realms, faction conflicts, and mythic forces that shape the world of Caelterra.'},
    {'title':'Card Preview: Meet the Shadow Courts','slug':'card-preview-shadow-courts','tag':'Cards','date':'2026-05-28','image':'news-cards.webp','summary':'A first look at intrigue-focused cards from the Shadow Courts faction.'},
    {'title':'TRPG Quickstart Guide in Development','slug':'trpg-quickstart-guide-in-development','tag':'TRPG','date':'2026-05-28','image':'news-quickstart.webp','summary':'A preview of character creation, core actions, and introductory campaign structure.'},
]
(ROOT/'data'/'products.json').write_text(json.dumps(products,indent=2),encoding='utf-8')
(ROOT/'data'/'releases.json').write_text(json.dumps(releases,indent=2),encoding='utf-8')
(ROOT/'data'/'news.json').write_text(json.dumps(news,indent=2),encoding='utf-8')

# ---------- CSS ----------
css = r'''
:root{
  color-scheme: dark;
  --bg:#05080c;
  --bg-2:#0a1118;
  --panel:#101821;
  --panel-2:#14101d;
  --line:rgba(218,168,83,.36);
  --line-soft:rgba(218,168,83,.18);
  --gold:#d7a34e;
  --gold-2:#f2d282;
  --text:#f5eee1;
  --muted:#c4b69d;
  --muted-2:#8d806e;
  --blue:#10283b;
  --purple:#22152d;
  --green:#173024;
  --danger:#6b221e;
  --radius:22px;
  --shadow:0 18px 60px rgba(0,0,0,.34);
  --max:1180px;
  --font-title: Georgia, 'Times New Roman', serif;
  --font-body: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;background:var(--bg)}
body{margin:0;font-family:var(--font-body);background:radial-gradient(circle at 50% 0, rgba(215,163,78,.10), transparent 28rem), linear-gradient(180deg,#05080c,#080b0f 40%,#05080c);color:var(--text);line-height:1.65;overflow-x:hidden}
a{color:inherit;text-decoration:none}
img{max-width:100%;display:block}
button,input,textarea{font:inherit}
.skip-link{position:absolute;left:-999px;top:auto;width:1px;height:1px;overflow:hidden}.skip-link:focus{left:16px;top:16px;z-index:9999;width:auto;height:auto;padding:10px 14px;background:#000;color:#fff;border:1px solid var(--gold)}
.container{width:min(var(--max), calc(100% - 32px));margin-inline:auto}
.ornate{position:relative}.ornate:before,.ornate:after{content:"";position:absolute;inset:0;pointer-events:none;border:1px solid var(--line);border-radius:inherit}.ornate:after{inset:6px;border-color:rgba(215,163,78,.12)}
.site-header{position:sticky;top:0;z-index:50;background:rgba(5,8,12,.82);backdrop-filter:blur(18px);border-bottom:1px solid var(--line-soft)}
.nav{height:74px;display:flex;align-items:center;justify-content:space-between;gap:24px}.brand{display:flex;align-items:center;gap:12px;font-family:var(--font-title);letter-spacing:.06em;text-transform:uppercase;font-size:1.48rem;color:var(--gold-2)}.brand img{width:38px;height:38px}.nav-links{display:flex;align-items:center;gap:24px;font-size:.78rem;text-transform:uppercase;letter-spacing:.12em;color:#f6e9d0}.nav-links a{position:relative;opacity:.88}.nav-links a:hover,.nav-links a.active{opacity:1;color:var(--gold-2)}.nav-links a.active:after{content:"";position:absolute;left:0;right:0;bottom:-25px;height:2px;background:linear-gradient(90deg, transparent,var(--gold),transparent)}.nav-toggle{display:none;background:transparent;color:var(--text);border:1px solid var(--line);border-radius:12px;padding:8px 10px}
.hero{position:relative;min-height:780px;display:flex;align-items:center;overflow:hidden;border-bottom:1px solid var(--line-soft)}.hero:before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,8,12,.88),rgba(5,8,12,.34) 42%,rgba(5,8,12,.72)),url('../images/hero-bg.webp') center/cover no-repeat;z-index:-3}.hero:after{content:"";position:absolute;inset:auto 0 0;height:280px;background:linear-gradient(0deg,var(--bg),transparent);z-index:-1}.hero-art-left{position:absolute;left:max(-110px, calc((100vw - var(--max))/2 - 210px));top:130px;width:520px;opacity:.96;filter:drop-shadow(0 24px 35px rgba(0,0,0,.55))}.hero-art-right{position:absolute;right:max(-120px, calc((100vw - var(--max))/2 - 210px));bottom:50px;width:570px;opacity:.92;filter:drop-shadow(0 24px 35px rgba(0,0,0,.55))}.hero-content{position:relative;z-index:1;max-width:760px;margin-inline:auto;text-align:center;padding-block:124px 140px}.sigil{width:170px;height:170px;margin:0 auto -82px;opacity:.58;background:url('../icons/scrollrealm-crest.svg') center/contain no-repeat;filter:drop-shadow(0 0 20px rgba(215,163,78,.22))}.eyebrow{margin:0 0 14px;color:var(--gold-2);letter-spacing:.22em;text-transform:uppercase;font-size:.75rem}.hero h1,.page-hero h1{font-family:var(--font-title);font-size:clamp(4.8rem,10vw,9.4rem);line-height:.88;margin:0;background:linear-gradient(180deg,#fff5c8,#d7a34e 48%,#785122);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:0 5px 30px rgba(0,0,0,.8)}.hero .lead{font-family:var(--font-title);font-size:clamp(1.7rem,3vw,3rem);line-height:1.1;margin:26px 0 8px}.hero .sublead{color:#e9ddc8;font-size:1.06rem;margin:0 auto 28px;max-width:660px}.cta-row{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:45px;padding:11px 18px;border:1px solid var(--line);border-radius:10px;background:rgba(7,10,14,.72);color:#fff4dc;text-transform:uppercase;letter-spacing:.08em;font-size:.76rem;box-shadow:inset 0 1px 0 rgba(255,255,255,.07),0 10px 24px rgba(0,0,0,.24);transition:.2s ease}.btn:hover{transform:translateY(-2px);border-color:var(--gold);box-shadow:0 16px 30px rgba(0,0,0,.36)}.btn-primary{background:linear-gradient(180deg,#d6a452,#7b4b1f);border-color:#e0b063;color:#170f08}.btn-blue{background:linear-gradient(180deg,#173a55,#0a1824)}.btn-purple{background:linear-gradient(180deg,#3b2258,#1c1128)}
.section{padding:74px 0}.section.compact{padding:46px 0}.section-head{display:flex;justify-content:space-between;gap:22px;align-items:end;margin-bottom:26px}.section-title{font-family:var(--font-title);font-size:clamp(1.8rem,3vw,3rem);line-height:1.05;margin:0;color:#f2ddad}.section-kicker{color:var(--gold);text-transform:uppercase;letter-spacing:.18em;font-size:.75rem;margin:0 0 8px}.section-sub{color:var(--muted);margin:8px 0 0;max-width:740px}.feature-grid{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:-80px;position:relative;z-index:3}.feature-card{min-height:360px;border-radius:var(--radius);border:1px solid var(--line);background:linear-gradient(145deg,rgba(13,34,49,.95),rgba(4,7,12,.95));box-shadow:var(--shadow);overflow:hidden;padding:34px;position:relative}.feature-card.trpg{background:linear-gradient(145deg,rgba(35,19,48,.95),rgba(4,7,12,.95))}.feature-visual{position:absolute;inset:auto auto -25px -40px;width:330px;opacity:.46;filter:saturate(1.1)}.feature-card.trpg .feature-visual{left:auto;right:-22px;width:270px;opacity:.82}.feature-content{position:relative;z-index:1;max-width:430px;margin-left:auto;text-align:center}.feature-card.trpg .feature-content{margin-left:0}.feature-card h2{font-family:var(--font-title);font-size:2.1rem;margin:0;color:#fff0ce}.feature-card .tagline{font-family:var(--font-title);letter-spacing:.08em;color:var(--gold-2);text-transform:uppercase;margin:4px 0 12px}.icon-row{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:25px 0}.icon-pill{padding:12px 8px;border:1px solid rgba(215,163,78,.22);border-radius:14px;background:rgba(0,0,0,.18);font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:#dacaa9}.icon-pill b{display:block;font-size:1.34rem;color:var(--gold-2);line-height:1;margin-bottom:8px}.world{background:linear-gradient(180deg,rgba(215,163,78,.05),rgba(0,0,0,0)), radial-gradient(circle at 50% 0, rgba(215,163,78,.14), transparent 34rem)}.lore-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}.lore-card{border-radius:18px;overflow:hidden;border:1px solid var(--line);background:var(--panel);box-shadow:var(--shadow);position:relative}.lore-card img{height:190px;width:100%;object-fit:cover}.lore-card .copy{padding:18px}.lore-card h3{font-family:var(--font-title);font-size:1.18rem;margin:0 0 4px;color:var(--gold-2)}.lore-card p{margin:0;color:var(--muted);font-size:.91rem}.product-schedule{display:grid;grid-template-columns:.9fr 1.1fr;gap:22px}.panel{border:1px solid var(--line);border-radius:var(--radius);background:linear-gradient(180deg,rgba(12,17,22,.96),rgba(5,8,12,.96));box-shadow:var(--shadow);padding:28px;overflow:hidden}.product-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.product-card{background:rgba(0,0,0,.22);border:1px solid rgba(215,163,78,.22);border-radius:18px;padding:14px;text-align:center}.product-card img{aspect-ratio:1/1;object-fit:cover;border-radius:14px;border:1px solid rgba(215,163,78,.18);margin-bottom:12px}.product-card h3{font-family:var(--font-title);color:#f2ddad;margin:0 0 6px;font-size:1.08rem}.product-card p{color:var(--muted);font-size:.86rem;margin:0 0 12px}.schedule{position:relative;display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:12px}.schedule:before{content:"";position:absolute;left:8%;right:8%;top:44px;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent);opacity:.55}.milestone{text-align:center;position:relative;padding-top:8px}.milestone .node{width:76px;height:76px;display:grid;place-items:center;margin:0 auto 14px;border-radius:50%;border:1px solid var(--line);background:radial-gradient(circle,#1b232d,#070a0e);font-size:1.9rem;color:var(--gold-2);box-shadow:0 0 0 8px rgba(215,163,78,.04)}.milestone h3{font-family:var(--font-title);font-size:1.03rem;color:var(--gold-2);margin:0}.milestone time{display:block;color:var(--gold);font-size:.86rem;margin:4px 0 8px}.milestone p{margin:0;color:var(--muted);font-size:.88rem}.news-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.news-card{border:1px solid var(--line-soft);border-radius:18px;overflow:hidden;background:rgba(9,13,18,.94);box-shadow:var(--shadow);transition:.2s ease}.news-card:hover{transform:translateY(-4px);border-color:var(--line)}.news-card img{height:180px;width:100%;object-fit:cover}.news-card .body{padding:18px}.badge{display:inline-flex;align-items:center;padding:4px 9px;border:1px solid var(--line);border-radius:999px;color:var(--gold-2);font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;background:rgba(215,163,78,.08)}.news-card h3{font-family:var(--font-title);font-size:1.24rem;line-height:1.2;margin:12px 0 8px;color:#fff0ce}.news-card p{margin:0;color:var(--muted);font-size:.93rem}.meta{margin-top:13px;color:var(--muted-2);font-size:.82rem}.games-teaser{display:grid;grid-template-columns:320px 1fr;gap:22px;align-items:stretch}.coming{border:1px solid var(--line);border-radius:var(--radius);padding:28px;background:radial-gradient(circle at 30% 30%,rgba(215,163,78,.14),transparent 45%),rgba(7,11,15,.94)}.placeholder-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.placeholder{min-height:168px;border:1px solid rgba(215,163,78,.18);border-radius:18px;background:radial-gradient(circle,rgba(215,163,78,.09),transparent 35%),rgba(255,255,255,.025);display:grid;place-items:center;color:rgba(242,210,130,.35);font-family:var(--font-title);font-size:3rem}.page-hero{padding:112px 0 68px;background:linear-gradient(90deg,rgba(5,8,12,.94),rgba(5,8,12,.66)),url('../images/hero-bg.webp') center/cover no-repeat;border-bottom:1px solid var(--line-soft)}.page-hero.nested{background:linear-gradient(90deg,rgba(5,8,12,.94),rgba(5,8,12,.66)),url('../../assets/images/hero-bg.webp') center/cover no-repeat}.page-hero h1{font-size:clamp(3rem,7vw,6.4rem)}.breadcrumb{font-size:.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:.12em;margin-bottom:18px}.content-grid{display:grid;grid-template-columns:1fr 360px;gap:32px}.prose{color:#dfd3bf}.prose h2,.prose h3{font-family:var(--font-title);color:#f2ddad;line-height:1.15}.prose h2{font-size:2.1rem}.prose p{color:#d6c9b5}.list{display:grid;gap:10px}.list li{padding:12px 14px;border:1px solid rgba(215,163,78,.16);border-radius:14px;background:rgba(255,255,255,.026)}.stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:24px 0}.stat{padding:18px;border:1px solid var(--line-soft);border-radius:18px;background:rgba(0,0,0,.18)}.stat b{display:block;color:var(--gold-2);font-family:var(--font-title);font-size:1.25rem}.form{display:grid;gap:12px}.field{display:grid;gap:6px}.field label{color:var(--gold-2);font-size:.78rem;text-transform:uppercase;letter-spacing:.1em}.field input,.field textarea,.newsletter input{width:100%;background:rgba(0,0,0,.28);color:var(--text);border:1px solid var(--line-soft);border-radius:12px;padding:12px 13px}.field textarea{min-height:130px;resize:vertical}.board-list{display:grid;gap:12px}.board-item{display:grid;grid-template-columns:130px 1fr auto;gap:16px;align-items:center;border:1px solid var(--line-soft);border-radius:18px;padding:15px;background:rgba(255,255,255,.025)}.board-item time{color:var(--gold);font-size:.85rem}.board-item h3{font-family:var(--font-title);margin:0;color:#fff0ce}.board-item p{margin:2px 0 0;color:var(--muted)}
.footer{border-top:1px solid var(--line-soft);background:#05070a;padding:44px 0 24px}.footer-grid{display:grid;grid-template-columns:1.3fr repeat(3,.72fr) 1.3fr;gap:26px}.footer h2,.footer h3{font-family:var(--font-title);color:var(--gold-2);margin:0 0 12px}.footer p,.footer a{color:var(--muted);font-size:.92rem}.footer a{display:block;margin:6px 0}.socials{display:flex;gap:10px;margin-top:14px}.socials a{width:34px;height:34px;border:1px solid var(--line-soft);border-radius:50%;display:grid;place-items:center;color:var(--gold-2)}.newsletter{display:flex;gap:8px}.copyright{margin-top:28px;color:var(--muted-2);font-size:.82rem;text-align:center}.reveal{opacity:0;transform:translateY(18px);transition:opacity .6s ease, transform .6s ease}.reveal.in{opacity:1;transform:none}
@media (max-width:1050px){.hero-art-left,.hero-art-right{opacity:.36}.feature-grid,.product-schedule,.content-grid,.games-teaser{grid-template-columns:1fr}.lore-grid{grid-template-columns:repeat(2,1fr)}.schedule{grid-template-columns:repeat(2,1fr)}.schedule:before{display:none}.footer-grid{grid-template-columns:1fr 1fr}.product-grid{grid-template-columns:repeat(3,1fr)}}
@media (max-width:820px){.nav-toggle{display:block}.nav-links{position:absolute;left:16px;right:16px;top:76px;display:none;flex-direction:column;align-items:stretch;gap:0;padding:12px;border:1px solid var(--line);border-radius:18px;background:rgba(5,8,12,.96)}.nav-links.open{display:flex}.nav-links a{padding:12px}.nav-links a.active:after{display:none}.hero{min-height:720px}.hero h1{font-size:clamp(4rem,17vw,6rem)}.feature-grid{margin-top:-55px}.feature-card{padding:26px}.feature-content,.feature-card.trpg .feature-content{max-width:none;margin:0}.feature-visual{opacity:.18}.icon-row,.product-grid,.news-grid,.placeholder-grid,.stat-grid{grid-template-columns:1fr}.lore-grid,.schedule{grid-template-columns:1fr}.footer-grid{grid-template-columns:1fr}.newsletter{flex-direction:column}.board-item{grid-template-columns:1fr}.section-head{display:block}.hero-art-left{left:-220px}.hero-art-right{right:-260px}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important;animation:none!important}.reveal{opacity:1;transform:none}}
'''
(ROOT/'assets'/'css'/'styles.css').write_text(css.strip()+"\n",encoding='utf-8')

# ---------- JS ----------
js = r'''
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
}
const observer = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (entry.isIntersecting) entry.target.classList.add('in');
  }
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
const year = document.querySelector('[data-year]');
if (year) year.textContent = new Date().getFullYear();
'''
(ROOT/'assets'/'js'/'main.js').write_text(js.strip()+"\n",encoding='utf-8')

# ---------- HTML helpers ----------
def rel(depth=0):
    return '../'*depth if depth else ''

def header(active='', depth=0):
    r = rel(depth)
    links = [('Caelterra',f'{r}caelterra/','caelterra'),('Products',f'{r}products/','products'),('Release Schedule',f'{r}release-schedule/','release'),('News',f'{r}news/','news'),('Games',f'{r}games/','games'),('About',f'{r}about/','about'),('Contact',f'{r}contact/','contact')]
    nav = ''.join(f'<a class="{"active" if key==active else ""}" href="{href}">{label}</a>' for label,href,key in links)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container nav">
    <a class="brand" href="{r}index.html" aria-label="Scrollrealm home"><img src="{r}assets/icons/scrollrealm-crest.svg" alt="" width="38" height="38"><span>Scrollrealm</span></a>
    <button class="nav-toggle" type="button" aria-label="Open navigation" aria-expanded="false">Menu</button>
    <nav class="nav-links" aria-label="Primary navigation">{nav}</nav>
  </div>
</header>'''

def footer(depth=0):
    r=rel(depth)
    return f'''<footer class="footer">
  <div class="container footer-grid">
    <div><a class="brand" href="{r}index.html"><img src="{r}assets/icons/scrollrealm-crest.svg" alt="" width="38" height="38"><span>Scrollrealm</span></a><p>We create immersive worlds and tabletop games that bring people together through strategy, storytelling, and adventure.</p><div class="socials"><a href="#" aria-label="Discord">D</a><a href="#" aria-label="X">X</a><a href="#" aria-label="Instagram">I</a><a href="#" aria-label="YouTube">Y</a></div></div>
    <div><h3>Explore</h3><a href="{r}caelterra/">Caelterra</a><a href="{r}products/">Products</a><a href="{r}release-schedule/">Release Schedule</a><a href="{r}news/">News</a><a href="{r}games/">Games</a></div>
    <div><h3>Company</h3><a href="{r}about/">About Us</a><a href="{r}about/#team">Our Team</a><a href="{r}contact/">Contact</a></div>
    <div><h3>Support</h3><a href="{r}downloads/">Downloads</a><a href="{r}contact/">Retailers</a><a href="{r}contact/">Press</a><a href="{r}privacy.html">Privacy</a></div>
    <div><h3>Stay in the Realm</h3><p>Subscribe for news, updates, and exclusive content.</p><form class="newsletter" action="https://formspree.io/f/your-form-id" method="POST"><input type="email" name="email" placeholder="Enter your email" aria-label="Email address"><button class="btn btn-primary" type="submit">Subscribe</button></form></div>
  </div><div class="container copyright">© <span data-year>2026</span> Scrollrealm. All rights reserved.</div>
</footer>
<script src="{r}assets/js/main.js" defer></script>'''

def head(title, desc, path='', depth=0, image='assets/images/og-caelterra.webp', extra=''):
    r=rel(depth)
    canonical = DOMAIN + ('/' + path.strip('/') if path.strip('/') else '') + '/'
    if canonical.endswith('//'): canonical = canonical[:-1]
    img_url = DOMAIN + '/' + image
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#05080c">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{img_url}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{r}assets/icons/scrollrealm-crest.svg" type="image/svg+xml">
  <link rel="preload" as="image" href="{r}assets/images/hero-bg.webp">
  <link rel="stylesheet" href="{r}assets/css/styles.css">
  {extra}
</head>
<body>'''

def page_hero(title, eyebrow, desc, depth=0, nested=True):
    cls = 'page-hero nested' if depth else 'page-hero'
    return f'''<section class="{cls}"><div class="container"><div class="breadcrumb">{eyebrow}</div><h1>{title}</h1><p class="section-sub">{desc}</p></div></section>'''

# Home page structured data
home_schema = json.dumps({
    '@context':'https://schema.org',
    '@graph':[
        {'@type':'Organization','name':'Scrollrealm','url':DOMAIN,'logo':DOMAIN+'/assets/icons/scrollrealm-crest.svg','brand':{'@type':'Brand','name':'Caelterra'}},
        {'@type':'WebSite','name':'Scrollrealm','url':DOMAIN,'description':'Official site for Caelterra, a fantasy TCG and TRPG universe by Scrollrealm.'},
        {'@type':'CreativeWork','name':'Caelterra','genre':['Fantasy','Trading Card Game','Tabletop Roleplaying Game'],'creator':{'@type':'Organization','name':'Scrollrealm'},'url':DOMAIN+'/caelterra/'}
    ]
}, ensure_ascii=False)

home = head('Caelterra | Fantasy TCG & TRPG by Scrollrealm', 'Caelterra is a fantasy TCG and TRPG universe by Scrollrealm, created for collectible card battles, roleplaying campaigns, and lore-driven tabletop adventures.', depth=0, extra=f'<script type="application/ld+json">{home_schema}</script>') + header('caelterra',0) + f'''
<main id="main">
<section class="hero">
  <img class="hero-art-left" src="assets/images/card-stack.webp" alt="Caelterra collectible card previews" width="850" height="640">
  <img class="hero-art-right" src="assets/images/hero-figures.webp" alt="Fantasy warrior and mage representing Caelterra TCG and TRPG" width="760" height="650">
  <div class="container hero-content">
    <div class="sigil" aria-hidden="true"></div>
    <p class="eyebrow">Official Scrollrealm Homepage</p>
    <h1>Caelterra</h1>
    <p class="lead">One world. Two ways to play.</p>
    <p class="sublead">A fantasy TCG &amp; TRPG universe by Scrollrealm, built for tactical card battles, epic campaigns, and lore-rich tabletop adventures.</p>
    <div class="cta-row"><a class="btn btn-primary" href="caelterra/">Explore Caelterra</a><a class="btn btn-blue" href="caelterra/tcg/">Discover the TCG</a><a class="btn btn-purple" href="caelterra/trpg/">Start the TRPG</a></div>
  </div>
</section>
<section class="container feature-grid" aria-label="Caelterra play modes">
  <article class="feature-card ornate reveal"><img class="feature-visual" src="assets/images/card-stack.webp" alt="" loading="lazy"><div class="feature-content"><h2>Caelterra TCG</h2><p class="tagline">Strategy. Collection. Victory.</p><p>Build your deck, command your faction, and outwit your opponent in tactical card battles across the realms.</p><div class="icon-row"><span class="icon-pill"><b>▣</b>Deck-building</span><span class="icon-pill"><b>◆</b>Faction Strategy</span><span class="icon-pill"><b>◈</b>Collectible Cards</span><span class="icon-pill"><b>⚔</b>Tactical Battles</span></div><a class="btn btn-blue" href="caelterra/tcg/">Discover the TCG</a></div></article>
  <article class="feature-card trpg ornate reveal"><img class="feature-visual" src="assets/images/product-core-rulebook.webp" alt="" loading="lazy"><div class="feature-content"><h2>Caelterra TRPG</h2><p class="tagline">Create. Explore. Become Legend.</p><p>Create unique characters, embark on epic campaigns, and shape the story of Caelterra with your party.</p><div class="icon-row"><span class="icon-pill"><b>♟</b>Character Creation</span><span class="icon-pill"><b>✦</b>Campaign Adventures</span><span class="icon-pill"><b>✧</b>World Exploration</span><span class="icon-pill"><b>✎</b>Storytelling Freedom</span></div><a class="btn btn-purple" href="caelterra/trpg/">Start the TRPG</a></div></article>
</section>
<section class="section world"><div class="container"><div class="section-head"><div><p class="section-kicker">World &amp; Lore</p><h2 class="section-title">Discover the Factions and Realms of Caelterra</h2><p class="section-sub">A realm of luminous empires, hidden courts, ancient wilds, and volcanic frontiers.</p></div><a class="btn" href="caelterra/world/">Explore Lore</a></div><div class="lore-grid">
  <article class="lore-card reveal"><img src="assets/images/realm-aurelian.webp" alt="Aurelian Empire fantasy city" loading="lazy"><div class="copy"><h3>The Aurelian Empire</h3><p>Order, duty, civilization — a realm of law and light.</p></div></article>
  <article class="lore-card reveal"><img src="assets/images/realm-shadow.webp" alt="Shadow Courts dark spires" loading="lazy"><div class="copy"><h3>The Shadow Courts</h3><p>Intrigue, ambition, power — where secrets shape destiny.</p></div></article>
  <article class="lore-card reveal"><img src="assets/images/realm-verdant.webp" alt="Verdant Wilds ancient forest" loading="lazy"><div class="copy"><h3>The Verdant Wilds</h3><p>Nature, balance, ancient magic — the wilds remember.</p></div></article>
  <article class="lore-card reveal"><img src="assets/images/realm-ashen.webp" alt="Ashen Wastes volcanic region" loading="lazy"><div class="copy"><h3>The Ashen Wastes</h3><p>Chaos, survival, rebirth — from ruin, new paths arise.</p></div></article>
</div></div></section>
<section class="section"><div class="container product-schedule"><div class="panel ornate reveal"><p class="section-kicker">Featured Products</p><h2 class="section-title">Start Your Journey</h2><div class="product-grid">{''.join(f'<article class="product-card"><img src="assets/images/{p["image"]}" alt="{p["name"]}" loading="lazy"><h3>{p["name"]}</h3><p>{p["summary"]}</p><a class="btn" href="products/{p["slug"]}/">{p["cta"]}</a></article>' for p in products)}</div></div><div class="panel ornate reveal"><p class="section-kicker">Release Schedule</p><h2 class="section-title">Upcoming Milestones</h2><div class="schedule">{''.join(f'<div class="milestone"><div class="node">{icon}</div><h3>{item["title"]}</h3><time>{item["period"]}</time><p>{item["desc"]}</p></div>' for item,icon in zip(releases,['◉','♜','▤','☷']))}</div></div></div></section>
<section class="section compact"><div class="container"><div class="section-head"><div><p class="section-kicker">Latest News</p><h2 class="section-title">News &amp; Dev Updates</h2></div><a class="btn" href="news/">View All News</a></div><div class="news-grid">{''.join(f'<a class="news-card reveal" href="news/{n["slug"]}/"><img src="assets/images/{n["image"]}" alt="{n["title"]}" loading="lazy"><div class="body"><span class="badge">{n["tag"]}</span><h3>{n["title"]}</h3><p>{n["summary"]}</p><div class="meta">{n["date"]} · Read More →</div></div></a>' for n in news)}</div></div></section>
<section class="section compact"><div class="container games-teaser"><div class="coming ornate reveal"><p class="section-kicker">Future Worlds</p><h2 class="section-title">Other Games by Scrollrealm</h2><p class="section-sub">Caelterra leads the way. New tabletop worlds and adventures will be revealed here as Scrollrealm expands.</p><a class="btn" href="games/">Explore All Games</a></div><div class="placeholder-grid"><div class="placeholder">✦</div><div class="placeholder">☉</div><div class="placeholder">♢</div></div></div></section>
</main>''' + footer(0) + '</body></html>'
(ROOT/'index.html').write_text(home,encoding='utf-8')

# Generic content page generator
def write_page(path, active, title, desc, body_html, eyebrow='Scrollrealm', depth=1, schema=None):
    p=ROOT/path
    p.mkdir(parents=True, exist_ok=True)
    extra = f'<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>' if schema else ''
    rel_path = p.relative_to(ROOT).as_posix()
    html = head(title, desc, path=rel_path, depth=depth, extra=extra) + header(active,depth) + '<main id="main">' + page_hero(title.split('|')[0].strip(), eyebrow, desc, depth=depth) + body_html + '</main>' + footer(depth) + '</body></html>'
    (p/'index.html').write_text(html,encoding='utf-8')

# caelterra pages
body = '''<section class="section"><div class="container content-grid"><div class="prose"><h2>One World. Two Ways to Play.</h2><p>Caelterra is Scrollrealm’s flagship fantasy universe, designed to support both competitive collectible card play and narrative tabletop roleplaying. The TCG focuses on faction identity, deck construction, and tactical combat. The TRPG expands the same world into campaigns, characters, mysteries, and realm-changing stories.</p><div class="stat-grid"><div class="stat"><b>TCG</b>Collectible card battles and faction strategy.</div><div class="stat"><b>TRPG</b>Campaign-ready fantasy roleplaying.</div><div class="stat"><b>Lore</b>Shared factions, regions, and mythic conflicts.</div></div><h2>Built for Global Tabletop Fans</h2><p>The site is structured for North American and European players, retailers, press, and future community growth. Product pages, release updates, lore articles, and downloads are designed as independent, search-friendly pages.</p></div><aside class="panel ornate"><p class="section-kicker">Quick Links</p><h2 class="section-title">Enter Caelterra</h2><div class="list"><a class="btn btn-blue" href="tcg/">Discover the TCG</a><a class="btn btn-purple" href="trpg/">Start the TRPG</a><a class="btn" href="world/">Explore World &amp; Lore</a><a class="btn" href="../products/">View Products</a></div></aside></div></section>'''
write_page(ROOT/'caelterra', 'caelterra', 'Caelterra Official Site | TCG & TRPG Fantasy World', 'Explore Caelterra, a fantasy tabletop universe combining trading card game strategy with tabletop roleplaying adventures.', body, 'Caelterra', 1)

body_tcg = '''<section class="section"><div class="container content-grid"><div class="prose"><h2>Collectible Strategy Across the Realms</h2><p>Caelterra TCG is built around faction identity, resource tension, and tactical choices. Players assemble decks around leaders, relics, units, spells, and realm-shaping events.</p><ul class="list"><li>Build around one or more faction identities.</li><li>Win through board control, tempo, attrition, or objective pressure.</li><li>Expand through starter sets, booster waves, and organized play support.</li></ul><h2>Designed for Discoverability</h2><p>Card previews, faction guides, starter deck pages, and product pages are separated so that players can search for exactly what they need.</p></div><aside class="panel ornate"><img src="../../assets/images/card-stack.webp" alt="Caelterra TCG cards"><h2 class="section-title">TCG Resources</h2><a class="btn btn-blue" href="../../products/starter-set/">Starter Set</a></aside></div></section>'''
write_page(ROOT/'caelterra'/'tcg', 'caelterra', 'Caelterra TCG | Fantasy Trading Card Game', 'Build decks, command factions, and battle across the world of Caelterra in a fantasy trading card game by Scrollrealm.', body_tcg, 'Caelterra TCG', 2)

body_trpg = '''<section class="section"><div class="container content-grid"><div class="prose"><h2>Campaigns, Characters, and Realm-Shaping Choices</h2><p>Caelterra TRPG uses the same world as the TCG to create a campaign-ready tabletop roleplaying experience. Players create heroes, explore ancient lands, negotiate with factions, and confront forces that can reshape the realm.</p><ul class="list"><li>Character creation designed for heroic fantasy archetypes.</li><li>Faction-driven campaign hooks and setting conflicts.</li><li>Quickstart and core rulebook pages ready for future downloads.</li></ul></div><aside class="panel ornate"><img src="../../assets/images/product-core-rulebook.webp" alt="Caelterra Core Rulebook"><h2 class="section-title">TRPG Resources</h2><a class="btn btn-purple" href="../../products/core-rulebook/">Core Rulebook</a></aside></div></section>'''
write_page(ROOT/'caelterra'/'trpg', 'caelterra', 'Caelterra TRPG | Fantasy Tabletop Roleplaying Game', 'Create heroes, explore ancient realms, and build campaigns in Caelterra TRPG, a fantasy tabletop roleplaying game by Scrollrealm.', body_trpg, 'Caelterra TRPG', 2)

body_world = '''<section class="section world"><div class="container"><div class="lore-grid"><article class="lore-card"><img src="../../assets/images/realm-aurelian.webp" alt=""><div class="copy"><h3>The Aurelian Empire</h3><p>Order, duty, civilization — a realm of law and light.</p></div></article><article class="lore-card"><img src="../../assets/images/realm-shadow.webp" alt=""><div class="copy"><h3>The Shadow Courts</h3><p>Intrigue, ambition, power — where secrets shape destiny.</p></div></article><article class="lore-card"><img src="../../assets/images/realm-verdant.webp" alt=""><div class="copy"><h3>The Verdant Wilds</h3><p>Nature, balance, ancient magic — the wilds remember.</p></div></article><article class="lore-card"><img src="../../assets/images/realm-ashen.webp" alt=""><div class="copy"><h3>The Ashen Wastes</h3><p>Chaos, survival, rebirth — from ruin, new paths arise.</p></div></article></div></div></section>'''
write_page(ROOT/'caelterra'/'world', 'caelterra', 'Caelterra World & Lore | Factions and Realms', 'Discover the factions, regions, and mythic conflicts of Caelterra, the fantasy TCG and TRPG universe by Scrollrealm.', body_world, 'World & Lore', 2)

# Products listing
body_products = f'''<section class="section"><div class="container"><div class="product-grid">{''.join(f'<article class="product-card"><img src="../assets/images/{p["image"]}" alt="{p["name"]}"><h3>{p["name"]}</h3><p>{p["summary"]}</p><a class="btn" href="{p["slug"]}/">{p["cta"]}</a></article>' for p in products)}</div></div></section>'''
write_page(ROOT/'products', 'products', 'Caelterra Products | Starter Set, Booster Packs, Rulebook', 'Browse Caelterra products by Scrollrealm, including the Starter Set, Booster Packs, and Core Rulebook.', body_products, 'Products', 1)
for p in products:
    schema={'@context':'https://schema.org','@type':'Product','name':p['name'],'brand':{'@type':'Brand','name':'Caelterra'},'manufacturer':{'@type':'Organization','name':'Scrollrealm'},'description':p['summary'],'image':DOMAIN+f'/assets/images/{p["image"]}','url':DOMAIN+f'/products/{p["slug"]}/','offers':{'@type':'Offer','availability':'https://schema.org/PreOrder','priceCurrency':'USD','url':DOMAIN+f'/products/{p["slug"]}/'}}
    body=f'''<section class="section"><div class="container content-grid"><div class="prose"><h2>{p['name']}</h2><p>{p['summary']}</p><ul class="list"><li><strong>Product Type:</strong> {p['type']}</li><li><strong>Status:</strong> {p['status']}</li><li><strong>Universe:</strong> Caelterra</li><li><strong>Publisher:</strong> Scrollrealm</li></ul><p>This page is prepared for future retail links, preorder details, downloadable assets, reviews, and structured product metadata.</p><a class="btn btn-primary" href="../../contact/">Retail &amp; Distribution Inquiry</a></div><aside class="panel ornate"><img src="../../assets/images/{p['image']}" alt="{p['name']}"></aside></div></section>'''
    write_page(ROOT/'products'/p['slug'], 'products', f'{p["name"]} | Caelterra by Scrollrealm', p['summary'], body, 'Product', 2, schema=schema)

# Release schedule
body_release = f'''<section class="section"><div class="container panel ornate"><div class="schedule">{''.join(f'<div class="milestone"><div class="node">{icon}</div><h3>{item["title"]}</h3><time>{item["period"]}</time><p>{item["desc"]}</p></div>' for item,icon in zip(releases,['◉','♜','▤','☷']))}</div></div></section>'''
write_page(ROOT/'release-schedule', 'release', 'Caelterra Release Schedule | Upcoming TCG & TRPG Milestones', 'Track upcoming Caelterra milestones, including preview material, starter set launch, booster releases, and TRPG rulebook development.', body_release, 'Release Schedule', 1)

# News listing and detail
body_news = f'''<section class="section"><div class="container"><div class="board-list">{''.join(f'<a class="board-item" href="{n["slug"]}/"><time>{n["date"]}</time><div><h3>{n["title"]}</h3><p>{n["summary"]}</p></div><span class="badge">{n["tag"]}</span></a>' for n in news)}</div></div></section>'''
write_page(ROOT/'news', 'news', 'Caelterra News & Dev Updates | Scrollrealm', 'Read Caelterra development updates, card previews, release notes, and worldbuilding news from Scrollrealm.', body_news, 'News Board', 1)
for n in news:
    body=f'''<section class="section"><div class="container content-grid"><article class="prose"><p><span class="badge">{n['tag']}</span> <span class="meta">{n['date']}</span></p><h2>{n['title']}</h2><p>{n['summary']}</p><p>This article page is part of the static news board. Replace this placeholder with the full update, images, community links, and downloadable resources when the announcement is ready.</p><p>Recommended structure: opening summary, details, player impact, timeline, CTA, and FAQ.</p></article><aside class="panel ornate"><img src="../../assets/images/{n['image']}" alt="{n['title']}"><a class="btn" href="../">Back to News</a></aside></div></section>'''
    write_page(ROOT/'news'/n['slug'], 'news', f'{n["title"]} | Scrollrealm News', n['summary'], body, 'News', 2)

# Games, about, contact, downloads, privacy
body_games = '''<section class="section"><div class="container games-teaser"><div class="coming ornate"><p class="section-kicker">Featured Title</p><h2 class="section-title">Caelterra</h2><p class="section-sub">Scrollrealm’s flagship fantasy TCG &amp; TRPG universe.</p><a class="btn btn-primary" href="../caelterra/">Explore Caelterra</a></div><div class="placeholder-grid"><div class="placeholder">✦</div><div class="placeholder">☉</div><div class="placeholder">♢</div></div></div></section>'''
write_page(ROOT/'games', 'games', 'Games by Scrollrealm | Caelterra and Future Titles', 'Explore tabletop games by Scrollrealm, beginning with Caelterra and future fantasy game worlds.', body_games, 'Games', 1)
body_about = '''<section class="section"><div class="container content-grid"><div class="prose"><h2>Creator of Caelterra</h2><p>Scrollrealm is a tabletop game studio focused on immersive fantasy worlds, collectible strategy, and narrative roleplaying experiences.</p><p>Our flagship universe, Caelterra, is designed to support both TCG and TRPG play while leaving room for future products, organized play, lore expansions, and new games.</p><h2 id="team">Our Approach</h2><ul class="list"><li>World-first tabletop design.</li><li>Player-friendly rules and strong visual identity.</li><li>Expandable product architecture for future releases.</li></ul></div><aside class="panel ornate"><img src="../assets/images/og-caelterra.webp" alt="Caelterra key art"><h2 class="section-title">Scrollrealm</h2><p class="section-sub">Fantasy tabletop worlds for strategy, storytelling, and adventure.</p></aside></div></section>'''
write_page(ROOT/'about', 'about', 'About Scrollrealm | Creator of Caelterra', 'Scrollrealm is the tabletop game studio behind Caelterra, creating fantasy card games, roleplaying games, and immersive tabletop worlds.', body_about, 'About Scrollrealm', 1)
body_contact = '''<section class="section"><div class="container content-grid"><div class="prose"><h2>Contact Scrollrealm</h2><p>Use this page for retail, distribution, press, partnership, and community inquiries. The demo form is wired for Formspree; replace the form action with your real endpoint before launch.</p><form class="form" action="https://formspree.io/f/your-form-id" method="POST"><div class="field"><label for="name">Name</label><input id="name" name="name" required></div><div class="field"><label for="email">Email</label><input id="email" type="email" name="email" required></div><div class="field"><label for="topic">Topic</label><input id="topic" name="topic" placeholder="Retail, Press, Community, Support"></div><div class="field"><label for="message">Message</label><textarea id="message" name="message" required></textarea></div><button class="btn btn-primary" type="submit">Send Inquiry</button></form></div><aside class="panel ornate"><h2 class="section-title">Business Inquiries</h2><p class="section-sub">Retailers, distributors, press, and creators can use the form to contact Scrollrealm about Caelterra and future games.</p></aside></div></section>'''
write_page(ROOT/'contact', 'contact', 'Contact Scrollrealm | Caelterra Retail, Press & Community', 'Contact Scrollrealm for Caelterra retail, distribution, press, community, partnership, and support inquiries.', body_contact, 'Contact', 1)
body_downloads = '''<section class="section"><div class="container"><div class="board-list"><a class="board-item" href="#"><time>TBA</time><div><h3>Caelterra TCG Quick Rules</h3><p>Placeholder for future quick-start PDF.</p></div><span class="badge">PDF</span></a><a class="board-item" href="#"><time>TBA</time><div><h3>Caelterra TRPG Quickstart</h3><p>Placeholder for future TRPG download.</p></div><span class="badge">PDF</span></a></div></div></section>'''
write_page(ROOT/'downloads', '', 'Caelterra Downloads | Rulebooks and Quickstart Files', 'Download future Caelterra rulebooks, quickstart guides, card references, and tabletop resources by Scrollrealm.', body_downloads, 'Downloads', 1)
privacy = head('Privacy Policy | Scrollrealm','Privacy policy placeholder for Scrollrealm.', path='privacy', depth=0)+header('',0)+'<main id="main"><section class="section"><div class="container prose"><h1>Privacy Policy</h1><p>This is a placeholder privacy policy. Replace it with your final legal text before launch.</p></div></section></main>'+footer(0)+'</body></html>'
(ROOT/'privacy.html').write_text(privacy,encoding='utf-8')

# Robots, sitemap, CNAME, README, tools
urls = ['', 'caelterra', 'caelterra/tcg', 'caelterra/trpg', 'caelterra/world', 'products', 'products/starter-set', 'products/booster-packs', 'products/core-rulebook', 'release-schedule', 'news'] + [f'news/{n["slug"]}' for n in news] + ['games','about','contact','downloads']
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}/{u + ("/" if u else "")}</loc><lastmod>{DATE}</lastmod><changefreq>{"weekly" if u in ["news","release-schedule"] else "monthly"}</changefreq><priority>{"1.0" if u=="" else "0.8"}</priority></url>\n' for u in urls) + '</urlset>\n'
(ROOT/'sitemap.xml').write_text(sitemap,encoding='utf-8')
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n',encoding='utf-8')
(ROOT/'CNAME').write_text('scrollrealm.com\n',encoding='utf-8')
(ROOT/'.nojekyll').write_text('',encoding='utf-8')
readme = '''# Scrollrealm / Caelterra GitHub Pages Site

This package is a ready-to-upload static website for `scrollrealm.com`.

## What is included

- Complete static HTML/CSS/JS homepage and subpages
- Caelterra-first visual design for a fantasy TCG & TRPG brand
- Product pages, release schedule, static news board, company page, contact page
- SEO metadata, Open Graph image, JSON-LD structured data, `sitemap.xml`, `robots.txt`
- `CNAME` configured for `scrollrealm.com`
- Optimized WebP image assets generated for this project
- No external frontend framework or build step required

## Recommended GitHub Pages deployment

1. Create a repository such as `scrollrealm-site`.
2. Upload all files in this folder to the repository root.
3. In GitHub: Settings → Pages → Deploy from branch → main → root.
4. Confirm the custom domain is `scrollrealm.com`.
5. Configure DNS with your domain provider according to GitHub Pages instructions.
6. Submit `https://scrollrealm.com/sitemap.xml` to Google Search Console and Naver Search Advisor.

## Before launch

- Replace placeholder release windows if needed.
- Replace Formspree placeholder form action with a real form endpoint.
- Replace social links in the footer.
- Add real product purchase links once Shopify, Amazon, Kickstarter, Gamefound, or another sales channel is ready.
- Add real legal text to `privacy.html`.

## Editing content

Static content is in each page's `index.html`.
Reusable sample data is also provided in:

- `data/products.json`
- `data/releases.json`
- `data/news.json`

## Image sources

Images in `assets/images/` are generated original assets for this prototype. The original design concept preview is also included as `assets/images/design-concept-preview.png`.
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
# Put current script as generate_assets source
asset_script = '''# Asset generation source
# The original build script used to generate this package is available as /mnt/data/build_scrollrealm.py in the creation environment.
# To regenerate assets, adapt the Pillow image generation functions from that script.
'''
(ROOT/'tools'/'README.md').write_text(asset_script,encoding='utf-8')
shutil.copy('/mnt/data/build_scrollrealm.py', ROOT/'tools'/'build_scrollrealm.py')

# Basic validation: ensure no href to missing index? simple list
# Zip
zip_path = Path('/mnt/data/scrollrealm-github-pages.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for file in ROOT.rglob('*'):
        z.write(file, file.relative_to(ROOT))
print('created', ROOT)
print('zip', zip_path, zip_path.stat().st_size)
print('files', sum(1 for _ in ROOT.rglob('*') if _.is_file()))

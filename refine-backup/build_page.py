import base64, json, html
from pathlib import Path
from fontTools.ttLib import TTFont

ROOT=json.load(open('megacrew-metadata-v2.json'))
ASSETS=json.load(open('asset-map.json'))
MEDIA=json.load(open('media-map.json')) if Path('media-map.json').exists() else {}
NODES={}
def index(n):
    NODES[n['id']]=n
    for c in n.get('children',[]): index(c)
index(ROOT)
RX,RY=ROOT['absoluteBoundingBox']['x'],ROOT['absoluteBoundingBox']['y']
ESC=html.escape
def url(i):
    return MEDIA.get(i,{}).get('url','https://dunamismovement.com/wp-content/uploads/2026/10/'+ASSETS[i]['file'])
def img(i,alt='',cls=''):
    return f'<img class="{cls}" src="{url(i)}" alt="{ESC(alt,quote=True)}" loading="lazy" decoding="async">'
def color(p):
    c=p.get('color',{});return 'rgba(%s,%s,%s,%s)'%(round(c.get('r',0)*255),round(c.get('g',0)*255),round(c.get('b',0)*255),p.get('opacity',1)*c.get('a',1))
def fill(n):
    return next((color(p) for p in n.get('fills',[]) if p.get('visible',True) and p['type']=='SOLID'),'transparent')
def effects(n):
    vals=[]
    for e in n.get('effects',[]):
        if e['type'] in ['DROP_SHADOW','INNER_SHADOW'] and e.get('visible',True):
            vals.append(('%s '%('inset' if e['type']=='INNER_SHADOW' else ''))+f"{e['offset']['x']}px {e['offset']['y']}px {e['radius']}px {e.get('spread',0)}px "+color({'color':e['color']}))
    return ','.join(vals) or 'none'
FONT_WEIGHTS={'Regular':400,'Medium':500,'Bold':700,'Heavy':900}
def font_style(n,base=None):
    base=base or n
    fn=n.get('fontName') or (n.get('segments') or [{}])[0].get('fontName') or {'family':'Ageo','style':'Medium'}
    size=n.get('fontSize',base.get('fontSize',24))
    st=f"font-family:'MC{fn['family']}';font-weight:{FONT_WEIGHTS.get(fn['style'],700)};font-size:{size}px;"
    lh=n.get('lineHeight',{'unit':'AUTO'})
    if lh['unit']=='PERCENT': lv=size*lh['value']/100
    elif lh['unit']=='PIXELS':lv=lh['value']
    else:
        # Match the original font's vertical metrics used by Figma.
        suffix='.otf' if fn['family']=='Katl' else '.ttf'
        f=TTFont('/Users/macbookpro1/Library/Fonts/'+fn['family']+'-'+fn['style']+suffix)
        lv=size*(f['hhea'].ascent-f['hhea'].descent+f['hhea'].lineGap)/f['head'].unitsPerEm
    st+=f'line-height:{lv}px;'
    ls=n.get('letterSpacing',{'unit':'PERCENT','value':0})
    st+=f"letter-spacing:{size*ls.get('value',0)/100 if ls['unit']=='PERCENT' else ls.get('value',0)}px;color:{fill(n)};text-transform:{'uppercase' if n.get('textCase',base.get('textCase'))=='UPPER' else 'none'};"
    return st
def rich(i,mobile=False):
    n=NODES[i];out=[]
    for s in n.get('segments',[]):
        fn=s.get('fontName',{'family':'Ageo','style':'Medium'})
        style=(f"font-family:'MC{fn['family']}';font-weight:{FONT_WEIGHTS.get(fn['style'],500)};color:{fill(s)};" if mobile else font_style(s,n))
        out.append(f'<span style="{style}">{ESC(s["characters"]).replace(chr(10),"<br>")}</span>')
    return ''.join(out) or ESC(n.get('characters','')).replace('\n','<br>')

anchor_map={'O que é':'o-que-e','Programação':'programacao','Escolas':'escolas','Dunamis Farm':'farm','Testemunhos':'testemunhos','Valor':'valor','FAQ':'faq'}
social_map={'Instagram':'https://www.instagram.com/dunamis.1luv/','YouTube':'https://www.youtube.com/@Dunamis1LUV','TikTok':None,'WhatsApp':'https://whatsapp.com/channel/0029VavXZ8jDJ6Gx82DZr03f'}
cta_ids=[i for i,n in NODES.items() if n['type']=='FRAME' and n['name'].startswith('botão')]
asset_ids=set(ASSETS)-{'865:841','865:845','865:857','865:861','865:1053','865:1058'}
desktop=[]
def affine(n):
    m=n['absoluteTransform'];return f"width:{n['width']}px;height:{n['height']}px;transform:matrix({m[0][0]},{m[1][0]},{m[0][1]},{m[1][1]},{m[0][2]-RX},{m[1][2]-RY});"
def box(b):return f"left:{b['x']-RX}px;top:{b['y']-RY}px;width:{b['width']}px;height:{b['height']}px;"
def desc_text(n):
    return ' '.join([n.get('characters','')]+[desc_text(c) for c in n.get('children',[])]).strip()
def render(n):
    if not n.get('visible',True):return
    i=n['id']
    if i=='865:1051':
        # Original repeating fabric and wall layers, in their original stacking order.
        for g in n['children']:
            for t in g['children']:
                k='865:1053' if t['name'].startswith('tecido') else '865:1058'
                desktop.append(f'<img class="mc-node mc-texture" aria-hidden="true" src="{url(k)}" alt="" style="{box(t["absoluteBoundingBox"])}mix-blend-mode:{t["blendMode"].lower()};opacity:.5" decoding="async">')
        return
    if i in asset_ids:
        a=ASSETS[i];b=a['renderBounds'] or a['bbox']
        alt=desc_text(n)
        if i=='865:1190':alt='Adolescentes reunidos no Mega Crew'
        if i=='865:978':alt='Mega Crew 27 — DNMS e 1LUV'
        if i=='865:954':alt='Dunamis 1Luv'
        desktop.append(f'<img class="mc-node mc-art" src="{url(i)}" alt="{ESC(alt,quote=True)}" style="{box(b)}" decoding="async" '+('fetchpriority="high"' if i=='865:1190' else 'loading="lazy"')+'>')
        return
    if n['type']=='TEXT':
        tag='h2' if i in ['865:24','865:873','865:884','863:14','863:47','865:1018'] else 'div';attrs=''
        text=n.get('characters','')
        if n['name'].startswith('link') or i in [f'865:{k}' for k in range(1419,1426)]:
            tag='a';attrs=f' href="#{anchor_map.get(text,"inicio")}"'
        if i in [f'865:{k}' for k in range(1428,1432)]:
            tag='a';attrs=f' href="{social_map[text]}"' if social_map[text] else ' aria-disabled="true" data-pending-link="TikTok"'
        white='pre' if n.get('textAutoResize')=='WIDTH_AND_HEIGHT' else 'pre-wrap'
        desktop.append(f'<{tag} class="mc-node mc-text" data-node="{i}" style="{affine(n)}{font_style(n)}text-align:{n.get("textAlignHorizontal","LEFT").lower()};white-space:{white};"{attrs}>{rich(i)}</{tag}>')
    elif i!=ROOT['id'] and (n.get('fills') or n.get('strokes') or n.get('effects')):
        st=affine(n)+f'background:{fill(n)};border-radius:{n.get("cornerRadius",0)}px;box-shadow:{effects(n)};opacity:{n.get("opacity",1)};'
        if n.get('strokes'):st+=f'border:{n.get("strokeWeight",0)}px solid {color(n["strokes"][0])};'
        desktop.append(f'<div class="mc-node mc-shape" aria-hidden="true" style="{st}"></div>')
    for c in n.get('children',[]):render(c)
render(ROOT)
sections={'inicio':0,'o-que-e':950,'programacao':2750,'escolas':4130,'farm':5186,'testemunhos':6720,'valor':8340,'faq':10460}
for name,y in sections.items():desktop.append(f'<span id="mc-d-{name}" class="mc-node" style="top:{y}px"></span>')
for i in cta_ids:
    n=NODES[i]
    desktop.append(f'<a class="mc-node mc-hit mc-cta" style="{affine(n)}" href="#valor" aria-label="{ESC(desc_text(n),quote=True)}"></a>')

answers=[
    'Adolescentes de 13 a 17 anos. O Mega Crew é a escola do Dunamis 1Luv, braço de missões estudantis do Dunamis Movement.',
    'Na Dunamis Farm, em Pariquera-Açu, no interior de São Paulo.',
    'Café da manhã, almoço e jantar, hospedagem, ônibus de ida e volta para São Paulo, kit de participante e toda a programação. Cada adolescente deve levar sua própria roupa de cama.',
    'O ônibus de ida e volta para São Paulo está incluso. O ponto de encontro é a Zion Church Morumbi. A locomoção até esse ponto de encontro é responsabilidade do participante.',
    'Você pode pagar em 12 parcelas de R$ 189,45 ou R$ 2.559,00 à vista.'
]
# Real accordion controls preserve all original closed rows and expand into a readable panel.
for j in range(5):
    q=NODES['866:'+str(1493+j*2)]
    y=[10781,10901.8,11021.8,11141.8,11261.8][j]
    desktop.append(f'<button class="mc-node mc-hit mc-faq-trigger" style="left:113.9px;top:{y}px;width:1212px;height:90px" aria-expanded="false" aria-controls="mc-answer-panel" data-answer="{j}" aria-label="{ESC(q["characters"],quote=True)}"></button>')
desktop.append('<div class="mc-answer-panel" id="mc-answer-panel" hidden><button class="mc-answer-close" aria-label="Fechar resposta">×</button><h3></h3><p></p></div>')

def txt(i):return rich(i,True)
def cta(label='QUERO FAZER PARTE DISSO',purple=False):return f'<a href="#valor" class="mc-btn mc-cta {"purple" if purple else ""}">{label}</a>'
def heading(kicker,title):return f'<header class="mc-heading"><p>{kicker}</p><h2>{title}</h2></header>'
mobile=[]
mobile.append(f'<section class="mc-m-hero" id="mc-m-inicio"><img class="mc-m-bg" src="{url("865:1190")}" alt="Adolescentes reunidos no Mega Crew" fetchpriority="high"><div class="mc-m-shade"></div><nav>{img("865:1241","Mega Crew 27")}<a class="mc-btn mc-cta" href="#valor">INSCREVA-SE</a></nav><div class="mc-m-hero-content"><h1>{img("865:978","Mega Crew 27 — DNMS e 1LUV")}</h1>{cta()}</div>{img("865:972","","mc-m-doodle left")}{img("865:973","","mc-m-doodle right")}</section>')
mobile.append(f'<section class="mc-m-section cream torn" id="mc-m-o-que-e"><div class="mc-m-about-title"><h2>O QUE É?</h2>{img("865:25")}</div><div class="mc-copy">{txt("865:22")}</div>{cta(purple=True)}<figure class="mc-m-video">{img("865:19","Área do vídeo de apresentação")}{img("865:20","","mc-m-play")}</figure></section>')
mobile.append('<section class="mc-m-section mc-m-includes textured"><div class="mc-paper"><h3>O QUE ESTÁ INCLUSO</h3><ul>'+''.join('<li>'+txt('866:'+str(k))+'</li>' for k in [1523,1530,1537,1544,1551])+'</ul></div><div class="mc-paper cream"><h3>O QUE NÃO<br>ESTÁ INCLUSO</h3><ul>'+''.join('<li>'+txt('866:'+str(k))+'</li>' for k in [1561,1568,1575])+'</ul></div></section>')
mobile.append(f'<section class="mc-m-section vivid textured" id="mc-m-programacao">{heading("a parte mais irada…","PROGRAMAÇÕES")}<div class="mc-copy">{txt("865:1343")}</div><div class="mc-m-program-grid">'+''.join(img(i,label) for i,label in [('865:841','Aulas'),('865:857','Crew Girls'),('865:845','Crew Boys'),('865:861','Revival Night'),('865:853','Interclasses'),('865:865','Por série'),('865:869','Devocionais'),('865:849','Formatura')])+'</div></section>')
mobile.append(f'<section class="mc-m-section textured mc-m-schools" id="mc-m-escolas"><h2>2 escolas,<br>mesma programação!</h2><div class="mc-copy">{txt("865:883")}</div>{img("865:885","Participantes do Mega Crew","mc-m-school-photo")}<div class="mc-m-dates">{img("865:892","Escola 01: 8 a 14 de janeiro de 2027")}{img("865:897","Escola 02: 16 a 22 de janeiro de 2027")}</div>{cta()}</section>')
mobile.append(f'<section class="mc-m-section textured" id="mc-m-farm">{heading("o lugar onde tudo acontece…","DUNAMIS FARM")}<div class="mc-copy">{txt("863:16")}</div><div class="mc-m-farm-grid">')
for a,t,desc in [('865:1344','865:1347','863:23'),('865:1348',None,'863:27'),('865:1352',None,'863:31'),('865:1356',None,'863:36'),('865:1360',None,'863:40'),('865:1364',None,'863:44')]:
    title='PLAZA' if t else ''
    mobile.append('<figure>'+img(a,NODES[desc]['characters'])+(f'<h3>{title}</h3>' if title else '')+f'<figcaption>{txt(desc)}</figcaption></figure>')
mobile.append('</div></section>')
mobile.append(f'<section class="mc-m-section cream torn" id="mc-m-testemunhos">{heading("quem viveu, conta…","TESTEMUNHOS")}<div class="mc-m-stories">')
for a,q,b,s in [('865:1368','863:53','863:54','863:55'),('865:1372','863:59','863:60','863:61'),('865:1376','863:65','863:66','863:67')]:
    mobile.append('<article>'+img(a,NODES[s]['characters'])+f'<blockquote>{txt(q)}</blockquote><p>{txt(b)}</p><strong>{txt(s)}</strong></article>')
mobile.append('</div>'+cta(purple=True)+'</section>')
mobile.append(f'<section class="mc-m-section vivid textured mc-m-value" id="mc-m-valor">{img("865:931","Valor fixo de cada escola","mc-m-value-art")}<p class="mc-price">12x 189,45</p><p class="mc-cash">ou R$ 2.559,00 à vista</p>{cta("GARANTA SUA VAGA")}</section>')
mobile.append(f'<section class="mc-m-section textured mc-m-luv">{img("865:954","Dunamis 1Luv","mc-m-luv-logo")}<div class="mc-copy">{txt("869:1608")}</div>{cta()}<div class="mc-m-luv-photo">{img("865:949")}{img("865:951","Adolescentes do Dunamis 1Luv")}{img("865:955","","mc-m-luv-doodle")}</div></section>')
mobile.append('<section class="mc-m-section cream torn mc-m-faq" id="mc-m-faq"><h2>FAQ</h2>')
for j in range(5):mobile.append(f'<details><summary>{NODES["866:"+str(1493+j*2)]["characters"]}<span aria-hidden="true">+</span></summary><p>{ESC(answers[j])}</p></details>')
mobile.append('</section>')
mobile.append(f'<footer class="mc-m-section mc-m-footer">{img("865:1383","Mega Crew 27")}<p>{txt("865:1416")}</p><div class="mc-m-footer-cols"><div><h3>NAVEGUE</h3>'+''.join(f'<a href="#{slug}">{label}</a>' for label,slug in anchor_map.items())+'</div><div><h3>CONHEÇA NOSSAS REDES SOCIAIS</h3>'+''.join((f'<a href="{u}">{l}</a>' if u else f'<a aria-disabled="true" data-pending-link="{l}">{l}</a>') for l,u in social_map.items())+cta('INSCREVA-SE')+'</div></div><div class="mc-m-copyright"><p>© 2026 Dunamis Movement · Todos os direitos reservados</p><p>Dunamis Farm · Pariquera-Açu, SP</p></div></footer>')

css=Path('page.css').read_text()
fonts=''
for name in ['Ageo-Regular','Ageo-Medium','Ageo-Bold','Ageo-Heavy','Katl-Regular','Katl-Bold']:
    family,style=name.split('-');data=base64.b64encode((Path('assets')/(name+'.woff')).read_bytes()).decode()
    fonts+=f"@font-face{{font-family:'MC{family}';font-style:normal;font-weight:{FONT_WEIGHTS[style]};font-display:swap;src:url(data:font/woff;base64,{data}) format('woff')}}\n"
script=Path('page.js').read_text().replace('/*ANSWERS*/',json.dumps(answers,ensure_ascii=False)).replace('/*QUESTIONS*/',json.dumps([NODES['866:'+str(1493+j*2)]['characters'] for j in range(5)],ensure_ascii=False))
result='<style>'+fonts+css+'</style><main id="megacrew-reforma"><div class="mc-desktop"><div class="mc-stage">'+''.join(desktop)+'</div></div><div class="mc-mobile">'+''.join(mobile)+'</div></main><script>'+script+'</script>'
Path('megacrew.html').write_text(result)
print('Página gerada:',len(result),'caracteres')

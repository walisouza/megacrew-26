import base64, json, html
from pathlib import Path

ROOT=json.load(open('megacrew-metadata-v2.json'))
ASSETS=json.load(open('asset-map.json'))
MEDIA=json.load(open('media-map.json'))
NODES={}
def index(n):
    NODES[n['id']]=n
    for c in n.get('children',[]): index(c)
index(ROOT)
ESC=html.escape
FONT_WEIGHTS={'Regular':400,'Medium':500,'Bold':700,'Heavy':900}
def url(i):return MEDIA[i]['url']
def img(i,alt='',cls='',priority=False):
    a=ASSETS[i];w=a.get('renderBounds',a['bbox'])['width'];h=a.get('renderBounds',a['bbox'])['height']
    return f'<img class="{cls}" src="{url(i)}" alt="{ESC(alt,quote=True)}" width="{round(w)}" height="{round(h)}" '+('fetchpriority="high" loading="eager"' if priority else 'loading="lazy"')+' decoding="async">'
def txt(i):
    n=NODES[i];out=[]
    for s in n.get('segments',[]):
        fn=s.get('fontName',{'family':'Ageo','style':'Medium'})
        # The design's rich weights are retained; font size follows the responsive section.
        st=f"font-family:MC{fn['family']};font-weight:{FONT_WEIGHTS.get(fn['style'],500)};"
        out.append(f'<span style="{st}">{ESC(s["characters"]).replace(chr(10),"<br>")}</span>')
    return ''.join(out) or ESC(n.get('characters','')).replace('\n','<br>')
def cta(label='QUERO FAZER PARTE DISSO',purple=False):
    return f'<a href="#valor" class="mc-btn mc-cta {"purple" if purple else ""}">{label}</a>'
def heading(kicker,title):return f'<header class="mc-heading"><p>{kicker}</p><h2>{title}</h2></header>'
def edge(i,cls=''):return '<div class="mc-edge '+cls+'" aria-hidden="true">'+img(i)+'</div>'
def section_start(classes,slug=''):return f'<section class="mc-section {classes}"'+(f' id="mc-{slug}"' if slug else '')+'><div class="mc-inner">'
anchor_map={'O que é':'o-que-e','Programação':'programacao','Escolas':'escolas','Dunamis Farm':'farm','Testemunhos':'testemunhos','Valor':'valor','FAQ':'faq'}
social_map={'Instagram':'https://www.instagram.com/dunamis.1luv/','YouTube':'https://www.youtube.com/@Dunamis1LUV','TikTok':None,'WhatsApp':'https://whatsapp.com/channel/0029VavXZ8jDJ6Gx82DZr03f'}
answers=[
    'Adolescentes de 13 a 17 anos. O Mega Crew é a escola do Dunamis 1Luv, braço de missões estudantis do Dunamis Movement.',
    'Na Dunamis Farm, em Pariquera-Açu, no interior de São Paulo.',
    'Café da manhã, almoço e jantar, hospedagem, ônibus de ida e volta para São Paulo, kit de participante e toda a programação. Cada adolescente deve levar sua própria roupa de cama.',
    'O ônibus de ida e volta para São Paulo está incluso. O ponto de encontro é a Zion Church Morumbi. A locomoção até esse ponto de encontro é responsabilidade do participante.',
    'Você pode pagar em 12 parcelas de R$ 189,45 ou R$ 2.559,00 à vista.'
]
out=[]
nav=''.join(f'<a href="#{anchor_map[l]}">{l}</a>' for l in ['O que é','Programação','Dunamis Farm','Testemunhos','FAQ'])
out.append(f'<section class="mc-hero" id="mc-inicio">{img("865:1190","Adolescentes reunidos no Mega Crew","mc-hero-bg",True)}<div class="mc-hero-shade"></div><nav class="mc-inner mc-nav" aria-label="Navegação principal"><a href="#inicio" aria-label="Mega Crew — início">{img("865:1241","Mega Crew 27",priority=True)}</a><div class="mc-nav-links">{nav}</div>{cta("INSCREVA-SE")}</nav><div class="mc-inner mc-hero-content"><h1>{img("865:978","Mega Crew 27 — DNMS e 1LUV",priority=True)}</h1>{cta()}</div>{img("865:972","","mc-hero-doodle left")}{img("865:973","","mc-hero-doodle right")}<div class="mc-hero-edge" aria-hidden="true"></div></section>')
out.append(section_start('cream mc-about','o-que-e')+f'<div class="mc-about-copy"><div class="mc-about-title"><h2>O QUE É?</h2>{img("865:25")}</div><div class="mc-copy">{txt("865:22")}</div>{cta(purple=True)}</div><figure class="mc-video">{img("865:19","Área do vídeo de apresentação")}{img("865:20","","mc-play")}</figure></div><div class="mc-about-edge" aria-hidden="true"></div></section>')
out.append(section_start('textured mc-includes')+'<div class="mc-paper"><h3>O QUE ESTÁ INCLUSO</h3><ul>'+''.join('<li>'+img('866:'+str(icon),'','mc-list-icon')+txt('866:'+str(k))+'</li>' for k,icon in [(1523,1518),(1530,1525),(1537,1532),(1544,1539),(1551,1546)])+'</ul></div><div class="mc-paper cream"><h3>O QUE NÃO<br>ESTÁ INCLUSO</h3><ul>'+''.join('<li>'+img('866:'+str(icon),'','mc-list-icon')+txt('866:'+str(k))+'</li>' for k,icon in [(1561,1556),(1568,1563),(1575,1570)])+'</ul></div></div></section>')
out.append(section_start('vivid textured mc-program','programacao').replace('<div class="mc-inner">',edge('865:94','mc-edge-top mc-program-edge')+'<div class="mc-inner">')+heading('a parte mais irada…','PROGRAMAÇÕES')+f'<div class="mc-copy mc-centered-copy">{txt("865:1343")}</div><div class="mc-program-grid">'+''.join(img(i,label) for i,label in [('865:841','Aulas'),('865:857','Crew Girls'),('865:845','Crew Boys'),('865:861','Revival Night'),('865:853','Interclasses'),('865:865','Por série'),('865:869','Devocionais'),('865:849','Formatura')])+'</div></div>'+edge('866:1580','mc-edge-bottom')+'</section>')
out.append(section_start('textured mc-schools','escolas')+f'<div class="mc-school-copy"><h2>2 escolas,<br>mesma programação!</h2><div class="mc-copy">{txt("865:883")}</div><div class="mc-dates">{img("865:892","Escola 01: 8 a 14 de janeiro de 2027")}{img("865:897","Escola 02: 16 a 22 de janeiro de 2027")}</div></div>{img("865:885","Participantes do Mega Crew","mc-school-photo")}<div class="mc-school-cta">{cta()}</div></div></section>')
out.append(section_start('textured mc-farm','farm')+heading('o lugar onde tudo acontece…','DUNAMIS FARM')+f'<div class="mc-copy mc-centered-copy">{txt("863:16")}</div><div class="mc-farm-grid">')
for a,t,desc,label in [('865:1344',True,'863:23','Plaza'),('865:1348',False,'863:27','Auditório'),('865:1352',False,'863:31','Refeitório'),('865:1356',False,'863:36','Casas'),('865:1360',False,'863:40','Campo'),('865:1364',False,'863:44','Quadra')]:
    out.append('<figure><div class="mc-farm-art">'+img(a,label)+(f'<h3>PLAZA</h3>' if t else '')+'</div><figcaption>'+txt(desc)+'</figcaption></figure>')
out.append('</div></div></section>')
out.append(section_start('cream mc-stories','testemunhos').replace('<div class="mc-inner">',edge('866:1578','mc-edge-top')+'<div class="mc-inner">')+heading('quem viveu, conta…','TESTEMUNHOS')+'<div class="mc-stories-grid">')
for a,q,b,s in [('865:1368','863:53','863:54','863:55'),('865:1372','863:59','863:60','863:61'),('865:1376','863:65','863:66','863:67')]:
    out.append('<article>'+img(a,NODES[s]['characters'])+f'<blockquote>{txt(q)}</blockquote><p>{txt(b)}</p><strong>{txt(s)}</strong></article>')
out.append('</div><div class="mc-center">'+cta(purple=True)+'</div></div>'+edge('866:1579','mc-edge-bottom')+'</section>')
out.append(section_start('vivid textured mc-value','valor')+img('865:931','Valor fixo de cada escola','mc-value-art')+f'<div class="mc-value-copy"><p class="mc-price">12x 189,45</p><p class="mc-cash">ou R$ 2.559,00 à vista</p>{cta("GARANTA SUA VAGA")}</div></div>'+edge('866:1580','mc-edge-bottom')+'</section>')
out.append(section_start('textured mc-luv')+f'<div class="mc-luv-copy">{img("865:954","Dunamis 1Luv","mc-luv-logo")}<div class="mc-copy">{txt("869:1608")}</div>{cta()}</div><div class="mc-luv-photo">{img("865:949","","mc-luv-frame")}{img("865:951","Adolescentes do Dunamis 1Luv","mc-luv-people")}{img("865:955","","mc-luv-doodle")}</div></div></section>')
out.append(section_start('cream mc-faq','faq').replace('<div class="mc-inner">',edge('866:1581','mc-edge-top')+'<div class="mc-inner">')+'<h2>FAQ</h2><div class="mc-faq-list">')
for j in range(5):out.append(f'<details><summary><span class="mc-question">{NODES["866:"+str(1493+j*2)]["characters"]}</span><span class="mc-plus" aria-hidden="true">+</span></summary><p>{ESC(answers[j])}</p></details>')
out.append('</div></div></section>')
socials=''.join((f'<a href="{u}">{l}</a>' if u else f'<a aria-disabled="true" data-pending-link="{l}">{l}</a>') for l,u in social_map.items())
links=''.join(f'<a href="#{slug}">{label}</a>' for label,slug in anchor_map.items())
out.append(f'<footer class="mc-section mc-footer">{edge("866:1582","mc-edge-top")}<div class="mc-inner"><div class="mc-footer-brand">{img("865:1383","Mega Crew 27")}<p>{txt("865:1416")}</p></div><div class="mc-footer-links"><h3>NAVEGUE</h3>{links}</div><div class="mc-footer-social"><h3>CONHEÇA NOSSAS REDES SOCIAIS</h3>{socials}{cta("INSCREVA-SE")}</div><div class="mc-copyright"><p>© 2026 Dunamis Movement · Todos os direitos reservados</p><p>Dunamis Farm · Pariquera-Açu, SP</p></div></div></footer>')
css=Path('page.css').read_text()
fonts=''
for name in ['Ageo-Regular','Ageo-Medium','Ageo-Bold','Ageo-Heavy','Katl-Regular','Katl-Bold']:
    family,style=name.split('-');data=base64.b64encode((Path('assets')/(name+'.woff')).read_bytes()).decode()
    fonts+=f"@font-face{{font-family:MC{family};font-style:normal;font-weight:{FONT_WEIGHTS[style]};font-display:swap;src:url(data:font/woff;base64,{data}) format('woff')}}\n"
result='<style>'+fonts+css+'</style><main id="megacrew-reforma">'+''.join(out)+'</main><script>'+Path('page.js').read_text()+'</script>'
Path('megacrew.html').write_text(result)
print('Página gerada:',len(result),'caracteres')

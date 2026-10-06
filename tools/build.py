#!/usr/bin/env python3
"""Build the static GitHub Pages tree for BoxTech gifts (event-gift.grok.me mirror).
Usage: build.py [BASE] [SITE_URL]
  BASE      '/theboxgift/' for a project site, '/' for a user/org root site.
  SITE_URL  absolute site URL for og:image (optional).
Source: pristine mirror in /workspace/boxgift-mirror (assets, catalog, og.jpg, favicon.svg, __grok/icon-180.png).
"""
import os, sys, shutil, re, json
SRC = '/workspace/boxgift-mirror'
OUT = os.environ.get('OUT', '/workspace/boxgift-pages')
BASE = sys.argv[1] if len(sys.argv) > 1 else '/theboxgift/'
if not BASE.startswith('/'): BASE = '/' + BASE
if not BASE.endswith('/'): BASE += '/'
SITE = (sys.argv[2] if len(sys.argv) > 2 else '').rstrip('/')
BP = BASE.rstrip('/')  # router basepath: '' for root, '/theboxgift' for project

COLLECTIONS = 'boxes carry desk drink mark nature prayer scent tech welcome'.split()
PRODUCTS = ('welcome-folio welcome-gray welcome-green box-flying box-drawer box-handle nature-cork nature-trio nature-seed '
            'tech-bank tech-multi tech-adapter tech-mag tech-note drink-cork drink-thermos drink-infuser desk-pen desk-note '
            'desk-stand prayer-agate prayer-stone prayer-promo scent-reed scent-car scent-burner carry-sleeve carry-certificate '
            'carry-tote carry-pouch mark-key mark-card mark-lanyard mark-brooch').split()
ROUTES = ['list'] + ['collection/' + c for c in COLLECTIONS] + ['product/' + p for p in PRODUCTS]

# clean OUT but keep .git
os.makedirs(OUT, exist_ok=True)
for n in os.listdir(OUT):
    if n in ('.git', 'README.md'): continue
    p = os.path.join(OUT, n)
    shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)
shutil.copytree(f'{SRC}/assets', f'{OUT}/assets')
shutil.copytree(f'{SRC}/catalog', f'{OUT}/catalog')
for f in ('og.jpg', 'favicon.svg'): shutil.copy(f'{SRC}/{f}', f'{OUT}/{f}')
shutil.copy(f'{SRC}/__grok/icon-180.png', f'{OUT}/apple-touch-icon.png')

def patch(name, pairs):
    p = f'{OUT}/assets/{name}'
    s = open(p, encoding='utf8').read()
    for a, b, n in pairs:
        c = s.count(a)
        assert c == n, (name, a[:60], c, n)
        s = s.replace(a, b)
    open(p, 'w', encoding='utf8').write(s)

# 1) entry bundle: client-only createRoot (no SSR hydration), router basepath, head links
patch('index-DLFO-8IC.js', [
    ('e.hydrateRoot=function(e,t,n){if(!o(e))throw Error(a(299));',
     'e.createRoot=function(e,t){if(!o(e))throw Error(a(299));var r=!1,i=``,s=Oc,c=kc,l=Ac,u=null;return t!=null&&(!0===t.unstable_strictMode&&(r=!0),t.identifierPrefix!==void 0&&(i=t.identifierPrefix),t.onUncaughtError!==void 0&&(s=t.onUncaughtError),t.onCaughtError!==void 0&&(c=t.onCaughtError),t.onRecoverableError!==void 0&&(l=t.onRecoverableError)),t=lh(e,1,!1,null,null,r,i,u,s,c,l,Uh),t.context=uh(null),e[Pt]=t.current,Wf(e),new Wh(t)},e.hydrateRoot=function(e,t,n){if(!o(e))throw Error(a(299));', 1),
    ('e.stores.ids.get().length||await Zn(e),e}var iv=rv', 'e}var iv=rv', 1),
    ('(0,cv.hydrateRoot)(document,(0,R.jsx)(L.StrictMode,{children:(0,R.jsx)(sv,{})}))',
     '(0,cv.createRoot)(document).render((0,R.jsx)(L.StrictMode,{children:(0,R.jsx)(sv,{})}))', 1),
    ('e.update({basepath:``,serializationAdapters:t})', 'e.update({basepath:`%s`,serializationAdapters:t})' % BP, 1),
    ('{rel:`manifest`,href:`/__grok/manifest.webmanifest`},{rel:`apple-touch-icon`,href:`/__grok/icon-180.png`}',
     '{rel:`manifest`,href:`%smanifest.webmanifest`},{rel:`apple-touch-icon`,href:`%sapple-touch-icon.png`}' % (BASE, BASE), 1),
    ('href:`/favicon.svg`}', 'href:`%sfavicon.svg`},{rel:`icon`,href:`%sfavicon.ico`,sizes:`48x48`}' % (BASE, BASE), 1),
    ('`/assets/styles-C6nPWCr9.css`', '`%sassets/styles-C6nPWCr9.css`' % BASE, 1),
])
# 2) Vite dynamic-import preload base
patch('preload-helper-CTNSAW6c.js', [('B=function(e){return`/`+e}', 'B=function(e){return`%s`+e}' % BASE, 1)])
# 3) catalog image paths
patch('locale-LgrRR7N2.js', [('`/catalog/', '`%scatalog/' % BASE, 11)])
patch('routes-T_lj7gbW.js', [('`/catalog/', '`%scatalog/' % BASE, 2)])

og = (SITE + '/og.jpg') if SITE else (BASE + 'og.jpg')
shell = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>BoxTech gifts — كتالوج ٢٠٢٦</title>
<meta name="description" content="كتالوج BoxTech gifts ٢٠٢٦ للهدايا الدعائية وأطقم الترحيب."/>
<meta name="theme-color" content="#F6F1E7"/>
<meta property="og:title" content="BoxTech gifts"/>
<meta property="og:description" content="كتالوج BoxTech gifts ٢٠٢٦ للهدايا الدعائية وأطقم الترحيب."/>
<meta property="og:image" content="{og}"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta name="twitter:card" content="summary_large_image"/>
<link rel="icon" type="image/svg+xml" href="{BASE}favicon.svg"/>
<link rel="icon" href="{BASE}favicon.ico" sizes="48x48"/>
<link rel="apple-touch-icon" href="{BASE}apple-touch-icon.png"/>
<link rel="manifest" href="{BASE}manifest.webmanifest"/>
<link rel="stylesheet" href="{BASE}assets/styles-C6nPWCr9.css"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&amp;family=Fraunces:ital,wght@0,500;0,600;1,500&amp;family=IBM+Plex+Sans+Arabic:wght@400;500;600&amp;display=swap"/>
<link rel="modulepreload" href="{BASE}assets/index-DLFO-8IC.js"/>
<link rel="modulepreload" href="{BASE}assets/locale-LgrRR7N2.js"/>
<link rel="modulepreload" href="{BASE}assets/routes-T_lj7gbW.js"/>
<script>window["$_TSR"]=window["$_TSR"]||{{buffer:[],initialized:!1,e:function(){{}},c:function(){{}},p:function(e){{this.initialized?e():this.buffer.push(e)}},h:function(){{this.initialized=!0;var b=this.buffer.splice(0);for(var i=0;i<b.length;i++)b[i]()}},router:{{manifest:{{routes:{{}}}},matches:[]}}}};</script>
</head>
<body>
<div id="root"></div>
<script type="module" src="{BASE}assets/index-DLFO-8IC.js"></script>
</body>
</html>
'''
for r in [''] + ROUTES:
    os.makedirs(f'{OUT}/{r}', exist_ok=True)
    open(f'{OUT}/{r}/index.html' if r else f'{OUT}/index.html', 'w', encoding='utf8').write(shell)
open(f'{OUT}/404.html', 'w', encoding='utf8').write(shell)  # deep-link fallback (GitHub Pages serves it for any missing path)
json.dump({"name": "BoxTech gifts", "short_name": "BoxTech gifts", "lang": "ar", "dir": "rtl", "id": BASE, "start_url": BASE,
           "scope": BASE, "display": "standalone", "background_color": "#F6F1E7", "theme_color": "#F6F1E7",
           "icons": [{"src": BASE + "apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}]},
          open(f'{OUT}/manifest.webmanifest', 'w', encoding='utf8'), ensure_ascii=False, indent=2)
open(f'{OUT}/robots.txt', 'w').write('User-agent: *\nAllow: /\n')
if SITE:
    urls = [SITE + '/'] + [f'{SITE}/{r}' for r in ROUTES]
    open(f'{OUT}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join(f'<url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    open(f'{OUT}/robots.txt', 'a').write(f'Sitemap: {SITE}/sitemap.xml\n')
open(f'{OUT}/.nojekyll', 'w').close()
try:
    from PIL import Image
    Image.open(f'{OUT}/apple-touch-icon.png').convert('RGBA').save(f'{OUT}/favicon.ico', sizes=[(32, 32), (48, 48)])
except Exception as e:
    print('favicon.ico skipped:', e)
os.makedirs(f'{OUT}/tools', exist_ok=True)
shutil.copy(os.path.abspath(__file__), f'{OUT}/tools/build.py')
print(f'built {OUT} with BASE={BASE} basepath={BP!r} routes={len(ROUTES)+1}')

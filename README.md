# BoxTech gifts — كتالوج ٢٠٢٦ (static GitHub Pages build)

Arabic-first (RTL, with an English toggle) catalog of corporate & welcome gifts, mirrored from
https://event-gift.grok.me and published as a **client-only SPA** on GitHub Pages:

**Live:** https://theaterstage.github.io/theboxgift/

- Routes: `/`, `/list` (request list), `/collection/:slug` (10 collections), `/product/:id` (34 products).
- No login, no server: the request list lives in the browser's `localStorage`; requests are sent via WhatsApp
  (`wa.me`), copy-to-clipboard, or print.
- `index.html`, `404.html` and every route folder contain the same SPA shell; `404.html` is the deep-link fallback.
- Entry bundle `assets/index-DLFO-8IC.js` is patched: `createRoot` instead of SSR `hydrateRoot`, router `basepath`.

## Base path / moving to a root site
Built for the project path `/theboxgift/`. To rebuild for another base (e.g. a user/org root site):

```sh
python3 tools/build.py /                 https://<org>.github.io          # root site
python3 tools/build.py /theboxgift/      https://theaterstage.github.io/theboxgift   # this repo
```
(`tools/build.py` regenerates the tree from the pristine mirror in `/workspace/boxgift-mirror`.)

#!/usr/bin/env node
// Render the built site in a real browser. No deployed-site mutations or analytics requests.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const assert = require('node:assert/strict');

const root = path.resolve(process.argv[2] || '_site');
const artifacts = path.resolve(process.argv[3] || '.artifacts/browser');
const baseline = process.argv.includes('--baseline');
const failures = [];
let checks = 0;
const check = (ok, message) => { checks++; if (!ok) failures.push(message); };
const types = { '.html': 'text/html', '.png': 'image/png', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.css': 'text/css', '.js': 'text/javascript', '.pdf': 'application/pdf', '.xml': 'application/xml' };
function htmlFiles(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(entry => {
    const file = path.join(dir, entry.name);
    return entry.isDirectory() ? htmlFiles(file) : file.endsWith('.html') ? [file] : [];
  });
}
const routes = htmlFiles(root).map(file => '/' + path.relative(root, file).split(path.sep).join('/').replace(/index\.html$/, ''));
assert(routes.includes('/'), 'Build the site before running browser checks');
fs.mkdirSync(artifacts, { recursive: true });
const server = http.createServer((req, res) => {
  let file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://localhost').pathname));
  if (!file.startsWith(root + path.sep) && file !== root) { res.writeHead(403).end(); return; }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!fs.existsSync(file)) { res.writeHead(404).end(); return; }
  res.setHeader('Content-Type', types[path.extname(file)] || 'application/octet-stream');
  fs.createReadStream(file).pipe(res);
});

(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  try {
    for (const width of [320, 390, 768, 1440]) {
      const context = await browser.newContext({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
      // External services are not prerequisites for reading the site. This also exercises fallback fonts.
      await context.route('**/*', route => new URL(route.request().url()).origin === origin ? route.continue() : route.abort());
      const page = await context.newPage();
      page.on('pageerror', error => failures.push(`${width}px JavaScript: ${error.message}`));
      for (const route of routes) {
        const response = await page.goto(origin + route);
        check(response.status() === 200, `${width}px ${route}: HTTP status`);
        check(await page.locator('h1').isVisible(), `${width}px ${route}: H1 hidden`);
        for (const name of ['Writing', 'Work', 'Contact']) {
          check(await page.locator('nav.top').getByRole('link', { name, exact: true }).isVisible(), `${width}px ${route}: ${name} navigation hidden`);
        }
        for (const img of await page.locator('img[loading="lazy"]').all()) {
          await img.scrollIntoViewIfNeeded();
          await img.evaluate(el => el.decode());
        }
        await page.evaluate(() => scrollTo(0, 0));
        const layout = await page.evaluate(() => ({
          overflow: document.documentElement.scrollWidth > innerWidth + 1,
          overflowNodes: [...document.querySelectorAll('body *')].filter(el => {
            const r = el.getBoundingClientRect();
            return r.width > 0 && r.right > innerWidth + 1;
          }).slice(0, 12).map(el => `${el.tagName}.${el.className}: ${el.getBoundingClientRect().right.toFixed(1)}px`),
          clipped: [...document.querySelectorAll('h1, h2, h3, nav.top a, .hero .actions a')].filter(el => {
            const rect = el.getBoundingClientRect();
            return rect.width > 0 && (rect.left < -1 || rect.right > innerWidth + 1);
          }).map(el => el.textContent.trim()),
          brokenImages: [...document.images].filter(img => !img.complete || !img.naturalWidth).map(img => img.src),
        }));
        check(!layout.overflow, `${width}px ${route}: horizontal page overflow (${layout.overflowNodes.join('; ')})`);
        check(!layout.clipped.length, `${width}px ${route}: clipped content ${layout.clipped.join(', ')}`);
        check(!layout.brokenImages.length, `${width}px ${route}: broken images ${layout.brokenImages}`);
        if ((route.startsWith('/notes/') && route !== '/notes/') && !baseline) {
          const crumbs = page.getByRole('navigation', { name: 'Breadcrumb', exact: true });
          check(await crumbs.isVisible(), `${width}px ${route}: breadcrumb hidden`);
          check(await crumbs.locator('[aria-current="page"]').innerText() === await page.locator('h1').innerText(), `${width}px ${route}: breadcrumb title mismatch`);
          const destination = '/notes/';
          await crumbs.getByRole('link', { name: 'Lab Notes', exact: true }).click();
          check(new URL(page.url()).pathname === destination, `${width}px ${route}: breadcrumb destination`);
          await page.goto(origin + route);
        }
        if (route === '/' && !baseline) {
          const writing = page.locator('.hero .actions').getByRole('link', {name:'Read my writing'});
          check(await writing.isVisible(), `${width}px homepage: writing button hidden`);
          await writing.click();
          check(new URL(page.url()).pathname === '/notes/', `${width}px: writing button destination`);
          await page.goto(origin + route);
        }
        // Keep full-page evidence for every route, at both desktop and narrow mobile widths.
        if (width === 390 || width === 1440) {
          await page.screenshot({ path: path.join(artifacts, `${width}-${route.replace(/\//g, '_') || 'home'}.png`), fullPage: true });
        }
      }
      // Exercise actual navigation when available, rather than merely checking hrefs.
      await page.goto(origin + '/');
      await page.keyboard.press('Tab');
      const focus = await page.evaluate(() => ({
        tag: document.activeElement.tagName,
        outline: getComputedStyle(document.activeElement).outlineStyle,
        width: getComputedStyle(document.activeElement).outlineWidth,
      }));
      check(focus.tag === 'A' && focus.outline !== 'none' && focus.width !== '0px', `${width}px: keyboard focus lacks a visible outline`);
      for (const [name, expected] of [['Writing', '/notes/'], ['Work', '/#work'], ['Contact', '/#contact']]) {
        const link = page.locator('nav.top').getByRole('link', { name, exact: true });
        if (await link.isVisible()) {
          await link.click();
          check(page.url() === origin + expected, `${width}px: ${name} navigation destination`);
          if (expected.includes('#')) {
            await page.waitForFunction(selector => document.querySelector(selector).getBoundingClientRect().top < 250 || scrollY + innerHeight >= document.documentElement.scrollHeight - 1, expected.slice(1), { timeout: 3000 }).catch(() => {});
            const top = await page.locator(expected.slice(1)).evaluate(el => el.getBoundingClientRect().top);
            const bottom = await page.locator('header.bar').evaluate(el => el.getBoundingClientRect().bottom);
            const atEnd = await page.evaluate(() => scrollY + innerHeight >= document.documentElement.scrollHeight - 1);
            check((top < 250 || atEnd) && top < 860 && top >= Math.max(0, bottom) - 1, `${width}px: ${name} target obscured or not scrolled into view`);
          }
          await page.goto(origin + '/');
        }
      }
      await context.close();
    }
    for (const javaScriptEnabled of [false, true]) {
      const context = await browser.newContext({ viewport: { width: 390, height: 844 }, javaScriptEnabled });
      await context.route('**/*', route => new URL(route.request().url()).origin === origin ? route.continue() : route.abort());
      if (javaScriptEnabled) await context.addInitScript(() => { window.IntersectionObserver = undefined; });
      const page = await context.newPage();
      for (const route of routes) {
        await page.goto(origin + route);
        check(await page.locator('h1').isVisible(), `no-script-dependency ${route}: H1 hidden`);
        const clippedTables = await page.locator('.article-body table').evaluateAll(tables => tables.filter(table => {
          if (table.getBoundingClientRect().right <= innerWidth + 1) return false;
          for (let el = table; el; el = el.parentElement) {
            if (['auto', 'scroll'].includes(getComputedStyle(el).overflowX) && el.getBoundingClientRect().right <= innerWidth + 1) return false;
          }
          return true;
        }).length);
        check(!clippedTables, `no-script-dependency ${route}: ${clippedTables} tables clipped without scrolling`);
      }
      await page.goto(origin + '/');
      const hidden = await page.locator('.reveal').evaluateAll(nodes => nodes.filter(el => Number(getComputedStyle(el).opacity) === 0).length);
      check(hidden === 0, `${javaScriptEnabled ? 'missing observer' : 'no JS'}: ${hidden} homepage blocks invisible`);
      check(await page.locator('nav.top').isVisible(), `${javaScriptEnabled ? 'missing observer' : 'no JS'}: navigation hidden`);
      await page.screenshot({ path: path.join(artifacts, javaScriptEnabled ? 'missing-observer.png' : 'no-js.png'), fullPage: true });
      await context.close();
    }
    // Inspect the actual typography separately from the deterministic fallback-font matrix.
    for (const width of [390, 1440]) {
      const context = await browser.newContext({ viewport: { width, height: 1000 } });
      await context.route('**/*', route => {
        const url = new URL(route.request().url());
        return url.origin === origin || ['fonts.googleapis.com', 'fonts.gstatic.com'].includes(url.hostname) ? route.continue() : route.abort();
      });
      const page = await context.newPage();
      await page.goto(origin + '/');
      await page.evaluate(() => document.fonts.ready);
      await page.screenshot({ path: path.join(artifacts, `${width}-home-top.png`) });
      check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${width}px: loaded-font homepage overflow`);
      await context.close();
    }
    fs.writeFileSync(path.join(artifacts, 'results.json'), JSON.stringify({ checks, routes, failures }, null, 2) + '\n');
    for (const failure of failures) console.error('FAIL: ' + failure);
    console.log(`${checks} browser checks over ${routes.length} pages: ${failures.length} failure(s). Screenshots: ${artifacts}`);
    process.exitCode = failures.length ? 1 : 0;
  } finally {
    await browser.close();
    server.close();
  }
})().catch(error => { console.error(error); server.close(); process.exitCode = 1; });

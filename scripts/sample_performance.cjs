#!/usr/bin/env node
// Controlled local lab samples, not field Core Web Vitals or an SEO ranking score.
const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const root = path.resolve(process.argv[2]);
const output = process.argv[3];
const routes = process.argv.slice(4);
if (!output || !routes.length) throw new Error('Usage: node scripts/sample_performance.cjs BUILD OUTPUT_JSON ROUTE...');
const server = http.createServer((req, res) => {
  let file = path.resolve(root, '.' + new URL(req.url, 'http://localhost').pathname);
  if (file !== root && !file.startsWith(root + path.sep)) return res.writeHead(403).end();
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!fs.existsSync(file)) return res.writeHead(404).end();
  const ext = path.extname(file);
  res.setHeader('Content-Type', ({'.html':'text/html','.png':'image/png','.svg':'image/svg+xml','.ico':'image/x-icon'})[ext] || 'application/octet-stream');
  fs.createReadStream(file).pipe(res);
});
(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  const samples = [];
  try {
    for (const profile of [
      {name:'mobile',width:390,height:844,latency:150,mbps:1.6,cpu:4},
      {name:'desktop',width:1440,height:1000,latency:40,mbps:10,cpu:1},
    ]) {
      for (const route of routes) for (let run = 1; run <= 3; run++) {
        const context = await browser.newContext({viewport:profile,reducedMotion:'reduce'});
        await context.route('**/*', r => new URL(r.request().url()).origin === origin ? r.continue() : r.abort());
        const page = await context.newPage();
        const cdp = await context.newCDPSession(page);
        await cdp.send('Network.enable');
        await cdp.send('Network.setCacheDisabled', {cacheDisabled:true});
        await cdp.send('Network.emulateNetworkConditions', {offline:false,latency:profile.latency,downloadThroughput:profile.mbps*1e6/8,uploadThroughput:profile.mbps*1e6/8});
        await cdp.send('Emulation.setCPUThrottlingRate', {rate:profile.cpu});
        await page.addInitScript(() => {
          window.lab = {lcp:0,cls:0};
          new PerformanceObserver(list => {for (const e of list.getEntries()) window.lab.lcp=e.startTime;}).observe({type:'largest-contentful-paint',buffered:true});
          new PerformanceObserver(list => {for (const e of list.getEntries()) if (!e.hadRecentInput) window.lab.cls+=e.value;}).observe({type:'layout-shift',buffered:true});
        });
        await page.goto(origin + route, {waitUntil:'load'});
        await page.waitForTimeout(1000);
        const metrics = await page.evaluate(() => ({...window.lab,
          encodedBytes:performance.getEntriesByType('navigation').concat(performance.getEntriesByType('resource')).reduce((n,e)=>n+e.encodedBodySize,0),
          domNodes:document.querySelectorAll('*').length,
          images:[...document.images].map(i=>({src:new URL(i.src).pathname,width:i.naturalWidth,height:i.naturalHeight,renderedWidth:Math.round(i.getBoundingClientRect().width)})),
        }));
        samples.push({profile:profile.name,route,run,...metrics});
        await context.close();
      }
    }
    fs.writeFileSync(output, JSON.stringify({chromium:browser.version(),conditions:'Local HTTP, cold cache, external requests blocked, fallback fonts, reduced motion, 1s post-load observation; mobile 1.6Mbps/150ms/4x CPU, desktop 10Mbps/40ms/1x CPU. CLS is a short-window sum, not a field session-window score.',samples},null,2)+'\n');
    console.log(`${samples.length} samples written to ${output}`);
  } finally {await browser.close();server.close();}
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});

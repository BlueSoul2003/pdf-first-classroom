'use strict';
const assert=require('node:assert/strict');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const fs=require('node:fs');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..');
const file=process.env.CLASSROOM_HTML?path.resolve(process.env.CLASSROOM_HTML):path.join(root,'examples/eye-detecting-light/classroom.html');
let browser;
(async()=>{
 browser=await chromium.launch({headless:true,...(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{})});
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(file).href);await page.evaluate(()=>Presenter.whenReady());
 assert.equal(await page.locator('#language option').count(),5);
 assert.equal(await page.locator('.answer.visible').count(),0);
 await page.keyboard.press('Space');
 assert.equal(await page.locator('.answer.visible').count(),2,'Bilingual answers reveal together');
 await page.keyboard.press('ArrowRight');await page.keyboard.press('ArrowRight');await page.evaluate(()=>Presenter.whenReady());
 assert.equal(await page.evaluate(()=>Presenter.getState().page),1);
 await page.keyboard.press('ArrowLeft');await page.evaluate(()=>Presenter.whenReady());
 assert.equal(await page.evaluate(()=>Presenter.getState().page),0);
 assert.equal(await page.evaluate(()=>Presenter.getState().reveals['en-zh:0']),2);
 await page.click('[data-open="notes-dialog"]');await page.locator('#note').fill('Teacher note retained');
 await page.keyboard.press('ArrowLeft');assert.equal(await page.evaluate(()=>Presenter.getState().reveals['en-zh:0']),2);
 await page.click('#notes-dialog [data-close]');await page.reload();await page.evaluate(()=>Presenter.whenReady());
 assert.equal(await page.evaluate(()=>Presenter.getState().notes['en-zh:0']),'Teacher note retained');
 await page.keyboard.press('ArrowRight');await page.evaluate(()=>Presenter.whenReady());
 for(let i=0;i<4;i++)await page.keyboard.press('Space');await page.keyboard.press('ArrowRight');
 assert.equal(await page.evaluate(()=>Presenter.getState().page),1,'Final page stops');
 for(const code of ['en','zh','ms','ms-zh','en-zh']){
  await page.selectOption('#language',code);await page.evaluate(()=>Presenter.whenReady());
  const total=await page.evaluate(()=>Presenter.getPageInfo().total);
  for(let i=0;i<total;i++){
   await page.evaluate(i=>Presenter.goToPage(i),i);await page.evaluate(()=>Presenter.whenReady());
   assert.equal(await page.locator('#page-image').evaluate(img=>img.naturalWidth),2380);
  }
 }
 await page.selectOption('#language','en-zh');await page.evaluate(()=>Presenter.whenReady());
 await page.selectOption('#zoom','fit');await page.locator('#heading').click();
 const screenshots=process.env.TEST_OUTPUT_DIR?path.resolve(process.env.TEST_OUTPUT_DIR):path.join(root,'test-results');fs.mkdirSync(screenshots,{recursive:true});
 await page.screenshot({path:path.join(screenshots,'classroom.png')});
 await page.selectOption('#zoom','150');await page.locator('#viewport').evaluate(el=>el.scrollTo({top:900,behavior:'instant'}));await page.screenshot({path:path.join(screenshots,'enlarged.png')});
 await page.emulateMedia({reducedMotion:'reduce'});await page.selectOption('#zoom','fit');
 await page.evaluate(()=>Presenter.goToPage(1));await page.evaluate(()=>Presenter.whenReady());
 assert.equal(await page.evaluate(()=>document.getElementById('paper').getAnimations().length),0);
 const videoPage=await browser.newPage();
 await videoPage.route('**/*youtube*',route=>route.fulfill({contentType:'text/html',body:'Video fixture'}));
 const html=fs.readFileSync(file,'utf8');
 const match=html.match(/(<script id="presenter-data" type="application\/json">)([\s\S]*?)(<\/script>)/);
 const data=JSON.parse(match[2]);data.lessons[0].video={id:'abcdefghijk',title:{en:'Video fixture'}};
 await videoPage.setContent(html.replace(match[0],match[1]+JSON.stringify(data).replace(/</g,'\\u003c')+match[3]));await videoPage.evaluate(()=>Presenter.whenReady());
 await videoPage.click('#video-open');await videoPage.click('#load-video');
 assert.equal(await videoPage.locator('#video-frame a').getAttribute('href'),'https://www.youtube.com/watch?v=abcdefghijk');
 assert.equal(await videoPage.locator('#video-frame a').textContent(),'Open on YouTube');
 await videoPage.close();
 assert.deepEqual(errors,[]);
 await browser.close();console.log('PASS keyboard boundaries, bilingual reveals, notes, reload, nine 2380px pages, reduced motion, and screenshots.');
})().catch(async error=>{console.error(error);await browser?.close();process.exitCode=1;});

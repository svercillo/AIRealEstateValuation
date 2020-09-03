const puppeteer = require('puppeteer');
const devices = require('puppeteer/DeviceDescriptors');
const iPhonex = devices['iPhone X'];
puppeteer.launch({headless:false}).then(async browser => {
  const page = await browser.newPage();
  //We use here page.emulate so no more need to set the viewport separately
  //await page.setViewport({ width: 1280, height: 800 })
  await page.emulate(iPhonex);
  await page.goto('https://www.homedepot.com/');
  await page.screenshot({ path: 'homedepot-iphoneX.png'});
  await browser.close();
});
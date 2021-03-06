//export this function for use elsewhere 
module.exports = {
    coords: get_coords_from_address
}

// geo location retrieval
async function get_coords_from_address (ADDRESS){
    const puppeteer = require('puppeteer');
    return await (async () => {
        try {
            const browser = await puppeteer.launch({
                executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                headless: true,
                userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
                args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080'] 
            });
            
            // create new page
            const page = await browser.newPage();


            // set permission for website to access gps
            const context = browser.defaultBrowserContext()
            await context.overridePermissions("https://www.gps-coordinates.net/", ['geolocation'])

            //set location
            await page.setGeolocation({latitude:43.664305 , longitude:-79.52661})
            
            //open url
            await page.goto("https://www.gps-coordinates.net/", {waitUntil: 'networkidle2'});

            // scroll to bottom of the page to enable page to work
            await page.evaluate(async () => {
                await new Promise((resolve, reject) => {
                    var totalHeight = 0;
                    
                    // scroll down by 100 pixes
                    var distance = 100;
                    var timer = setInterval(() => {
                        var scrollHeight = document.body.scrollHeight;
                        window.scrollBy(0, distance);
                        totalHeight += distance;

                        if(totalHeight >= scrollHeight){
                            clearInterval(timer);
                            // resolve promise
                            resolve(); 
                        }
                    // 100 ms delay each scrolls
                    }, 100);    
                });
                
                // scroll back up
                await new Promise((resolve, ) => {
                    var totalHeight = 0;
                    
                    // scroll down by 100 pixes
                    var distance = 100;
                    var timer = setInterval(() => {
                        var scrollHeight = 200;
                        window.scrollBy(0, distance);
                        totalHeight -= distance;

                        if(totalHeight <= scrollHeight){
                            clearInterval(timer);
                            // resolve promise
                            resolve(); 
                        }
                    // 100 ms delay each scrolls
                    }, 100);    
                });
            });


            await page.evaluate( () => document.getElementById("address").value = "");
            
            // insert address into input tag
            await page.type('input[id="address"]', ADDRESS.concat(", Toronto, ON, Canada"), {delay: 200})


            await page.evaluate(() => {
                var  query = document.querySelectorAll('button[class="btn btn-primary"]');
                query[0].click();
            })


            // OPTIMIZE THIS
            // wait one second for the long and lat to load                        
            await wait(2000);

            async function wait(ms) {
                return new Promise(resolve => {
                    setTimeout(resolve, ms);
                });
            }

            let string = await page.evaluate(() => {
                return document.querySelector('div[id="iwcontent"]').innerText
            })

            // the number of columns passed
            let numC =0;  

            let lat = ""
            let lon = ""
            for (let i =0; i< string.length; i++){
                if (string[i] == ':'){
                    numC++;
                } else if (string[i] == " "){
                    numC++;
                } else if (string[i] == '\n' ){
                    break;
                }
                if (numC ==2){
                    lat += string[i];
                } else if (numC ==6){
                    lon += string[i];
                }
            }

            let obj = {'lon': parseFloat(lon), 'lat' : parseFloat(lat)}

            await browser.close();
            return obj
        } catch (err){
            return {'error' : err}
        }
    })();
} 

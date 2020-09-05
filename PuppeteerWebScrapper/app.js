const puppeteer = require('puppeteer');

puppeteer.launch({ 
    executablePath: 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    headless: true,
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080'] 
    }).then(async browser => {


    // create new page
    const page = await browser.newPage();
    
    // open file stream
    const fs = require('fs');


    // represents the num of cols before pushing to the csv file
    const MAXCOLS = 2;

    const ObjectsToCsv = require('objects-to-csv')

    var csvCols = [];



    // this does nothing atm
    var endofentries = false;
    var pageNum = 1
    while( !endofentries){ 
        // go to the appropriate base url + if necessary
        if (pageNum ==1){
            await page.goto("https://www.zolo.ca/toronto-real-estate/sold");
        } else {
            await page.goto("https://www.zolo.ca/toronto-real-estate/sold/page-".concat(pageNum.toString(10)));
        }
        
        // get every link tag
        const urls = await page.$$eval('a', as => as.map(a => a.href));
        // set of used urls so we dont go the same place twice
        let used_urls = new Set();

        for ( var i =0; i<urls.length; i++){
            // use the string in the split function as a delimeter for the url 
            var split =   urls[i].split("https://www.zolo.ca/toronto-real-estate/"); 
            // if the url is a sold house
            if (split[1] != null){
                var firstChar = split[1][0];
                // if link is a valid address...
                if ( !used_urls.has(urls[i]) && firstChar >= '0' && firstChar <='9'){    
                    console.log(urls[i]);
                    console.log(i)
                    used_urls.add(urls[i]);
                    await page.goto(urls[i], {waitUntil: 'networkidle2'});  // wait for no more than 2 network connections for 500ms    
                    
                    // check if login pages 
                    try { 
                        await page.$eval('#email', el => el.value = 'svercillo7@gmail.com');
                        await page.click("#formprop1submit")
                    } catch (er) {
                        // pass
                    }

                    await page.goto(urls[i], {waitUntil: 'networkidle2'});  // this works well
                    
                    // await wait(150000);
                    // async function wait(ms) {
                    //     return new Promise(resolve => {
                    //         setTimeout(resolve, ms);
                    //     });
                    // }

                    let pagedata = await page.evaluate(() => {
                        try{
                            // create a set of known columns in the middle of the page, check to see nothing weird is coming up
                            const possibleColumns = new Set();
                            possibleColumns.add('Type');
                            possibleColumns.add('Style');
                            possibleColumns.add('Size');
                            possibleColumns.add('Lot Size');
                            possibleColumns.add('Age');
                            possibleColumns.add('Taxes');
                            possibleColumns.add('Walk Score');
                            possibleColumns.add('Pets');
                            possibleColumns.add('Days on Site');
                            possibleColumns.add('Maintenance Fees');
                            possibleColumns.add('Lease Term');
                            possibleColumns.add('Possession');
                            possibleColumns.add('All Inclusive');
                            
                            // get all the spans
                            let spans =  document.querySelectorAll('span[class="priv"]');
                            
                            // if these conditions are true, page is not a SOLD property 
                            if (spans[6] == undefined || spans[6].innerText.localeCompare("Sold") !=0){
                                return -1;
                            }

                            
                            let col_names =  document.querySelectorAll('dt[class="column-label"]');

                            // skip Walk Score cause this is being weird
                            let temp = [];
                            for (var tt = 0 ; tt < col_names.length; tt++){
                                if (col_names[tt].innerText.localeCompare('Walk Score') != 0){
                                    temp.push(col_names[tt]);
                                }
                            }
                            col_names = temp;

                            // all of these are the same for each page
                            let address =  document.querySelector('section>h1').innerText;
                            let bedNum = spans[0].innerText;
                            let bathNum = spans[1].innerText;
                            let sqarefootage = spans[2].innerText;
                            let sold_price = spans[3].innerText;
                            let soldOn = spans[5].innerText;


                            // init return
                            obj = 
                            {
                                'sold_price': sold_price,
                                'address' : address,
                                'bedNum': bedNum,
                                'bathNum': bathNum,
                                'sqarefootage' : sqarefootage,
                                'soldOn' : soldOn,
                                'Type' : null,
                                'Style' : null,
                                'Size' : null,
                                'Lot Size' : null,
                                'Age' : null, 
                                'Taxes' : null, 
                                'Walk Score' : null, 
                                'Days on Site': null, 
                                'Pets' : null,
                                'Maintenance Fees' : null,
                                'Lease Term' : null,
                                'Possession' : null,
                                'All Inclusive' : null
                            }
                            
                            var y = 0; 
                            for (var w =0; w < col_names.length; w++){
                                var col = col_names[w+y].innerText;
                                // some weird column name has come up
                                if(!possibleColumns.has(col)){
                                    // invalid 
                                    return -1;
                                }
                                obj[col] =  spans[7+ w].innerText;
                            }

                            // this is the list of nearby amenities
                            const nearbyCols = [];
                            nearbyCols.push("Groceries");
                            nearbyCols.push("Liquor Store");
                            nearbyCols.push("Restaurants");
                            nearbyCols.push("Coffee");
                            nearbyCols.push("Bank");
                            nearbyCols.push("Gas Station");
                            nearbyCols.push('Health & Fitness');
                            nearbyCols.push("Park");
                            nearbyCols.push("Library");
                            nearbyCols.push("Medical Care");
                            nearbyCols.push("Pharmacy");
                            nearbyCols.push("Mall");
                            nearbyCols.push("Movie Theatre");
                            nearbyCols.push("Bar");

                            // get all divs
                            let divs =  document.querySelectorAll('div[class="media-heading"]');
                            
                            //get all distances 
                            let dists = document.querySelectorAll('span[class="badge badge--small badge--mono"]')
                            
                            // temp object
                            let ndata = {};
                            let arr =[];
                            let lastCol = "";
                            for (var e =0; e<divs.length; e++){
                                let category = false;
    
                                for (var r = 0; r<nearbyCols.length; r++){
                                    let col = nearbyCols[r];
                                    if (divs[e].innerText.includes(col) 
                                        && divs[e].innerText[divs[e].innerText.length-2]  == 'k'
                                        && divs[e].innerText[divs[e].innerText.length-1] == 'm'
                                    ){
                                        category = true;
                                        if (arr.length > 0){
                                            ndata[lastCol] = arr; 
                                            arr = [];
                                        } 
                                        lastCol = col;
                                        break;
                                    } 1
                                }
                                if (!category ){
                                    // let o = {};
                                    // o.name = divs[e].innerText
                                    // o.name = dists[e].innerText;
                                    // arr.push(o);

                                    // get only the distance i.e. "0.12 km" from this span 
                                    let string = dists[e].innerText
                                    let startind = -1;
                                    let endind = -1;
                                    for (var c =0; c<string.length; c++){
                                        let char = string[c];
                                        if (char >="0" && char <= "9" && startind == -1){
                                            startind = c;
                                        } else if  (char == 'k'){
                                            endind =c+2;
                                        }
                                    }
                                    string = string.substring(startind, endind);
                                    arr.push(string);
                                }
                            }
    
                            delete ndata[""]
                            obj['Amenities'] = ndata;
                            
                            let schoolRatings = document.querySelectorAll('div[class="media-text"]');
                            let allSchoolType = document.querySelectorAll('div[class="media-sub-heading text-secondary"]');
                            let allSchoolDis = document.querySelectorAll('span[class="badge badge--small badge--mono"]');

                            obj['Nearest Schools'] = []
                            for (var e =0 ;e < schoolRatings.length; e ++){
                                let temp = {};
                                temp['type'] = allSchoolType[allSchoolType.length - schoolRatings.length + e].innerText;
                                temp['distance'] = allSchoolDis[allSchoolDis.length - schoolRatings.length + e].innerText;
                                temp['rating'] = schoolRatings[e].innerText
                                obj['Nearest Schools'].push(temp)
                            }
                            return obj;
                        } catch(err){
                            return {"error" : err }
                        }
                    });
                    if (pagedata == -1){
                        continue;
                    }

                    // replace empty spaces in the address with regex and using this as file name
                    const filename = pagedata.address.replace(/\s/g, '');
                    const filepath = ("data/".concat(filename)).concat(".json");
                    
                    pagedata['pageNum'] = pageNum;
                    pagedata['iterationNum'] = i;
                    pagedata['weblink'] = urls[i]
                    console.log(pagedata);


                    // convert json to string
                    pagedata = JSON.stringify(pagedata);
                    
                    // save json object to data folder
                    
                                                                // // check if file already exits, if so skip
                                                                // try {
                                                                //     if (!fs.existsSync(filepath)) {
                                                                //         //file does exists
                                                                //         continue;
                                                                //     }
                                                                // } catch(err) {
                                                                //     pagedata['error'] = err
                                                                //     // continue;
                                                                // }

                    // fs.writeFile(filepath, pagedata, function(err) {
                    //     if (err) {
                    //         console.log(err);
                    //     }
                    // });

                    csvCols.push(pagedata);
                    
                    if (csvCols.length >= MAXCOLS){

                        let string  = "";
                        for (var z = 0; z <csvCols.length; z++){
                            string += csvCols[z] + '\n';
                        }

                        fs.appendFile('../Data/data.txt', string, function (err) {
                            if (err) throw err;
                            console.log('Saved!');
                        });
                        csvCols = [];
                    }

                }
            }
        }
        
  

        pageNum ++;
    }


    await browser.close();

}).catch(function(error) {
    console.error(error);
});



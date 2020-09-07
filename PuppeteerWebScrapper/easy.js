const tools = require('./tools')
async function aaa(){
  let obj = {"a" : "100 Bloor St W"}
  // console.log( obj['a'])
  var d = await tools.coords(obj.a)
  console.log(d); 
}

aaa()


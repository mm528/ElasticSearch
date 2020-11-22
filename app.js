const express = require('express');
const app = express();
const path = require('path');
const router = express.Router();
var bodyParser	= require("body-parser")
const mongoose = require('mongoose')
const PostRoute =  require (__dirname + '/posts')

app.use(bodyParser.json())
//Middleware   
app.use('/posts',PostRoute)


app.get('/',function(req,res){
  res.sendFile(path.join(__dirname+'/index.html'));
  
  //__dirname : It will resolve to your project folder.
});



mongoose.connect('mongodb+srv://123456789mi:123456789mi@cluster0.8cso8.mongodb.net/test', {useNewUrlParser: true , useUnifiedTopology: true},
 ()=>{
    console.log('connected DB')
});


router.get('/sitemap',function(req,res){
  res.sendFile(path.join(__dirname +'/sitemap.html'));
});

//add the router
app.use('/', router);
app.listen(process.env.port || 3000);
app.use(bodyParser.json()); 
console.log('Running at Port 3000');


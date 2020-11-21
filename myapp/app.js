const express = require('express');
const app = express();
const path = require('path');
const router = express.Router();
const mongoose = require('mongoose');
//const { assert } = require('console');
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
const { callbackify } = require('util');
const bodyParser = require('body-parser');
var AirbnbSchema = require(__dirname +'/information_airbnb');
// Connection URL
const url = "mongodb+srv://michalis:159753mi@database.rdfok.mongodb.net/test";

require ('dotenv/config');






var resultArray = [];
router.get('/',function(req,res){
  res.sendFile(path.join(__dirname+'/index.html'));

  //__dirname : It will resolve to your project folder.
  // Use connect method to connect to the Server
  MongoClient.connect(url,{useUnifiedTopology: true }, function(err, client) {
  assert.equal(null, err);
  
  const db = client.db("sample_airbnb");
  var cursor = db.collection('listingsAndReviews').find({});
    



  function iterateFunc(doc) {
   // console.log(JSON.stringify(doc, null, 10));
    const air = new AirbnbSchema({
      _id:doc._id,
      listing_url: doc.listing_url,
      name :doc.name,
      summary : doc.summary,
      space : doc.space,
      description : doc.description,
      neighborhood_overview : doc.neighborhood_overview,
      notes : doc.notes,
      transit : doc.transit,
      access : doc.access,
      interaction : doc.interaction,
      house_rules : doc.house_rules,
      property_type : doc.property_type,
      room_type : doc.room_type,
      bed_type : doc.bed_type,
      minimum_nights : doc.minimum_nights,
      maximum_nights : doc.maximum_nights,
      cancellation_policy : doc.cancellation_policy,
      last_scraped : doc.last_scraped,
      calendar_last_scraped : doc.calendar_last_scraped,
      accommodates:  doc.accommodates,
      bedrooms : doc.bedrooms,
      beds : doc.beds,
      number_of_reviews : doc.number_of_reviews,
      bathrooms : doc.bathrooms,
      amenities : doc.amenities,
      price : doc.price,
      extra_people : doc.extra_people,
      guests_included : doc.guests_included,
      images : doc.images,
      host : doc.host,
      address : doc.address,
      availability : doc.availability,
      review_scores : doc.review_scores,
      reviews : doc.reviews
    });
   
   }
 
 function errorFunc(error) {
    console.log(error);
 }
 
 cursor.forEach(iterateFunc, errorFunc);




});


});

app.get('/test', (req,res)=> {
MongoClient.connect(url,{useUnifiedTopology: true }, function(err, client) {

  const db = client.db("sample_airbnb");
  var cursor = db.collection('listingsAndReviews').find({name: ""}).toArray((err,documents)=>{
    //res.json(documents)
      res.json(documents);
    
      
  });
    


})});


//connect with DB ONLINE   MongoClient.connect(url, (error, client) => {
mongoose.connect(process.env.DB_CONNECTION,
  
{ useNewUrlParser: true, useUnifiedTopology: true },function (err,db){
   
    console.log('Connected to DB')
    //console.log(db)
});









//add the router
app.use('/', router);
app.listen(process.env.port || 3000);
console.log('Running at Port 3000');



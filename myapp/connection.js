
const mongoose = require('mongoose')
var uri = "mongodb+srv://michalis:<159753mi>@database.rdfok.mongodb.net/<dbname>?retryWrites=true&w=majority"
var MongoClient = require('mongodb').MongoClient;

const connectDB = async()=> {
    mongoose.connect(URI);
}



module.exports = connectDB

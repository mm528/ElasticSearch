var mongoose = require ('mongoose');
var Schema = mongoose.Schema;

var postSchema = new Schema ({
    content : String,
    user : Schema.ObjectId
});

mongoose.model('posts',postSchema);
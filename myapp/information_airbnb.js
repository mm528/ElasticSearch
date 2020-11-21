var mongoose = require ('mongoose');

const airbnbSchema = mongoose.Schema( {
    _id:String,
    listing_url: String,
    name :String,
    summary : String,
    space : String,
    description : String,
    neighborhood_overview : String,
    notes : String,
    transit : String,
    access : String,
    interaction : String,
    house_rules : String,
    property_type : String,
    room_type : String,
    bed_type : String,
    minimum_nights : String,
    maximum_nights : String,
    cancellation_policy : String,
    last_scraped : Date,
    calendar_last_scraped : Date,
    accommodates:  Number,
    bedrooms : Number,
    beds : Number,
    number_of_reviews : Number,
    bathrooms : Number,
    amenities : Array,
    price : Number,
    extra_people : Number,
    guests_included : Number,
    images : Object,
    host : Object,
    address : Object,
    availability : Object,
    review_scores : Object,
    reviews : Object

});

module.exports = mongoose.model('Airbnb',airbnbSchema );

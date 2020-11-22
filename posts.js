const express = require('express');
const router = express.Router();
const Post = require(__dirname +'/Post');

router.get('/', (req,res)=> {
    console.log(req.body);
})
router.get('/specific', (req, res)=> {
    res.send('We are on specific post')
}); 

router.post('/', (req,res)=> {
    const post = new Post({
        title: req.body.title,
        description :req.body.description
    });
    post.save()
    .exec()
    .then(data => {
        res.json(data);
    })
    .catch(err => {
        res.json({ message: err});
    })
})


module.exports = router;
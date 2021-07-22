const express = require('express');
const router = express.Router();

const login_router = require('./login');
const user_router = require('./users');

router.use('/login', login_router);
router.use('/users', user_router);

router.get('/', function (req, res) {
   res.send('This is the API for Simulated Superstore Data System');
});

module.exports = router;
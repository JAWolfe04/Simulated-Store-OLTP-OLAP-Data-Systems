const app = require('express')();

const login_router = require('./endpoints/login');
const user_router = require('./endpoints/users');

app.use('/login', login_router);
app.use('/users', user_router);

app.get('/', function (req, res) {
   res.send('This is the API for Simulated Superstore Data System');
});

module.exports = app
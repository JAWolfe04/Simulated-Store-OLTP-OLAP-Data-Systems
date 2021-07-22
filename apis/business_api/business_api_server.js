const express = require('express');
const app = express();
const router = require('./endpoints/api_router');

app.use('/', router);

const server = app.listen(8081, function () {
   let host = server.address().address;
   const port = server.address().port;
   
   if (host == '::') {
	   host = 'localhost';
   };
   
   console.log('Listening at http://%s:%s', host, port);
});
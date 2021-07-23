const router = require('express').Router();
const bodyParser = require('body-parser');
const multer = require('multer')();
const crud_user = require('../crud/user');
const security = require('../security');

router.use(bodyParser.json());
router.use(bodyParser.urlencoded({ extended: true }));

router.post('/access-token', multer.array(), async function (req, res, next) {
	const username = req.body.username;
	const password = req.body.password;
	if (!username) { return res.status(400).send('"username" Field Not Provided'); };
	if (!password) { return res.status(400).send('"password" Field Not Provided'); };
	try {
		const auth = await crud_user.authentiate_user(username, password);
		console.log(auth);
		if (auth == null) {
			res.status(401).send('Invalid username or password');
		} else if (auth.disabled) {
			res.status(401).send('Blocked user');
		} else {
			const access_token = await security.create_access_token(username);
			res.json({"access_token": access_token, "token_type": "bearer"});
		};
	} catch (err) { console.log(err.stack); };
});

module.exports = router;
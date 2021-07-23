const express = require('express');
const router = express.Router();
const bodyParser = require('body-parser');
const multer = require('multer')();
const crud_user = require('../crud/user');

router.use(bodyParser.json());
router.use(bodyParser.urlencoded({ extended: true }));

router.post('/', multer.array(), async function (req, res, next) {
	const username = req.body.username;
	const password = req.body.password;
	if (!username) { return res.status(400).send('"username" Field Not Provided'); };
	if (!password) { return res.status(400).send('"password" Field Not Provided'); };
	try {
		const existing_user = await crud_user.get_user(username);
		if (existing_user == null) {
			const response = await crud_user.create_user(req.body.username, req.body.password);
			res.status(201).send(response);
		} else { res.status(409).send('Username already exists'); };
	} catch (err) { console.log(err.stack); };
});

router.delete('/', multer.array(), async function (req, res, next) {
	const username = req.body.username;
	const password = req.body.password;
	if (!username) { return res.status(400).send('"username" Field Not Provided'); };
	if (!password) { return res.status(400).send('"password" Field Not Provided'); };
	try {
		const auth = await crud_user.authentiate_user(username, password);
		if (auth !== null) {
			crud_user.delete_user(username);
			res.status(204).end();
		} else { res.status(404).send('Invalid username or password'); };
	} catch (err) { console.log(err.stack); };
});

module.exports = router;
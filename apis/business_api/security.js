const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const config = require('./config');

const jwtExpirySeconds = 60 * 60 * 3;
const algorithm = 'HS256';

async function create_access_token(username) {
	try {
		return await jwt.sign({ username }, config.JWT_KEY, 
			{ algorithm: algorithm,
			  expiresIn: jwtExpirySeconds, });
	} catch (err) { console.log(err.stack); };
};

async function verify_access_token(token, res) {
	if (!token) {
		res.status(401).send('Missing Required Access Token');
		return null;
	};
	let payload;
	try {
		payload = await jwt.verify(token, config.JWT_KEY);
	} catch (err) {
		if (err instanceof jwt.JsonWebTokenError) {
			res.status(401).send('Invalid Access Token');
		} else { res.status(400).end(); };
		return null;
	};
	
	return payload.username;
};

async function verify_password(plain_password, hashed_password) {
	try {
		return await bcrypt.compareSync(plain_password, hashed_password);
	} catch (err) { console.log(err.stack); };
};

async function get_password_hash(password) {
	try {
		return await bcrypt.hash(password, 10);
	} catch (err) { console.log(err.stack); };
};

module.exports = {
	create_access_token,
	verify_password,
	get_password_hash
};
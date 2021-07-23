const db = require('../crud/database');
const security = require('../security');

async function get_user(username) {
	try {
		const text = 'SELECT * FROM users WHERE username = $1';
		const values = [username];
		const response = await db.query(text, values);
		return (response.rows.length > 0 ? response.rows[0] : null);
	} catch (err) { console.log(err.stack); };
};

async function create_user(username, password) {
	try {
		const text = 'INSERT INTO users(username, hash_password, disabled) VALUES ($1, $2, $3) RETURNING *';
		const hash_password = await security.get_password_hash(password);
		const values = [username, hash_password, false];
		const response = await db.query(text, values);
		return response.rows[0];
	} catch (err) { console.log(err.stack); };
};

async function authentiate_user(username, password) {
	try {
		const user = await get_user(username);
		if (user == null) {
			return null;
		} else {
			const verified = await security.verify_password(password, user.hash_password);
			if (!verified) {
				return null;
			} else { 
				return user; 
			};
		};
	} catch (err) { console.log(err.stack); };
};

async function delete_user(username) {
	try {
		const text = 'DELETE FROM users WHERE username = $1';
		const values = [username];
		const response = await db.query(text, values);
	} catch (err) { console.log(err.stack); };	
};

module.exports = {
	get_user,
	create_user,
	authentiate_user,
	delete_user
};
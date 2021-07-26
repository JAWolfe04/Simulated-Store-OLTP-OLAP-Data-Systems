/* istanbul ignore file */
const { Client } = require('pg');
const config = require('../../config');

async function query(text, values, database_name) {
	const client = new Client({ 
						user: config.ADMIN_USER,
						host: config.HOST,
						database: database_name,
						password: config.ADMIN_PASSWORD,
						port: config.PORT, });
	client.connect();
	let response;
	try {
		response = await client.query(text, values);
	} catch (err) { console.log(err.stack); };
	client.end();
	return response;
};

async function create_database(database_name) {	
	const client = new Client({ user: config.ADMIN_USER,
								host: config.HOST,
								database: config.ADMIN_DB,
								password: config.ADMIN_PASSWORD,
								port: config.PORT, });
	client.connect();
	await client.query(`DROP DATABASE IF EXISTS ${database_name};`)
	await client.query(`CREATE DATABASE ${database_name} TEMPLATE test_template_db;`);
	client.end();
};

module.exports = {
  query,
  create_database
};
const dotenv = require('dotenv');
dotenv.config();
module.exports = {
	POSTGRES_DB_CONN: process.env.POSTGRES_DB_CONN,
	JWT_KEY: process.env.JWT_KEY,
};
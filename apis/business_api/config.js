const dotenv = require('dotenv');
dotenv.config();
module.exports = {	
	BUSINESS_USER: process.env.BUSINESS_USER,
	BUSINESS_PASSWORD: process.env.BUSINESS_PASSWORD,
	BUSINESS_DB: process.env.BUSINESS_DB,
	ADMIN_USER: process.env.ADMIN_USER,
	ADMIN_PASSWORD: process.env.ADMIN_PASSWORD,
	ADMIN_DB: process.env.ADMIN_DB,
	HOST: process.env.HOST,
	PORT: process.env.PORT,
	JWT_KEY: process.env.JWT_KEY,
	JWT_EXPIRY_SECONDS: 60 * 60 * 3,
	ALGORITHM: 'HS256',
};
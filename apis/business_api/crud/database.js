const { Pool } = require('pg');
const config = require('../config');

const pool = new Pool({ user: config.BUSINESS_USER,
						host: config.HOST,
						database: config.BUSINESS_DB,
						password: config.BUSINESS_PASSWORD,
						port: config.PORT, });

module.exports = {
  query: (text, params, callback) => {
	  return pool.query(text, params, callback);
  },
};
const { Pool } = require('pg');
const config = require('../config');

const connectionString = config.POSTGRES_DB_CONN;

const pool = new Pool({ connectionString, });

module.exports = {
  query: (text, params, callback) => {
	  return pool.query(text, params, callback);
  },
};
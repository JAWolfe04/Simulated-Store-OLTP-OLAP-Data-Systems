const db = require('./test_database');
const crud_user = require('../../crud/user');
const prod_db = require('../../crud/database');
const security = require('../../security');

describe('User integration testing postgres', () => {
	let database_name = 'test_user_db';
	const data = { "username": "testusername", "password": "testpassword", "disabled": false };
	
	beforeAll(async () => {
		await db.create_database(database_name);
	}, 15000);
	
	beforeEach(async () => {
		await db.query('DELETE FROM users;', [], database_name);
	});
	
	test('should get existing user', () => {
		const mock_query = jest.spyOn(prod_db, 'query').mockImplementation((text, values) => db.query(text, values, database_name));
		
		expect.assertions(4);
		return db.query('INSERT INTO users(username, hash_password, disabled) VALUES ($1, $2, $3);', [data.username, data.password, false], database_name).then(() => {
			return crud_user.get_user(data.username).then(response => {
				expect(response).toBeTruthy();
				expect(response.username).toBe(data.username);
				expect(response.hash_password).toBe(data.password);
				expect(response.disabled).toBe(false);
			});
		});
	});
	
	test('should create the provided user entry', () => {
		const mock_query = jest.spyOn(prod_db, 'query').mockImplementation((text, values) => db.query(text, values, database_name));
		const mock_get_password_hash = jest.spyOn(security, 'get_password_hash').mockImplementation((password) => password);
		
		expect.assertions(5);
		return crud_user.create_user(data.username, data.password).then(() => {
			return db.query('SELECT * FROM users WHERE username = $1', [data.username], database_name).then(response => {
				expect(response).toBeTruthy();
				expect(response.rows.length).toBe(1);
				expect(response.rows[0].username).toBe(data.username);
				expect(response.rows[0].hash_password).toBe(data.password);
				expect(response.rows[0].disabled).toBe(false);
			});
		});
	});
	
	test('should authenticate valid user', () => {
		const mock_query = jest.spyOn(prod_db, 'query').mockImplementation((text, values) => db.query(text, values, database_name));
		const mock_verify_password = jest.spyOn(security, 'verify_password').mockReturnValue(true);
		
		expect.assertions(4);
		return db.query('INSERT INTO users(username, hash_password, disabled) VALUES ($1, $2, $3);', [data.username, data.password, false], database_name).then(() => {
			return crud_user.authentiate_user(data.username, data.password).then((response) => {
				expect(response).toBeTruthy();
				expect(response.username).toBe(data.username);
				expect(response.hash_password).toBe(data.password);
				expect(response.disabled).toBe(false);
			});
		});
	});
	
	test('should delete existing user', () => {
		const mock_query = jest.spyOn(prod_db, 'query').mockImplementation((text, values) => db.query(text, values, database_name));
		
		expect.assertions(1);
		return db.query('INSERT INTO users(username, hash_password, disabled) VALUES ($1, $2, $3);', [data.username, data.password, false], database_name).then(() => {
			return crud_user.delete_user(data.username).then(() => {
				return db.query('SELECT * FROM users WHERE username = $1', [data.username], database_name).then((response) => {
					expect(response.rows.length).toBe(0);
				});
			});
		});
	});
});
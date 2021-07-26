const security = require('../security');
const config = require('../config');
const jwt = require('jsonwebtoken');

describe('Security unit testing', () => {
	test('should return a valid access token provided a username', () => {
		const username = 'testusername';
		expect.assertions(6);
		return security.create_access_token(username).then(response => {
			const sections = response.split('.');
			const encoding_prop = JSON.parse(Buffer.from(sections[0], 'base64'));
			const user_prop = JSON.parse(Buffer.from(sections[1], 'base64'));
			const date = Math.round(Date.now() / 1000);
			
			expect(encoding_prop.alg).toBe(config.ALGORITHM);
			expect(encoding_prop.typ).toBe('JWT');
			expect(user_prop.username).toBe(username);
			expect(user_prop.exp - user_prop.iat).toBe(config.JWT_EXPIRY_SECONDS);
			expect(user_prop.iat).toBeLessThanOrEqual(date);
			expect(user_prop.exp).toBeGreaterThan(date);
		});
	});
	
	test('should return the username of the provided access token', () => {
		const username = 'testusername';
		let res;
		
		expect.assertions(1);
		return security.create_access_token(username).then(token => {
			return security.verify_access_token(token, res).then(response => {
				expect(response).toBe(username);
			});
		});
	});
	
	test('should return true that a plain password matched the hashed password', () => {
		const password = 'testpassword';
		
		expect.assertions(1);
		return security.get_password_hash(password).then(hash_password => {
			return security.verify_password(password, hash_password).then(response => {
				expect(response).toBe(true);
			});
		});
	});
	
	test('should return a hashed password provided a password', () => {
		const password = 'testpassword';
		
		expect.assertions(6);
		return security.get_password_hash(password).then(response => {
			hash_parts = response.split("$");
			expect(response).toBeTruthy();
			expect(response.length).toBe(60);
			expect(hash_parts[0]).toBe('');
			expect(hash_parts[1]).toBe('2a');
			expect(hash_parts[2]).toBe('10');
			expect(hash_parts[3].length).toBe(53);
		});
	});
});
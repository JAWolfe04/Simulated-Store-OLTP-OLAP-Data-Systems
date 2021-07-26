const app = require('../../server_app');
const crud_user = require('../../crud/user');
const security = require('../../security');
const supertest = require('supertest');

describe('Tests the login endpoint', () => {
	test('should respond with a fake access token with a posted username and password', () => {
		const data = { username: "testusername", password: "testpassword" };
		
		const mock_authentiate_user = jest.spyOn(crud_user, 'authentiate_user')
			.mockReturnValue(data);
		const mock_create_access_token = jest.spyOn(security, 'create_access_token')
			.mockReturnValue('fake_access_token');
			
		expect.assertions(3);
		return supertest(app).post("/login/access-token/")
			.send(data).then(response => {
			expect(response.status).toBe(201);
			expect(response.body.access_token).toBe('fake_access_token');
			expect(response.body.token_type).toBe('bearer');
			});
	});
});
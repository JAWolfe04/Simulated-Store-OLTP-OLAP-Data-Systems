const app = require('../../server_app');
const crud_user = require('../../crud/user');
const security = require('../../security');
const supertest = require('supertest');

test('POST /login/access-token/', async () => {
	const data = { username: "testusername", password: "testpassword" };
	
	const mock_authentiate_user = jest.spyOn(crud_user, 'authentiate_user')
		.mockReturnValue(data);
	const mock_create_access_token = jest.spyOn(security, 'create_access_token')
		.mockReturnValue('fake_access_token');
		
	const response = await supertest(app).post("/login/access-token/")
		.send(data).expect(201);
		
	expect(response.body.access_token).toBe('fake_access_token');
	expect(response.body.token_type).toBe('bearer');
		
	mock_authentiate_user.mockRestore();
	mock_create_access_token.mockRestore();
});
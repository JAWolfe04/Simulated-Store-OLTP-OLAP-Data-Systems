const app = require('../../server_app');
const crud_user = require('../../crud/user');
const supertest = require('supertest');

test('POST /users/', async () => {
	const data = { username: "testusername", password: "testpassword" };
	
	const mock_get_user = jest.spyOn(crud_user, 'get_user')
		.mockReturnValue(null);
	const mock_create_user = jest.spyOn(crud_user, 'create_user')
		.mockReturnValue(
			{"username": data.username,
			 "hash_password": data.password,
			 "disabled": false});
		
	const response = await supertest(app).post("/users/")
		.send(data).expect(201);
		
	expect(response.body.username).toBe(data.username);
	expect(response.body.hash_password).toBe(data.password);
	expect(response.body.disabled).toBe(false);
	
	mock_get_user.mockRestore();
	mock_create_user.mockRestore();
});

test('DELETE /users/', async () => {
	const data = { username: "testusername", password: "testpassword" };
	
	const mock_authentiate_user = jest.spyOn(crud_user, 'authentiate_user')
		.mockReturnValue(data);
	const mock_delete_user = jest.spyOn(crud_user, 'delete_user');
	
	await supertest(app).delete("/users/").send(data).expect(204);
	
	mock_authentiate_user.mockRestore();
	mock_delete_user.mockRestore();
});
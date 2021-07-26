const app = require('../../server_app');
const crud_user = require('../../crud/user');
const supertest = require('supertest');

describe('Tests users endpoint', () => {
	test('should respond with user data from a post with username and password', () => {
		const data = { username: "testusername", password: "testpassword" };
		
		const mock_get_user = jest.spyOn(crud_user, 'get_user')
			.mockReturnValue(null);
		const mock_create_user = jest.spyOn(crud_user, 'create_user')
			.mockReturnValue(
				{"username": data.username,
				 "hash_password": data.password,
				 "disabled": false});
			
		expect.assertions(4);
		return supertest(app).post("/users/")
			.send(data).then(response => {
				expect(response.status).toBe(201);
				expect(response.body.username).toBe(data.username);
				expect(response.body.hash_password).toBe(data.password);
				expect(response.body.disabled).toBe(false);
			});
	});

	test('should respond with a 204 from a delete with a username and password', () => {
		const data = { username: "testusername", password: "testpassword" };
		
		const mock_authentiate_user = jest.spyOn(crud_user, 'authentiate_user')
			.mockReturnValue(data);
		const mock_delete_user = jest.spyOn(crud_user, 'delete_user');
		
		expect.assertions(1);
		return supertest(app).delete("/users/").send(data).then(response => {
			expect(response.status).toBe(204);
		});
	});
});
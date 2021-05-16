from employee_utilities import employee_utility, RAND_USER_URL
import pytest
import datetime

@pytest.fixture
def setup_employee(session, cursor):
    add_employee_query = """INSERT INTO employee (location_id, position_id, name,
                    salary, start_date) VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(add_employee_query, (1, 1, 'Jane Doe', 50000.00,
                                        datetime.datetime.now()))
    session.commit()
    return cursor.lastrowid

@pytest.mark.database_setup
class Test_Database_Setup:
    
    def test_database_connection(self, session):
        assert session.is_connected()

    def test_create_db_setup(self, cursor):
        cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in cursor.fetchall()]
        assert "testdb" in databases

    @pytest.mark.usefixtures("setup_departments")
    def test_department_table_setup(self, cursor):
        cursor.execute("SELECT * FROM department")
        departments = [dept[1] for dept in cursor.fetchall()]
        expected_dept = ["Management", "Home and Office",
                         "Beauty, Bath and Health", "Food"]
        assert all(dept in departments for dept in expected_dept)

    @pytest.mark.usefixtures("setup_jobs")
    def test_position_table_setup(self, cursor):
        cursor.execute("SELECT * FROM job_position")
        jobs = {job[2] for job in cursor.fetchall()}
        assert len(jobs) == 7

    @pytest.mark.usefixtures("setup_locations")
    def test_location_table_setup(self, cursor):
        cursor.execute("SELECT * FROM location")
        assert len(cursor.fetchall()) == 10

    @pytest.mark.usefixtures("setup_employees")
    def test_employee_table_setup(self, cursor):
        cursor.execute("DESCRIBE employee")
        col_names = [col[0] for col in cursor.fetchall()]
        expected_names = ["employee_id", "location_id", "position_id",
                          "salary", "start_date", "end_date"]
        assert all(col in col_names for col in expected_names)

@pytest.mark.class_init
class Test_Employee_Utility_Class_Initialization:
    def test_employee_utility_class_init(self, session):
        assert employee_utility(session)

    def test_employee_utility_class_init_with_none_provided(self):
        with pytest.raises(TypeError):
            assert employee_utility(None)


@pytest.mark.hire_emp
@pytest.mark.usefixtures("setup_employees")
class Test_Hire_Employee:
    def test_hire_employee_returns_id(self, session, cursor):
        cursor.execute("DELETE FROM employee")
        cursor.execute("ALTER TABLE employee AUTO_INCREMENT=1")
        session.commit()
        utility = employee_utility(session)
        id = utility.hire_employee(1, 1, 'Jane Doe', 50000.00)
        assert id == 1

    @pytest.mark.parametrize("col, result", [
        (1, 1),
        (2, 1),
        (3, 'Jane Doe'),
        (4, 50000.00)])
    def test_hire_employee_added_correct_employee_data(self, session, cursor,
                                                       col, result):
        utility = employee_utility(session)
        employee_id = utility.hire_employee(1, 1, 'Jane Doe', 50000.00)
        query = "SELECT * FROM employee WHERE employee_id = %s"
        cursor.execute(query, (employee_id,))
        assert cursor.fetchall()[0][col] == result

    @pytest.mark.parametrize("location, position, name, salary", [
        (None, 1, 'Jane Doe', 50000.00),
        (1, None, 'Jane Doe', 50000.00),
        (1, 1, None, 50000.00),
        (1, 1, 'Jane Doe', None)])
    def test_hire_employee_with_invalid_argument_types(self,
            session, location, position, name, salary):
        utility = employee_utility(session)
        with pytest.raises(TypeError):
            assert utility.hire_employee(location, position, name, salary)

    @pytest.mark.parametrize("location, position, name, salary", [
        (-1, 1, 'Jane Doe', 50000.00),
        (100, 1, 'Jane Doe', 50000.00),
        (1, -1, 'Jane Doe', 50000.00),
        (1, 100, 'Jane Doe', 50000.00),
        (1, 1, '', 50000.00),
        (1, 1, ' ', 50000.00),
        (1, 1, 'Jane Doe', -1.00),
        (1, 1, 'Jane Doe', 10000000.00)])
    def test_hire_employee_with_undesired_input(self,
            session, location, position, name, salary):
        utility = employee_utility(session)
        with pytest.raises(ValueError):
            assert utility.hire_employee(location, position, name, salary)
   
@pytest.mark.fire_emp
@pytest.mark.usefixtures("setup_employees")
class Test_Fire_Employee:
        
    def test_fire_employee_has_fired_employee(self, session, cursor,
                                              setup_employee):
        # Employee end_date should be null as long as they are employed
        employee_id = setup_employee
        fire_query = "SELECT end_date FROM employee WHERE employee_id = %s"
        cursor.execute(fire_query, (employee_id,))
        pre_fired_date = cursor.fetchall()[0][0]
        employee_utility(session).fire_employee(employee_id)
        cursor.execute(fire_query, (employee_id,))
        post_fired_date = cursor.fetchall()[0][0]
        assert pre_fired_date is not post_fired_date

    def test_fire_employee_has_correct_end_date(self, session, cursor,
                                                setup_employee):
        # May not be true if the test is run at the exact time where
        # the function is called on on day and the comparison is tested
        # on the next day.
        # Very highly unlikely to be possible
        employee_id = setup_employee
        employee_utility(session).fire_employee(employee_id)
        fire_query = "SELECT end_date FROM employee WHERE employee_id = %s"
        cursor.execute(fire_query, (employee_id,))
        fired_date = cursor.fetchall()[0][0]
        assert fired_date == datetime.datetime.now().date()

    def test_fire_employee_gives_valid_return(self, session, setup_employee):
        employee_id = setup_employee
        return_id = employee_utility(session).fire_employee(employee_id)
        assert return_id > 0

    def test_fire_employee_with_None_input(self, session):
        with pytest.raises(TypeError):
            assert employee_utility(session).fire_employee(None)

    @pytest.mark.parametrize("employee_id", [(-1), (1000)])
    def test_fire_employee_with_undesired_input(self, session, employee_id):
        with pytest.raises(ValueError):
            assert employee_utility(session).fire_employee(employee_id)

@pytest.mark.transfer_emp
@pytest.mark.usefixtures("setup_employees")
class Test_Transfer_Employee:
    def test_transfer_employee_changes_employee_data(self, session,
                                                     cursor, setup_employee):
        employee_id = setup_employee
        employee_utility(session).transfer_employee(employee_id, 2, 2)
        query = "SELECT location_id, position_id FROM employee " \
                "WHERE employee_id = %s"
        cursor.execute(query, (employee_id,))
        location, position = cursor.fetchall()[0]
        assert location == 2 and position == 2

    def test_transfer_employee_gives_valid_return(self, session, setup_employee):
        employee_id = setup_employee
        utility = employee_utility(session)
        return_id = utility.transfer_employee(employee_id, 2, 2)
        assert return_id == employee_id

    @pytest.mark.parametrize("employee_id, location_id, position_id", [
        (None, 2, 2),
        (0, None, 2),
        (0, 2, None)])
    def test_transfer_employee_with_invalid_types(self, session, employee_id,
                                    location_id, position_id, setup_employee):
        if employee_id == 0:
            employee_id = setup_employee
        else:
            setup_employee

        utility = employee_utility(session)
        with pytest.raises(TypeError):
            assert utility.transfer_employee(employee_id, location_id,
                                             position_id)

    @pytest.mark.parametrize("employee_id, location_id, position_id", [
        (-1, 2, 2),
        (1000, 2, 2),
        (0, -1, 2),
        (0, 1000, 2),
        (0, 2, -1),
        (0, 2, 1000)])
    def test_transfer_employee_with_undesired_input(self, session, employee_id,
                                    location_id, position_id, setup_employee):
        if employee_id == 0:
            employee_id = setup_employee
        else:
            setup_employee

        utility = employee_utility(session)
        with pytest.raises(ValueError):
            assert utility.transfer_employee(employee_id, location_id,
                                             position_id)

@pytest.mark.usefixtures("setup_employees")
@pytest.mark.change_salary
class Test_Change_Salary:
    def test_change_salary_alters_salary(self, session, cursor, setup_employee):
        employee_id = setup_employee
        employee_utility(session).change_salary(employee_id, 60000.00)
        query = "SELECT salary FROM employee WHERE employee_id = %s"
        cursor.execute(query, (employee_id,))
        assert cursor.fetchall()[0][0] == 60000.00

    def test_change_salary_gives_valid_return(self, session, setup_employee):
        employee_id = setup_employee
        utility = employee_utility(session)
        return_id = utility.change_salary(employee_id, 60000.00)
        assert return_id == employee_id

    @pytest.mark.parametrize("employee_id, salary", [
        (None, 60000.00), (0, None)])
    def test_change_salary_with_invalid_types(self, session, setup_employee,
                                                   employee_id, salary):
        if employee_id == 0:
            employee_id = setup_employee
        else:
            setup_employee
            
        with pytest.raises(TypeError):
            assert employee_utility(session).change_salary(employee_id, salary)

    @pytest.mark.parametrize("employee_id, salary", [
        (-1, 60000.00), (1000, 60000.00), (0, 1.00), (0, 1000000.00)])
    def test_change_salary_with_undesired_input(self, session, setup_employee,
                                                employee_id, salary):
        if employee_id == 0:
            employee_id = setup_employee
        else:
            setup_employee
            
        with pytest.raises(ValueError):
            assert employee_utility(session).change_salary(employee_id, salary)

@pytest.mark.create_person
class Test_Create_Person:    
    def test_create_person_ok_response(self, session, requests_mock):
        requests_mock.get(RAND_USER_URL, status_code = 200)
        response = employee_utility(session).create_person()
        assert response is not None

    def test_create_person_page_not_found(self, session, requests_mock):
        requests_mock.get(RAND_USER_URL, status_code = 404)
        response = employee_utility(session).create_person()
        assert response is None

    def test_create_person_returns_json(self, session, requests_mock):
        mock_json = {"results":[
            {"gender":"female",
             "name":{"title":"Miss", "first":"Sophie", "last":"Young"},
             "location":{"street":{"number":358,"name":"Daisy Dr"},
                         "city":"Lincoln",
                         "state":"Delaware",
                         "country":"United States",
                         "postcode":81807,
                         "coordinates":{"latitude":"-62.8675",
                                        "longitude":"101.9698"},
                         "timezone":{"offset":"+8:00",
                                     "description":"Beijing, Perth, " \
                                     "Singapore, Hong Kong"}},
             "email":"sophie.young@example.com",
             "dob":{"date":"1953-07-15T23:27:59.847Z","age":68},
             "phone":"(447)-017-7966",
             "cell":"(110)-838-1074"}]}
        requests_mock.get(RAND_USER_URL, status_code = 200, json = mock_json)
        response = employee_utility(session).create_person()
        assert response.json() == mock_json
        
@pytest.mark.add_person
class Test_Add_Person_To_Records:
    pass

import pytest
import datetime

from src.employee.employee_utilities import employee_utility, RAND_USER_URL

@pytest.mark.fire_emp
@pytest.mark.usefixtures("setup_employees")
class Test_Fire_Employee:
        
    def test_has_fired_employee(self, session, cursor, setup_employee):
        # Employee end_date should be null as long as they are employed
        employee_id = setup_employee
        fire_query = "SELECT end_date FROM employee WHERE employee_id = %s"
        cursor.execute(fire_query, (employee_id,))
        pre_fired_date = cursor.fetchall()[0][0]
        employee_utility(session).fire_employee(employee_id)
        cursor.execute(fire_query, (employee_id,))
        post_fired_date = cursor.fetchall()[0][0]
        assert pre_fired_date is not post_fired_date

    def test_sets_correct_end_date(self, session, cursor, setup_employee):
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

    def test_gives_valid_return(self, session, setup_employee):
        employee_id = setup_employee
        return_id = employee_utility(session).fire_employee(employee_id)
        assert return_id > 0

    def test_with_None_input(self, session):
        with pytest.raises(TypeError):
            assert employee_utility(session).fire_employee(None)

    @pytest.mark.parametrize("employee_id", [(-1), (1000)])
    def test_with_undesired_input(self, session, employee_id):
        with pytest.raises(ValueError):
            assert employee_utility(session).fire_employee(employee_id)

import pytest

from src.employee.employee_utilities import employee_utility

@pytest.mark.change_salary
@pytest.mark.usefixtures("setup_employees")
class Test_Change_Salary:
    def test_alters_salary(self, session, cursor, setup_employee):
        employee_id = setup_employee
        employee_utility(session).change_salary(employee_id, 60000.00)
        query = "SELECT salary FROM employee WHERE employee_id = %s"
        cursor.execute(query, (employee_id,))
        assert cursor.fetchall()[0][0] == 60000.00

    def test_gives_valid_return(self, session, setup_employee):
        employee_id = setup_employee
        utility = employee_utility(session)
        return_id = utility.change_salary(employee_id, 60000.00)
        assert return_id == employee_id

    @pytest.mark.parametrize("employee_id, salary", [
        (None, 60000.00),
        (0, None)])
    def test_with_invalid_types(
            self, session, setup_employee, employee_id, salary):
        if employee_id == 0:
            employee_id = setup_employee
        else:
            setup_employee
            
        with pytest.raises(TypeError):
            assert employee_utility(session).change_salary(employee_id, salary)

    @pytest.mark.parametrize("employee_id, salary", [
        (-1, 60000.00),
        (1000, 60000.00),
        (0, 1.00),
        (0, 1000000.00)])
    def test_with_undesired_input(
            self, session, setup_employee, employee_id, salary):
        if employee_id == 0:
            employee_id = setup_employee
        else:
            setup_employee
            
        with pytest.raises(ValueError):
            assert employee_utility(session).change_salary(employee_id, salary)

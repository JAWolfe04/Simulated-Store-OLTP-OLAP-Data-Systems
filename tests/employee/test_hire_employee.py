import pytest

from src.employee.employee_utilities import employee_utility

@pytest.mark.hire_emp
@pytest.mark.usefixtures("setup_employees")
class Test_Hire_Employee:
    def test_returns_id(self, session, cursor):
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
    def test_added_correct_employee_data(self, session, cursor, col, result):
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
    def test_with_wrong_argument_types(
            self, session, location, position, name, salary):
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
    def test_with_undesired_input(
            self, session, location, position, name, salary):
        utility = employee_utility(session)
        with pytest.raises(ValueError):
            assert utility.hire_employee(location, position, name, salary)

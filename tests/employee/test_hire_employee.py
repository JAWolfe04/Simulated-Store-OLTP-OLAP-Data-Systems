import pytest
from datetime import datetime
from pathlib import Path

from src.employee.employee_utilities import employee_utility
from src.employee.constants import DEFAULT_REPO_NAME
from tests.constants import MOCK_EMPLOYEE_DATA

@pytest.mark.hire_emp
@pytest.mark.usefixtures("setup_employees")
class Test_Hire_Employee:
    def test_returns_id(self, session, tmp_path, reset_employees):
        reset_employees
        path = tmp_path / "employee_repo.csv"
        emp_id = employee_utility(session).hire_employee(
            MOCK_EMPLOYEE_DATA, path)
        assert emp_id == 1

    def test_creates_repo_in_default_path(self, session):
        employee_utility(session).hire_employee(MOCK_EMPLOYEE_DATA)
        path = Path.cwd() / DEFAULT_REPO_NAME
        assert path.exists()

    def test_create_repo_in_custom_path(self, tmp_path, session):
        path = tmp_path / "custom_employee_repo.csv"
        employee_utility(session).hire_employee(MOCK_EMPLOYEE_DATA, path)
        assert path.exists()

    def test_added_employee_data(self, session, cursor,
                                 tmp_path, reset_employees):
        reset_employees
        path = tmp_path / "employee_repo.csv"
        emp_id = employee_utility(session).hire_employee(
            MOCK_EMPLOYEE_DATA, path)
        query = "SELECT * FROM employee WHERE employee_id = %s"
        cursor.execute(query, (emp_id,))
        expected = (1, 1, 1, "Sophie Young", 50000.00,
                    datetime.now().date(), None)
        assert cursor.fetchone() == expected

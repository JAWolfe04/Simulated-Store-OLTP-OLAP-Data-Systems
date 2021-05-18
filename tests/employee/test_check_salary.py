import pytest
import random

import mysql.connector

from src import settings
from src.employee.employee_utilities import employee_utility

@pytest.mark.check_salary
@pytest.mark.usefixtures("setup_jobs")
class Test_Check_Salary:
    def test_returns_no_errors_with_valid_inputs(self, session, cursor):
        cursor.execute("SELECT position_id, min_salary, max_salary "
                       "FROM job_position")
        results = cursor.fetchall()
        for result in results:
            salary = random.uniform(float(result[1]), float(result[2]))
            salary = round(salary, 2)
            employee_utility(session).check_salary( result[0], salary)
    
    @pytest.mark.parametrize("position_id, salary", [
        (None, 50000.00), (1, None)])
    def test_with_wrong_types(self, session, cursor, position_id, salary):
        with pytest.raises(TypeError):
            assert employee_utility(session).check_salary(position_id, salary)

    @pytest.mark.parametrize("position_id, salary", [
        (-1, 50000.00), (1000, 50000.00), (1, -1.00), (1, 10000000.00)])
    def test_with_undesired_input(self, session, cursor, position_id, salary):
        with pytest.raises(ValueError):
            assert employee_utility(session).check_salary(position_id, salary)

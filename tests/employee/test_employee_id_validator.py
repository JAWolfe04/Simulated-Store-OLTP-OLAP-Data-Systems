import pytest

from src.employee.employee_utilities import employee_utility

@pytest.mark.emp_id_validator
@pytest.mark.usefixtures("setup_employees", "reset_employees", "setup_employee")
class Test_Employee_Id_Validtator:
    def test_with_valid_id(self, session):
        employee_utility(session).employee_id_validator(1)

    @pytest.mark.parametrize("employee_id, error", [
        (None, TypeError), (-1, ValueError), (1000000, ValueError)])
    def test_with_undesired_input(self, session, employee_id, error):
        with pytest.raises(error):
            assert employee_utility(session).employee_id_validator(employee_id)

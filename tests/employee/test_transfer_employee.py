import pytest

from src.employee.employee_utilities import employee_utility

@pytest.mark.transfer_emp
@pytest.mark.usefixtures("setup_employees")
class Test_Transfer_Employee:
    def test_changes_employee_data(self, session, cursor, setup_employee):
        employee_id = setup_employee
        employee_utility(session).transfer_employee(employee_id, 2, 2)
        query = ("SELECT location_id, position_id FROM employee "
                 "WHERE employee_id = %s")
        cursor.execute(query, (employee_id,))
        location, position = cursor.fetchall()[0]
        assert location == 2 and position == 2

    def test_gives_valid_return(self, session, setup_employee):
        employee_id = setup_employee
        utility = employee_utility(session)
        return_id = utility.transfer_employee(employee_id, 2, 2)
        assert return_id == employee_id

    @pytest.mark.parametrize("employee_id, location_id, position_id", [
        (None, 2, 2),
        (0, None, 2),
        (0, 2, None)])
    def test_with_invalid_types(self, session, employee_id, location_id,
                                position_id, setup_employee):
        if employee_id == 0:
            employee_id = setup_employee
        else:
            setup_employee

        utility = employee_utility(session)
        with pytest.raises(TypeError):
            assert utility.transfer_employee(
                employee_id, location_id, position_id)

    @pytest.mark.parametrize("employee_id, location_id, position_id", [
        (-1, 2, 2),
        (1000, 2, 2),
        (0, -1, 2),
        (0, 1000, 2),
        (0, 2, -1),
        (0, 2, 1000)])
    def test_with_undesired_input(self, session, employee_id, location_id,
                                  position_id, setup_employee):
        if employee_id == 0:
            employee_id = setup_employee
        else:
            setup_employee

        utility = employee_utility(session)
        with pytest.raises(ValueError):
            assert utility.transfer_employee(
                employee_id, location_id, position_id)

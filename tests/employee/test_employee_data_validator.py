import pytest
import copy

from src.employee.employee_utilities import employee_utility
from tests.constants import MOCK_EMPLOYEE_DATA

@pytest.mark.emp_data_validator
class Test_Employee_Data_Validator:
    @pytest.mark.parametrize("data, error", [
        (None, TypeError), ({}, ValueError)])
    def test_with_wrong_employee_data_format(self, session, data, error):
        with pytest.raises(error):
            assert employee_utility(session).employee_data_validator(data)
            
    @pytest.mark.parametrize("key_name, key_value", [
        ("start_date", None), ("gender", None),
        ("name", None), ("address", None),
        ("city", None), ("state_code", None),
        ("postal_code", None), ("email", None),
        ("dob", None), ("phone", None), ("cell", None)])
    def test_non_nullable_fields(self, session, key_name, key_value):
        new_emp_data = copy.deepcopy(MOCK_EMPLOYEE_DATA)
        new_emp_data[key_name] = key_value
        with pytest.raises(TypeError):
            assert employee_utility(session).employee_data_validator(
                new_emp_data)

    @pytest.mark.parametrize("key_name, key_value", [
        ("start_date", "1700-01-01"),
        ("gender", "female"), ("name", " "), ("name", "Joe "),
        ("address", " "), ("city", " "),
        ("state_code", " "), ("state_code", "Alabama"),
        ("postal_code", " "), ("postal_code", "aaaaa"),
        ("postal_code", "111111"), ("email", " "), ("email", "@.com"),
        ("dob", "1700-01-01"), ("phone", "(1234)-567-7890"),
        ("cell", "(1234)-567-7890")])
    def test_with_wrong_employee_data_value_types(
            self, session, key_name, key_value):
        new_emp_data = copy.deepcopy(MOCK_EMPLOYEE_DATA)
        new_emp_data[key_name] = key_value
        with pytest.raises(ValueError):
            assert employee_utility(session).employee_data_validator(
                new_emp_data)

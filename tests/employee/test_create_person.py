import re

import pytest
import requests_mock

from src.employee.employee_utilities import employee_utility, RAND_USER_URL
from tests.constants import MOCK_JSON, MOCK_EMPLOYEE_DATA

@pytest.mark.create_person
@pytest.mark.usefixtures("setup_jobs", "setup_locations")
class Test_Create_Person:
    def test_ok_response(self, session, requests_mock):
        requests_mock.get(RAND_USER_URL, status_code = 200, json = MOCK_JSON)
        response = employee_utility(session).create_person(1, 1)
        assert response is not None

    def test_page_not_found(self, session, requests_mock):
        requests_mock.get(RAND_USER_URL, status_code = 404, json = MOCK_JSON)
        response = employee_utility(session).create_person(1, 1)
        assert response is None

    def test_returns_correct_employee_data_format(self, session, requests_mock):
        requests_mock.get(RAND_USER_URL, status_code = 200, json = MOCK_JSON)
        data = employee_utility(session).create_person(1, 1)
        assert data.keys() == MOCK_EMPLOYEE_DATA.keys()

    @pytest.mark.parametrize("location_id, position_id", [(None, 1), (1, None)])
    def test_with_wrong_agrument_type(
            self, session, requests_mock, location_id, position_id):
        requests_mock.get(RAND_USER_URL, status_code = 200, json = MOCK_JSON)
        with pytest.raises(TypeError):
            assert employee_utility(session).create_person(location_id,
                                                           position_id)

    @pytest.mark.parametrize("location_id, position_id", [
        (-1, 1), (1000, 1), (1, -1), (1, 1000)])
    def test_with_undesired_input(
            self, session, requests_mock, location_id, position_id):
        requests_mock.get(RAND_USER_URL, status_code = 200, json = MOCK_JSON)
        with pytest.raises(ValueError):
            assert employee_utility(session).create_person(location_id,
                                                           position_id)

    def test_returns_valid_gender_format(self, session, requests_mock):
        requests_mock.get(RAND_USER_URL, status_code = 200, json = MOCK_JSON)
        data = employee_utility(session).create_person(1, 1)
        assert data.get("gender") == 'm' or data.get("gender") == 'f'
        

    def test_returns_valid_salary_for_position(
            self, session, cursor, requests_mock):
        salary_query = ("SELECT min_salary, max_salary FROM job_position "
                        "WHERE position_id = %s")
        cursor.execute(salary_query, (1,))
        min_salary, max_salary = cursor.fetchall()[0]
        requests_mock.get(RAND_USER_URL, status_code = 200, json = MOCK_JSON)
        data = employee_utility(session).create_person(1, 1)
        assert min_salary <= data.get("salary") <= max_salary

    def test_returns_valid_name_format(self, session, requests_mock):
        requests_mock.get(RAND_USER_URL, status_code = 200, json = MOCK_JSON)
        data = employee_utility(session).create_person(1, 1)
        assert len(data.get("name").split()) == 2

    def test_return_valid_state_format(self, session, requests_mock):
        requests_mock.get(RAND_USER_URL, status_code = 200, json = MOCK_JSON)
        data = employee_utility(session).create_person(1, 1)
        assert len(data.get("state_code")) == 2

    def test_returns_valid_dob_format(self, session, requests_mock):
        requests_mock.get(RAND_USER_URL, status_code = 200, json = MOCK_JSON)
        data = employee_utility(session).create_person(1, 1)
        dob_format = "^[12][90][0-9][0-9]-[01][0-9]-[0-3][0-9]$"
        assert re.search(dob_format, data.get("dob"))

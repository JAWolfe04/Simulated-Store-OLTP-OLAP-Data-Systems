import pytest
import requests

from src.employee.constants import RAND_USER_URL
from constants import MOCK_JSON

@pytest.mark.integration_tests
class Test_Integration:
    def test_randomuser_api(self):
        # Tests if the API's response json mirrors the mock json used in tests
        response = requests.get(RAND_USER_URL)
        response_keys = response.json().get("results")[0].keys()
        mock_keys = MOCK_JSON.get("results")[0].keys()
        assert response_keys == mock_keys

    def test_dev_database_connection(self, dev_session):
        assert dev_session.is_connected()

    def get_queries(self, dev_cursor, cursor, table_query):
        # Runs a query and returns lists of the first item of each
        # row of the resulting query for the dev and test databases
        dev_cursor.execute(table_query)
        dev_col_names = [col[0] for col in dev_cursor.fetchall()]
        cursor.execute(table_query)
        test_col_names = [col[0] for col in cursor.fetchall()]
        return (dev_col_names, test_col_names)

    @pytest.mark.usefixtures("setup_departments")
    def test_department_table(self, dev_cursor, cursor):
        dev_col_names, test_col_names = self.get_queries(
            dev_cursor, cursor, "DESCRIBE department")
        assert test_col_names == dev_col_names

    @pytest.mark.usefixtures("setup_departments")
    def test_departments(self, dev_cursor, cursor):
        dev_depts, test_depts = self.get_queries(
            dev_cursor, cursor, "SELECT name FROM department")
        assert dev_depts == test_depts

    @pytest.mark.usefixtures("setup_jobs")
    def test_position_table(self, dev_cursor, cursor):
        dev_col_names, test_col_names = self.get_queries(
            dev_cursor, cursor, "DESCRIBE job_position")
        assert test_col_names == dev_col_names

    @pytest.mark.usefixtures("setup_jobs")
    def test_positions(self, dev_cursor, cursor):
        dev_jobs, test_jobs = self.get_queries(
            dev_cursor, cursor, "SELECT title FROM job_position")
        assert dev_jobs == test_jobs

    @pytest.mark.usefixtures("setup_locations")
    def test_location_table(self, dev_cursor, cursor):
        dev_col_names, test_col_names = self.get_queries(
            dev_cursor, cursor, "DESCRIBE location")
        assert test_col_names == dev_col_names

    @pytest.mark.usefixtures("setup_locations")
    def test_locations(self, dev_cursor, cursor):
        dev_locations, test_locations = self.get_queries(
            dev_cursor, cursor, "SELECT location_id FROM location")
        assert len(dev_locations) == len(test_locations)

    @pytest.mark.usefixtures("setup_employees")
    def test_employee_table(self, dev_cursor, cursor):
        dev_col_names, test_col_names = self.get_queries(
            dev_cursor, cursor, "DESCRIBE employee")
        assert test_col_names == dev_col_names

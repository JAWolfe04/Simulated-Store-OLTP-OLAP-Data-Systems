import pytest
import pandas
import requests_mock
import copy

from src.employee.employee_utilities import employee_utility
from src.employee.constants import RAND_USER_URL
from tests.constants import MOCK_EMPLOYEE_DATA, MOCK_JSON

@pytest.mark.hire_all_emp
@pytest.mark.usefixtures("setup_employees", "reset_employees")
class Test_Hire_All_Open_Postions:
    def add_employee(self, location_id, position_id, cursor, session, path):
        new_emp_data = copy.deepcopy(MOCK_EMPLOYEE_DATA)
        new_emp_data["location_id"] = location_id
        new_emp_data["position_id"] = position_id

        query = ("INSERT INTO employee (location_id, position_id, name, "
                 "salary, start_date) VALUES (%s, %s, %s, %s, %s)")
        hire_data = (new_emp_data.get("location_id"),
                     new_emp_data.get("position_id"),
                     new_emp_data.get("name"),
                     new_emp_data.get("salary"),
                     "2021-05-20")
        cursor.execute(query, hire_data)
        session.commit()
        new_emp_data["employee_id"] = cursor.lastrowid
        new_emp_data["start_date"] = "2021-05-20"

        try:
            repo_df = pandas.read_csv(path)
            repo_df = repo_df.set_index("employee_id")
            repo_df = repo_df.astype({"postal_code": str})
            new_data_df = pandas.DataFrame.from_dict([new_emp_data])
            new_data_df = new_data_df.set_index("employee_id")
            if new_emp_data.get("employee_id") in repo_df.index:
                repo_df.update(new_data_df)
            else:
                repo_df = repo_df.append(new_data_df)
            repo_df.to_csv(path)
        except (pandas.errors.EmptyDataError, FileNotFoundError):
            repo_df = pandas.DataFrame.from_dict([new_emp_data])
            repo_df = repo_df.set_index("employee_id")
            repo_df.to_csv(path)
    
    def test_all_database_positions_filled_from_empty(
            self, tmp_path, session, cursor, requests_mock):
        utility = employee_utility(session)
        open_jobs = utility.get_open_positions()
        path = tmp_path / "test_1_employee_repo.csv"
        requests_mock.get(RAND_USER_URL, status_code = 200, json = MOCK_JSON)
        utility.hire_all_open_positions(path)
        cursor.execute("SELECT location_id, position_id FROM employee")
        assert cursor.fetchall() == open_jobs

    def test_all_repo_positions_filled_from_empty(
        self, tmp_path, session, requests_mock):
        utility = employee_utility(session)
        open_jobs = utility.get_open_positions()
        path = tmp_path / "test_2_employee_repo.csv"
        requests_mock.get(RAND_USER_URL, status_code = 200, json = MOCK_JSON)
        utility.hire_all_open_positions(path)
        repo_df = pandas.read_csv(path)
        assert len(repo_df.index) == len(open_jobs)

    def test_all_database_positions_filled_from_part_filled(
            self, tmp_path, session, cursor, requests_mock):
        utility = employee_utility(session)
        open_jobs = utility.get_open_positions()
        path = tmp_path / "test_3_employee_repo.csv"
        half_count = round(len(open_jobs) / 2)
        for idx in range(0, half_count):
            self.add_employee(open_jobs[idx][0], open_jobs[idx][1],
                         cursor, session, path)
        requests_mock.get(RAND_USER_URL, status_code = 200, json = MOCK_JSON)
        utility.hire_all_open_positions(path)
        cursor.execute("SELECT location_id, position_id FROM employee")
        assert cursor.fetchall() == open_jobs

    def test_all_repo_positions_filled_from_part_filled(
            self, tmp_path, session, cursor, requests_mock):
        utility = employee_utility(session)
        open_jobs = utility.get_open_positions()
        path = tmp_path / "test_4_employee_repo.csv"
        half_count = round(len(open_jobs) / 2)
        for idx in range(0, half_count):
            self.add_employee(open_jobs[idx][0], open_jobs[idx][1],
                         cursor, session, path)
        requests_mock.get(RAND_USER_URL, status_code = 200, json = MOCK_JSON)
        utility.hire_all_open_positions(path)
        repo_df = pandas.read_csv(path)
        assert len(repo_df.index) == len(open_jobs)

    def test_sample_names_are_unique(self, tmp_path, session, cursor):
        utility = employee_utility(session)
        path = tmp_path / "test_5_employee_repo.csv"
        open_jobs = utility.get_open_positions()
        for idx in range(0, len(open_jobs) - 10):
            self.add_employee(open_jobs[idx][0], open_jobs[idx][1],
                         cursor, session, path)
        utility.hire_all_open_positions(path)
        cursor.execute("SELECT name FROM employee")
        names = cursor.fetchall()[-10::1]
        assert len(names) == len(set(names))
            
        

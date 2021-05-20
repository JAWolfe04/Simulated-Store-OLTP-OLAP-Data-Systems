import pytest
import pandas
import copy

from src.employee.employee_utilities import employee_utility
from tests.constants import MOCK_EMPLOYEE_DATA
        
@pytest.mark.update_emp_repo
@pytest.mark.usefixtures("setup_employees", "reset_employees", "setup_employee")
class Test_Update_Employee_Repository:
    def write_test_employee_repo(self, employee_data, path):
        if path.exists(): path.remove()
        repo_df = pandas.DataFrame.from_dict([employee_data])
        repo_df.to_csv(path, index = False)
        if "employee_id" in repo_df.columns:
            repo_df = repo_df.set_index("employee_id")
        return repo_df
  
    def test_creates_csv_repo(self, session, tmp_path):
        path = tmp_path / "test_1_employee_repo.csv"
        if path.exists(): path.remove()
        employee_utility(session).update_employee_repository(
            MOCK_EMPLOYEE_DATA, path)
        assert path.exists()

    def test_updates_empty_csv_repo(self, session, tmp_path):
        path = tmp_path / "test_2_employee_repo.csv"
        self.write_test_employee_repo({}, path)
        employee_utility(session).update_employee_repository(
            MOCK_EMPLOYEE_DATA, path)
        assert len(path.read_text().strip()) > 0

    def test_updates_csv_repo_with_data(self, session, cursor, tmp_path):
        path = tmp_path / "test_3_employee_repo.csv"
        pre_emp_repo_df = self.write_test_employee_repo(
            MOCK_EMPLOYEE_DATA, path)
        # Use different data so the record is added and not updated
        new_emp_data = copy.deepcopy(MOCK_EMPLOYEE_DATA)
        new_emp_data["employee_id"] = 2
        new_emp_data["location_id"] = 2
        cursor.execute("INSERT INTO employee (location_id, position_id, "
                       "name, salary, start_date) VALUES (2, 1, "
                       "'Sophie Young', 50000.00, '2021-05-16')")
        session.commit()
        employee_utility(session).update_employee_repository(
            new_emp_data, path)
        post_emp_repo_df = pandas.read_csv(path)
        assert len(post_emp_repo_df.index) > len(pre_emp_repo_df.index)

    def test_updates_proper_field_for_employee(self, session, tmp_path):
        path = tmp_path / "test_4_employee_repo.csv"
        pre_emp_repo_df = self.write_test_employee_repo(
            MOCK_EMPLOYEE_DATA, path)
        # Using the same employee_id should cause an update
        new_emp_data = copy.deepcopy(MOCK_EMPLOYEE_DATA)
        new_emp_data["salary"] = 60000.00
        employee_utility(session).update_employee_repository(
            new_emp_data, path)
        post_emp_repo_df = pandas.read_csv(path)
        post_emp_repo_df = post_emp_repo_df.set_index("employee_id")
        post_emp_repo_df = post_emp_repo_df.astype({"postal_code": str})
        assert len(post_emp_repo_df.index) == len(pre_emp_repo_df.index)
        assert post_emp_repo_df.loc[1, "salary"] == 60000.00
        test_fields = ["location_id", "position_id", "start_date", "gender",
                       "name", "address", "city", "state_code", "postal_code",
                       "email", "dob", "phone", "cell"]
        assert post_emp_repo_df.loc[1, test_fields].equals(
            pre_emp_repo_df.loc[1, test_fields])
    
    def test_only_accepts_csv_files(self, session, tmp_path):
        path = tmp_path / "test_5_employee_repo.xml"
        with pytest.raises(ValueError):
            assert employee_utility(session).update_employee_repository(
                MOCK_EMPLOYEE_DATA, path)

    def test_with_non_existing_directory(self, session, tmp_path):
        path = tmp_path / "sub" / "test_6_employee_repo.csv"
        with pytest.raises(FileNotFoundError):
            assert employee_utility(session).update_employee_repository(
                MOCK_EMPLOYEE_DATA, path)

    @pytest.mark.parametrize("has_data, has_path", [
        (False, True), (True, False)])
    def test_with_wrong_input_type(self, session, tmp_path, has_data, has_path):
        path = tmp_path / "test_7_employee_repo.csv" if has_path else None
        emp_data = MOCK_EMPLOYEE_DATA if has_data else None
        with pytest.raises(TypeError):
            assert employee_utility(session).update_employee_repository(
                emp_data, path)

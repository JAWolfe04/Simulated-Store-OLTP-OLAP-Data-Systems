import pytest

from src.employee.employee_utilities import employee_utility

@pytest.mark.open_positions
@pytest.mark.usefixtures("setup_employees")
class Test_Get_Open_Positions:
    @pytest.fixture
    def get_total_jobs(self, cursor):
        cursor.execute("SELECT COUNT(*) FROM job_position")
        jobs_len = cursor.fetchall()[0][0]
        cursor.execute("SELECT COUNT(*) FROM location")
        locations_len = cursor.fetchall()[0][0]
        return jobs_len * locations_len
    
    def test_gives_correct_list_length(self, session, cursor, get_total_jobs):
        cursor.execute("DELETE FROM employee")
        session.commit()
        open_jobs = employee_utility(session).get_open_positions()
        assert get_total_jobs == len(open_jobs)

    def test_omits_filled_jobs(self, session, cursor, get_total_jobs):
        cursor.execute("DELETE FROM employee")
        cursor.execute(
            "INSERT INTO employee (location_id, position_id, name, salary, "
            "start_date) VALUES (1, 1, 'Jane Doe', 50000.00, '2021-5-17')")
        cursor.execute(
            "INSERT INTO employee (location_id, position_id, name, salary, "
            "start_date) VALUES (2, 1, 'Jane Doe', 50000.00, '2021-5-17')")
        cursor.execute(
            "INSERT INTO employee (location_id, position_id, name, salary, "
            "start_date) VALUES (3, 1, 'Jane Doe', 50000.00, '2021-5-17')")
        cursor.execute(
            "INSERT INTO employee (location_id, position_id, name, salary, "
            "start_date) VALUES (4, 1, 'Jane Doe', 50000.00, '2021-5-17')")
        cursor.execute(
            "INSERT INTO employee (location_id, position_id, name, salary, "
            "start_date) VALUES (5, 1, 'Jane Doe', 50000.00, '2021-5-17')")
        session.commit()

        open_jobs = employee_utility(session).get_open_positions()
        assert (get_total_jobs - 5) == len(open_jobs)

    def test__fired_emp_dont_fill_jobs(self, session, cursor, get_total_jobs):
        cursor.execute("DELETE FROM employee")
        cursor.execute(
            "INSERT INTO employee (location_id, position_id, name, salary, "
            "start_date, end_date) VALUES (6, 1, 'Jane Doe', 50000.00, "
            "'2019-8-2','2021-5-17')")
        cursor.execute(
            "INSERT INTO employee (location_id, position_id, name, salary, "
            "start_date, end_date) VALUES (7, 1, 'Jane Doe', 50000.00, "
            "'2019-8-2','2021-5-17')")
        cursor.execute(
            "INSERT INTO employee (location_id, position_id, name, salary, "
            "start_date, end_date) VALUES (8, 1, 'Jane Doe', 50000.00, "
            "'2019-8-2','2021-5-17')")
        cursor.execute(
            "INSERT INTO employee (location_id, position_id, name, salary, "
            "start_date, end_date) VALUES (9, 1, 'Jane Doe', 50000.00, "
            "'2019-8-2','2021-5-17')")
        cursor.execute(
            "INSERT INTO employee (location_id, position_id, name, salary, "
            "start_date, end_date) VALUES (10, 1, 'Jane Doe', 50000.00, "
            "'2019-8-2','2021-5-17')")
        session.commit()

        open_jobs = employee_utility(session).get_open_positions()
        assert get_total_jobs == len(open_jobs)

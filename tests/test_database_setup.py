import pytest

@pytest.mark.database_setup
class Test_Database_Setup: 
    def test_database_connection(self, session):
        assert session.is_connected()

    def test_create_db_setup(self, cursor):
        cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in cursor.fetchall()]
        assert "testdb" in databases

    @pytest.mark.usefixtures("setup_departments")
    def test_department_table_setup(self, cursor):
        cursor.execute("SELECT * FROM department")
        departments = [dept[1] for dept in cursor.fetchall()]
        expected_dept = ["Management", "Home and Office",
                         "Beauty, Bath and Health", "Food"]
        assert all(dept in departments for dept in expected_dept)

    @pytest.mark.usefixtures("setup_jobs")
    def test_position_table_setup(self, cursor):
        cursor.execute("SELECT * FROM job_position")
        jobs = {job[2] for job in cursor.fetchall()}
        assert len(jobs) == 7

    @pytest.mark.usefixtures("setup_locations")
    def test_location_table_setup(self, cursor):
        cursor.execute("SELECT * FROM location")
        assert len(cursor.fetchall()) == 10

    @pytest.mark.usefixtures("setup_employees")
    def test_employee_table_setup(self, cursor):
        cursor.execute("DESCRIBE employee")
        col_names = [col[0] for col in cursor.fetchall()]
        expected_names = ["employee_id", "location_id", "position_id",
                          "salary", "start_date", "end_date"]
        assert all(col in col_names for col in expected_names)

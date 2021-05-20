import pytest

from src.employee.employee_utilities import employee_utility

@pytest.mark.location_id_validator
@pytest.mark.usefixtures("setup_locations")
class Test_Location_Id_Validator:
    def test_with_valid_ids(self, session, cursor):
        cursor.execute("SELECT location_id from location")
        for location_id in cursor.fetchall():
            employee_utility(session).location_id_validator(location_id[0])
    
    @pytest.mark.parametrize("location_id, error", [
        (None, TypeError), (-1, ValueError), (10000, ValueError)])
    def test_with_undesired_input(self, session, location_id, error):
        with pytest.raises(error):
            assert employee_utility(session).location_id_validator(location_id)

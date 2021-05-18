import pytest

from src.employee.employee_utilities import employee_utility, RAND_USER_URL

@pytest.mark.class_init
class Test_Employee_Utility_Class_Initialization:
    def test_init(self, session):
        assert employee_utility(session)

    def test_init_with_none_provided(self):
        with pytest.raises(TypeError):
            assert employee_utility(None)

import pytest

from src.utils.helpers.common import login_and_verify_dashboard
from src.utils.helpers.common_checks import check_login_error_message
from src.utils.helpers.login_helper import login_with_credentials


@pytest.mark.smoke_checklist
@pytest.mark.parametrize("role", ["learner","trainer","admin"])
async def test_login_with_valid_credentials(page,role):
         await login_and_verify_dashboard(page,role)

@pytest.mark.regression
@pytest.mark.parametrize("role",["learner","trainer","admin"])
async def test_login_with_invalid_email(page,role):
    await login_with_credentials(page,role,"john!doe@example.com", "test-login")
    error_message=await check_login_error_message(page)
    if error_message:
        print(f"Login Failed !! Error:{error_message}")






import re

import pytest
from playwright.async_api import expect

from src.utils.helpers.common_checks import check_login_error_message, check_success_message
from src.utils.helpers.csv_reader import get_random_credentials_from_google_sheet
from src.utils.helpers.logger import logger
from src.utils.helpers.login_helper import login_with_credentials


@pytest.mark.smoke_checklist
@pytest.mark.parametrize("role", ["learner","trainer","admin"])
async def test_login_with_valid_credentials(page,role):
    #login
    user=get_random_credentials_from_google_sheet(role)
    await login_with_credentials(page,role,user["email"],user["password"])

    # Check for error message
    err_msg = await check_login_error_message(page)
    if err_msg:
         pytest.fail(f"\nLogin Failed!!")

    #Chcek for success message
    success_msg=await check_success_message(page)
    assert success_msg, f"Login success msg not found for role {role}"

    #Verify dashboard
    await expect(page).to_have_url(re.compile(r".*dashboard.*"))
    logger.info(f"Login successful for {role} - redirected to dashboard")



@pytest.mark.regression
@pytest.mark.parametrize("role",["learner","trainer","admin"])
async def test_login_with_invalid_email(page,role):
    #login
    await login_with_credentials(page,role,"john!doe@example.com", "test-login")

    #Check for error msg
    error_message=await check_login_error_message(page)
    if error_message:
       logger.info(f"Login Failed !! Error:{error_message}")






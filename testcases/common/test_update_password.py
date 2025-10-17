import re

import pytest
from playwright.async_api import expect

from src.base.base_page import BasePage
from src.utils.generators.data_generator import get_random_digits
from src.utils.helpers.common_checks import check_success_message, check_and_close_page_modal
from src.utils.helpers.logger import logger
from src.utils.helpers.login_helper import login_with_credentials
from src.utils.helpers.update_password_manager import get_cred_from_json, save_new_password_in_json_file


@pytest.mark.parametrize("role",["learner","trainer"])
async def test_user_is_able_to_login_with_updated_password(page,role):
    cred=get_cred_from_json(role)

    # Login with Email Password
    try:
        await login_with_credentials(page,role,cred["email"],cred["password"])
        await check_and_close_page_modal(page)
    except Exception as e:
        raise Exception(f"Unable to navigate to Settings {str(e)}")

    #Update Password
    new_password = get_random_digits(8)

    try:
        base_page=BasePage(page)
        success=await base_page.update_password(cred["password"],new_password)
        assert success,f"Unable to update password"
        logger.info("\nPassword updated successfully")
    except Exception as e:
        raise Exception(f"Unable to update password {str(e)}")

    # #Logout
    await page.locator("//span[contains(text(),'Logout')]").click()

    #Login with updated password
    try:
        logger.info("\nLogging With Updated Password.....")
        await login_with_credentials(page, role, cred["email"], new_password)
        logger.info(await check_success_message(page))
        # Save new password
        save_new_password_in_json_file(role, new_password)
    except Exception as e:
        raise Exception(f"Unable to login with updated password {str(e)}")

from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.pages.admin.learners.admin_learners import AdminLearner
from src.utils.helpers.admin.learner_helper import change_account_status
from src.utils.helpers.common_checks import check_success_message, check_login_error_message
from src.utils.helpers.logger import logger
from src.utils.helpers.login_helper import login_by_name_or_email


async def test_deactivate_learner_account_prevents_login(page,login):
    """Test that if admin deactivates learner account
    then learner should not allow to login"""

    #login to admin portal
    await login(page,"admin")

    #navigate to learner
    menu=AdminDashboard(page)
    await menu.navigate_to_learner()

    #Navigate to activated list
    await page.get_by_role("button", name=AdminLearner.STATUS_ACTIVATED).first.click()

    #Change account status from activated to deactivated
    target_email = await change_account_status(page, "activate")

    # Navigate to Learner portal
    url = "https://beta.findyourcourses.org/signin"
    await page.goto(url)
    logger.info(f"Navigating to : {url}")

    #Login by email
    await login_by_name_or_email(page,"learner",target_email)

    #verify deactivation msg
    err_msg = await check_login_error_message(page)
    assert "account is not activated" in err_msg

    logger.info(f"Verified!! Got Message > {err_msg}")

async def test_activate_learner_account_allows_login(page,login):
    """Test that if admin activates learner account
    then learner should allow to login"""

    #login to admin portal
    await login(page,"admin")

    #navigate to learner
    menu=AdminDashboard(page)
    await menu.navigate_to_learner()

    #Navigate to deactivated list
    await page.get_by_role("button", name=AdminLearner.STATUS_DEACTIVATED).first.click()

    #Change account status from deactivated to activated
    target_email = await change_account_status(page, "deactivate")

    # Navigate to Learner portal
    url="https://beta.findyourcourses.org/signin"
    await page.goto(url)
    logger.info(f"\nNavigating to : {url}")

    #Login by email
    await login_by_name_or_email(page,"learner",target_email)

    # verify message
    success_msg = await check_success_message(page)
    logger.info(f"\n{success_msg}")
    assert "user login" in success_msg.lower(), f"Expected {success_msg} but got: {success_msg}"


    logger.info(f"Verified!! Got Message > {success_msg}")

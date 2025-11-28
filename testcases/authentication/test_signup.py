import pytest
from src.utils.generators.generate_test_data import get_random_digits
from src.utils.helpers.common_checks import check_err_msg, check_and_close_page_modal
from src.utils.helpers.logger import logger

@pytest.mark.regression
async def test_learner_signup_with_existing_email_shows_error_message(page):
    """Learner Signup With Existing Email"""
    await page.goto("https://findyourcourses.org/signup")
    await page.locator("#name").fill("Mariam Imran")
    await page.locator("#email").fill("fyctest5401+23@gmail.com")
    await page.locator("#contactNumber").fill("+923351209776")
    password=page.locator("#password")
    await password.fill(get_random_digits(8))
    confirm_password=await password.input_value()
    await page.locator("#confirmPassword").fill(confirm_password)
    signup_btn=page.get_by_role("button",name="Sign Up")
    await signup_btn.nth(2).click()
    err_msg=await check_err_msg(page)
    assert err_msg,f"\nSystem didnt show any error msg"
    logger.info(f"\nVerified! Signup with existing email shows error message\n{err_msg} ")

async def test_trainer_signup_with_existing_email_shows_error_message(page):
    """Trainer Signup With Existing Email"""
    await page.goto("https://beta-tp.findyourcourses.org/signup")
    await check_and_close_page_modal(page)
    await page.locator("#name").fill("Mariam Imran")
    await page.locator("#email").fill("fyctest5401+42@gmail.com")
    await page.locator("#password").fill(get_random_digits(8))
    continue_btn = page.get_by_role("button", name="Continue")
    await continue_btn.click()
    err_msg = await check_err_msg(page)
    assert err_msg, f"\nSystem didnt show any error msg"
    logger.info(f"\nVerified! Signup with existing email shows error message\n{err_msg} ")

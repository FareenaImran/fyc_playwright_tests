import re
from datetime import date, timedelta
from playwright.async_api import expect
from src.utils.helpers.common_checks import check_and_close_page_modal, check_login_error_message
from src.utils.helpers.csv_reader import get_untried_emails
from src.utils.helpers.logger import logger
from src.utils.helpers.login_helper import login_with_credentials


#Select dropdown option from React Select
async def rs_dropdown(page,locator_value,options):
    await page.locator(locator_value).click()
    for option in options:
        await page.fill(locator_value,option)
        await page.keyboard.press("Enter")

##Login
async def login_and_verify_dashboard(page,role:str):
    tried_emails = set()
    while True:
        user = get_untried_emails(role, tried_emails)
        user_email = user["email"]
        tried_emails.add(user_email)
        await login_with_credentials(page, role, user_email, user["password"])
        err_msg = await check_login_error_message(page)
        if err_msg:
            logger.info(f"Error  :{err_msg}")
            continue
        await expect(page).to_have_url(re.compile(r"/dashboard$"))
        assert "dashboard" in page.url or "profile" in await page.content()
        logger.info(f"\nLogin successful for role: {role} - {user['email']}")
        logger.info(f"\nNavigated to : {page.url}")
        await check_and_close_page_modal(page)
        return user

#Navigate to Courses
async def navigate_to_courses(page):
    await check_and_close_page_modal(page)
    await page.get_by_role("button", name="Courses").first.click()
    await expect(page).to_have_url(re.compile(r".*/courses$"))
    print(f"Navigated to {page.url}")
    await check_and_close_page_modal(page)
    await page.wait_for_load_state("domcontentloaded")


#picks today + days_from_today
async def pick_date(page, locator, days_from_today=0):
    await locator.click()
    await page.wait_for_timeout(500)

    target_date = date.today() + timedelta(days=days_from_today)

    # Find the VISIBLE calendar
    calendar = page.locator(
        'div[role="dialog"]:visible, [role="application"]:visible, .calendar-container:visible').first
    await calendar.wait_for(state='visible')

    # Navigate to correct month
    current_month = await calendar.locator('[aria-live="polite"]').text_content()
    while target_date.strftime("%B %Y") not in current_month:
        if target_date > date.today():
            await calendar.locator('button[aria-label*="next month"]').click()
        else:
            await calendar.locator('button[aria-label*="previous month"]').click()
        await page.wait_for_timeout(300)
        current_month = await calendar.locator('[aria-live="polite"]').text_content()

    # Click the day within this specific calendar
    await calendar.locator(f'button:has-text("{target_date.day}")').first.click()
    return target_date
import re
from datetime import date, timedelta
from playwright.async_api import expect
from src.utils.helpers.common_checks import check_and_close_page_modal, check_login_error_message, check_success_message
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
        print(await check_success_message(page))
        # logger.info(f"\nLogin successful for role: {role} - {user['email']}")
        logger.info(f"\nNavigated to : {page.url}")
        await check_and_close_page_modal(page)
        return user


#open action menu and select option
async def select_menu_option(page,text,option):
    #open menu
    action_btn = page.locator(f"tr:has-text('{text}') td:last-child button")
    await action_btn.click()

    #Select option
    menu_option = page.locator(f"div[role='menu']  div:nth-child({option})")
    await menu_option.wait_for(state="visible")
    await menu_option.click()

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
    await calendar.locator(f'button:has-text("{target_date.day}"):not([disabled])').first.click()
    return target_date

#Get card by specific locator [name, book,mark]
async def find_and_open_card_by_element(page,elements,element):
    first_ele=elements.first
    await first_ele.wait_for(state="visible")
    page_no = 1
    while True:
        await page.wait_for_load_state('domcontentloaded')
        all_elements = await elements.all()

        for elem in all_elements:
            title = await elem.get_attribute("title")
            if  title.strip() == element:
                print(f"Found '{element}' on page {page_no}.")
                parent_ele=elem.first.locator("xpath=..")
                await parent_ele.wait_for(state="visible")
                await parent_ele.click()
                await page.wait_for_load_state('domcontentloaded')
                return element

        next_btn = page.locator("//button[contains(text(),'Next')]")
        await next_btn.scroll_into_view_if_needed()

        if await next_btn.is_enabled():
            page_no += 1
            await next_btn.click()
        else:
            print("no more pages to check further..")
            break

    raise Exception(f"Did not find {element} in any page ")




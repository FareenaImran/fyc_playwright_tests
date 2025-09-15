import re

from selenium.webdriver.common.devtools.v133.dom import query_selector

from src.locators.base_locators.common_locators import CommonLocators
from src.locators.base_locators.login_locators import LoginLocators
from src.utils.helpers.logger import logger
from src.utils.helpers.login_helper import login_with_credentials
from src.utils.test_data.csv_reader import get_untried_emails
from playwright.async_api import expect


#Navigate to course
async def navigate_to_courses(page):
    await close_in_page_modal(page)
    await page.get_by_role("button", name="Courses").first.click()
    await expect(page).to_have_url(re.compile(r".*/courses$"))
    print(f"Navigated to {page.url}")
    await close_in_page_modal(page)
    await page.wait_for_load_state("domcontentloaded")

async def is_btn_enabled(page,btn):
    await expect(btn).to_be_enabled(timeout=5000)
    await btn.click()

async def check_element_in_table(page,text,column,status):
    try:
        # Wait for table to be visible
        await page.wait_for_selector("tbody", state="visible", timeout=20000)

        # Get all cells in the specified column
        cell_selector = f"tbody tr td:nth-child({column})"
        await page.wait_for_selector(cell_selector, state="attached")
        cells = await page.query_selector_all(cell_selector)

        # Check each cell for the text (looking at all text content)
        text_exists = False
        for cell in cells:
            cell_text = (await cell.text_content() or "").strip()
            cell_title = (await cell.get_attribute("title") or "").strip()
            if str(text).strip() in cell_text or str(text).strip() in cell_title:
                text_exists = True
                break

        if not text_exists:
            # raise  Exception(f"'{text}' does not exist in table column {column}")
            return False,None

        print(f"\n'{text}' exists in: {status}")

        # Find the specific row containing the text
        row_selector = f'tbody tr:has(td:nth-child({column}):has-text("{text}"))'
        text_row = await page.query_selector(row_selector)

        if text_row:
            # Get headers
            headers = []
            header_elements = await page.query_selector_all("thead tr th")
            for header in header_elements:
                headers.append((await header.text_content()).strip())

            # Get all cells from the row
            cells = await text_row.query_selector_all('td')
            row_data = []

            for i, (header, cell) in enumerate(zip(headers, cells), 1):
                try:
                    dropdown=await cell.query_selector("select")
                    if dropdown:
                        select_text=await dropdown.query_selector("option:checked")
                        cell_text=(await select_text.text_content()).strip()
                        print(f"{header}: {cell_text}")
                    else:
                        cell_text=(await cell.text_content() or "").strip()
                        if not cell_text:
                            img = await cell.query_selector('img')
                            if img:
                                cell_text = await img.get_attribute('alt') or "[Image]"
                                print(f"Image found in {header}: {cell_text}")

                except Exception as e:
                    print(f"Error processing cell {header}: {e}")
                    cell_text = "Error"

                row_data.append(f"{header} : {cell_text.strip()}")

            print("\nDetails in table:")
            print("\n".join(row_data))
            return text,text_row

        print(f"Found '{text}' in column but couldn't locate row")
        return False,None

    except Exception as e:
        print(f"Error checking element in table: {str(e)}")
        return False,None


#Close modal
async def close_in_page_modal(page):
    modal_selector = '[role="dialog"][data-state="open"]'
    close_btn_selector = "[role='dialog'][data-state='open']>.absolute.right-4"

    try:
        # Wait a short time for the modal to appear
        await page.wait_for_selector(modal_selector, timeout=500)
        print("[MODAL DETECTED] Closing it...")

        await page.click(close_btn_selector)
        print("[MODAL CLOSED]")
    except:
        # No modal detected within the timeout
        pass

#Login
async def login_and_verify_dashboard(page,role:str):
    tried_emails = set()
    while True:
        user = get_untried_emails(role, tried_emails)
        user_email = user["email"]
        tried_emails.add(user_email)
        await login_with_credentials(page, role, user_email, user["password"])
        err_msg = await get_login_error_message(page)
        if err_msg:
            logger.info(f"Error  :{err_msg}")
            continue
        await expect(page).to_have_url(re.compile(r"/dashboard$"))
        assert "dashboard" in page.url or "profile" in await page.content()
        print("=" * 60)
        logger.info(f"\nNavigated to {role} Portal : {page.url}" )
        print("=" * 60)
        logger.info(f"\nLogin successful for role: {role} - {user['email']}")
        logger.info(f"\nNavigated to : {page.url}")
        await close_in_page_modal(page)
        return user

async def get_login_error_message(page):
    try:
        await page.wait_for_selector(LoginLocators.EMAIL_ERR_MSG, timeout=10000)
        error_locator = page.locator(LoginLocators.EMAIL_ERR_MSG).filter(has_text=re.compile(
                r"(invalid|valid email address|invalid-credential|account not activated)",re.IGNORECASE)).first

        if await error_locator.is_visible():
            return await error_locator.inner_text()
            # return await error_locator.text_content()

    except TimeoutError as e:
       print (f"Time out error {e}")
       return None
    return None


async def get_success_message(page):
    try:
        await page.wait_for_selector(CommonLocators.SUCCESS_MSG, timeout=10000)
        success_locator = page.locator(CommonLocators.SUCCESS_MSG).filter(has_text=re.compile(
                r"(Live|Under Review|Need Attention|Approved)",re.IGNORECASE)).first

        if await success_locator.is_visible():
            return await success_locator.text_content()

    except TimeoutError as e:
       print (f"Time out error {e}")
       return None
    return None


#Check element in all pages
async def check_ele_in_all_pages(page,text,column,status):
    original_text=text
    page_no=1
    while True:
        text,text_row=await check_element_in_table(page,original_text,column,status)
        if text:
            return text,text_row

        next_btn = page.locator("//button[contains(text(),'Next')]")
        await next_btn.scroll_into_view_if_needed()

        if await next_btn.is_enabled():
            page_no+=1
            print(f"Finding {original_text} in Page # {page_no}....")
            await next_btn.click()
            await page.wait_for_load_state('networkidle')
            continue
        else:
            break

    raise Exception(f"Did not find {original_text} in current page and no more pages to check further..")









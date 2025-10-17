import re
from src.locators.base_locators.common_locators import CommonLocators
from src.locators.base_locators.login_locators import LoginLocators
from src.utils.generators.data_generator import get_image
from src.utils.helpers.logger import logger
from playwright.async_api import expect, Error


#Check btn is enabled?
async def check_is_btn_enabled(page,btn):
    await btn.scroll_into_view_if_needed()
    await expect(btn).to_be_enabled()
    await btn.click()

#Check Broken Images
async def check_broken_images(page):

    """Check if there are any broken images on the current page."""
    broken_images=set()
    await page.wait_for_timeout(2000)
    await page.wait_for_load_state("networkidle")
    img_elements=await page.locator('img').all()

    for img in img_elements:
        src=await img.get_attribute("src")

        if not src:
            continue
        #remove spaces in url
        src = src.replace(" ", "").strip()

        if not await img.is_visible():
            continue

        await page.wait_for_timeout(200)
        is_broken = await img.evaluate("""
                    img => !img.complete | img.naturalWidth == 0 | img.naturalHeight == 0
                """)

        if is_broken :
             broken_images.add(src)

    return broken_images


#Check element is present in table
async def check_element_in_table(page, text, column, status):
    try:
        # Wait for table
        await page.wait_for_selector("tbody tr", state="visible")

        # All cells in given column
        cells = await page.query_selector_all(f"tbody tr td:nth-child({column})")

        for cell in cells:
            cell_text = (await cell.text_content() or "").strip()
            cell_title = (await cell.get_attribute("title") or "").strip()

            if str(text).strip() in (cell_text or cell_title):
                print(f"\n'{text}' exists in '{status}'")

                # Row containing the text
                row = await cell.evaluate_handle("el => el.closest('tr')")
                row_cells = await row.query_selector_all("td")

                # Print all cell values in row
                row_data = []
                for c in row_cells:
                    dropdown = await c.query_selector("select")
                    if dropdown:
                        selected = await dropdown.query_selector("option:checked")
                        value = (await selected.text_content()).strip() if selected else ""
                    else:
                        value = (await c.text_content() or "").strip()
                    row_data.append(value)
                print(" | ".join(row_data))
                return text, row

        print(f"'{text}' not found in {status}")
        return False, None

    except Exception as e:
        print(f"Error checking table: {e}")
        return False, None

#Close modal
async def check_and_close_page_modal(page):
    try:
        close_btn = page.get_by_role("button", name="Close")
        await close_btn.wait_for(state="visible", timeout=3000)
        await close_btn.click(force=True)
        return
    except Exception as e:
        # No modal detected within the timeout
        pass

#Login Error
async def check_login_error_message(page):
    try:
        await page.wait_for_selector(LoginLocators.EMAIL_ERR_MSG)
        error_locator = page.locator(LoginLocators.EMAIL_ERR_MSG).filter(has_text=re.compile(
                r"(invalid|valid email address|invalid-credential|account not activated)",re.IGNORECASE)).first

        if await error_locator.is_visible():
            return await error_locator.text_content()

    except Error as e:
       logger.warning (f"Time out error {e}")
       return None
    return None

#Check success message
async def check_success_message(page):
    try:
        await page.wait_for_selector(CommonLocators.SUCCESS_MSG)
        success_locator = page.locator(CommonLocators.SUCCESS_MSG).filter(has_text=re.compile(
                r"(Live|Under Review|Need Attention|approved|profile|success|login|featured|deactivated|active|claim|Request)",re.IGNORECASE)).first

        if await success_locator.is_visible():
            return await success_locator.inner_text()

    except TimeoutError as e:
       print (f"Time out error {e}")
       return None
    return None


#Check element in all pages
async def check_ele_in_all_pages(page,text,column,status):
    original_text=text
    page_no=1
    while True:
        print(f"\nFinding {original_text} in Page # {page_no}....")
        text,text_row=await check_element_in_table(page,original_text,column,status)
        if text:
            return text,text_row
        next_btn = page.locator("//button[contains(text(),'Next')]")
        await next_btn.scroll_into_view_if_needed()

        if await next_btn.is_enabled():
            page_no+=1
            await next_btn.click()
            await page.wait_for_load_state('networkidle')
        else:
            print("\nNo more pages to check further..")
            break

    raise Exception(f"Did not find {original_text} in any page ")

#check image uploaded successfully
async def upload_and_verify_image(page,image_input_locator, image_filename, alt_text):
    # Upload the image
    ele_id=await image_input_locator.get_attribute("id")
    await image_input_locator.set_input_files(get_image(image_filename))

    if ele_id and "cover" in ele_id.lower():
        await page.get_by_role("button", name="Save").click()

    # Verify the image
    image_element = page.get_by_alt_text(alt_text)
    image_src = await image_element.get_attribute("src")

    try:
        await expect(image_element).to_be_visible()
    except Exception:
        await expect(image_src).to_be_visible()

    return image_src
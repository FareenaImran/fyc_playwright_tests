import re
from datetime import date, timedelta
from playwright.async_api import expect

#Select dropdown option from React Select
async def rs_dropdown(page,locator_value,options):
    await page.locator(locator_value).click()
    for option in options:
        await page.fill(locator_value,option)
        await page.keyboard.press("Enter")


#open action menu and select option
async def select_menu_option(page,option,text):
    #open menu

    action_btn = page.locator(f"tr:has-text('{text}') td:last-child button").first
    await action_btn.scroll_into_view_if_needed()
    await action_btn.click()

    #Select option
    menu_option = page.locator(f"div[role='menu']  div:nth-child({option})").first
    await menu_option.wait_for(state="visible")
    await menu_option.click()
    return True

#View Details for specific
async def view_course_details(page):
    menu_option = page.locator(f"div[role='menu']  div:nth-child(1)").first
    await menu_option.wait_for(state="visible")
    await menu_option.click()

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

#Get card by specific locator [name, bookmark]
async def find_and_open_card_by_element(page,elements,element):
    first_ele=elements.first
    await first_ele.wait_for(state="visible")
    page_no = 1
    while True:
        print(f"\nFinding [{element}] on page # {page_no}....")
        await page.wait_for_load_state('domcontentloaded')
        all_elements = await elements.all()

        for elem in all_elements:
            title = await elem.get_attribute("title")
            if  title.strip() == element:
                print(f"\n\n'{element}' exists on page {page_no}.")
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

#Get button/text count
async def get_count(locator):
    try:
        # Wait for the element to contain a number in parentheses
        await locator.click()
        await expect(locator).to_contain_text(re.compile(r"\(\d+\)"), timeout=10000)

        text = (await locator.text_content()).strip()
        text_count = re.search(r"\((\d+)\)", text)

        if text_count:
            count = int(text_count.group(1))
            print(f"Get > {text}")
            return count
        return False

    except Exception as e:
        print(f"Expected count pattern not found: {e}")
        return False


#Count rows in all pages
async def count_rows_in_all_pages(page):
    rows=page.locator("tbody>tr")
    page_no=1
    count=0
    while True:
        await rows.first.wait_for(state="attached")
        next_btn=page.get_by_role("button" ,name="Next")
        rows_in_page= await rows.count()
        if rows_in_page>0 :
            if (await rows.first.text_content()) == "No records found":
                break
            count += rows_in_page
            print(f"Rows on page # {page_no} :{rows_in_page}")
            if await next_btn.is_visible():
                if await next_btn.is_enabled():
                    await next_btn.scroll_into_view_if_needed()
                    await next_btn.click()
                    page_no += 1
                else:
                    break
            else:
                break
        else:
            print(f"No Records found after page {page_no}")
            break

    print(f"\nTotal rows : {count}")
    return count

#Get rows
async def get_rows(page):
    await page.wait_for_load_state("domcontentloaded")
    await page.wait_for_selector("table > tbody > tr",state="visible")
    rows = page.locator("table > tbody > tr")
    count = await rows.count()
    if count==1:
        record=await rows.nth(0).locator("td").nth(0).inner_text()
        if record.strip()=="No records found":
            return 0,rows

    return count,rows


#Get row text
async def get_row_text(page,column_no,row_no=None):
    column=column_no-1
    count, rows = await get_rows(page)
    if count == 0:
        print("\nNo Records Found in Table !")
        return None
    if row_no is not None:
        if row_no>=count:
            raise Exception(f"Row {row_no} doesn't exist. Table has only {count} rows.")

        row = rows.nth(0)
        try:
            text=await row.locator("td").nth(column).inner_text()
            print(f"\nGot {text}  in table ")
            return text.strip()
        except Exception as e:
            raise Exception(f"Unable to get row text : {str(e)}")
    else:
        all_text=[]
        for i in range(count):
            row=rows.nth(i)
            try:
                text = await row.locator("td").nth(column).inner_text()
                all_text.append(text.strip())
            except Exception as e:
                raise Exception(f"Failed to get text from row {i}: {str(e)}")


        return all_text

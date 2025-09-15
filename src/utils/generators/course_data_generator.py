import datetime
import string
import random
from datetime import date, timedelta,datetime
from pathlib import Path

from playwright.async_api import expect

from src.utils.meta_data.course_data import COURSES, TP_NAMES, INSTRUCTORS


#Fees/Rupees
def get_random_digits():
    return f"{random.choices(string.digits,k=5)}"

#Instructor Name
def get_random_instructor_name():
    return f"{random.choice(INSTRUCTORS)}"

#course name
def get_random_course_name():
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"COURSE {random.choice(COURSES)} - {suffix}"

#TP name
def get_random_tp_name():
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{random.choice(TP_NAMES)} BETA TP {suffix}"

#field text
def get_random_data():
    suffix = "".join(random.choices(string.ascii_uppercase , k=50))
    return f"{suffix}"

#Image
def get_random_image():
    project_root = Path(__file__).resolve().parents[3]
    images_dir = project_root / "resources" / "images"
    image_files = [f for f in images_dir.iterdir() if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg", ".png","webp")]
    if not image_files:
        raise FileNotFoundError(f"No images found in {images_dir}")
    return str(random.choice(image_files))

#fill same fields
async def fill_same_fields(page,locator):
    for i in range(1, 5):
        field_id = f"{locator}{i}"
        random_text = get_random_data()
        await page.fill(field_id, random_text)
        print(f"Learning Objective {i} : {random_text}")

#select random radix dropdown
async def select_random_radix_dropdown(page, dropdown_locator, expected_time=None, timeout=5000):
    try:
        await expect(dropdown_locator).to_be_visible(timeout=timeout)
        await dropdown_locator.scroll_into_view_if_needed()

        current_time = (await dropdown_locator.text_content() or "").strip()
        if expected_time and current_time == expected_time:
            return expected_time

        listbox_id = await dropdown_locator.get_attribute("aria-controls")
        if not listbox_id:
            raise Exception("Dropdown missing aria-controls attribute")

        await dropdown_locator.click()
        listbox = page.locator(f'[id="{listbox_id}"][role="listbox"]')
        await expect(listbox).to_be_visible(timeout=timeout)

        options = listbox.locator('[role="option"]')
        count = await options.count()
        if count == 0:
            raise Exception("No time options found in dropdown")

        selected_text = None

        if expected_time:
            target_option = options.filter(has_text=expected_time)
            if await target_option.count() == 0:
                raise Exception(f"Time option '{expected_time}' not found")
            await target_option.click()
        else:
            idx = random.randint(0, count - 1)
            selected_option = options.nth(idx)
            selected_text = (await selected_option.text_content() or "").strip()
            await selected_option.click(force=True)

        return selected_text

    except Exception as e:
        print(f"Error selecting time: {str(e)}")
        raise


#Select random days
async def select_random_days(page):
    try:
        await page.wait_for_selector('div.flex.gap-4', state='visible', timeout=5000)
        day_buttons = await page.locator('div.flex.gap-4 > button[title]').all()

        if not day_buttons:
            raise Exception("No day buttons found")

        enabled_days = []
        for button in day_buttons:
            class_attr = await button.get_attribute('class')
            if 'bg-blue-500' not in class_attr:  # Skip already selected days
                enabled_days.append(button)

        if not enabled_days:
            print("All days already selected, selecting a random one anyway")
            enabled_days = day_buttons

        # Select and click random day
        selected_button = random.choice(enabled_days)
        day_name = await selected_button.get_attribute('title')
        await selected_button.click()

        selected_class = await selected_button.get_attribute('class')
        if 'bg-blue-500' not in selected_class:
            print(f"Warning: Day selection may not have worked - {day_name}")

        print(f"Selected Day: {day_name}")
        return day_name

    except Exception as e:
        print(f"Error selecting random day: {str(e)}")
        raise

#Checkbox
async def select_random_checkbox(page,checkboxes):
        count = await checkboxes.count()
        if count == 0:
            print("No checkboxes buttons found!")
            return

        random_index = random.randint(0, count - 1)
        checkbox = checkboxes.nth(random_index)

        # Small wait to avoid re-render timing issues
        await page.wait_for_timeout(200)

        checkbox_id = await checkbox.get_attribute("id")
        if checkbox_id:
            label_locator = page.locator(f'label[for="{checkbox_id}"]')
            if await label_locator.count() > 0:
                await label_locator.click()
            else:
                await checkbox.check(force=True)
        else:
            await checkbox.check(force=True)

        # Verify and retry once if needed
        try:
            await expect(checkbox).to_be_checked()
        except:
            print("Retry: Checkbox button is not checked after first attempt.")
            await checkbox.check(force=True)
            await expect(checkbox).to_be_checked()

        # Print label text if available
        label_text = ""
        if checkbox_id:
            try:
                label_text = await page.locator(f'label[for="{checkbox_id}"]').text_content()
            except:
                label_text = "(Label not found)"
        print(f"Selected Checkbox: {label_text.strip() if label_text else '(No label)'}")


#dropdown
async def select_random_dropdown_option(page,dropdown):
    await dropdown.scroll_into_view_if_needed()
    # Case 1: Native <select> dropdown
    if await dropdown.evaluate("el => el.tagName.toLowerCase()") == "select":
        options = await dropdown.locator("option").all()
        values = [await opt.get_attribute("value") for opt in options if await opt.get_attribute("value")]
        random_value = random.choice(values)
        await dropdown.select_option(random_value)
        print(f"Selected : {random_value.strip()}")
        return

    # Case 2: Custom dropdown
    await dropdown.click()

    # Wait for React Select menu to appear
    menu = page.locator(".css-xxx-menu, [class*='-menu']")
    await menu.wait_for()

    # Get all options inside THIS menu
    options = menu.locator("[id^='react-select-'][id*='-option-']")
    count = await options.count()

    if count == 0:
        print("No options found in Education Requirement dropdown")
        return

    # Pick a random option
    random_index = random.randint(0, count - 1)
    selected_option = options.nth(random_index)
    selected_text = (await selected_option.text_content()) or ""
    await selected_option.click()
    print(f"Selected: {selected_text.strip()}")

#Pick Date
async def navigate_to_date(page, target_date):
    """Navigate to the target month/year in the calendar"""
    max_retries = 3

    for retry in range(max_retries):
        try:
            # Wait for calendar to be fully loaded
            await page.wait_for_selector('[aria-live="polite"]', state='visible', timeout=5000)
            await page.wait_for_timeout(300)  # Allow calendar to stabilize

            # Get current month/year from calendar header
            month_year_locator = page.locator('[aria-live="polite"]').first
            await month_year_locator.wait_for(state='visible')
            month_year_text = await month_year_locator.text_content()

            if not month_year_text or len(month_year_text.split()) < 2:
                if retry < max_retries - 1:
                    await page.wait_for_timeout(500)
                    continue
                raise Exception("Cannot read calendar month/year")

            current_month_str, current_year_str = month_year_text.strip().split()
            current_year = int(current_year_str)
            current_month = datetime.strptime(current_month_str, "%B").month

            # Calculate months difference
            months_diff = (target_date.year - current_year) * 12 + (target_date.month - current_month)

            # Navigate months with proper waiting
            if months_diff > 0:
                next_button = page.locator('button[aria-label="Go to next month"]')
                for i in range(months_diff):
                    await next_button.wait_for(state='visible')
                    await next_button.click()
                    await page.wait_for_timeout(200)  # Wait for month change

            elif months_diff < 0:
                prev_button = page.locator('button[aria-label="Go to previous month"]')
                for i in range(abs(months_diff)):
                    await prev_button.wait_for(state='visible')
                    await prev_button.click()
                    await page.wait_for_timeout(200)  # Wait for month change

            # Verify we reached the target month
            await page.wait_for_timeout(300)
            final_header = await page.locator('[aria-live="polite"]').first.text_content()
            if target_date.strftime("%B %Y") in final_header:
                return True

        except Exception as e:
            if retry < max_retries - 1:
                print(f"Navigation retry {retry + 1}: {e}")
                await page.wait_for_timeout(1000)
            else:
                raise Exception(f"Failed to navigate to {target_date.strftime('%B %Y')}: {e}")

    return False


async def click_day(page, day, target_date):
    await page.wait_for_timeout(300)

    day_locator = page.locator(
        f'button:has-text("{day}")' +
        ':not([disabled])' +
        ':not(.day-outside)' +
        f'[aria-label*="{target_date.strftime("%B")}"]'
    ).first

    if await day_locator.count() == 0:
        visible_calendar = page.locator('div[role="dialog"]:visible, .calendar-container:visible').first
        day_locator = visible_calendar.locator(
            f'button:has-text("{day}")' +
            ':not([disabled])' +
            ':not(.day-outside)'
        ).first

    await day_locator.wait_for(state="visible", timeout=5000)
    await expect(day_locator).to_be_enabled()
    await day_locator.click()

    # Wait for calendar to close/update
    await page.wait_for_timeout(300)


# Pick Start Date (Present or Future)
async def select_random_present_or_future_date(page, locator):
    """Select a random date from today to 1 year ahead"""
    await locator.wait_for(state='visible')
    await locator.click()

    # Pick a random date from today to 1 year ahead
    today = date.today()
    random_days = random.randint(0, 365)
    target_date = today + timedelta(days=random_days)

    try:
        await navigate_to_date(page, target_date)
        await click_day(page, target_date.day, target_date)

        return target_date

    except Exception as e:
        raise Exception(f"Error selecting start date: {e}")


# Pick End Date After Start Date
async def pick_date_after_the_given_date(page, start_date_obj, locator):
    await locator.wait_for(state='visible')
    await locator.click()

    # Calculate date range (1 day to 1 year after start date)
    min_end_date = start_date_obj + timedelta(days=1)
    max_end_date = min_end_date + timedelta(days=365)
    days_diff = (max_end_date - min_end_date).days
    target_date = min_end_date + timedelta(days=random.randint(0, days_diff))

    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            await navigate_to_date(page, target_date)
            await click_day(page, target_date.day, target_date)
            return target_date

        except Exception as e:
            print(f"Attempt {attempt + 1} failed to pick end date: {e}")
            if attempt < max_attempts - 1:
                await page.wait_for_timeout(1000)
                # Re-open calendar if it closed
                await locator.click()
            else:
                raise Exception(f"Failed to select end date after {max_attempts} attempts: {e}")



# Select Same Date (for publish/unpublish dates)
async def select_same_date(page, locator, target_date):
    """Select a specific date that matches the given target_date"""
    await locator.wait_for(state='visible')
    await locator.click()

    try:
        await navigate_to_date(page, target_date)
        await click_day(page, target_date.day, target_date)

        return target_date

    except Exception as e:
        raise Exception(f"Error selecting same date {target_date.strftime('%B %d, %Y')}: {e}")

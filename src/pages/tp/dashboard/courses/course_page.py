import random
import re
import pytest
from playwright.async_api import expect
from src.base.base_page import BasePage
from src.pages.tp.dashboard.courses.fill_course_steps import FillCourseSteps
from src.pages.tp.dashboard.courses.fill_offering_steps import FillOfferingSteps
from src.pages.tp.dashboard.dashboard_page import TPDashboardPage
from src.utils.helpers.common_checks import check_element_in_table
from testcases.fixtures.login_fixtures import login


class CoursePage(BasePage):
    #Start Offering
    async def start_offering(self):
        await self.page.get_by_role("button", name="Continue to Start Offering this Course").click()
        await self.page.get_by_role("button", name="Add Course Offering").click()

    # Add New Course
    async def add_new_course(self):
        try:
            add_course_button = None
            for button_name in ["Add New Course", "Start Creating Course"]:
                button = self.page.get_by_role("button", name=button_name)
                if await button.count() > 0:
                    add_course_button = button
                    break

            if not add_course_button:
                raise Exception("No course creation button found")

            await expect(add_course_button).to_be_visible()
            await add_course_button.click()
            await self.page.get_by_role("button", name="Close").click()
            print("\nAdding new course...")
            course_steps=FillCourseSteps(self.page)
            course_name=await course_steps.fill_first_step()
            await course_steps.fill_second_step()
            await course_steps.fill_third_step()
            await course_steps.fill_fourth_step()
            return course_name

        except Exception as e:
            print(f"Error in handle_popup_and_click_button: {str(e)}")
            raise

    #Add New Offerings
    async def add_offering(self):
       try:
            offering_steps=FillOfferingSteps(self.page)
            await offering_steps.fill_first_step()
            await offering_steps.fill_second_step("No")
            await offering_steps.fill_third_step()
       except Exception as e:
           raise  Exception(f"Error{str(e)}")
    #Verify Course appears in [status]
    async def verify_course_appears_in_table(self,course_name:str,column_num:int,status:str):
        await self.page.get_by_role("button" ,name=status).click()
        course_name=await check_element_in_table(self.page,course_name,column_num,status)
        return course_name

    #Get Status Count
    async def click_any_non_empty_status(self):
            statuses = ["Live", "Approved", "Needs Attention"]
            buttons = self.page.locator(".flex.space-x-4.border-b-2 button")
            count = await buttons.count()
            eligible_buttons = []

            for i in range(count):
                btn = buttons.nth(i)
                text = (await btn.text_content() or "").strip()
                for status in statuses:
                    if text.startswith(status):
                        match = re.search(r"\((\d+)\)", text)
                        if match and int(match.group(1)) > 0:
                            eligible_buttons.append((status, btn))
                        break  # Avoid matching more than one status per button

            if eligible_buttons:
                chosen_status, chosen_btn = random.choice(eligible_buttons)
                print(f"Status: {chosen_status}")
                await chosen_btn.click()
                return chosen_status
            else:
                return None

    #Find course with status
    async def find_course_with_status(self,login,role):
            for attempt in range(5):
                await login(self.page,role)
                tp_menu = TPDashboardPage(self.page)
                await tp_menu.navigate_to_courses()

                course = CoursePage(self.page)
                chosen_status = await course.click_any_non_empty_status()

                if chosen_status:
                    return chosen_status
                else:
                    print(f"No course found with non-empty status for {role}, attempt {attempt + 1}")
                    await self.page.locator("button:has-text('Logout')").click()

            pytest.skip(" No eligible course found after 5 attempts")
            return None
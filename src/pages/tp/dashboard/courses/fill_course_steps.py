import random
import re
from src.base.base_page import BasePage
from src.utils.generators.course_data_generator import get_random_course_name, get_random_data, get_random_image, \
    select_random_checkbox, select_random_dropdown_option, fill_same_fields
from src.utils.helpers.common_checks import is_btn_enabled


class FillCourseSteps(BasePage):

    #Fill First Step
    async def fill_first_step(self):
        step_title=await self.page.get_by_text("Course Description").text_content()
        print("=" * 90)
        print(f"Filling First Step : {step_title}")
        print("=" * 90)
        await self.page.get_by_placeholder("e.g: Introduction to Programming").fill(get_random_course_name())
        course_name=await self.page.locator("#courseTitle").get_attribute("value")
        print(f"Course Title :{course_name}")
        await self.page.get_by_placeholder("e.g Learn Python in 30 Days").fill(get_random_data())
        await self.page.get_by_placeholder("Enter a brief description of what this course is about?").fill(
            get_random_data())

        print(f"\nCourse Category")
        dropdown = self.page.locator("#courseCategory")
        await select_random_dropdown_option(self.page,dropdown)

        print(f"\nTraining Method")
        dropdown = self.page.locator("#trainingMethod")
        await select_random_dropdown_option(self.page, dropdown)

        await self.page.locator('input[type="file"]').set_input_files(get_random_image())

        next_btn = self.page.get_by_role("button", name="Next")
        await is_btn_enabled(self, next_btn)

        print("\nNext Step...")
        return course_name.strip()

    #Fill Second Step
    async def fill_second_step(self):
        await self.page.wait_for_load_state("domcontentloaded")
        step_title=await self.page.get_by_text("Who is this course for").first.text_content()
        print("=" * 90)
        print(f"Filling 2nd Step : {step_title}")
        print("=" * 90)
        await self.page.wait_for_timeout(100)
        await self.page.locator("#courseDescription").type(get_random_data())

        checkbox=self.page.locator('input[name="idealApplicants"]')
        await select_random_checkbox(self.page,checkbox)

        print(f"\n{await self.page.get_by_text('Education Requirement').first.text_content()}")
        dropdown = self.page.locator("#educationRequirements")
        await select_random_dropdown_option(self.page, dropdown)

        print(f"\n{await self.page.get_by_text('Experience').first.text_content()}")
        dropdown = self.page.locator("#experience")
        await select_random_dropdown_option(self.page, dropdown)

        print(f"\nOther Prerequisites")
        dropdown = self.page.locator("#otherPrerequisites")
        await select_random_dropdown_option(self.page, dropdown)

        next_btn = self.page.get_by_role("button", name="Next")
        await is_btn_enabled(self,next_btn)

        print("\nNext Step...")

    #Add third step
    async def fill_third_step(self):
        await self.page.wait_for_load_state("domcontentloaded")
        step_title = await self.page.get_by_text("Learning Outcomes").first.text_content()
        print("=" * 90)
        print(f"Filling third Step : {step_title}")
        print("=" * 90)

        #Fill all learning objectives
        await fill_same_fields(self.page,"#learningObjective")

        print(f"\nSkills Covered")
        dropdown = self.page.locator("#coveredSkills")
        await select_random_dropdown_option(self.page, dropdown)

        print(f"\nTools Covered")
        dropdown = self.page.locator("#toolsCovered")
        await select_random_dropdown_option(self.page, dropdown)

        next_btn = self.page.get_by_role("button", name="Next")
        await is_btn_enabled(self, next_btn)

        print("\nNext Step...")

    # Add fourth step
    async def fill_fourth_step(self):
        await self.page.wait_for_load_state("domcontentloaded")
        step_title = await self.page.get_by_text("Certification").first.text_content()
        print("=" * 90)
        print(f"Filling fourth Step : {step_title}")
        print("=" * 90)

        await self.page.get_by_role("radio", name="No").click()

        print(f"\n'Which companies have the previous course graduates joined?'")
        dropdown = self.page.locator("#alumni")
        await select_random_dropdown_option(self.page, dropdown)
        

        



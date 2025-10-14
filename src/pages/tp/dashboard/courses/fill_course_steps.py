from src.base.base_page import BasePage
from src.utils.generators.course_data_generator import get_random_course_name, get_random_data, get_image, fill_same_fields
from src.utils.helpers.common import rs_dropdown
from src.utils.helpers.common_checks import check_is_btn_enabled


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
        await self.page.get_by_placeholder("e.g Learn Python in 30 Days").fill(f"Learn {course_name} "+get_random_data())
        await self.page.get_by_placeholder("Enter a brief description of what this course is about?").fill(
            get_random_data())

        print(f"\nCourse Category")
        dropdown = self.page.locator("#courseCategory")
        await dropdown.select_option(value="AI & Machine Learning")
        # await select_random_dropdown_option(self.page,dropdown)

        print(f"\nTraining Method")
        dropdown = self.page.locator("#trainingMethod")
        await dropdown.select_option(value="Professional Training")
        # await select_random_dropdown_option(self.page, dropdown)

        #Generate Search keywords
        await self.page.get_by_role("button",name="Generate").click()

        #Course Image
        await self.page.locator('input[type="file"]').set_input_files(get_image("course_cover.png"))

        #Next  Button
        next_btn = self.page.get_by_role("button", name="Next")
        await check_is_btn_enabled(self, next_btn)

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
        await self.page.locator("#courseDescription").type("This course is for beginners "+get_random_data())

        #Who is your ideal applicant?
        await self.page.get_by_label("University Students").check()

        # checkbox=self.page.locator('input[name="idealApplicants"]')
        # await select_random_checkbox(self.page,checkbox)

        print(f"\n{await self.page.get_by_text('Education Requirement').first.text_content()}")
        edu_req = "input#react-select-3-input"
        await rs_dropdown(self.page, edu_req, ["Bachelor’s Degree"])

        # dropdown = self.page.locator("#educationRequirements")
        # await select_random_dropdown_option(self.page, dropdown)

        print(f"\n{await self.page.get_by_text('Experience').first.text_content()}")
        exp = "input#react-select-4-input"
        await rs_dropdown(self.page, exp, ["1–2 years of relevant experience"])
        # dropdown = self.page.locator("#experience")
        # await select_random_dropdown_option(self.page, dropdown)

        print(f"\nOther Prerequisites")
        other_prereq = "input#react-select-5-input"
        await rs_dropdown(self.page, other_prereq, ["Stable internet connection"])
        # dropdown = self.page.locator("#otherPrerequisites")
        # await select_random_dropdown_option(self.page, dropdown)

        next_btn = self.page.get_by_role("button", name="Next")
        await check_is_btn_enabled(self,next_btn)

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
        skills_cov = "input#react-select-6-input"
        await rs_dropdown(self.page, skills_cov, ["Machine Learning","Generative AI","BlockChain","Accounting Software"])
        # dropdown = self.page.locator("#coveredSkills")
        # await select_random_dropdown_option(self.page, dropdown)

        print(f"\nTools Covered")
        tools_cov = "input#react-select-7-input"
        await rs_dropdown(self.page, tools_cov, ["Python", "R", "GitHub", "TensorFlow"])

        # dropdown = self.page.locator("#toolsCovered")
        # await select_random_dropdown_option(self.page, dropdown)

        next_btn = self.page.get_by_role("button", name="Next")
        await check_is_btn_enabled(self, next_btn)

        print("\nNext Step...")

    # Add fourth step
    async def fill_fourth_step(self):
        await self.page.wait_for_load_state("domcontentloaded")
        step_title = await self.page.get_by_text("Certification").first.text_content()
        print("=" * 90)
        print(f"Filling fourth Step : {step_title}")
        print("=" * 90)

        await self.page.get_by_role("radio", name="No").click()


        

        



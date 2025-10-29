from src.base.base_page import BasePage
from src.locators.common_locators import CommonLocators
from src.utils.generators.generate_test_data import get_random_course_name, get_random_data, get_image, fill_same_fields
from src.utils.helpers.common import rs_dropdown
from src.utils.helpers.common_checks import check_is_btn_enabled


class FillCourseSteps(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.first_step_title=page.get_by_text("Course Description")
        self.course_title=page.locator("#courseTitle")
        self.sub_title=page.locator("#courseSubTitle")
        self.course_overview=page.locator("#courseOverview")
        self.course_category=page.locator("#courseCategory")
        self.training_method=page.locator("#trainingMethod")
        self.generate_btn=page.get_by_role("button",name="Generate")
        self.upload_option=page.locator('input[type="file"]')
        self.second_step_title=page.get_by_text("Who is this course for")
        self.course_desc=page.locator("#courseDescription")
        self.ideal_app_uni_stu=page.get_by_label("University Students")
        self.edu_req = "input#react-select-3-input"
        self.exp = "input#react-select-4-input"
        self.other_prereq = "input#react-select-5-input"
        self.third_step_title=page.get_by_text("Learning Outcomes")
        self.learning_obj="#learningObjective"
        self.skills_cov = "input#react-select-6-input"
        self.fourth_step_title=page.get_by_text("Certification")
        self.tools_cov = "input#react-select-7-input"
        self.cert_awarded_option=page.get_by_role("radio", name="No")


    #Fill First Step
    async def fill_first_step(self):
        step_title=await self.first_step_title.text_content()
        print("=" * 90)
        print(f"Filling First Step : {step_title}")
        print("=" * 90)

        await self.course_title.fill(get_random_course_name())
        course_name=await self.course_title.get_attribute("value")
        print(f"Course Title :{course_name}")

        await self.sub_title.fill(f"Learn {course_name} "+get_random_data())
        await self.course_overview.fill(get_random_data())

        print(f"\nCourse Category")
        dropdown = self.course_category
        await dropdown.select_option(value="AI & Machine Learning")
        # await select_random_dropdown_option(self.page,dropdown)

        print(f"\nTraining Method")
        dropdown = self.training_method
        await dropdown.select_option(value="Professional Training")
        # await select_random_dropdown_option(self.page, dropdown)

        #Generate Search keywords
        await self.generate_btn.click()

        #Course Image
        await self.upload_option.set_input_files(get_image("course_cover.png"))

        #Next  Button
        await check_is_btn_enabled(self.page,CommonLocators.NEXT_BTN)
        return course_name.strip()

    #Fill Second Step
    async def fill_second_step(self):
        await self.page.wait_for_load_state("domcontentloaded")
        step_title=await self.second_step_title.first.text_content()
        print("=" * 90)
        print(f"Filling 2nd Step : {step_title}")
        print("=" * 90)
        await self.page.wait_for_timeout(100)
        await self.course_desc.type("This course is for beginners "+get_random_data())

        #Who is your ideal applicant?
        await self.ideal_app_uni_stu.check()

        # checkbox=self.page.locator('input[name="idealApplicants"]')
        # await select_random_checkbox(self.page,checkbox)

        await rs_dropdown(self.page, self.edu_req, ["Bachelor’s Degree"])

        # dropdown = self.page.locator("#educationRequirements")
        # await select_random_dropdown_option(self.page, dropdown)

        await rs_dropdown(self.page, self.exp, ["1–2 years of relevant experience"])
        # dropdown = self.page.locator("#experience")
        # await select_random_dropdown_option(self.page, dropdown)

        await rs_dropdown(self.page, self.other_prereq, ["Stable internet connection"])
        # dropdown = self.page.locator("#otherPrerequisites")
        # await select_random_dropdown_option(self.page, dropdown)
        await check_is_btn_enabled(self.page,CommonLocators.NEXT_BTN)

    #Add third step
    async def fill_third_step(self):
        await self.page.wait_for_load_state("domcontentloaded")
        step_title = await self.third_step_title.first.text_content()
        print("=" * 90)
        print(f"Filling third Step : {step_title}")
        print("=" * 90)

        #Fill all learning objectives
        await fill_same_fields(self.page,self.learning_obj)

        await rs_dropdown(self.page, self.skills_cov, ["Machine Learning","Generative AI","BlockChain","Accounting Software"])
        # dropdown = self.page.locator("#coveredSkills")
        # await select_random_dropdown_option(self.page, dropdown)

        await rs_dropdown(self.page, self.tools_cov, ["Python", "R", "GitHub", "TensorFlow"])

        # dropdown = self.page.locator("#toolsCovered")
        # await select_random_dropdown_option(self.page, dropdown)
        await check_is_btn_enabled(self.page,CommonLocators.NEXT_BTN)

    # Add fourth step
    async def fill_fourth_step(self):
        await self.page.wait_for_load_state("domcontentloaded")
        step_title = await self.fourth_step_title.first.text_content()
        print("=" * 90)
        print(f"Filling fourth Step : {step_title}")
        print("=" * 90)

        await self.cert_awarded_option.click()


        

        



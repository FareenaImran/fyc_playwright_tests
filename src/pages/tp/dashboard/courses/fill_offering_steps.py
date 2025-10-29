from playwright.async_api import expect
from src.base.base_page import BasePage
from src.locators.common_locators import CommonLocators
from src.utils.generators.generate_test_data import get_image, get_random_data, get_random_name,get_random_digits
from src.utils.helpers.common import pick_date
from src.utils.helpers.common_checks import check_element_in_table, check_is_btn_enabled


class FillOfferingSteps(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.first_step_title=page.get_by_text("Add details for your next batch")
        self.mode_of_teaching=page.locator("#modeOfTeaching")
        self.learning_methodology=page.get_by_label("Recorded Lectures")
        self.upload_option=page.locator('input[type="file"]')
        self.img_alt=page.locator('img[alt="Uploaded course image"]')
        self.inst_name=page.locator("#instructorName")
        self.about_inst=page.locator("#instructorAbout")
        self.inst_linkedin=page.locator("#instructorLinkedin")
        self.add_inst=page.get_by_role("button",name="Add instructor")
        self.collaboration_with=page.locator("#collaborationWith")
        self.submit_for_review_btn="button[id='submit-btn']"

    async def fill_first_step(self):
        try:
            step_title = await self.first_step_title.text_content()
            print("="*90)
            print(f"Filling First Step : {step_title}")
            print("=" * 90)
            await self.mode_of_teaching.click()
            await self.mode_of_teaching.select_option(value="Self Paced")
            # await select_random_dropdown_option(self.page,mode_of_teaching)
            # learning_method=self.page.locator('input[name="learningMethod"]')
            # await select_random_checkbox(self.page,learning_method)
            await self.learning_methodology.check()

            #Instructor Info
            await self.upload_option.set_input_files(get_image("instructor.jpg"))
            await expect(self.img_alt).to_be_visible()
            await self.inst_name.fill(get_random_name())
            instructor_name=await self.inst_name.get_attribute("value")
            await self.about_inst.fill(f"{instructor_name} "+get_random_data())
            await self.inst_linkedin.fill("https://www.linkedin.com/in/xyz")
            await self.add_inst.click()
            #Verify instructor added in table
            await check_element_in_table(self.page,instructor_name,2,"Instructor Table Below")

            #In Collaboration With
            await self.collaboration_with.fill("TestCollab - ABC Training "+get_random_data())

            #Next Button
            await check_is_btn_enabled(self.page,CommonLocators.NEXT_BTN)

        except Exception as e:
            raise Exception(f"while adding 2nd step of offering :{str(e)}")

    async def fill_second_step(self,orientation_radio_btn:str):
        try:
            await self.page.wait_for_load_state("domcontentloaded")
            step_title = await self.page.get_by_text("Now, lets fill out information related to course schedule").text_content()
            print("=" * 90)
            print(f"Filling Second Step : {step_title}")
            print("=" * 90)
            if orientation_radio_btn=="Yes":
               await self.page.get_by_role("radio",name=orientation_radio_btn).click()

             # Select start date
            start_date_ele = self.page.locator('[name="courseStartDate"]')
            start_date = await pick_date(self.page, start_date_ele, 7)
            print(f"Start Date: {start_date.strftime('%B %d, %Y')}")

            # Select end date
            end_date_ele = self.page.locator('[name="courseEndDate"]')
            end_date = await pick_date(self.page, end_date_ele, 30)  # 30 days from today
            print(f"End Date: {end_date.strftime('%B %d, %Y')}")

            #Days
            await self.page.locator("button[title='Wednesday']").click()

            #Start Time
            await self.page.locator("select[name='courseStartTime']").select_option(value="12:00 PM")

            #End Time
            await self.page.locator("select[name='courseEndTime']").select_option(value="1:30 PM")

            # Publish Date
            await self.page.locator("input[type='radio'][name='publishDate.type'][value='custom']").check()
            await self.page.wait_for_timeout(500)
            publish_date_ele = self.page.locator("(//span[contains(text(),'Select Custom Date')])[2]")
            publish_date = await pick_date(self.page, publish_date_ele, 7)
            print(f"Publish Date: {publish_date.strftime('%B %d, %Y')}")

            #Unpublish date
            await self.page.locator("input[type='radio'][name='unPublishDate.type'][value='custom']").check()
            unpublish_date_ele = self.page.locator("(//span[contains(text(),'Select Custom Date')])[3]")
            unpublish_date = await pick_date(self.page, unpublish_date_ele, 30)
            print(f"UnPublish Date: {unpublish_date.strftime('%B %d, %Y')}")  #M D, Y

            #Next Btn
            await check_is_btn_enabled(self.page,CommonLocators.NEXT_BTN)

        except Exception as e:
            raise Exception(f"while adding 2nd step of offering :{str(e)}")

    async def fill_third_step(self):
        try:
            await self.page.wait_for_load_state("domcontentloaded")
            step_title = await self.page.get_by_text("Cost & Price Related Information").text_content()
            print("=" * 90)
            print(f"Filling Third Step : {step_title}")
            print("=" * 90)
            reg_fee=await self.page.locator("#registrationFees").type(get_random_digits(4))
            print(f"Registration Fee  : {reg_fee}\t")

            reg_fee_ele=self.page.locator("button[name='registrationFeesDueDate']")
            # reg_date=await select_random_present_or_future_date(self.page, reg_fee_ele)
            reg_date = await pick_date(self.page, reg_fee_ele, 7)
            print(f"Registration Fee Due Date : {reg_date.strftime('%B %d, %Y')}\t")

            total_fee=await self.page.locator("#totalCourseFee").type(get_random_digits(4))
            print(f"Total Course Fee  : {total_fee}\t")
            await self.page.locator("#paymentInformation").fill("Monthly Payment")

            total_fee_ele=self.page.locator("button[name='courseFeeDueDate']")
            # total_fee_date=await select_random_present_or_future_date(self.page, total_fee_ele)
            total_fee_date = await pick_date(self.page, total_fee_ele, 7)
            print(f"Total Fee Due Date: {total_fee_date.strftime('%B %d, %Y')}\t")

            await check_is_btn_enabled(self.page, self.submit_for_review_btn)

        except Exception as e:
            raise Exception(f"while adding 2nd step of offering :{str(e)}")



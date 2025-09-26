from playwright.async_api import expect
from src.base.base_page import BasePage
from src.utils.generators.course_data_generator import get_random_image, get_random_data, get_random_name,get_random_digits
from src.utils.helpers.common import pick_date
from src.utils.helpers.common_checks import check_element_in_table, check_is_btn_enabled


class FillOfferingSteps(BasePage):

    async def fill_first_step(self):
        try:
            step_title = await self.page.get_by_text("Add details for your next batch").text_content()
            print("="*90)
            print(f"Filling First Step : {step_title}")
            print("=" * 90)
            print(f"\n Mode of Teaching ")
            mode_of_teaching=self.page.locator("#modeOfTeaching")
            await mode_of_teaching.click()
            await mode_of_teaching.select_option(value="Self Paced")
            # await select_random_dropdown_option(self.page,mode_of_teaching)
            print(f"\n Learning Methodology")
            # learning_method=self.page.locator('input[name="learningMethod"]')
            # await select_random_checkbox(self.page,learning_method)
            await self.page.get_by_label("Recorded Lectures").check()

            #Instructor Info
            await self.page.locator('input[type="file"]').set_input_files(get_random_image())
            await expect(self.page.locator('img[alt="Uploaded course image"]')).to_be_visible()
            await self.page.locator("#instructorName").fill(get_random_name())
            instructor_name=await self.page.locator("#instructorName").get_attribute("value")
            await self.page.locator("#instructorAbout").fill(f"{instructor_name} "+get_random_data())
            await self.page.locator("#instructorLinkedin").fill("https://www.linkedin.com/in/xyz")
            add_instructor=self.page.get_by_role("button",name="Add instructor")
            await add_instructor.click()
            #Verify instructor added in table
            await check_element_in_table(self.page,instructor_name,2,"Instructor Table Below")

            #In Collaboration With
            await self.page.locator("#collaborationWith").fill("TestCollab - ABC Training "+get_random_data())

            #Next Button
            next_btn=self.page.get_by_role("button",name="Next")
            await check_is_btn_enabled(self,next_btn)

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

            # Select end date (after start date)
            end_date_ele = self.page.locator('button[name="courseEndDate"]')
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
            next_btn = self.page.locator("button[id='submit-btn']")
            await check_is_btn_enabled(self.page, next_btn)

        except Exception as e:
            raise Exception(f"while adding 2nd step of offering :{str(e)}")

    async def fill_third_step(self):
        try:
            await self.page.wait_for_load_state("domcontentloaded")
            step_title = await self.page.get_by_text("Cost & Price Related Information").text_content()
            print("=" * 90)
            print(f"Filling Third Step : {step_title}")
            print("=" * 90)
            reg_fee=await self.page.locator("#registrationFees").type(get_random_digits())
            print(f"Registration Fee  : {reg_fee}\t")

            reg_fee_ele=self.page.locator("button[name='registrationFeesDueDate']")
            # reg_date=await select_random_present_or_future_date(self.page, reg_fee_ele)
            reg_date = await pick_date(self.page, reg_fee_ele, 7)
            print(f"Registration Fee Due Date : {reg_date.strftime('%B %d, %Y')}\t")

            total_fee=await self.page.locator("#totalCourseFee").type(get_random_digits())
            print(f"Total Course Fee  : {total_fee}\t")
            await self.page.locator("#paymentInformation").fill("Monthly Payment")

            total_fee_ele=self.page.locator("button[name='courseFeeDueDate']")
            # total_fee_date=await select_random_present_or_future_date(self.page, total_fee_ele)
            total_fee_date = await pick_date(self.page, total_fee_ele, 7)
            print(f"Total Fee Due Date: {total_fee_date.strftime('%B %d, %Y')}\t")

            next_btn = self.page.locator("button[id='submit-btn']")
            await check_is_btn_enabled(self.page, next_btn)

        except Exception as e:
            raise Exception(f"while adding 2nd step of offering :{str(e)}")



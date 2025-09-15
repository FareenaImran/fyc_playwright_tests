from playwright.async_api import expect
from src.base.base_page import BasePage
from src.utils.generators.course_data_generator import select_random_dropdown_option, select_random_checkbox, \
    get_random_image, get_random_data, get_random_instructor_name, select_random_days, select_random_radix_dropdown, \
    get_random_digits, select_random_present_or_future_date, pick_date_after_the_given_date, select_same_date
from src.utils.helpers.common_checks import check_element_in_table, is_btn_enabled


class FillOfferingSteps(BasePage):

    async def fill_first_step(self):
        try:
            step_title = await self.page.get_by_text("Add details for your next batch").text_content()
            print("="*90)
            print(f"Filling First Step : {step_title}")
            print("=" * 90)
            print(f"\n Mode of Teaching ")
            mode_of_teaching=self.page.locator("#modeOfTeaching")
            await select_random_dropdown_option(self.page,mode_of_teaching)
            print(f"\n Learning Methodology")
            learning_method=self.page.locator('input[name="learningMethod"]')
            await select_random_checkbox(self.page,learning_method)
            await self.page.locator('input[type="file"]').set_input_files(get_random_image())
            await expect(self.page.locator('img[alt="Uploaded course image"]')).to_be_visible()
            await self.page.locator("#instructorName").fill(get_random_instructor_name())
            instructor_name=await self.page.locator("#instructorName").get_attribute("value")
            await self.page.locator("#instructorAbout").fill(get_random_data())
            await self.page.locator("#instructorLinkedin").fill("https://www.linkedin.com/in/xyz")
            add_instructor=self.page.get_by_role("button",name="Add instructor")
            await add_instructor.click()
            await check_element_in_table(self.page,instructor_name,2,"Instructor Table Below")
            await self.page.locator("#collaborationWith").fill(get_random_data())
            next_btn=self.page.get_by_role("button",name="Next")
            await is_btn_enabled(self,next_btn)

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
            start_date = await select_random_present_or_future_date(self.page, start_date_ele)
            print(f"Start Date: {start_date.strftime('%B %d, %Y')}")

            # Select end date (after start date)
            end_date_ele = self.page.locator('button[name="courseEndDate"]')
            end_date = await pick_date_after_the_given_date(self.page, start_date, end_date_ele)
            print(f"End Date: {end_date.strftime('%B %d, %Y')}")

            #Days
            await select_random_days(self.page)

            #Start Time
            start_time_dropdown = self.page.locator("button[role='combobox']").filter(
                has_text="Select Start Time").first
            start_time = await select_random_radix_dropdown(self.page, start_time_dropdown)
            print(f"\nStart Time: {start_time}")

            #End Time
            await self.page.wait_for_timeout(500)
            end_time_dropdown = self.page.locator("button[role='combobox']").filter(has_text="Select End Time").first
            end_time = await select_random_radix_dropdown(self.page, end_time_dropdown)
            print(f"End Time: {end_time}")

            await self.page.locator("input[type='radio'][name='publishDate.type'][value='custom']").check()
            await self.page.wait_for_timeout(500)

            publish_date_ele = self.page.get_by_role("button", name="Select Custom Date").nth(0)
            pub_date = await select_same_date(self.page, publish_date_ele, start_date)
            print(f"Publish Date: {pub_date.strftime('%B %d, %Y')}")

            await self.page.locator("input[type='radio'][name='unPublishDate.type'][value='custom']").check()
            unpublish_date_ele = self.page.locator("input[name='unPublishDate.type'][value='custom']").locator("xpath=following::button[.//span[text()='Select Custom Date']][1]")
            unpub_date = await select_same_date(self.page, unpublish_date_ele, end_date)
            print(f"UnPublish Date: {unpub_date.strftime('%B %d, %Y')}")

            next_btn = self.page.locator("button[id='submit-btn']")
            await is_btn_enabled(self.page, next_btn)

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
            reg_date=await select_random_present_or_future_date(self.page, reg_fee_ele)
            print(f"Registration Fee Due Date : {reg_date.strftime('%B %d, %Y')}\t")

            total_fee=await self.page.locator("#totalCourseFee").type(get_random_digits())
            print(f"Total Course Fee  : {total_fee}\t")
            await self.page.locator("#paymentInformation").fill("Monthly Payment")

            total_fee_ele=self.page.locator("button[name='courseFeeDueDate']")
            total_fee_date=await select_random_present_or_future_date(self.page, total_fee_ele)
            print(f"Total Fee Due Date: {total_fee_date.strftime('%B %d, %Y')}\t")

            next_btn = self.page.locator("button[id='submit-btn']")
            await is_btn_enabled(self.page, next_btn)

        except Exception as e:
            raise Exception(f"while adding 2nd step of offering :{str(e)}")



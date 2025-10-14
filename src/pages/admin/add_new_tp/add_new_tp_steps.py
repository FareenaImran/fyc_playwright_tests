from playwright.async_api import expect

from src.base.base_page import BasePage
from src.utils.generators.course_data_generator import get_random_tp_name, get_random_data, get_image
from src.utils.helpers.common import rs_dropdown
from src.utils.helpers.common_checks import check_is_btn_enabled, check_success_message, upload_and_verify_image
from src.utils.helpers.logger import logger


class AddTPInfo(BasePage):

    #Add new TP
    async def add_new_tp(self):
        tp_name=await self.fill_1st_step()
        await self.fill_2nd_step()
        await self.fill_3rd_step()
        # Click submit
        submit_btn = self.page.get_by_role("button", name="Submit")
        await check_is_btn_enabled(self.page, submit_btn)
        # Success msg
        logger.info(f"\n{await check_success_message(self.page)}")
        return tp_name

    #Add Step 1
    async def fill_1st_step(self):
        try:
            #Enter Institute name
            tp_name_ele=self.page.locator("#instituteName")
            tp_name=await tp_name_ele.fill(get_random_tp_name() + " " + get_random_data())
            tp=await tp_name_ele.input_value()
            #Enter About the Institute
            await self.page.locator("//div[@class='ql-editor ql-blank']").fill("Hello " + tp + " " + get_random_data())
            #Institute Official Email Address
            await self.page.locator("#instituteEmailAddress").fill("test@gmail.com")
            #Enter Contact Number
            await self.page.locator("#contactNumber").fill("03343278990")
            #Enter Institute Website
            await self.page.locator("#website").fill("https://test.pk")
            #Select No. of Campuses
            await self.page.select_option("#numberOfCampuses",value="2-4")
            #Enter location
            await self.page.locator("#location").fill("Main lee market chok, Siddiq Wahab Rd")
            #Click next
            next_btn=self.page.get_by_role("button" ,name="Next")
            await check_is_btn_enabled(self.page,next_btn)
            #Success msg
            logger.info(f"\n{await check_success_message(self.page)}")
            return tp
        except Exception as e:
            logger.info(f"Error while adding 1st step : {str(e)}")

    #Add 2nd Step
    async def fill_2nd_step(self):
        try:
            #How would you categorize your institute?
            category = self.page.locator("#category")
            await category.click()
            await category.select_option(value="Independent Training Provider")
            await self.page.wait_for_timeout(1000)
            #Affiliations/Accreditations
            aff_acc="input#react-select-2-input"
            await rs_dropdown(self.page,aff_acc,["PEC","Saylani","HEC"])
            #List the key skills your institute teaches
            skills = "input#react-select-3-input"
            await rs_dropdown(self.page, skills, ["Accounting Software", "Adaptability", "Full-Stack Web Development"])
            #What education level does your institute primarily cater to
            await self.page.get_by_label("University Students").check()
            #What is the duration of the courses being offered?
            await self.page.get_by_label("6 months to 1 year").check()
            #Do you offer a certification?
            await self.page.get_by_label("Yes").check()
            # Click next
            next_btn = self.page.get_by_role("button", name="Next")
            await check_is_btn_enabled(self.page, next_btn)
            # Success msg
            logger.info(f"\n{await check_success_message(self.page)}")

        except Exception as e:
            logger.info(f"Error while adding 2nd step : {str(e)}")

    async def fill_3rd_step(self):
        try:
            #Cover Image
            cover_img=self.page.locator('input[id="coverPhotoUpload"][type="file"]')
            cover_src=await upload_and_verify_image(self.page,cover_img, "TP_cover_img.png", "Cover Photo")

            #Institute Logo
            tp_logo=self.page.locator('input[id="instituteLogoUpload"][type="file"]')
            logo_src=await upload_and_verify_image(self.page,tp_logo, "TP_logo.png", "Institute Logo")

            return cover_src,logo_src

        except Exception as e:
            logger.info(f"Error while adding 3rd step : {str(e)}")
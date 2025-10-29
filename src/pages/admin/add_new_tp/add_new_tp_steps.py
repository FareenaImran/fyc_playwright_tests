from src.base.base_page import BasePage
from src.locators.common_locators import CommonLocators
from src.utils.generators.generate_test_data import get_random_tp_name, get_random_data
from src.utils.helpers.common import rs_dropdown
from src.utils.helpers.common_checks import check_is_btn_enabled, check_success_message, upload_and_verify_image
from src.utils.helpers.logger import logger


class AddTPInfo(BasePage):

    # ------ LOCATORS ------
    SUBMIT_BTN="//button[contains(text(),'Submit')]"
    ABOUT_THE_INSTITUTE="//div[@class='ql-editor ql-blank']"
    INSTITUTE_EMAIL_ADDRESS="#instituteEmailAddress"
    CONTACT_NUMBER="#contactNumber"
    WEBSITE="#website"
    NUM_OF_CAMPUSES_DROPDOWN ="#numberOfCampuses"
    LOCATION="#location"
    CATEGORIZE_YOUR_INS="#category"
    AFF_ACC="input#react-select-2-input"
    SKILLS = "input#react-select-3-input"
    EDU_LEVEL="University Students"
    COURSE_DURATION="6 months to 1 year"
    OFFER_CERT_YES="Yes"
    UPLOAD_COVER_IMG_BTN='input[id="coverPhotoUpload"][type="file"]'
    UPLOAD_LOGO_BTN='input[id="instituteLogoUpload"][type="file"]'

    #------METHODS------
    async def fill_1st_step(self):
        """Adding Step 1"""
        try:
            #Enter Institute name
            tp_name_ele=self.page.locator("#instituteName")
            tp_name=await tp_name_ele.fill(get_random_tp_name() + " " + get_random_data())
            tp=await tp_name_ele.input_value()
            #Enter About the Institute
            await self.page.locator(self.ABOUT_THE_INSTITUTE).fill("Hello " + tp + " " + get_random_data())
            #Institute Official Email Address
            await self.page.locator(self.INSTITUTE_EMAIL_ADDRESS).fill("test@gmail.com")
            #Enter Contact Number
            await self.page.locator(self.CONTACT_NUMBER).fill("03343278990")
            #Enter Institute Website
            await self.page.locator(self.WEBSITE).fill("https://test.pk")
            #Select No. of Campuses
            await self.page.locator(self.NUM_OF_CAMPUSES_DROPDOWN).select_option(value="2-4")
            #Enter location
            await self.page.locator(self.LOCATION).fill("Main lee market chok, Siddiq Wahab Rd")
            #Click next
            await check_is_btn_enabled(self.page,CommonLocators.NEXT_BTN)
            #Success msg
            logger.info(f"\n{await check_success_message(self.page)}")
            return tp
        except Exception as e:
            logger.info(f"Error while adding 1st step : {str(e)}")

    async def fill_2nd_step(self):
        """Adding Step 2"""
        try:
            #How would you categorize your institute?
            await self.page.locator(self.CATEGORIZE_YOUR_INS).click()
            await self.page.locator(self.CATEGORIZE_YOUR_INS).select_option(value="Independent Training Provider")
            await self.page.wait_for_timeout(1000)
            #Affiliations/Accreditations
            await rs_dropdown(self.page,self.AFF_ACC,["PEC","Saylani","HEC"])
            #List the key skills your institute teaches
            await rs_dropdown(self.page, self.SKILLS, ["Accounting Software", "Adaptability", "Full-Stack Web Development"])
            #What education level does your institute primarily cater to
            await self.page.get_by_label(self.EDU_LEVEL).check()
            #What is the duration of the courses being offered?
            await self.page.get_by_label(self.COURSE_DURATION).check()
            #Do you offer a certification?
            await self.page.get_by_label(self.OFFER_CERT_YES).check()
            # Click next
            await check_is_btn_enabled(self.page, CommonLocators.NEXT_BTN)
            # Success msg
            logger.info(f"\n{await check_success_message(self.page)}")
        except Exception as e:
            logger.info(f"Error while adding 2nd step : {str(e)}")

    async def fill_3rd_step(self):
        """Adding Step 3"""
        try:
            #Cover Image
            cover_src=await upload_and_verify_image(self.page,self.page.locator(self.UPLOAD_COVER_IMG_BTN), "TP_cover_img.png", "Cover Photo")
            #Institute Logo
            logo_src=await upload_and_verify_image(self.page,self.page.locator(self.UPLOAD_LOGO_BTN), "TP_logo.png", "Institute Logo")
            return cover_src,logo_src
        except Exception as e:
            logger.info(f"Error while adding 3rd step : {str(e)}")
import re
import pytest
from src.base.base_page import BasePage
from src.utils.generators.course_data_generator import get_random_data
from src.utils.helpers.common import find_and_open_card_by_element
from src.utils.helpers.logger import logger


class CourseDetailPage(BasePage):

    #Get TP name from course detail page
    async def get_tp_name(self):
        tp_name=await self.page.locator("div.flex-1>p[title]").inner_text()
        if not tp_name:
            raise Exception("Did not get TP name")
        print(f"\nGet TP name :{tp_name}")
        return tp_name

    #Get Course name from course detail page
    async def get_course_name(self):
        course_name=await self.page.locator("div>h1").inner_text()
        if not course_name:
            raise Exception("Did not get Course name")
        print(f"\nGet Course Name : {course_name}")
        return course_name

    #Open enrollment pop
    async def open_and_verify_enrollment_modal(self):
        await self.page.get_by_role("button", name="Enroll Now").first.click()
        await self.page.wait_for_load_state("domcontentloaded")
        app_already_sub=self.page.locator("//h2[normalize-space()='Application Already Submitted']")
        if await app_already_sub.is_visible():
            return True
        #Wait for enrollment modal to be visible
        await self.page.get_by_role("button", name="Submit Application").click()
        complete_app=self.page.get_by_role("button",name="Complete Application")
        if await complete_app.is_visible():
            pytest.skip("Application is not complete, Skipping this test..... ")
        #Wait for enrollment verification modal to be visible
        await self.page.get_by_text(re.compile(r".*application.*sent.*training partners.*",re.IGNORECASE)).wait_for(state="visible")
        return None

    #Click on 'Learn More' and wait for modal to be visible
    async def open_inquiry_popup(self):
        await self.page.wait_for_load_state("domcontentloaded")
        await self.page.get_by_role("button", name="Learn More").first.click()
        await self.page.get_by_text("Course Inquiry").wait_for(state="visible")

    #Fill Inquiry
    async def fill_inquiry_form(self):
        contact_method=self.page.locator("[name='contactMethod']")
        await contact_method.select_option(value="WhatsApp")

        inquiry_type = self.page.locator("[name='inquiryType']")
        await inquiry_type.select_option(value="Pricing & Payment Options")

        msg_locator=self.page.locator("textarea[name='message']")
        await msg_locator.fill(get_random_data())
        msg=await msg_locator.input_value()

        if not msg:
            raise Exception("Did not enter any inquiry message ")
        print(f"\nInquiry Message:{msg}")
        return msg

    #Submit Inquiry Form
    async def submit_inquiry_form(self):
        await self.page.get_by_role("button", name="Send Inquiry").click()
        await self.page.get_by_text("Thanks! We've Shared Your Inquiry With the Training Partner").wait_for(state="visible")
        await self.page.locator("svg.absolute.top-3").click()

    #Verify Claim Option
    async def verify_claim_option_visible(self,tp_name):

        # Navigate to Training Partners
        url="https://beta.findyourcourses.org/training-partner"
        await self.page.goto(url)
        logger.info(f"\nNavigated to {url}")

        # get all tp names
        all_elements = self.page.locator("div.group.relative h3[title]")
        await find_and_open_card_by_element(self.page, all_elements, tp_name)

        # Is claim profile button visible?
        claim_profile = self.page.get_by_role("button", name="Claim Profile")
        await claim_profile.wait_for(state="attached")
        found = await claim_profile.is_visible()

        return found
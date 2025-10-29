import re
import pytest
from src.base.base_page import BasePage
from src.utils.generators.generate_test_data import get_random_data


class CourseDetailPage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.tp_name=page.locator("div.flex-1>p[title]")
        self.course_name=page.locator("div>h1")
        self.enroll_now=page.get_by_role("button", name="Enroll Now")
        self.already_submitted_text=page.locator("//h2[normalize-space()='Application Already Submitted']")
        self.submit_application=page.get_by_role("button", name="Submit Application")
        self.complete_application=page.get_by_role("button",name="Complete Application")
        self.learn_more=page.get_by_role("button", name="Learn More")
        self.course_inquiry=page.get_by_text("Course Inquiry")
        self.contact_method_dropdown=page.locator("[name='contactMethod']")
        self.inquiry_type_dropdown=page.locator("[name='inquiryType']")
        self.inquiry_textarea=page.locator("textarea[name='message']")
        self.send_inquiry=page.get_by_role("button", name="Send Inquiry")
        self.inquiry_modal_close_btn=page.locator("svg.absolute.top-3")
        self.success_msg=page.get_by_text("Thanks! We've Shared Your Inquiry With the Training Partner")

     #Get TP name from course detail page
    async def get_tp_name(self):
        tp_name=await self.tp_name.inner_text()
        if not tp_name:
            raise Exception("Did not get TP name")
        print(f"\nGet TP name :{tp_name}")
        return tp_name

    #Get Course name from course detail page
    async def get_course_name(self):
        course_name=await self.course_name.inner_text()
        if not course_name:
            raise Exception("Did not get Course name")
        print(f"\nGet Course Name : {course_name}")
        return course_name

    #Open enrollment pop
    async def open_and_verify_enrollment_modal(self):
        await self.enroll_now.first.click()
        await self.page.wait_for_load_state("domcontentloaded")
        app_already_sub=self.already_submitted_text
        if await app_already_sub.is_visible():
            return True
        #Wait for enrollment modal to be visible
        await self.submit_application.click()
        complete_app=self.complete_application
        if await complete_app.is_visible():
            pytest.skip("Application is not complete, Skipping this test..... ")
        #Wait for enrollment verification modal to be visible
        await self.page.get_by_text(re.compile(r".*application.*sent.*training partners.*",re.IGNORECASE)).wait_for(state="visible")
        return None

    #Click on 'Learn More' and wait for modal to be visible
    async def open_inquiry_popup(self):
        await self.page.wait_for_load_state("domcontentloaded")
        await self.learn_more.first.click()
        await self.course_inquiry.wait_for(state="visible")

    #Fill Inquiry
    async def fill_inquiry_form(self):
        contact_method=self.contact_method_dropdown
        await contact_method.select_option(value="WhatsApp")

        inquiry_type = self.inquiry_type_dropdown
        await inquiry_type.select_option(value="Pricing & Payment Options")

        msg_locator=self.inquiry_textarea
        await msg_locator.fill(get_random_data())
        msg=await msg_locator.input_value()

        if not msg:
            raise Exception("Did not enter any inquiry message ")
        print(f"\nInquiry Message:{msg}")
        return msg

    #Submit Inquiry Form
    async def submit_inquiry_form(self):
        await self.send_inquiry.click()
        await self.success_msg.wait_for(state="visible")
        await self.inquiry_modal_close_btn.click()


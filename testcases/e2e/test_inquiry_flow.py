import re
import pytest

from src.base.base_page import BasePage
from src.pages.admin.learners.Learners import AdminLearners
from src.pages.learner.course_detail_page import CourseDetailPage
from src.pages.learner.course_listing import CourseListing
from src.pages.learner.dashboard_page import DashboardPage
from src.pages.learner.my_courses.inquired_courses import InquiredCourses
from src.utils.helpers.common_checks import login_and_verify_dashboard, check_ele_in_all_pages
from src.utils.helpers.logger import logger
from src.utils.helpers.login_by_name import login_by_name

'''
Test End to End Learner Inquiry on all portal
'''
@pytest.mark.e2e
async def test_inquiry_appears_on_all_portals(page):
    '''
    LEARNER : Send and Verify Inquiry msg
    '''
    #Login
    await login_and_verify_dashboard(page,"learner")
    #get learner name
    home_page = DashboardPage(page)
    learner_name=await home_page.get_learner_name()
    # Navigate to home pg
    await home_page.navigate_to_home_page()
    await page.get_by_role("button", name="Browse Courses").click()
    # Open any course
    course_listing = CourseListing(page)
    course_card = await course_listing.get_random_course_card()
    await course_card.click()

    #get TP name
    course_detail = CourseDetailPage(page)
    tp_name=await course_detail.get_tp_name()
    # Open inquiry popup
    await course_detail.open_inquiry_popup()

    # Fill Inquiry form
    inquiry_msg_sent = await course_detail.fill_inquiry_form()
    # Submit Inquiry form
    await course_detail.submit_inquiry_form()
    # Navigate to dashboard
    base_page = BasePage(page)
    await base_page.click_on_profile_icon()
    # Get recent inquiry msg
    inquiry = InquiredCourses(page)
    inquiry_msg_in_list = await inquiry.get_recent_inquiry(5)
    # verify inquiry message sent by learner appears in list on top
    assert inquiry_msg_sent == inquiry_msg_in_list, (
        f"Expect inquiry '{inquiry_msg_sent}' ,but found '{inquiry_msg_in_list}'"
    )
    logger.info(f"\nInquiry verified successfully! '{inquiry_msg_sent}' appears in Inquiried Courses")

    '''
    TP : Verify Recent Inquiry msg
    '''
    await login_by_name(page,"trainer",tp_name)
    #navigate to learner
    await page.get_by_text("Learners").click()
    #Click on Inquiry
    await page.get_by_role("button",name=re.compile("inquiries",re.IGNORECASE)).click()
    #get recent inquiry
    inquiry_msg_in_list = await base_page.get_column_text(6)
    # verify inquiry message sent by learner appears in tp portal
    assert inquiry_msg_sent == inquiry_msg_in_list, f"Expect inquiry '{inquiry_msg_sent}' ,but found '{inquiry_msg_in_list}'"
    logger.info(f"\nInquiry verified successfully! '{inquiry_msg_sent}' appears in TP's Inquiry Table")

    '''
     Admin : Verify Recent Inquiry msg
    '''
    #Login
    await login_and_verify_dashboard(page,"admin")
    #Navigate to leaner
    await page.get_by_text("Learners").first.click()
    #Check Learner in all pages
    _,text_row=await check_ele_in_all_pages(page, learner_name, 3,"All Learners")
    #View Learner details
    learners=AdminLearners(page)
    await learners.view_learner_details(text_row)
    #View Inquiries
    await page.locator("//button[contains(text(),'Inquiries')]").click()
    inquiry_msg_in_list = await base_page.get_column_text(1)
    # verify inquiry message sent by learner appears in list on top
    assert inquiry_msg_sent == inquiry_msg_in_list, (
        f"Expect inquiry '{inquiry_msg_sent}' ,but found '{inquiry_msg_in_list}'"
    )
    logger.info(f"\nInquiry verified successfully! '{inquiry_msg_sent}' appears in Inquiry table")

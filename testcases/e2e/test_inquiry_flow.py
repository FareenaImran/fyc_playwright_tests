import re
import pytest

from src.base.base_page import BasePage
from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.pages.learner.course_detail_page import CourseDetailPage
from src.pages.learner.course_listing import CourseListing
from src.pages.learner.dashboard_page import DashboardPage
from src.pages.tp.dashboard.dashboard_page import TPDashboardPage
from src.utils.helpers.common import  select_menu_option
from src.utils.helpers.common_checks import  check_ele_in_all_pages, check_element_in_table
from src.utils.helpers.logger import logger
from src.utils.helpers.login_helper import login_by_name_or_email

'''
Test End to End Learner Inquiry on all portal
'''
@pytest.mark.e2e
async def test_inquiry_appears_on_all_portals(page,login):
    '''
    LEARNER : Send and Verify Inquiry msg
    '''
    #Login
    await login(page,"learner")
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
    logger.info("\n--------Verifying Inquiry in table---------\n")
    #Navigate to My Courses
    dashboard = DashboardPage(page)
    await dashboard.navigate_to_my_courses()
    #Navigate to Inquired Courses
    await page.get_by_text("Inquired Courses").click()
    # Get recent inquiry msg
    found_inquiry,row_data=await check_element_in_table(page, inquiry_msg_sent, 5, "Inquired Courses")
    assert found_inquiry, f"Inquiry {found_inquiry} should be in 'Inquired Courses' but was not found"

    '''
    TP : Verify Recent Inquiry msg
    '''
    await login_by_name_or_email(page,"trainer",tp_name)
    #navigate to learner
    tp_menu=TPDashboardPage(page)
    await tp_menu.navigate_to_learner()
    #Click on Inquiry
    await page.get_by_role("button",name=re.compile("inquiries",re.IGNORECASE)).click()
    #Verify recent inquiry
    found_inquiry, row_data = await check_element_in_table(page, inquiry_msg_sent, 6, "Inquiries")
    assert found_inquiry, f"Inquiry {found_inquiry} should be in 'Inquired Courses' but was not found"

    '''
     Admin : Verify Recent Inquiry msg
    '''
    #Login
    await login(page,"admin")
    #Navigate to leaner
    admin_menu=AdminDashboard(page)
    await admin_menu.navigate_to_learner()
    #Check Learner in all pages
    text,_=await check_ele_in_all_pages(page, learner_name, 3,"All Learners")
    #View Learner details
    await select_menu_option(page,1,text)
    #View Inquiries
    await page.locator("//button[contains(text(),'Inquiries')]").click()
    #Verify recent inquiry
    found_inquiry, row_data = await check_element_in_table(page, inquiry_msg_sent, 1, "Inquiries")
    assert found_inquiry, f"Inquiry {found_inquiry} should be in 'Inquired Courses' but was not found"

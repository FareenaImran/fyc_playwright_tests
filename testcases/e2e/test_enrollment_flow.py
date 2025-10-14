import pytest
from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.pages.learner.course_detail_page import CourseDetailPage
from src.pages.learner.course_listing import CourseListing
from src.pages.learner.dashboard_page import DashboardPage
from src.pages.tp.dashboard.dashboard_page import TPDashboardPage
from src.utils.helpers.common import select_menu_option
from src.utils.helpers.common_checks import  check_element_in_table, check_ele_in_all_pages
from src.utils.helpers.login_helper import login_by_name_or_email

@pytest.mark.e2e
async def test_enrollment_appears_on_all_portal(page,login):
    '''
    Test End to End Enrollment Flow on all portal
    '''

    """
    1. Login To Learner
    2. Enroll to any course
    3. Verify enrollment
    """
    await login(page,"learner")
    # get learner name
    home_page = DashboardPage(page)
    learner_name = await home_page.get_learner_name()
    #Navigate to Home Page
    dashboard=DashboardPage(page)
    await dashboard.navigate_to_home_page()
    await page.get_by_role("button", name="Browse Courses").click()
    while True:
        # Open random course
        course_listing = CourseListing(page)
        course_card=await course_listing.get_random_course_card()
        await course_card.click()
        #Get TP and course name from course detail page
        course_detail=CourseDetailPage(page)
        tp_name=await course_detail.get_tp_name()
        course_name=await course_detail.get_course_name()
        #Enroll to course
        already_enrolled=await course_detail.open_and_verify_enrollment_modal()
        if already_enrolled:
            await page.go_back()
            continue
        if not already_enrolled:
            break
    #Verify Enrollment
    course_detail=await dashboard.verify_enrollment_appears_in_applied_courses(course_name)
    assert course_detail,"Did not get applied course detail"

    """
    1. Login to TP by name
    2. Verify Application appears in Application list 
    """

    await login_by_name_or_email(page,"trainer",tp_name)
    #Navigate to learner
    tp_dashboard=TPDashboardPage(page)
    await tp_dashboard.navigate_to_learner()
    #Navigate to Applications tab
    await page.get_by_text("Applications").click()
    #Check course name in table
    recent_applied_course,text_detail=await check_element_in_table(page,course_name,3,"Applications")
    assert course_name==recent_applied_course,(
        f"Did not get '{course_name}' in Application table"
    )

    '''
     Admin : Verify Recent Application
    '''
    #Login
    await login(page,"admin")
    #Navigate to leaner
    admin_menu=AdminDashboard(page)
    await admin_menu.navigate_to_learner()
    #Check Learner in all pages
    found,_=await check_ele_in_all_pages(page, learner_name, 3,"All Learners")
    #View Learner details
    await select_menu_option(page, 1,found)
    #View Inquiries
    await page.locator("//button[contains(text(),'Applications')]").click()
    # Check course name in table
    recent_applied_course, text_detail = await check_element_in_table(page, course_name, 1, "Applications")
    assert course_name == recent_applied_course, (
        f"Did not get '{course_name}' in Application table"
    )

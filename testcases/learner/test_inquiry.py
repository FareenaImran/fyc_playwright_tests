import pytest
from src.pages.learner.course_detail_page import CourseDetailPage
from src.pages.learner.course_listing import CourseListing
from src.pages.learner.dashboard_page import DashboardPage
from src.utils.helpers.common_checks import  check_element_in_table
from src.utils.helpers.logger import logger


@pytest.mark.parametrize("role",["learner"])
@pytest.mark.smoke_checklist
async def test_inquiry_by_learner_appears_in_inquired_courses(page,login,role):
    await login(page,role)
    #Navigate to home pg
    home_page=DashboardPage(page)
    await home_page.navigate_to_home_page()
    #Open any course
    await page.get_by_role("button",name="Browse Courses").click()
    course_listing=CourseListing(page)
    course_card=await course_listing.get_random_course_card()
    await course_card.click()
    #Open inquiry popup
    course_detail=CourseDetailPage(page)
    await course_detail.open_inquiry_popup()

    #Fill Inquiry form
    inquiry_msg_sent=await course_detail.fill_inquiry_form()
    #Submit Inquiry form
    await course_detail.submit_inquiry_form()

    #Navigate to dashboard
    await home_page.click_on_profile_icon()
    #Navigate to My Courses
    dashboard = DashboardPage(page)
    await dashboard.navigate_to_my_courses()
    logger.info(f"\nNavigated to {page.url}")
    #Click on Inquired Courses
    await page.get_by_text("Inquired Courses").click()

    #Verify recent inquiry
    found_inquiry, row_data = await check_element_in_table(page, inquiry_msg_sent, 5, "Inquiries")
    assert found_inquiry, f"Inquiry {found_inquiry} should be in 'Inquired Courses' but was not found"
    logger.info("\nVerified !! Inquiry by learner appears in Inquired Courses")
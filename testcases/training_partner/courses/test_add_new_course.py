import pytest
from src.pages.tp.dashboard.courses.course_page import CoursePage
from src.utils.helpers.common_checks import login_and_verify_dashboard, navigate_to_courses


@pytest.mark.parametrize("role",["trainer"])
@pytest.mark.smoke_checklist
async def test_newly_added_course_appears_in_inprogress_on_save_and_exit(page,role):
    await login_and_verify_dashboard(page,role)
    await navigate_to_courses(page)
    tp_courses=CoursePage(page)
    course_name=await tp_courses.add_new_course()
    await page.get_by_role("button", name="Save and Exit").click()
    await tp_courses.verify_course_appears_in_table(course_name,3,'In Progress')
    print(f"\nVerified !!{course_name} Appeared in 'In Progress'")


@pytest.mark.parametrize("role", ["trainer"])
@pytest.mark.smoke_checklist
async def test_new_course_with_offering_appears_in_under_review_after_submission(page, role):
    await login_and_verify_dashboard(page, role)
    await navigate_to_courses(page)
    tp_courses = CoursePage(page)
    course_name=await tp_courses.add_new_course()
    if course_name:
        print(f"Added {course_name} Successfully !! ")
    await tp_courses.start_offering()
    await tp_courses.add_offering()
    course_exists=await tp_courses.verify_course_appears_in_table(course_name,3,"Under Review")
    if course_exists:
        print(f"\nVerified !! {course_name} with an offering appeared in 'Under Review'")







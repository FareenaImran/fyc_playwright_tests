import pytest
from src.pages.tp.dashboard.courses.course_actions import CourseActions
from src.pages.tp.dashboard.courses.course_page import CoursePage


@pytest.mark.parametrize("role",["trainer"])
@pytest.mark.smoke_checklist
async def test_new_offering_appears_in_existing_course(page,login,role):
    course=CoursePage(page)
    await course.find_course_with_status(login,role)
    #Click on Action button
    action=CourseActions(page)
    offering_data=await action.click_on_action_icon()
    if offering_data:
        course_name=offering_data[2]
        offerings = int(offering_data[4]) if offering_data[4].isdigit() else 0
        print(f"Course {course_name} have offering(s): {offerings}")
        #Start Offering
        await action.start_offering()
        #Add Offering
        course=CoursePage(page)
        await course.add_offering()
        #Verify offerings
        course_exists = await course.verify_course_appears_in_table(course_name, 3, "Under Review")
        if course_exists:
            print(f"\nVerified! After adding an offering, total offerings: {offerings + 1}")
    else:
        raise Exception(f"Could not get row data")


import pytest

from src.pages.learner.dashboard_page import DashboardPage
from src.utils.helpers.logger import logger


@pytest.mark.parametrize("role",["learner"])
@pytest.mark.smoke_checklist
async  def test_learner_bookmarked_courses_count(page,login,role):
        while True:
            await login(page,role)

            dashboard=DashboardPage(page)
            get_count=await dashboard.verify_bookmark_course_count()

            if not get_count:
              continue

            logger.info(f"Verified course count successfully!")
            break

@pytest.mark.parametrize("role",["learner"])
@pytest.mark.smoke_checklist
async def test_course_appears_in_bookmark_section_after_saving(page,login,role):
        #login
        await login(page,role)
        #navigate to home page
        dashboard = DashboardPage(page)
        await dashboard.navigate_to_home_page()
        #Verify course in bookmark section
        course_saved=await dashboard.verify_save_course_from_course_listing_appears_in_bookmark_section()
        #Verify
        assert course_saved,f"Saved course doesnt exits in bookmarked section"


import pytest

from src.pages.learner.dashboard_page import DashboardPage
from src.utils.helpers.common import login_and_verify_dashboard
from src.utils.helpers.logger import logger



@pytest.mark.parametrize("role",["learner"])
@pytest.mark.smoke_checklist
async  def test_learner_bookmarked_courses_count(page,role):
        while True:
            await login_and_verify_dashboard(page,role)
            dashboard=DashboardPage(page)
            get_count=await dashboard.verify_bookmark_course_count()
            if not get_count:
              continue
            logger.info(f"Verified course count successfully!")
            break

@pytest.mark.parametrize("role",["learner"])
@pytest.mark.smoke_checklist
async def test_course_appears_in_bookmark_section_after_saving(page,role):
        await login_and_verify_dashboard(page,role)
        dashboard = DashboardPage(page)
        await dashboard.navigate_to_home_page()
        course_saved=await dashboard.verify_save_course_from_course_listing_appears_in_bookmark_section()
        if not course_saved:
           raise Exception("\nDid not find saved course in bookmarked section")

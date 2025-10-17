import pytest

from src.base.base_page import BasePage
from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.utils.helpers.logger import logger

test_cases = [
    ("Training Partners", "BETATP_UP1"),
    ("Courses", "COURSE Test Automation - lwko"),
    ("Learners", "BETAL_UP1")
]

@pytest.mark.parametrize("category,search_term", test_cases)
async def test_search_displays_correct_results_in_table(page, login, category, search_term):
    locator = "//input[contains(@placeholder,'Search')]"
    await login(page, "admin")

    admin = AdminDashboard(page)
    base = BasePage(page)

    if category == "Training Partners":
        await admin.navigate_to_tp()
        found, data = await base.search_in_table(locator, search_term, 4, "ALL TPs")
    elif category == "Courses":
        await admin.navigate_to_courses()
        found, data = await base.search_in_table(locator, search_term, 3, "ALL TPs")
    elif category == "Learners":
        await admin.navigate_to_learner()
        found, data = await base.search_in_table(locator, search_term, 3, "ALL TPs")
    else:
        raise Exception("\nSide menu option is not defined")

    assert found, "Didn't get result for search in table"
    logger.info("\nVerified!! Search Result found in Table")
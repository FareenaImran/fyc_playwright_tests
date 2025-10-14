import pytest

from src.base.base_page import BasePage
from src.utils.helpers.logger import logger

@pytest.mark.parametrize("role",["learner","trainer","admin"])
async def test_side_menu_navigation(page,login,role):
    """Test that side menu options navigating to correct url"""
    #login
    await login(page,role)

    #verify menu navigation
    menu=BasePage(page)
    await menu.verify_side_menu_navigation()

    logger.info("Verified menu options navigating to correct url")



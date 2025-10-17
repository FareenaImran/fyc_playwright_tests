import re

import pytest
from playwright.async_api import expect
from src.utils.helpers.common_checks import check_login_error_message, check_and_close_page_modal
from src.utils.helpers.csv_reader import get_untried_emails
from src.utils.helpers.logger import logger
from src.utils.helpers.login_helper import login_with_credentials

#Login
@pytest.fixture
async def login():
    async def _login_and_verify_dashboard(page, role: str):
        """Login..."""
        tried_emails = set()
        while True:
            user = get_untried_emails(role, tried_emails)
            user_email = user["email"]
            tried_emails.add(user_email)
            await login_with_credentials(page, role, user_email, user["password"])
            err_msg = await check_login_error_message(page)
            if err_msg:
                continue
            await page.wait_for_load_state("networkidle")
            await expect(page).to_have_url(re.compile(r"/dashboard$"))
            assert "dashboard" in page.url or "profile" in await page.content()
            logger.info(f"\nNavigated to : {page.url}")
            await check_and_close_page_modal(page)
            return user
    return _login_and_verify_dashboard

import re
import pytest
from playwright.async_api import async_playwright, expect

from src.utils.helpers.logger import logger


@pytest.mark.parametrize(
    "role,link",[
    ("learner","https://beta.findyourcourses.org/portal/dashboard"),
    ("trainer","https://beta-tp.findyourcourses.org/portal/dashboard"),
    ("admin","https://beta-admin.findyourcourses.org/portal/dashboard")
],)
async def test_login_session_in_incognito_and_diff_browsers(login,role,link):
    """Ensure sessions do not persist in incognito or across browsers."""

    async with async_playwright() as p:

        # Chromium
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Login and verify dashboard
        await login(page,role)
        logger.info(f"\nLogged inside Chromium")


        #Incognito - new context in same browser
        incognito_context = await browser.new_context()
        incognito_page = await incognito_context.new_page()

        await incognito_page.goto(link)
        await expect(incognito_page).to_have_url(re.compile(".*(login|sign|org).*"))
        logger.info(f"\nVerified !! {role} not logged in inside incognito mode")

        # Firefox
        firefox_browser = await p.firefox.launch(headless=False)
        firefox_context = await firefox_browser.new_context()
        firefox_page = await firefox_context.new_page()

        await firefox_page.goto(link)
        await expect(incognito_page).to_have_url(re.compile(".*(login|sign|org).*"))
        logger.info(f"\nVerified !! {role} not logged in inside firefox")

        #Webkit
        webkit_browser = await p.webkit.launch(headless=False)
        webkit_context = await webkit_browser.new_context()
        webkit_page = await webkit_context.new_page()

        await webkit_page.goto(link)
        await expect(incognito_page).to_have_url(re.compile(".*(login|sign|org).*"))
        logger.info(f"\nVerified !! {role} not logged in inside webkit")

        await browser.close()
        await firefox_browser.close()
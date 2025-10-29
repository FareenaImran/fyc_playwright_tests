import re
import pytest
from playwright.async_api import async_playwright, expect
from src.utils.helpers.logger import logger

@pytest.mark.no_default_browser
@pytest.mark.parametrize(
    "role,link", [
        ("learner", "https://beta.findyourcourses.org/portal/dashboard"),
        ("trainer", "https://beta-tp.findyourcourses.org/portal/dashboard"),
        ("admin", "https://beta-admin.findyourcourses.org/portal/dashboard")
    ], )
async def test_login_session_chromium_incognito(login, role, link):
    """Test session persistence in Chromium and incognito."""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Login in main context
            await login(page, role)
            logger.info(f"\nLogged inside Chromium for {role}")

            # Test incognito
            incognito_context = await browser.new_context()
            incognito_page = await incognito_context.new_page()
            await incognito_page.goto(link, wait_until="networkidle")
            await expect(incognito_page).to_have_url(re.compile(".*(login|sign|org).*"))
            logger.info(f"\nVerified !! {role} not logged in inside incognito")

            await incognito_context.close()
        finally:
            await context.close()
            await browser.close()

@pytest.mark.no_default_browser
@pytest.mark.parametrize(
    "role,link", [
        ("learner", "https://beta.findyourcourses.org/portal/dashboard"),
        ("trainer", "https://beta-tp.findyourcourses.org/portal/dashboard"),
        ("admin", "https://beta-admin.findyourcourses.org/portal/dashboard")
    ], )
async def test_login_session_firefox(login, role, link):
    """Test session persistence in Firefox."""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        context = await browser.new_context()
        page = await context.new_page()

        # Login in main context
        await login(page, role)
        logger.info(f"\nLogged inside Chromium for {role}")

        browser = await p.firefox.launch(headless=False, slow_mo=3000)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(link, wait_until="networkidle")
            await expect(page).to_have_url(re.compile(".*(login|sign|org).*"))
            logger.info(f"\nVerified !! {role} not logged in inside Firefox")
        finally:
            await context.close()
            await browser.close()

@pytest.mark.no_default_browser
@pytest.mark.parametrize(
    "role,link", [
        ("learner", "https://beta.findyourcourses.org/portal/dashboard"),
        ("trainer", "https://beta-tp.findyourcourses.org/portal/dashboard"),
        ("admin", "https://beta-admin.findyourcourses.org/portal/dashboard")
    ], )
async def test_login_session_webkit(login, role, link):
    """Test session persistence in Webkit """

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        context = await browser.new_context()
        page = await context.new_page()

        # Login in main context
        await login(page, role)
        logger.info(f"\nLogged inside Chromium for {role}")

        #Webkit
        browser = await p.webkit.launch(headless=False, slow_mo=3000)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(link, wait_until="networkidle", timeout=50000)
            await expect(page).to_have_url(re.compile(".*(login|sign|org).*"), timeout=15000)
            logger.info(f"\nVerified !! {role} not logged in inside Webkit")
        finally:
            await context.close()
            await browser.close()
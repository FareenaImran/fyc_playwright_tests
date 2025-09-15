import os
import shutil
import sys
import asyncio
import webbrowser
from src.utils.helpers.popup_handler import handle_popup

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


import pytest
from dotenv import load_dotenv
from playwright.async_api import async_playwright
import platform
import subprocess
from pathlib import Path

# Load .env early
env_path = Path(__file__).resolve().parents[1] / "config" / ".env"
load_dotenv(dotenv_path=env_path)

def pytest_sessionstart(session):
    results_dir = "reports/allure-results"
    if os.path.exists(results_dir):
        # print("Cleaning old Allure results before test run...")
        shutil.rmtree(results_dir)
    os.makedirs(results_dir, exist_ok=True)  # Ensure directory exists

@pytest.fixture(scope="function")
async def page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=500,
            channel="chrome",
            args=["--start-maximized"]
        )
        context = await browser.new_context(no_viewport=True)
        context.on("page", lambda p: p.on("console", lambda msg: None))

        # context.on("page", lambda p: p.on("console", lambda msg: print(msg.text)))
        page = await context.new_page()

        # Register global popup handler
        page.on("popup", handle_popup)

        yield page
        await context.close()
        await browser.close()



def pytest_sessionfinish(session, exitstatus):
    print("\nGenerating Allure report...")

    results_dir = "reports/allure-results"
    report_dir = "reports/allure-report"

    allure_cmd = (
        r"C:\Users\dell\scoop\apps\allure\current\bin\allure.bat"
        if platform.system() == "Windows"
        else "allure"
    )

    try:
        # Generate report only if results exist
        if not os.path.exists(results_dir) or not os.listdir(results_dir):
            print("No Allure results found, skipping report generation.")
            return

        subprocess.run([
            allure_cmd,
            "generate",
            results_dir,
            "-o",
            report_dir,
            "--clean"
        ], check=True)

        # Open the report in browser
        port = 5050
        os.chdir(report_dir)

        creation_flags = subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0

        server_process = subprocess.Popen(
            ["python", "-m", "http.server", str(port)],
            creationflags=creation_flags,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        local_url = f"http://localhost:{port}"
        webbrowser.open(local_url)


    except Exception as e:
        print(f"Error during report generation: {e}")
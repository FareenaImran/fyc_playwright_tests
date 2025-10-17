import pytest

from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.utils.helpers.common import get_row_text, select_menu_option, view_course_details
from src.utils.helpers.csv_reader import get_cred_from_csv
from src.utils.helpers.logger import logger
from src.utils.helpers.login_helper import login_by_name_or_email


async def approve_tp_profile(page,login,status):
    """Approve a TP profile from a given status list."""
    await login(page,"admin")
    menu=AdminDashboard(page)
    await menu.navigate_to_tp()
    await page.get_by_role("button",name=status).click()
    tps=await get_row_text(page,4)
    available_tps = get_cred_from_csv("trainer")

    tp_name = None
    for tp in tps:
        for user in available_tps:
            if user["name"] == tp:
                tp_name = tp
                break
        if tp_name:
            break
    if tp_name:
        await select_menu_option(page, 1, tp_name)
    else:
        logger.info("\nCredentials for TPs in under review are not found in csv")
        pytest.skip("\nSkipping Test...")

    logger.info(f"\nApproving '{tp_name}' ....")
    try:
        approve=page.get_by_role("button",name="Approve")
        await approve.wait_for(state="visible")
        await approve.click()
        await page.get_by_role("button",name="Yes, approve. I have verified details").click()
    except Exception as e:
        raise Exception(f"Unable to get 'Approve' button {str(e)}")

    return tp_name

#TP Dashboard Status
async def verify_tp_dashboard_status_is_approved(page,tp_name):
    """Verify TP Status on Dashboard"""
    #login
    await login_by_name_or_email(page,"trainer",tp_name)
    # get status
    status=await page.locator("(//p[contains(text(),'Profile Status')]/following-sibling::div/p)[1]").inner_text()
    return status.strip()

#Admin - CRM
async def navigate_to_crm(page,login,option):
    """Navigate to CRM"""
    await login(page, "admin")
    #Naviagte to TP / Courses /Learners
    try:
        if option=="tp":
            #Navigate to tp
            menu = AdminDashboard(page)
            await menu.navigate_to_tp()
        elif option=="courses":
            #Navigate to courses
            menu = AdminDashboard(page)
            await menu.navigate_to_courses()
        elif option=="learners":
            # Navigate to learners
            menu = AdminDashboard(page)
            await menu.navigate_to_learner()
    except ValueError as e:
        logger.info(f"\nNavigation option is invalid : {str(e)}")

    # view profile details
    await page.locator("tr:has(td:nth-child(1):has-text('1')) td:last-child button").first.click()
    await view_course_details(page)
    # CRM
    await page.get_by_role("button", name="CRM").click()




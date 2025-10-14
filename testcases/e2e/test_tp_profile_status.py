import pytest
from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.pages.admin.training_partners.profile_details import ProfileDetails
from src.utils.helpers.admin.training_partner_helper import approve_tp_profile, verify_tp_dashboard_status_is_approved
from src.utils.helpers.common import select_menu_option, get_row_text
from src.utils.helpers.common_checks import check_success_message
from src.utils.helpers.csv_reader import get_cred_from_csv
from src.utils.helpers.logger import logger
from src.utils.helpers.login_helper import login_by_name_or_email


@pytest.mark.e2e
async def test_send_feedback_to_tp_changes_their_status_to_needs_attention(page,login):
    """
    Test that when admin sends feedback to a TP,
    the TP's profile status changes to 'Needs Attention' on their dashboard
    """

    await login(page,"admin")

    menu=AdminDashboard(page)
    await menu.navigate_to_tp()
    await page.get_by_role("button",name="Up for review").click()

    tps_in_under_review = await get_row_text(page, 4)
    available_tps = get_cred_from_csv("trainer")

    tp_name=None
    for tp in tps_in_under_review:
        for user in available_tps:
            if user["name"]==tp:
                tp_name=tp
                break
        if tp_name:
            break
    if tp_name:
        await select_menu_option(page,1,tp_name)
    else:
        logger.info("\nCredentials for TPs in under review are not found in csv")
        pytest.skip("\nSkipping Test...")


    #send feedback
    tp_detail=ProfileDetails(page)
    admin_feedback=await tp_detail.send_feedback()

    #Login to TP and verify feedback
    await login_by_name_or_email(page,"trainer",tp_name)

    # get status
    status=await page.locator("(//p[contains(text(),'Profile Status')]/following-sibling::div/p)[1]").inner_text()
    assert status.strip()=="Need Attention",f"{tp_name} Profile status is not Need Attention"

    # feedback
    tp_feedback=await page.locator("(//p[contains(text(),'profile needs attention')]/following-sibling::div//p)[1]").inner_text()
    assert admin_feedback==tp_feedback,f"Admin's Feedback '{admin_feedback}' != TP's feedback {tp_feedback}"

    logger.info(f"Verified!! TP Profile Status is '{status}' and Feedback : '{admin_feedback}' appears in TP's dashboard")


@pytest.mark.e2e
@pytest.mark.parametrize("status",["Needs Attention","Up for review"])
async def test_profile_status_syncs_to_tp_dashboard_when_approved_by_admin(page,login,status):
    """
       Test that when admin changes TP profile status to 'Approved',
       the status is immediately reflected on the TP dashboard.
    """
    tp_name=await approve_tp_profile(page,login,status)
    assert await check_success_message(page),f"Failed to Approve TP Profile"
    # Verify status on tp dashboard
    status=await verify_tp_dashboard_status_is_approved(page,tp_name)
    assert status == "Approved - Published & Live", f"Expected status 'Approved' but got '{status}'"

    logger.info(f"Verified !! TP profile status is '{status}'")


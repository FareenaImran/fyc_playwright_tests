from src.pages.admin.training_partners.admin_tp_page import AdminTPPage
from src.pages.admin.training_partners.claim_accounts_page import AdminClaimAccounts
from src.pages.learner.all_tps.tp_detail_page import LearnerTPDetailPage
from src.pages.learner.all_tps.claim_profile import ClaimProfile
from src.pages.learner.dashboard_page import DashboardPage
from src.utils.helpers.common import select_menu_option
from src.utils.helpers.common_checks import check_ele_in_all_pages,check_success_message
from src.utils.helpers.logger import logger
from testcases.fixtures.tp_fixtures import setup_new_tp

async def test_tp_added_by_admin_appears_with_claim_option(page,setup_new_tp):
    """Verify that a TP added by admin appears with claim profile option"""

    #Add new TP by Admin
    tp_name=setup_new_tp

    #Verify TP appears with claim option
    tp_detail_pg=LearnerTPDetailPage(page)
    found=await tp_detail_pg.verify_claim_option_visible(tp_name)

    assert found, f"Did not find {tp_name} with claim option"
    print(f"\nVerified!! {tp_name} found with claim option")


async def test_claim_profile_moves_tp_to_claimed_section(page,setup_new_tp):
    """Verify that submitting claim profile form moves TP to claimed accounts section"""

    #Admin Portal : Add new TP by Admin
    tp_name = setup_new_tp
    assert tp_name

    # Learner Portal : Verify TP appears with claim option
    tp_detail_pg = LearnerTPDetailPage(page)
    found = await tp_detail_pg.verify_claim_option_visible(tp_name)

    assert found, f"{tp_name} with claim option does not exists"
    logger.info(f"\nVerified!! '{tp_name}' found with claim option")

    #Complete claim profile form
    fill_form=ClaimProfile(page)
    email=await fill_form.open_and_fill_claim_form()

    #Verify Claimed TP appears in Claimed Accounts Section on admin portal
    await page.goto("https://beta-admin.findyourcourses.org/portal/dashboard")
    await page.get_by_text(DashboardPage.TP).click()

    #Navigated to claim list
    await page.get_by_role("button",name=AdminTPPage.VIEW_CLAIMED_ACCOUNTS_BTN).click()
    logger.info(f"\nNavigated to : {page.url}")
    assert await page.get_by_text(AdminClaimAccounts.CLAIM_ACC).is_visible()

    #Find requested claim email in under review
    found,row_data=await check_ele_in_all_pages(page,email,4,"Under Review")
    assert found,f"Did not find claimed {email} in Claimed Accounts's List"
    logger.info(f"\nVerified !! '{email}' exists in Claimed Accounts's List")

    #Select approve from action
    await select_menu_option(page, 1,found)

    # Approved Claim Request
    logger.info(f"\nApproving '{email}....' ")
    await page.get_by_text("Yes, approve. I have verified details").click()
    logger.info(f"\n{await check_success_message(page)}")
    logger.info("\nVerified !! Claimed Request Approved by Admin")







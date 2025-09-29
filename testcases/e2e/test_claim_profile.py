from src.pages.learner.course_detail_page import CourseDetailPage
from src.pages.learner.my_courses.claim_profile import ClaimProfile
from src.utils.helpers.common import select_menu_option
from src.utils.helpers.common_checks import check_ele_in_all_pages,check_success_message
from src.utils.helpers.logger import logger
from src.utils.fixtures.tp_fixtures import setup_new_tp

"""Verify that a TP added by admin appears with claim profile option"""
async def test_tp_added_by_admin_appears_with_claim_option(page,setup_new_tp):
    #Add new TP by Admin

    tp_name=setup_new_tp
    logger.info(f"\nTp Added by Admin: {tp_name}")

    'Verify TP appears with claim option'
    course_detail_pg=CourseDetailPage(page)
    found=await course_detail_pg.verify_claim_option_visible(tp_name)

    assert found, f"Did not find {tp_name} with claim option"
    print(f"Verified!! {tp_name} found with claim option")


async def test_claim_profile_moves_tp_to_claimed_section(page,setup_new_tp):
    """Verify that submitting claim profile form moves TP to claimed accounts section"""

    #Admin Portal : Add new TP by Admin

    tp_name = setup_new_tp
    logger.info(f"\nTp Added by Admin: {tp_name}")

    # Learner Portal : Verify TP appears with claim option

    course_detail_pg = CourseDetailPage(page)
    found = await course_detail_pg.verify_claim_option_visible(tp_name)

    assert found, f"Did not find {tp_name} with claim option"
    logger.info(f"Verified!! {tp_name} found with claim option")

    #Complete claim profile form

    fill_form=ClaimProfile(page)
    email=await fill_form.open_and_fill_claim_form()

    #Verify Claimed TP appears in Claimed Accounts Section on admin portal
    await page.goto("https://beta-admin.findyourcourses.org/portal/dashboard")
    print(f"Navigated to : {page.url}")
    await page.get_by_text("Training Partners").click()
    await page.get_by_role("button",name="View Claimed Accounts").click()
    assert await page.get_by_text("Claim Accounts").is_visible()
    found,row_data=await check_ele_in_all_pages(page,email,4,"Under Review")
    assert found,f"Did not find claimed {email} in Claimed Accounts's List"
    logger.info(f"\nVerified !! [{email}] found in Claimed Accounts's List")

    #Select approve from action
    await select_menu_option(page, found, 1)

    # Approved Claim Request
    await page.get_by_text("Yes, approve. I have verified details").click()
    logger.info(f"\n{await check_success_message(page)}")






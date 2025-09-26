from src.pages.learner.course_detail_page import CourseDetailPage
from src.pages.learner.my_courses.claim_profile import ClaimProfile
from src.utils.helpers.common import login_and_verify_dashboard
from src.utils.helpers.common_checks import check_ele_in_all_pages, select_and_option_action_option, \
    check_success_message
from src.utils.helpers.logger import logger
from src.utils.fixtures.tp_fixtures import setup_new_tp

"""Verify that a TP added by admin appears with claim profile option"""
async def test_tp_added_by_admin_appears_with_claim_option(page,setup_new_tp):
    'Add new TP by Admin'

    tp_name=setup_new_tp
    logger.info(f"\nTp Added by Admin: {tp_name}")

    'Verify TP appears with claim option'
    course_detail_pg=CourseDetailPage(page)
    found=await course_detail_pg.verify_claim_option_visible(tp_name)

    assert found, f"Did not find {tp_name} with claim option"
    print(f"Verified!! {tp_name} found with claim option")


"""Verify that submitting claim profile form moves TP to claimed accounts section"""
async def test_claim_profile_moves_tp_to_claimed_section(page,setup_new_tp):
    '''
    Admin Portal
    Add new TP by Admin
    '''

    tp_name = setup_new_tp
    logger.info(f"\nTp Added by Admin: {tp_name}")

    '''
    Learner Portal 
    Verify TP appears with claim option
    '''

    course_detail_pg = CourseDetailPage(page)
    found = await course_detail_pg.verify_claim_option_visible(tp_name)

    assert found, f"Did not find {tp_name} with claim option"
    print(f"Verified!! {tp_name} found with claim option")

    'Complete claim profile form'

    fill_form=ClaimProfile(page)
    email=await fill_form.open_and_fill_claim_form()

    'Verify Claimed TP appears in Claimed Accounts Section on admin portal'
    await page.goto("https://beta-admin.findyourcourses.org/portal/dashboard")
    await page.get_by_text("Training Partners").click()
    await page.get_by_role("button",name="View Claimed Accounts").click()
    assert await page.get_by_text("Claim Accounts").is_visible()
    found,row_data=await check_ele_in_all_pages(page,email,4,"Under Review")
    assert found,f"Did not find claimed {email} in Claimed Accounts's List"
    print(f"\nVerified !! [{email}] found in Claimed Accounts's List")

    'Click on action button'
    action_btn=page.locator(f"tr:has-text('{found}') td:last-child button")
    await action_btn.click()

    'Approved Claim Request'
    menu_option=page.locator("div[role='menu']  div:nth-child(1)")
    await menu_option.wait_for(state="visible")
    await menu_option.click()
    await page.get_by_text("Yes, approve. I have verified details").click()

    print(f"\n{await check_success_message(page)}")






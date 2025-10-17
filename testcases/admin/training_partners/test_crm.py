import pytest
from src.pages.admin.training_partners.profile_details import ProfileDetails
from src.utils.helpers.admin.training_partner_helper import navigate_to_crm
from src.utils.helpers.common_checks import check_element_in_table

@pytest.mark.parametrize("navigate_to",["tp","courses"])
async def test_feedback_added_by_admin_shows_on_top(page,login,navigate_to):
    """Test that feedback added by admin for TP/Courses appears in feedback table"""
    #Navigate to CRM
    await navigate_to_crm(page,login,navigate_to)

    #add feedback
    await page.get_by_role("button",name="Add feedback").click()
    tp_detail = ProfileDetails(page)
    feedback = await tp_detail.send_feedback()

    #Verify feedback in table
    await page.wait_for_timeout(2000)
    await check_element_in_table(page, feedback, 1, "Feedback Table Below")

@pytest.mark.parametrize("navigate_to",["tp","courses","learners"])
async def test_crm_added_by_admin_shows_on_top(page,login,navigate_to):
    """Test that crm added by admin for TP & Courses & Learners appears in crm table"""
    # Navigate to CRM
    await navigate_to_crm(page, login,navigate_to)

    #add crm
    await page.get_by_role("button",name="Add CRM Note").click()
    tp_detail = ProfileDetails(page)
    crm = await tp_detail.add_crm()

    # Verify crm in table
    await page.wait_for_timeout(2000)
    await check_element_in_table(page, crm, 1, "CRM Table Below")



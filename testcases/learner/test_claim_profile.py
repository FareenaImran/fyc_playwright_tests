from src.utils.helpers.common import find_card_by_element
from src.utils.helpers.logger import logger
from src.utils.fixtures.tp_fixtures import setup_new_tp

"""Verify that a TP added by admin appears with claim profile option"""
async def test_tp_added_by_admin_appears_with_claim_option(page,setup_new_tp):
    '''Add new TP by Admin'''

    tp_name=setup_new_tp
    logger.info(f"\nTp Added by Admin: {tp_name}")

    '''Verify TP appears with claim option'''

    # Navigate to Training Partners
    await page.goto("https://beta.findyourcourses.org/training-partner")

    #get all tp names
    all_elements = page.locator("div.group.relative h3[title]")
    await find_card_by_element(page,all_elements,tp_name)

    #Is claim profile button visible?
    claim_profile=page.get_by_role("button",name="Claim Profile")
    await claim_profile.wait_for(state="attached")
    found=await claim_profile.is_visible()

    assert found,f"Did not find {tp_name} with claim option"
    print(f"Verified!! {tp_name} found with claim option")

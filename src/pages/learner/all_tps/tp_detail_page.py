from src.base.base_page import BasePage
from src.utils.helpers.common import find_and_open_card_by_element
from src.utils.helpers.logger import logger


class LearnerTPDetailPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.tp_names = page.locator("div.group.relative h3[title]")
        self.claim_profile_btn=page.get_by_role("button", name="Claim Profile")


    # Verify Claim Option
    async def verify_claim_option_visible(self, tp_name):
        # Navigate to Training Partners
        url = "https://beta.findyourcourses.org/training-partner"
        await self.page.goto(url)
        logger.info(f"\nNavigated to {url}")

        # get all tp names
        all_elements = self.tp_names
        await find_and_open_card_by_element(self.page, all_elements, tp_name)

        # Is claim profile button visible?
        claim_profile = self.claim_profile_btn
        await claim_profile.wait_for(state="attached")
        found = await claim_profile.is_visible()

        return found
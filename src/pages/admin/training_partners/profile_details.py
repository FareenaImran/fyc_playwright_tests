from playwright.async_api import expect

from src.base.base_page import BasePage
from src.utils.generators.course_data_generator import get_random_data
from src.utils.helpers.common_checks import check_success_message
from src.utils.helpers.logger import logger


class ProfileDetails(BasePage):

    #send feedback to TP
    async def send_feedback(self):
        await self.page.get_by_role("button",name="Send back with feedback").click()

        modal=self.page.locator("//h2[contains(text(),'detailed feedback')]")
        await expect(modal).to_be_visible()

        text_area=self.page.get_by_placeholder("Type your feedback here",exact=False)
        await text_area.fill(f"Complete Your Profile {get_random_data()}")
        feedback=await text_area.input_value()
        logger.info(f"\n{feedback}")

        await self.page.get_by_role("button",name="Send Feedback").click()

        success=await check_success_message(self.page)
        assert success,"Failed to send feedback to TP"
        logger.info(f"\n{success}")

        return feedback


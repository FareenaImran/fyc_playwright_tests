import re

from playwright.async_api import expect

from src.base.base_page import BasePage
from src.utils.generators.data_generator import get_random_data
from src.utils.helpers.common import rs_dropdown
from src.utils.helpers.common_checks import check_success_message
from src.utils.helpers.logger import logger


class ProfileDetails(BasePage):

    #send feedback to TP
    async def send_feedback(self):

        modal=self.page.locator("//h2[contains(text(),'detailed feedback')]")
        await expect(modal).to_be_visible()

        text_area=self.page.get_by_placeholder("Type your feedback here",exact=False)
        await text_area.fill(f"Complete Your Profile {get_random_data()}")
        feedback=await text_area.input_value()
        logger.info(f"\nFeed back : {feedback}")

        await self.page.get_by_role("button",name="Send Feedback").click()

        success=await check_success_message(self.page)
        assert success,"Failed to send feedback to TP"

        return feedback

    async def add_crm(self):
        # Verify modal
        try:
            try:
                await self.page.wait_for_timeout(1000)
                modal = self.page.get_by_text(re.compile(r'.*(crm for the Training Partner|crm for the Course|Save Note).*'))
                await expect(modal).to_be_visible()
            except TimeoutError as e:
                logger.info(f"CRM modal did not appear on screen {str(e)}")

            # Select Type of Interaction
            await self.page.locator("//button[@role='combobox']").click()
            await self.page.locator('[role="option"]:has-text("Email")').click()

            # Add crm
            text_area = self.page.get_by_placeholder("your crm note here", exact=False)
            await text_area.fill(f"Need to discuss about  {get_random_data()}")
            crm = await text_area.input_value()
            logger.info(f"\nCRM note : {crm}")
            await self.page.get_by_role("button", name=re.compile(r".*(Send Note|Save Note).*")).click()

            #Success msg
            success = await check_success_message(self.page)
            assert success, "Failed to add CRM"

            return crm

        except Exception as e:
            logger.info(f"Unable to add CRM notes {str(e)}")


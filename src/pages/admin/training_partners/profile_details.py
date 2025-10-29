import re

from playwright.async_api import expect

from src.base.base_page import BasePage
from src.utils.generators.generate_test_data import get_random_data
from src.utils.helpers.common import rs_dropdown
from src.utils.helpers.common_checks import check_success_message
from src.utils.helpers.logger import logger


class ProfileDetails(BasePage):
    # ------ LOCATORS ------#
    PROFILE_PIC="Profile Picture"
    SEND_FEEDBACK="Send back with feedback"

    def __init__(self, page):
        super().__init__(page)
        self.feedback_modal_text = page.locator("//h2[contains(text(),'detailed feedback')]")
        self.feedback_textarea = page.get_by_placeholder("Type your feedback here", exact=False)
        self.send_feedback_btn = page.get_by_role("button", name="Send Feedback")
        self.type_of_interaction = page.locator("//button[@role='combobox']")
        self.email_option = page.locator('[role="option"]:has-text("Email")')
        self.crm_text_area=page.get_by_placeholder("your crm note here", exact=False)
        self.send_or_save_note=page.get_by_role("button", name=re.compile(r".*(Send Note|Save Note).*"))

    # ------METHODS ------#
    async def send_feedback(self):
        """Sending Feedback to TP"""

        modal_text = self.feedback_modal_text
        await expect(modal_text).to_be_visible()

        text_area = self.feedback_textarea
        await text_area.fill(f"Complete Your Profile {get_random_data()}")
        feedback = await text_area.input_value()
        logger.info(f"\nFeed back : {feedback}")

        await self.send_feedback_btn.click()

        success = await check_success_message(self.page)
        assert success, "Failed to send feedback to TP"

        return feedback

    async def add_crm(self):
        """Adding and Verifying CRM """
        try:
            try:
                await self.page.wait_for_timeout(1000)
                modal = self.page.get_by_text(
                    re.compile(r'.*(crm for the Training Partner|crm for the Course|Save Note).*'))
                await expect(modal).to_be_visible()
            except TimeoutError as e:
                logger.info(f"CRM modal did not appear on screen {str(e)}")

            # Select Type of Interaction
            await self.type_of_interaction.click()
            await self.email_option.click()

            # Add crm
            text_area = self.crm_text_area
            await text_area.fill(f"Need to discuss about  {get_random_data()}")
            crm = await text_area.input_value()
            logger.info(f"\nCRM note : {crm}")
            await self.send_or_save_note.click()

            # Success msg
            success = await check_success_message(self.page)
            assert success, "Failed to add CRM"

            return crm

        except Exception as e:
            logger.info(f"Unable to add CRM notes {str(e)}")

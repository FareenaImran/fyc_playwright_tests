from src.base.base_page import BasePage
from src.utils.generators.course_data_generator import get_random_name
from src.utils.generators.email_generator import get_random_email
from src.utils.helpers.common_checks import check_success_message
from src.utils.helpers.logger import logger


class ClaimProfile(BasePage):
    async def open_and_fill_claim_form(self):
        '''Open Claim Profile form'''
        await self.page.get_by_role("button",name="Claim Profile").click()

        '''Fill Claim form'''
        tp_name=await self.page.locator("#instituteName").get_attribute("value")
        await self.page.locator("#representativeName").fill(get_random_name())
        designation=self.page.locator("select[name='designation']")
        await designation.select_option('IT Support Officer')
        await self.page.locator('#contactNumber').fill('+923365478665')
        email_loc=self.page.locator("#email")
        await email_loc.fill(get_random_email(tp_name))
        email=await email_loc.input_value()
        city = self.page.locator("select[name='city']")
        await city.select_option('Lahore')
        await self.page.locator("input[value='I want to expand the reach of my institute']").check()
        await self.page.get_by_role("button",name="Submit Claim Request").click(force=True)
        logger.info(f"\n{await check_success_message(self.page)}")
        return email









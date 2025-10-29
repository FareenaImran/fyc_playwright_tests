from src.base.base_page import BasePage
from src.utils.generators.generate_test_data import get_random_name
from src.utils.generators.email_generator import get_random_email
from src.utils.helpers.common_checks import check_success_message
from src.utils.helpers.logger import logger


class ClaimProfile(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.claim_profile_btn=page.get_by_role("button",name="Claim Profile")
        self.inst_name=page.locator("#instituteName")
        self.representative_name=page.locator("#representativeName")
        self.designation_dd=page.locator("select[name='designation']")
        self.contact_no=page.locator('#contactNumber')
        self.email=page.locator("#email")
        self.city_dd=page.locator("select[name='city']")
        self.expand_reach=page.locator("input[value='I want to expand the reach of my institute']")
        self.submit_claim_req_btn=page.get_by_role("button",name="Submit Claim Request")

    async def open_and_fill_claim_form(self):
        """Open Claim Profile form"""
        await self.claim_profile_btn.click()

        '''Fill Claim form'''
        tp_name=await self.inst_name.get_attribute("value")
        await self.representative_name.fill(get_random_name())
        designation=self.designation_dd
        await designation.select_option('IT Support Officer')
        await self.contact_no.fill('+923365478665')
        await self.email.fill(get_random_email(tp_name))
        email=await self.email.input_value()
        city = self.city_dd
        await city.select_option('Lahore')
        await self.expand_reach.check()
        await self.submit_claim_req_btn.click(force=True)
        logger.info(f"\n{await check_success_message(self.page)}")
        return email









from src.base.base_page import BasePage


class AdminLearners(BasePage):
    async def view_learner_details(self,text_row):
        cells = await text_row.query_selector_all('td')
        last_td = cells[-1]
        buttons = await last_td.query_selector_all('button')
        await buttons[0].click()
        await self.page.locator("//div[@role='menuitem'][contains(text(),'View Details')]").click()



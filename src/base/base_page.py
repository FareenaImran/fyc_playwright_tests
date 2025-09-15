
from src.utils.helpers.logger import get_logger


class BasePage:
    def __init__(self,page):
     self.page=page
     self.logger=get_logger(f"{self.__module__}.{self.__class__.__name__}")


    async def click_on_profile_icon(self):
        locators =[
            self.page.locator('svg.cursor-pointer.text-\\[\\#3F00C6\\][viewBox="0 0 496 512"]'),
            self.page.get_by_role("img", name="profile image")]

        for i, locator in enumerate(locators):
            try:
                await self.page.evaluate("window.scrollTo({ top: 0, behavior: 'instant' })")
                await self.page.wait_for_timeout(300)

                target_element = locator.first
                if not target_element:
                    continue
                await target_element.click(timeout=2000)
                return True

            except Exception as e:
                print(f"Error: {str(e)}")


        raise Exception("Unable to click the profile icon after 3 attempts")


    async def get_column_text(self,column):
        column=column-1
        rows=self.page.locator("table > tbody > tr")
        await rows.first.wait_for(state="visible")
        msg=await rows.nth(0).locator("td").nth(column).inner_text()
        print(f"Got [{msg}] in table")

        return msg.strip()


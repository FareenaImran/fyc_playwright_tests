import re
from asyncio import timeout

from playwright.async_api import expect

from src.utils.helpers.common_checks import check_and_close_page_modal
from src.utils.helpers.logger import get_logger, logger


class BasePage:
    def __init__(self,page):
     self.page=page
     self.logger=get_logger(f"{self.__module__}.{self.__class__.__name__}")

    #Click on profile button
    async def click_on_profile_icon(self):
        profile_locator = self.page.get_by_role("img", name="profile image").or_(
            self.page.locator("(//*[name()='svg'][@class='cursor-pointer text-[#3F00C6]'])[1]")
        )

        await profile_locator.scroll_into_view_if_needed()
        await profile_locator.click()


    async def verify_side_menu_navigation(self):
      options=self.page.locator("//div[@data-sidebar='group']//li//span")
      count=await options.count()
      if count==0:
          logger.warning("No menu options found")
          return
      for i in range(count):
          try:
              menu=options.nth(i)
              await menu.wait_for(state="visible")

              text=(await menu.text_content()).strip()

              if not text:
                  logger.warning(f"Menu option {i} has no text,skipping")
                  continue

              #Extract last word
              last_word=text.split()[-1].lower()

              #Click and wait for nav
              await menu.click()
              await self.page.wait_for_timeout(500)
              await self.page.wait_for_load_state("networkidle")

              logger.info(f"Clicked on {last_word}")
              assert last_word in self.page.url,f"{last_word} is not navigated to the correct url"
              logger.info(f"Navigated to correct page : {self.page.url}")

          except Exception as e:
              logger.error(f"Error testing menu option {i}: {str(e)}")
              continue




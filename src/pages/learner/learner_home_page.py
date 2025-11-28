from asyncio import timeout
from pydoc import pager

from playwright.sync_api import expect

from src.base.base_page import BasePage
from src.utils.helpers.logger import logger


class LearnerHomePage(BasePage):
    BROWSE_COURSES="Browse Courses"
    FEATURED_TP_NAME="(//div[@aria-roledescription='carousel'])[2]//h3"
    FEATURED_COURSE_NAME="(//div[@aria-roledescription='carousel'])[1]//h3"
    COURSE_CATEGORY="//div[contains(@class,'relative w-full')]//span"

    async def get_all_filter_options(self,filter_name):
        await self.page.locator(f"//*[contains(text(),'{filter_name}')]").wait_for()
        labels = await self.page.locator(
            "//*[contains(text(),'Category')]/ancestor::h3/following-sibling::div//label[@for]").all_text_contents()
        label_texts = [text.strip() for text in labels if text and text.strip()]
        return label_texts

    async def get_all_course_category_text(self):
        await self.page.wait_for_load_state('domcontentloaded')
        try:
            course_category_ele = self.page.locator(self.COURSE_CATEGORY)
            await course_category_ele.first.wait_for(state="visible",timeout=5000)
            course_category_texts = await course_category_ele.all_inner_texts()
            return course_category_texts
        except:
            result = self.page.get_by_text("No courses found", exact=False)
            await result.scroll_into_view_if_needed()
            await result.wait_for(state="visible",timeout=500)
            return None

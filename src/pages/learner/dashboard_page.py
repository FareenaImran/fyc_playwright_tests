import re
from playwright.async_api import expect
from src.base.base_page import BasePage
from src.locators.common_locators import CommonLocators
from src.pages.learner.course_listing import CourseListing
from src.utils.helpers.logger import logger

class DashboardPage(BasePage):
    TP="Training Partners"
    def __init__(self,page):
        super().__init__(page)
        self.logo_alt=page.get_by_alt_text("Logo")
        self.hello=page.locator("//p[@id='hello_text']")
        self.my_courses=page.get_by_text("My Courses")
        self.saved_courses=page.locator('p:has-text("Saved Courses") + h3')
        self.saved_courses_view_all=page.locator('p:has-text("Saved Courses") + p:has-text("View All")')

    async def navigate_to_home_page(self):
        await self.logo_alt.nth(1).click()
        await expect(self.page).to_have_url(re.compile(r"beta.findyourcourses.org/$"))
        logger.info(f"\nNavigated to : {self.page.url}")


    async def get_learner_name(self):
        welcome_text=await self.hello.inner_text()
        learner_name=re.search(r"Hello, (.*?)!",welcome_text)
        if learner_name:
            logger.info(f"\nLearner Name:{learner_name.group(1)}")
        return learner_name.group(1)

    async def navigate_to_my_courses(self):
        await expect(self.my_courses).to_be_visible()
        await self.my_courses.click()
        await expect(self.page).to_have_url(re.compile(r"/courses$"))



    async def navigate_and_open_bookmark_section(self):
        await self.page.wait_for_load_state("networkidle")
        await self.saved_courses.click()
        view_all =self.saved_courses_view_all
        await view_all.click()
        await self.page.locator(CommonLocators.COURSE_CARD).first.wait_for(state="visible")
        course_cards = self.page.locator(CommonLocators.COURSE_CARD)
        if course_cards:
           return course_cards
        else:
            return None

    async def verify_bookmark_course_count(self):
            try:
                await self.navigate_to_my_courses()
                count = await self.saved_courses.text_content()
                saved_courses_count = int(count.strip())

                if not saved_courses_count:
                    logger.info("\nThis learner have not bookmarked any course")
                    await self.page.context.clear_cookies()
                    return False

                print(f"\nGet Course count : {saved_courses_count}")
                course_cards=await self.navigate_and_open_bookmark_section()
                actual_count =await course_cards.count()
                print(f"Courses present in course section :{actual_count}")
                await expect(course_cards).to_have_count(saved_courses_count)
                return True
            except Exception as e:
                logger.warning(f"Exception:{e}")
                await self.page.context.clear_cookies()
                return False


    async def  verify_save_course_from_course_listing_appears_in_bookmark_section(self):
        homepage=CourseListing(self.page)
        course_card = await homepage.get_random_unbookmarked_course()
        course_title = await course_card.locator("h3").inner_text()
        bookmark_icon =course_card.get_by_label("Add to bookmarks")
        await bookmark_icon.scroll_into_view_if_needed()
        await bookmark_icon.click()
        logger.info(f"\nBookmarked course : '{course_title}'")

        await self.click_on_profile_icon()
        await self.navigate_to_my_courses()

        course_cards=await self.navigate_and_open_bookmark_section()
        saved_courses_title=await course_cards.locator("h3").all_inner_texts()
        for i,title in enumerate(saved_courses_title):
            if title.strip()==course_title:
               course_ele=course_cards.locator("h3").nth(i)
               await course_ele.scroll_into_view_if_needed()
               await course_ele.wait_for(state="visible")
               logger.info(f"\n'{course_title}' is present in bookmarked section")
               return course_title

        return None



import re
from src.base.base_page import BasePage
from playwright.async_api import expect
from src.pages.learner.course_listing import CourseListing
from src.utils.helpers.logger import logger

class DashboardPage(BasePage):

    async def navigate_to_home_page(self):
        await self.page.get_by_alt_text("Logo").nth(1).click()
        await expect(self.page).to_have_url(re.compile(r"beta.findyourcourses.org/$"))
        print(f"\nNavigated to : {self.page.url}")



    async def get_learner_name(self):
        welcome_text=await self.page.locator("//p[@id='hello_text']").inner_text()
        learner_name=re.search(r"Hello, (.*?)!",welcome_text)
        if learner_name:
            print(f"\nLearner Name:{learner_name.group(1)}")
        return learner_name.group(1)


    async def navigate_to_my_courses(self):
        await expect(self.page.get_by_text("My Courses")).to_be_visible()
        await self.page.get_by_text("My Courses").click()
        await expect(self.page).to_have_url(re.compile(r"/courses$"))

    #Get applied courses name
    async def get_applied_courses(self):
        applied_courses=await self.page.locator("//p[normalize-space()='Applied Courses']/following-sibling::div//h3").all_inner_texts()
        total=len(applied_courses)
        assert total !=0 ,"No Course found in Applied Courses"
        return applied_courses

    async def verify_enrollment_appears_in_applied_courses(self,course_name):
        back_to_my_courses=self.page.get_by_role("button",name="Back to My Courses")
        await back_to_my_courses.wait_for(state="visible")
        await back_to_my_courses.click()
        await expect(self.page).to_have_url(re.compile(r"/portal/courses$"))
        await self.page.locator("//p[normalize-space()='Applied to Courses']").click()
        applied_courses=await self.get_applied_courses()
        print(f"\nList of Applied Courses\n{applied_courses}")
        if course_name in applied_courses:
            course_detail=self.page.locator(f"//h3[normalize-space()='{course_name}']/parent::div")
            return await course_detail.inner_text()
        return None







    async def navigate_and_open_bookmark_section(self):
        await self.page.locator('p:has-text("Saved Courses") + h3').click()
        view_all =self.page.locator('p:has-text("Saved Courses") + p:has-text("View All")')
        await view_all.click()
        await self.page.locator("div.group.relative").first.wait_for(state="visible")
        course_cards = self.page.locator("div.group.relative")
        if course_cards:
           return course_cards
        else:
            return None

    async def verify_bookmark_course_count(self):
            try:
                await self.navigate_to_my_courses()
                count = await self.page.locator('p:has-text("Saved Courses") + h3').text_content()
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
        print(f"\nBookmarked course : '{course_title}'")

        await self.click_on_profile_icon()

        await self.navigate_to_my_courses()
        course_cards=await self.navigate_and_open_bookmark_section()
        saved_courses_title=await course_cards.locator("h3").all_inner_texts()
        for i,title in enumerate(saved_courses_title):
            if title.strip()==course_title:
               course_ele=course_cards.locator("h3").nth(i)
               await course_ele.scroll_into_view_if_needed()
               await course_ele.wait_for(state="visible")
               print(f"\n'{course_title}' is present in bookmarked section")
               return course_title

        return True



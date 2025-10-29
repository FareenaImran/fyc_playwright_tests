import random

from src.base.base_page import BasePage
from src.pages.learner.learner_home_page import LearnerHomePage


class CourseListing(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.course_card = page.locator("div.group.cursor-pointer")

    async def get_random_course_card(self):
        print(f"\nNavigated to : {self.page.url}")
        await self.course_card.first.wait_for(state="visible")
        total = await self.course_card.count()
        if total==0:
            print("No Course cards found!")
        print(f"\nTotal Course cards present :{total}")
        rand_index=random.randint(0,total-1)
        random_card=self.course_card.nth(rand_index)
        return random_card

    async def get_random_unbookmarked_course(self):
        await self.page.get_by_role("button",name=LearnerHomePage.BROWSE_COURSES).click()
        print(f"Navigated To : {self.page.url}")
        await self.course_card.first.wait_for(state="visible")
        unbookmarked_icons=self.course_card.get_by_label("Add to bookmarks")
        total = await unbookmarked_icons.count()
        print(f"\nTotal Unbookmarked Courses : {total}")
        if total==0:
            print("No Unbookmarked Courses found!")
        rand_index=random.randint(0,total-1)
        random_unbookmarked_icon=unbookmarked_icons.nth(rand_index)
        unbookmarked_course=random_unbookmarked_icon.locator("xpath=ancestor::div[contains(@class, 'group') and contains(@class, 'cursor-pointer')]")
        return unbookmarked_course

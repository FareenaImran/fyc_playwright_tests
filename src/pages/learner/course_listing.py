import random
from src.base.base_page import BasePage
from src.locators.learner_locators.home_page_locators import HomePageLocators


class CourseListing(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    async def get_random_course_card(self):
        course_cards = self.page.locator(HomePageLocators.COURSE_CARD)
        print(f"\nNavigated to : {self.page.url}")
        await course_cards.first.wait_for(state="visible")
        total = await course_cards.count()
        if total==0:
            print("No Course cards found!")
        print(f"\nTotal Course cards present :{total}")
        rand_index=random.randint(0,total-1)
        random_card=course_cards.nth(rand_index)
        return random_card

    async def get_random_unbookmarked_course(self):
        await self.page.get_by_role("button", name="Browse Courses").click()
        print(f"Navigated To : {self.page.url}")
        course_cards = self.page.locator(HomePageLocators.COURSE_CARD)
        await course_cards.first.wait_for(state="visible")
        unbookmarked_icons=course_cards.get_by_label("Add to bookmarks")
        total = await unbookmarked_icons.count()
        print(f"\nTotal Unbookmarked Courses : {total}")
        if total==0:
            print("No Unbookmarked Courses found!")
        rand_index=random.randint(0,total-1)
        random_unbookmarked_icon=unbookmarked_icons.nth(rand_index)
        unbookmarked_course=random_unbookmarked_icon.locator("xpath=ancestor::div[contains(@class, 'group') and contains(@class, 'cursor-pointer')]")
        return unbookmarked_course

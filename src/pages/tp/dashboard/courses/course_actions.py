import random
from src.base.base_page import BasePage


class CourseActions(BasePage):

    #Add New Offerings
    async def start_offering(self):
        await self.page.get_by_text("Add Offering").click()
        await self.page.get_by_role("button",name='Add Course Offering').click()


    #Click on any action button
    async def click_on_action_icon(self):
        buttons = self.page.locator(
            "button[id^='radix-'][aria-haspopup='menu'][type='button'] >> span:has-text('Open menu')"
        )
        count = await buttons.count()

        if count > 0:
            random_index = random.randint(0, count - 1)
            action_btn = buttons.nth(random_index)

            # Get row data
            button_row = action_btn.locator("xpath=ancestor::tr[1]")
            cell_count = await button_row.locator("td").count()
            row_data = []
            for cell in range(cell_count):
                # Get text and strip extra spaces/newlines
                text = await button_row.locator("td").nth(cell).inner_text()
                clean_text = " ".join(text.split())  # removes \n and extra spaces
                row_data.append(clean_text)

            # Click the action button
            await action_btn.wait_for(state="attached")
            await action_btn.wait_for(state="visible")
            await action_btn.click()
            print("Clicked action button")

            return row_data

        else:
            print("No action button found")
            return False

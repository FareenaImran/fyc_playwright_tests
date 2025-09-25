import re

from playwright.async_api import expect

from src.utils.helpers.logger import get_logger


class BasePage:
    def __init__(self,page):
     self.page=page
     self.logger=get_logger(f"{self.__module__}.{self.__class__.__name__}")

    #Get button/text count
    async def get_count(self, locator):
        try:
            # Wait for the element to contain a number in parentheses
            await locator.click()
            await expect(locator).to_contain_text(re.compile(r"\(\d+\)"), timeout=10000)

            text = (await locator.text_content()).strip()
            text_count = re.search(r"\((\d+)\)", text)

            if text_count:
                count = int(text_count.group(1))
                print(f"Get > {text}")
                return count
            return False

        except Exception as e:
            print(f"Expected count pattern not found: {e}")
            return False


    #Click on profile button
    async def click_on_profile_icon(self):
        try:
            icon_with_img=self.page.get_by_role("img", name="profile image")
            await icon_with_img.scroll_into_view_if_needed()
            await icon_with_img.click()
        except:
            icon_without_img=self.page.locator("(//*[name()='svg'][@class='cursor-pointer text-[#3F00C6]'])[1]")
            await icon_without_img.scroll_into_view_if_needed()
            await icon_without_img.click()

    #Count rows in all pages
    async def count_rows_in_all_pages(self):
        rows=self.page.locator("tbody>tr")
        page=1
        count=0
        while True:
            await rows.first.wait_for(state="attached")
            next_btn=self.page.get_by_role("button" ,name="Next")
            rows_in_page= await rows.count()
            if rows_in_page>0 :
                if (await rows.first.text_content()) == "No records found":
                    break
                count += rows_in_page
                print(f"Rows on page # {page} :{rows_in_page}")
                if await next_btn.is_visible():
                    if await next_btn.is_enabled():
                        await next_btn.scroll_into_view_if_needed()
                        await next_btn.click()
                        page += 1
                    else:
                        break
                else:
                    break
            else:
                print(f"No Records found after page {page}")
                break

        print(f"\nTotal rows : {count}")
        return count
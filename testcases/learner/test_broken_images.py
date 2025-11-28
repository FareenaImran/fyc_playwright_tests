import pytest
from src.utils.helpers.common_checks import check_broken_images
from src.utils.helpers.logger import logger

@pytest.mark.parametrize("page_name",["Training Partners","Courses"])
async def test_broken_images_in_all_pages(page,login,page_name):
    await page.goto("https://beta.findyourcourses.org/")
    await page.locator(f"//a[contains(text(),'{page_name}')]").click()
    await page.wait_for_load_state('domcontentloaded')

    page_no=1

    while True:
        print(f"\nChecking broken image(s) in page # {page_no}....")
        next_btn=page.locator("//button[contains(text(),'Next')]")

        broken_images = await check_broken_images(page)
        if broken_images:
            logger.info(f"{len(broken_images)} Broken image(s) found")
            for img in broken_images:
                logger.info(f"\n - {img}")

        if not await next_btn.is_hidden():
            page_no+=1
            await next_btn.click()
            await page.wait_for_load_state('networkidle')
        else:
            print("\nNo more pages to check further..")
            break

    if broken_images:
        raise Exception(f"Found The following broken images in > {page_name}")

    logger.info(f"\nVerified !! No broken image in {page_name}")



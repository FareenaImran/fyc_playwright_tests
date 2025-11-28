import re

from src.pages.learner.learner_home_page import LearnerHomePage
from src.utils.helpers.logger import logger


async def test_category_filter_displays_correct_courses(page):
    #Navigate to all Courses
    await page.goto("https://beta.findyourcourses.org/courses/all-courses")
    home_page=LearnerHomePage(page)
    labels=await home_page.get_all_filter_options("Category")

    for label in labels:
        print(f"\nVerifying {label}")
        #Select Label
        await page.get_by_label(label).click()
        await page.wait_for_timeout(1000)

        #Get course category
        course_category_texts=await home_page.get_all_course_category_text()
        if course_category_texts:
            print(f"\nList of courses' category for Selected label\n {course_category_texts}'")
        if not course_category_texts:
            print(f"\nNo Courses Found for {label}")
            #Deselect label
            await page.get_by_label(label).click()
            await page.wait_for_timeout(2000)
            continue

        # Check if label exist in course category
        found = any(
            category_text.lower().replace('...', '').startswith(label.lower()[:10])
            for category_text in course_category_texts)

        if not found:
            raise Exception(f"\nCategory Filter not working for {label}")

        # Deselect label
        await page.get_by_label(label).click()
        await page.wait_for_timeout(1500)

    else:
      logger.info("\n\n'Verified !! Category Filter is working as expected")

async def test_mode_of_teaching_filter_displays_correct_courses(page):
    #Navigate to all Courses
    await page.goto("https://beta.findyourcourses.org/courses/all-courses")
    home_page=LearnerHomePage(page)
    labels=await home_page.get_all_filter_options("Category")

    for label in labels:
        print(f"\nVerifying {label}")
        #Select Label
        await page.get_by_label(label).click()
        await page.wait_for_timeout(1000)

        #Get course category
        course_category_texts=await home_page.get_all_course_category_text()
        if course_category_texts:
            print(f"\nList of courses' category for Selected label\n {course_category_texts}'")
        if not course_category_texts:
            print(f"\nNo Courses Found for {label}")
            #Deselect label
            await page.get_by_label(label).click()
            await page.wait_for_timeout(2000)
            continue

        # Check if label exist in course category
        found = any(
            category_text.lower().replace('...', '').startswith(label.lower()[:10])
            for category_text in course_category_texts)

        if not found:
            raise Exception(f"\nCategory Filter not working for {label}")

        # Deselect label
        await page.get_by_label(label).click()
        await page.wait_for_timeout(1500)

    else:
      logger.info("\n\n'Verified !! Category Filter is working as expected")

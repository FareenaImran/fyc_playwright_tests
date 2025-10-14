import re

import pytest

from src.utils.helpers.common import get_row_text, select_menu_option
from src.utils.helpers.common_checks import check_success_message
from src.utils.helpers.csv_reader import get_cred_from_csv
from src.utils.helpers.logger import logger


async def change_account_status(page,status):

    try:
        # get emails
        emails = await get_row_text(page, 4)
        available_emails = get_cred_from_csv("learner")
        target_email = None
        for email in emails:
            for user in available_emails:
                if user["email"] == email:
                    target_email = email
                    logger.info(f"\n  Email :{target_email} | Status:  [{status}]")
                    break
            if target_email:
                break
        if target_email:
            await select_menu_option(page, 2, target_email)
        else:
            logger.info(f"\nCredentials for {target_email} are not found in csv")
            pytest.skip("\nSkipping Test...")

        # verify modal
        modal = page.get_by_text(re.compile(r".*(inactive|active).*"))
        assert await modal.is_visible(), f"\n{status} modal did not appear"

        # click on deactivate
        await page.get_by_role("button", name=re.compile(r".*(deactivate|activate).*")).click()

        # verify message
        success_msg = await check_success_message(page)
        logger.info(f"\n{success_msg}")
        assert "status updated" in success_msg.lower(), f"Expected {success_msg} but got: {success_msg}"

        return target_email

    except Exception as e:
        logger.error(f"Unable to change {status} status :{str(e)}")
        raise

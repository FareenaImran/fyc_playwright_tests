from src.base.base_page import BasePage
from src.pages.admin.add_new_tp.add_new_tp_steps import AddTPInfo
from src.utils.helpers.common_checks import check_is_btn_enabled, check_success_message
from src.utils.helpers.logger import logger


class AdminTPPage(BasePage):
    #------LOCATORS----
    APPROVED = "Approved"
    NEEDS_ATTENTION="Needs Attention"
    VIEW_CLAIMED_ACCOUNTS_BTN="View Claimed Accounts"
    UP_FOR_REVIEW_TAB="Up for review"

    #Add new TP
    async def add_new_tp(self):
        """Adding New TP"""
        add_new_tp=AddTPInfo(self.page)
        tp_name=await add_new_tp.fill_1st_step()
        await add_new_tp.fill_2nd_step()
        await add_new_tp.fill_3rd_step()
        # Click submit
        await check_is_btn_enabled(self.page, AddTPInfo.SUBMIT_BTN)
        # Success msg
        logger.info(f"\n{await check_success_message(self.page)}")
        return tp_name


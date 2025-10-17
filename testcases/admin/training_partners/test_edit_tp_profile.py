import pytest

from src.pages.admin.add_new_tp.add_new_tp_steps import AddTPInfo
from src.pages.admin.admin_dashboard_page import AdminDashboard
from src.utils.helpers.common import  select_menu_option, get_row_text
from src.utils.helpers.logger import logger


async def test_edit_tp_profile_picture(page,login,status="Up for review"):
     await login(page,"admin")
     dashboard= AdminDashboard(page)
     await dashboard.navigate_to_tp()
     await page.get_by_role("button",name=status).click()
     # Get ALL TP names from column 4
     tp_name = await get_row_text(page, 4,row_no=0)
     if tp_name:
         await select_menu_option(page, 1, tp_name)
         pro_pic=page.get_by_text("Profile Picture")
         await pro_pic.wait_for(state="visible")
         await pro_pic.click()
         logger.info(f"\nUpdating Profile Image for {tp_name}")
         step = AddTPInfo(page)
         cover_img,logo_img=await step.fill_3rd_step()
         if not cover_img and logo_img:
             raise Exception("Failed to upload profile image")
         logger.info(f"\n - Cover Image : {cover_img}\n - Institute Logo : {logo_img}")
         logger.info("\nProfile Image Updated successfully!!")




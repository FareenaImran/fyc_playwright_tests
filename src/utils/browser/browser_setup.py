from playwright.async_api import async_playwright


# async def launch_browser():
#     playwright=await async_playwright().start()
#     browser=await playwright.chromium.launch(headless=False,args=['--start-maximized'],slow_mo=30)
#     context=await browser.new_context()
#     page=await context.new_page()
#     return playwright,browser,context,page

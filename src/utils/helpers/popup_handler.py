async def handle_popup(popup):
    await popup.wait_for_load_state()
    print(f"[POPUP DETECTED] Title: {await popup.title()}")
    try:
        await popup.close()
    except Exception as e:
        print(f"Popup handling failed: {e}")
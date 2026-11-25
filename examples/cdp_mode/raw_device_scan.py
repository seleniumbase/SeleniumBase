from seleniumbase import SB

with SB(uc=True, incognito=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://deviceandbrowserinfo.com/are_you_a_bot")
    sb.wait_for_text("You are", "#resultsBotTest")
    status = sb.get_text("#resultsBotTest")
    print(status)
    if sb.headed:
        sb.sleep(2)  # Slow down for the live demo

from seleniumbase import sb_cdp

sb = sb_cdp.Chrome(incognito=True)
sb.goto("https://deviceandbrowserinfo.com/are_you_a_bot")
sb.wait_for_text("You are", "#resultsBotTest")
status = sb.get_text("#resultsBotTest")
print(status)
if sb.headed:
    sb.sleep(2)  # Slow down for the live demo

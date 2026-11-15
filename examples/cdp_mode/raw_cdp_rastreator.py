from seleniumbase import sb_cdp

sb = sb_cdp.Chrome()
sb.goto("https://www.rastreator.com/seguros-de-coche")
sb.hover_element("body")
sb.click_if_visible(".accept-btn", timeout=2)
sb.click('button[type="submit"]')
sb.sleep(1)
sb.click("label:has(#radioThinkingToBuying)")
sb.sleep(1)
sb.click("label:has(#radioNewCar)")
sb.sleep(1)
sb.solve_captcha()
sb.sleep(1)
expected_text = "El coche que quieres asegurar"
sb.highlight(f'h2:contains("{expected_text}")')
sb.sleep(2)

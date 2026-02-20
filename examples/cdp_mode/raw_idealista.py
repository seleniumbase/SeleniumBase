"""(Bypasses the DataDome slider CAPTCHA)"""
from seleniumbase import SB

with SB(uc=True, test=True, locale="es") as sb:
    url = "https://www.idealista.com/venta-viviendas/barcelona-provincia/"
    sb.activate_cdp_mode(url)
    sb.sleep(1)
    sb.solve_captcha()
    sb.sleep(2)
    sb.click("button#didomi-notice-agree-button")
    print("*** " + sb.get_text("h1"))
    items = sb.find_elements("div.item-info-container")
    for item in items:
        print(item.querySelector("a.item-link").text)
        print(item.querySelector("span.item-price").text)

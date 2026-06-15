"""An example that bypasses the DataDome Slider CAPTCHA.
(PyAutoGUI is installed at runtime if not yet installed.)"""
from seleniumbase import SB

with SB(uc=True, test=True, locale="es") as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.idealista.com/venta-viviendas/barcelona-provincia/")
    sb.sleep(1.5)
    sb.solve_captcha()
    sb.sleep(2)
    sb.click("button#didomi-notice-agree-button")
    print("*** " + sb.get_text("h1"))
    items = sb.find_elements("div.item-info-container")
    for item in items:
        item.flash(color="44CC88")
        print(item.querySelector("a.item-link").text)
        print(item.querySelector("span.item-price").text)

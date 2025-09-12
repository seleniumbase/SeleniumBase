import base64
from seleniumbase import SB
from selenium.webdriver.common.print_page_options import PrintOptions

with SB(uc=True, test=True, ad_block=True) as sb:
    url = "https://seleniumbase.io"
    sb.activate_cdp_mode(url)
    sb.reconnect()  # To access WebDriver methods
    print_options = PrintOptions()
    pdf_base64 = sb.driver.print_page(print_options)
    with open("downloaded_files/sb.pdf", "wb") as f:
        f.write(base64.b64decode(pdf_base64))

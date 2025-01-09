"""Mobile emulation test for Skype."""
from seleniumbase import SB

with SB(mobile=True, test=True) as sb:
    sb.open("https://www.skype.com/en/get-skype/")
    sb.assert_element('[aria-label="Microsoft"]')
    sb.assert_text("Download Skype", "h1")
    sb.highlight("div.appBannerContent")
    sb.highlight("h1")
    sb.assert_text("Skype for Mobile", "h2")
    sb.highlight("h2")
    sb.highlight("#get-skype-0")
    sb.highlight_click("span[data-dropdown-icon]")
    sb.highlight("#get-skype-0_android-download")
    sb.highlight('[data-bi-id*="ios"]')

"""SB Manager using UC Mode for evading bot-detection."""
from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.driver.uc_open_with_tab("https://nowsecure.nl/#relax")
    sb.sleep(1.2)
    if not sb.is_text_visible("OH YEAH, you passed!", "h1"):
        sb.get_new_driver(undetectable=True)
        sb.driver.uc_open_with_reconnect(
            "https://nowsecure.nl/#relax", reconnect_time=3
        )
        sb.sleep(1.2)
    if not sb.is_text_visible("OH YEAH, you passed!", "h1"):
        if sb.is_element_visible('iframe[src*="challenge"]'):
            with sb.frame_switch('iframe[src*="challenge"]'):
                sb.click("span.mark")
                sb.sleep(2)
    sb.activate_demo_mode()
    sb.assert_text("OH YEAH, you passed!", "h1", timeout=3)
